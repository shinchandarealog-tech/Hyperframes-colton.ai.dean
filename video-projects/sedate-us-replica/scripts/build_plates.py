"""Build speaker plates (1080x1920, 30 fps) for every speaker shot / split panel from raw.mp4.
Per shot: robust low-order polynomial fit of the per-frame SIFT similarity transform (scale, tx, ty, rot) measured
raw->ref (scratch trk_<name>.json), then per ref frame the raw frame with the lowest residual inside the shot's region
(monotonic), warped with Lanczos. usage: build_plates.py <rawdir> <refdir> <trkdir> <outdir> [names...]"""
import cv2, numpy as np, sys, json, math, subprocess, os
rawdir, refdir, trkdir, outdir = sys.argv[1:5]; only = sys.argv[5:]
SHOTS = {  # name: (f0, f1, region mask x0,y0,x1,y1, exclude rects)
    "S04top": (207, 301, (14, 14, 1066, 944), [(40, 660, 1000, 944)]),
    "S04bot": (207, 301, (14, 974, 1066, 1904), [(60, 1480, 440, 1600)]),
    "S05bot": (302, 415, (14, 974, 1066, 1904), []),
    "S06": (416, 537, (0, 0, 1080, 900), []), "S08": (718, 739, (0, 0, 1080, 900), []),
    "S10bot": (826, 948, (21, 962, 1059, 1450), []), "S11": (949, 1000, (0, 0, 1080, 1200), [(0, 940, 1080, 1060)]),
    "S12": (1001, 1107, (0, 0, 1080, 900), []), "S13": (1108, 1132, (0, 0, 1080, 900), []),
    "S15": (1189, 1304, (0, 0, 1080, 900), []), "S17": (1430, 1507, (0, 0, 1080, 900), []),
    "S18": (1508, 1530, (0, 0, 1080, 1920), []),
}
NRAW = 1224
rawc = {}
def raw(k, gray=True):
    key = (k, gray)
    if key not in rawc:
        im = cv2.imread(f"{rawdir}/f{k+1:04d}.png", 0 if gray else 1); rawc[key] = im
    return rawc[key]

def robust_poly(f, y, w, deg):
    keep = np.ones(len(f), bool)
    for _ in range(4):
        c = np.polyfit(f[keep], y[keep], deg, w=w[keep]); r = y - np.polyval(c, f)
        s = 1.4826 * np.median(np.abs(r[keep] - np.median(r[keep]))) + 1e-6; keep = np.abs(r) < 3 * s + 1e-4
    return c, keep

report = {}
for name, (f0, f1, reg, excl) in SHOTS.items():
    if only and name not in only: continue
    d = json.load(open(f"{trkdir}/trk_{name}.json"))
    fr = np.array(sorted(int(k) for k, v in d.items() if v and v["mad"] < 8 and v["inl"] >= 30), float)
    get = lambda key: np.array([d[str(int(f))][key] for f in fr])
    w = np.sqrt(get("inl")); n = len(fr); deg = 0 if n < 8 else (1 if n < 30 else 3)
    if name == "S10bot": fr_fit = fr  # entrance frames 826-849 use the rest transform (panel animates in HTML)
    fits = {}
    for key in ("s", "tx", "ty", "r"):
        c, keep = robust_poly(fr, get(key), w, deg if key != "r" else min(deg, 1)); fits[key] = c
    def M_at(f):
        ff = max(f, 850) if name == "S10bot" else f
        s, tx, ty, r = (np.polyval(fits[k], ff) for k in ("s", "tx", "ty", "r"))
        a = math.radians(r); return np.float64([[s * math.cos(a), -s * math.sin(a), tx], [s * math.sin(a), s * math.cos(a), ty]])
    mask = np.zeros((1920, 1080), bool); mask[reg[1]:reg[3], reg[0]:reg[2]] = True
    for (a, b, c2, e) in excl: mask[b:e, a:c2] = False
    ks = {}; mads = {}; prev = None
    for f in range(f0, f1 + 1):
        ref = cv2.imread(f"{refdir}/f{f+1:04d}.png", 0).astype(np.float32); M = M_at(f)
        k0 = int(f / 30 * 24000 / 1001); best = None
        if name == "S10bot" and f < 850: ks[f] = None; continue
        for win in ((k0 - 2, k0 + 5), (k0 - 14, k0 + 10)):
            for k in range(max(0, win[0], prev if prev is not None else 0), min(NRAW, win[1])):
                rw = cv2.warpAffine(raw(k), M, (1080, 1920)).astype(np.float32)
                m = float(np.abs(ref - rw)[mask].mean())
                if best is None or m < best[0]: best = (m, k)
            if best[0] < 8: break
        if best[0] >= 8 and prev is not None: best = (best[0], prev)   # nothing matches (raw cut elsewhere): hold
        ks[f] = best[1]; mads[f] = best[0]; prev = best[1]
    if name == "S10bot":  # extrapolate the map into the entrance frames with the measured offset
        off = np.median([ks[f] - f * 24000 / 1001 / 30 for f in range(850, 880)])
        for f in range(826, 850): ks[f] = int(round(f * 24000 / 1001 / 30 + off))
    out = f"{outdir}/plate_{name}.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "30", "-i", "-",
                          "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for f in range(f0, f1 + 1):
        fr_img = cv2.warpAffine(raw(ks[f], False), M_at(f), (1080, 1920), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
        p.stdin.write(fr_img.tobytes())
    p.stdin.close(); p.wait()
    mv = np.array(list(mads.values()))
    report[name] = dict(deg=deg, n_fit=n, mad_median=round(float(np.median(mv)), 2), mad_max=round(float(mv.max()), 2),
                        worst=int(max(mads, key=mads.get)), s_range=[round(float(np.polyval(fits["s"], f0)), 4), round(float(np.polyval(fits["s"], f1)), 4)], map={str(k): v for k, v in ks.items()})
    print(name, {k: v for k, v in report[name].items() if k != "map"}, flush=True)
json.dump(report, open(f"{outdir}/../scripts/plates_report_{'_'.join(only) or 'all'}.json", "w"))
