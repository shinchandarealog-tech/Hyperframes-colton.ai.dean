"""Render the text-free base footage layer (1080x1920 @30fps) with OpenCV.

Siham shots: face-tracked vertical MCU crop (eyes on the upper third), kept above the
burned-in caption band of the source (y >= ~1700), punch-ins per sentence, zoom-blur
cuts on every return, warm filmic grade, black gradient over the bottom third.
B-roll: Mixkit stock (free licence), cool blue tint for beat 2.
Collage: dark scrolling wall of stock tiles + one hero card per industry.
"""
import json, os, subprocess, sys
import numpy as np, cv2

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W, H, FPS = 1080, 1920, 30
TL = json.load(open(os.path.join(HERE, "timeline.json")))
SEG = {s["id"]: s for s in TL["segments"]}
DUR = TL["duration"]
NF = int(round(DUR * FPS))
RAW = os.path.join(ROOT, "raw-media/raw/take.mp4")
BR = os.path.join(ROOT, "raw-media/broll")
SRC_W, SRC_H = 1440, 2560
CAP_BAND_TOP = 1685          # never show source rows below this (burned-in captions)
BASE_H = 1170                # crop height at scale 1.0  -> 1.64x
W_OF = lambda t: SEG and None

# ---------------------------------------------------------------- shot list (output seconds)
def S(seg, scale=1.0, fx=540, look="warm", zin=False):
    return dict(kind="siham", seg=seg, scale=scale, fx=fx, look=look, zin=zin)

SHOTS = [
    (SEG["A"]["out_in"], SEG["A"]["out_out"], S("A", 1.0)),
    (SEG["B"]["out_in"], SEG["B"]["out_out"], dict(kind="broll", clip="39815", off=0.55, look="blue", fit="cover", ax=0.5)),
    (SEG["C"]["out_in"], SEG["C"]["out_out"], dict(kind="broll", clip="39790", off=3.0, look="blue", fit="cover", ax=0.32)),
    (SEG["D"]["out_in"], SEG["D"]["out_out"], S("D", 1.0, zin=True)),
    (SEG["E"]["out_in"], SEG["E"]["out_out"], S("E", 1.08)),
    (SEG["F"]["out_in"], SEG["F"]["out_out"], S("F", 1.17)),
    (SEG["G"]["out_in"], SEG["G"]["out_out"], S("G", 1.0)),
    (SEG["H"]["out_in"], 12.63, S("H", 1.08)),
    (12.63, SEG["I"]["out_out"], dict(kind="collage")),
    (SEG["J"]["out_in"], SEG["J"]["out_out"], S("J", 1.10, zin=True)),
    (SEG["K"]["out_in"], SEG["K"]["out_out"], dict(kind="broll", clip="42655", off=0.3, look="warm_broll", fit="cover", ax=0.62)),
    (SEG["L"]["out_in"], SEG["L"]["out_out"], S("L", 1.0, zin=True)),
    (SEG["M"]["out_in"], SEG["M"]["out_out"], S("M", 1.0, fx=330)),
    (SEG["N"]["out_in"], SEG["N"]["out_out"], S("N", 1.03, fx=330)),
    (SEG["O"]["out_in"], SEG["O"]["out_out"], S("O", 1.06, fx=330)),
    (SEG["P"]["out_in"], SEG["P"]["out_out"], S("P", 1.0, look="dim")),
    (SEG["Q"]["out_in"], SEG["Q"]["out_out"], S("Q", 1.0, look="dim")),
    (SEG["R"]["out_in"], DUR, S("R", 1.04, look="dim")),
]
POLAROID_T = 30.27   # background defocuses as the polaroid lands

# ---------------------------------------------------------------- face track
def load_track():
    f = json.load(open(os.path.join(HERE, "face.json")))
    t = np.array([r[0] for r in f]); x = np.array([r[1] if r[1] else np.nan for r in f], float)
    y = np.array([r[2] if r[2] else np.nan for r in f], float)
    bad = (np.abs(x - np.nanmedian(x)) > 150) | (np.abs(y - np.nanmedian(y)) > 120)
    x[bad] = np.nan; y[bad] = np.nan
    for a in (x, y):
        ok = ~np.isnan(a); a[~ok] = np.interp(t[~ok], t[ok], a[ok])
    k = np.ones(15) / 15                       # ~1.5 s moving average (samples every 0.1 s)
    xs = np.convolve(np.pad(x, 7, mode="edge"), k, "valid")
    ys = np.convolve(np.pad(y, 7, mode="edge"), k, "valid")
    return lambda st: (float(np.interp(st, t, xs)), float(np.interp(st, t, ys)))

EYE = load_track()

# ---------------------------------------------------------------- grade
def lut_curve(contrast=1.12, lift=0.025, gamma=1.0):
    x = np.arange(256) / 255.0
    y = 0.5 + (x - 0.5) * contrast
    y = y + 0.06 * np.sin((x - 0.5) * np.pi) * (contrast - 1) * 4  # gentle S
    y = lift + (1 - lift) * np.clip(y, 0, 1)
    y = np.clip(y, 0, 1) ** gamma
    return y

def make_lut(look):
    c = lut_curve()
    if look == "warm":
        r, g, b = c * 1.035, c * 1.0, c * 0.93
    elif look == "warm_broll":
        r, g, b = c * 1.05, c * 1.0, c * 0.9
    elif look == "blue":
        cc = lut_curve(1.1, 0.03)
        r, g, b = cc * 0.86, cc * 0.97, cc * 1.10
    elif look == "dim":
        cc = lut_curve(1.05, 0.02, 1.15)
        r, g, b = cc * 1.0, cc * 0.98, cc * 0.95
    else:
        r = g = b = c
    to8 = lambda a: np.clip(a * 255, 0, 255).astype(np.uint8)
    return np.dstack([to8(b), to8(g), to8(r)]).reshape(256, 1, 3)  # BGR

LUTS = {k: make_lut(k) for k in ("warm", "warm_broll", "blue", "dim")}

def grade(img, look):
    if look == "blue":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[..., None]
        img = cv2.addWeighted(img, 0.6, np.repeat(gray, 3, 2), 0.4, 0)
    if look == "dim":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[..., None]
        img = cv2.addWeighted(img, 0.3, np.repeat(gray, 3, 2), 0.7, 0)
        img = (img.astype(np.float32) * 0.62).astype(np.uint8)
    return cv2.LUT(img, LUTS[look])

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.28 * np.clip(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.42) / (H * 0.7)) ** 2, 0, 1))[..., None]
g0 = H * 2 / 3
BOTTOM = (1 - 0.78 * np.clip((yy - g0) / (H - g0), 0, 1) ** 1.2)[..., None]
FINISH = (VIG * BOTTOM).astype(np.float32)

def finish(img):
    return np.clip(img.astype(np.float32) * FINISH, 0, 255).astype(np.uint8)

# ---------------------------------------------------------------- readers
class RawReader:
    def __init__(self):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", RAW, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                                  stdout=subprocess.PIPE, bufsize=SRC_W * SRC_H * 3 * 2)
        self.idx = -1; self.frame = None
    def get(self, i):
        while self.idx < i:
            buf = self.p.stdout.read(SRC_W * SRC_H * 3)
            if len(buf) < SRC_W * SRC_H * 3:
                return self.frame
            self.frame = np.frombuffer(buf, np.uint8).reshape(SRC_H, SRC_W, 3); self.idx += 1
        return self.frame

def load_clip(clip, off, dur, w, h, ax=0.5):
    """Decode a stock clip, resample to 30fps, cover-crop to w x h (ax = horizontal anchor)."""
    path = os.path.join(BR, f"{clip}.mp4")
    sw, sh = map(int, subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
                 "stream=width,height", "-of", "csv=p=0", path]).decode().split(","))
    sc = max(w / sw, h / sh); nw, nh = int(round(sw * sc)), int(round(sh * sc))
    cx = int(round((nw - w) * ax)); cy = (nh - h) // 2
    vf = f"fps=30,scale={nw}:{nh}:flags=lanczos,crop={w}:{h}:{cx}:{cy}"
    out = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", str(off), "-t", str(dur + 0.2), "-i", path,
                                   "-vf", vf, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"])
    fr = np.frombuffer(out, np.uint8).reshape(-1, h, w, 3)
    return fr

# ---------------------------------------------------------------- siham framing
def siham_matrix(st, scale, fx, extra=1.0):
    ex, ey = EYE(st)
    h = BASE_H / scale; w = h * W / H
    top = ey - h / 3
    top = min(max(top, 0), CAP_BAND_TOP - h)
    left = ex - w * fx / W
    left = min(max(left, 0), SRC_W - w)
    k = H / h
    M = np.array([[k, 0, -left * k], [0, k, -top * k]], np.float32)
    if extra != 1.0:   # extra zoom around the eye point (zoom blur samples)
        px, py = (ex - left) * k, (ey - top) * k
        Z = np.array([[extra, 0, px * (1 - extra)], [0, extra, py * (1 - extra)], [0, 0, 1]], np.float32)
        M = (Z @ np.vstack([M, [0, 0, 1]]))[:2]
    return M, ((ex - left) * k, (ey - top) * k)

def render_siham(frame, st, scale, fx, zoomblur=0.0):
    if zoomblur <= 0.002:
        M, _ = siham_matrix(st, scale, fx)
        return cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    acc = np.zeros((H, W, 3), np.float32); n = 8
    for i in range(n):
        M, _ = siham_matrix(st, scale, fx, 1 + zoomblur * i / (n - 1))
        acc += cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return (acc / n).astype(np.uint8)

def zoomblur_img(img, amt, cx=W / 2, cy=H * 0.45):
    if amt <= 0.002:
        return img
    acc = np.zeros(img.shape, np.float32); n = 8
    for i in range(n):
        z = 1 + amt * i / (n - 1)
        M = np.array([[z, 0, cx * (1 - z)], [0, z, cy * (1 - z)]], np.float32)
        acc += cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return (acc / n).astype(np.uint8)

# ---------------------------------------------------------------- collage
COLLAGE_CLIPS = ["35902", "5461", "6367", "21780", "1728", "5454", "382", "40549", "12877"]
HERO = [(None, "35902"), (None, "6367"), (None, "5454"), (None, "382"), (None, "12877")]

def build_collage(t0, t1):
    words = TL["words"]
    get = lambda w: next(x["t"] for x in words if x["w"].lower().startswith(w))
    beats = [get("fintech"), get("pos"), get("saas"), get("cosmetics"), get("real")]
    dur = t1 - t0
    TW, TH = 330, 440
    tiles = {c: load_clip(c, 1.0, dur, TW, TH) for c in COLLAGE_CLIPS}
    HW, HH = 900, 600
    heroes = [load_clip(c, 1.5, dur, HW, HH) for _, c in HERO]
    # rounded mask
    def rmask(w, h, r):
        m = np.zeros((h, w), np.uint8)
        cv2.rectangle(m, (r, 0), (w - r, h), 255, -1); cv2.rectangle(m, (0, r), (w, h - r), 255, -1)
        for cx, cy in ((r, r), (w - r, r), (r, h - r), (w - r, h - r)):
            cv2.circle(m, (cx, cy), r, 255, -1, cv2.LINE_AA)
        return (m.astype(np.float32) / 255)[..., None]
    tmask = rmask(TW, TH, 22); hmask = rmask(HW, HH, 34)
    rng = np.random.default_rng(7)
    cols = []
    for ci in range(4):
        order = list(rng.permutation(COLLAGE_CLIPS))
        cols.append(dict(x=-90 + ci * (TW + 24), speed=(520 if ci % 2 == 0 else -460) * (1 + 0.1 * ci), order=order,
                         phase=rng.uniform(0, 400)))

    def frame(t):
        lt = t - t0
        img = np.full((H, W, 3), (14, 11, 10), np.uint8).astype(np.float32)
        fi = min(int(lt * FPS), len(next(iter(tiles.values()))) - 1)
        for c in cols:
            span = len(c["order"]) * (TH + 24)
            y0 = (c["phase"] + c["speed"] * lt) % span - span
            k = 0
            y = y0
            while y < H:
                clip = c["order"][k % len(c["order"])]
                yi = int(round(y))
                tile = tiles[clip][min(fi, len(tiles[clip]) - 1)].astype(np.float32) * 0.42
                x = c["x"]
                xa, xb = max(x, 0), min(x + TW, W); ya, yb = max(yi, 0), min(yi + TH, H)
                if xa < xb and ya < yb:
                    sub = tile[ya - yi:yb - yi, xa - x:xb - x]; m = tmask[ya - yi:yb - yi, xa - x:xb - x]
                    img[ya:yb, xa:xb] = img[ya:yb, xa:xb] * (1 - m) + sub * m
                y += TH + 24; k += 1
        # motion blur on the wall (fast-moving collage)
        img = cv2.blur(img, (1, 9))
        # hero card for current industry
        bi = max([i for i, b in enumerate(beats) if lt + t0 >= b - 0.05] or [0])
        since = t - beats[bi]
        p = np.clip((since + 0.05) / 0.22, 0, 1); e = 1 - (1 - p) ** 3
        sc = 0.86 + 0.14 * e
        hf = heroes[bi][min(fi, len(heroes[bi]) - 1)]
        hw, hh = int(HW * sc), int(HH * sc)
        hero = cv2.resize(hf, (hw, hh)).astype(np.float32); hm = cv2.resize(hmask, (hw, hh))[..., None]
        cx, cy = W // 2 + int((1 - e) * 160 * (1 if bi % 2 == 0 else -1)), 700
        x0, y0 = cx - hw // 2, cy - hh // 2
        # shadow
        sh = np.zeros((H, W), np.float32); cv2.rectangle(sh, (x0 + 10, y0 + 30), (x0 + hw - 10, y0 + hh + 20), 1, -1)
        sh = cv2.GaussianBlur(sh, (0, 0), 30)[..., None]
        img = img * (1 - 0.6 * sh)
        xa, xb = max(x0, 0), min(x0 + hw, W)
        reg = img[y0:y0 + hh, xa:xb]
        hs = hero[:, xa - x0:xb - x0]; ms = hm[:, xa - x0:xb - x0]
        img[y0:y0 + hh, xa:xb] = reg * (1 - ms) + hs * ms * 0.92
        # whip blur right after a beat lands
        img = img.astype(np.uint8)
        if 0 <= since < 0.12:
            img = cv2.blur(img, (int(40 * (1 - since / 0.12)) + 1, 1))
        return img
    return frame

# ---------------------------------------------------------------- main
def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "renders/base.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "14",
                            "-pix_fmt", "yuv420p", out_path], stdin=subprocess.PIPE)
    raw = RawReader()
    cache = {}
    collage = None
    last = None
    for n in range(NF):
        t = n / FPS
        shot_i = next(i for i, (a, b, _) in enumerate(SHOTS) if a - 1e-6 <= t < b - 1e-6 or i == len(SHOTS) - 1)
        a, b, sh = SHOTS[shot_i]
        lt = t - a
        nxt = SHOTS[shot_i + 1][2] if shot_i + 1 < len(SHOTS) else None
        if sh["kind"] == "siham":
            seg = SEG[sh["seg"]]
            st = min(seg["src_in"] + (t - seg["out_in"]), seg["src_out"] - 1 / FPS)
            fr = raw.get(int(round(st * FPS)))
            scale = sh["scale"] * (1 + 0.018 * lt / max(b - a, 0.5))   # slow push within the shot
            zb = 0.0
            if sh["zin"]:                       # zoom-blur cut back to Siham
                p = lt / 0.27
                if p < 1:
                    zb = 0.22 * (1 - p) ** 2; scale *= 1 + 0.14 * (1 - p) ** 3
            if nxt and nxt["kind"] != "siham" and b - t <= 3 / FPS + 1e-6:  # zoom-blur out into B-roll/graphic
                zb = max(zb, 0.06 * (3 - (b - t) * FPS + 1))
            img = render_siham(fr, st, scale, sh["fx"], zb)
            img = grade(img, sh["look"])
            if sh["look"] == "dim" and t >= POLAROID_T - 0.15:
                k = min((t - POLAROID_T + 0.15) / 0.35, 1)
                img = cv2.GaussianBlur(img, (0, 0), 1 + 24 * k)
                img = (img.astype(np.float32) * (1 - 0.3 * k)).astype(np.uint8)
        elif sh["kind"] == "broll":
            key = (sh["clip"], a)
            if key not in cache:
                cache[key] = load_clip(sh["clip"], sh["off"], b - a, W, H, sh.get("ax", 0.5))
            frs = cache[key]
            img = frs[min(int(round(lt * FPS)), len(frs) - 1)].copy()
            img = grade(img, sh["look"])
            # slow drift-in on B-roll
            z = 1.0 + 0.05 * lt / (b - a)
            M = np.array([[z, 0, W / 2 * (1 - z)], [0, z, H / 2 * (1 - z)]], np.float32)
            img = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            if lt < 4 / FPS:   # whip in
                img = zoomblur_img(img, 0.12 * (1 - lt * FPS / 4))
        else:
            if collage is None:
                collage = build_collage(a, b)
            img = collage(t)
            if lt < 4 / FPS:
                img = zoomblur_img(img, 0.12 * (1 - lt * FPS / 4))
        img = finish(img)
        enc.stdin.write(np.ascontiguousarray(img).tobytes())
        if n % 60 == 0:
            print(f"frame {n}/{NF}", flush=True)
    enc.stdin.close(); enc.wait()
    print("wrote", out_path)

if __name__ == "__main__":
    main()
