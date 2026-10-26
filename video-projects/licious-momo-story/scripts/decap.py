"""Remove burned-in captions from a static-camera talking-head video.

Pass 1: read only the caption band, build a per-frame text mask, detect shot changes,
        and build a clean background plate per shot (median of unmasked pixels).
Pass 2: stream full frames; replace masked pixels with the gain-matched plate, or with a
        diffusion inpaint where the subject overlaps the band.
"""
import subprocess, sys, json
import numpy as np
import cv2

SRC, DST = sys.argv[1], sys.argv[2]
W, H = 720, 1280
Y0, Y1 = 128, 244          # caption band rows (text sits ~150-215)
BH = Y1 - Y0
DIL = 7
RNG = np.random.default_rng(7)

def frames(cmd_vf, h):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-vf", cmd_vf, "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, bufsize=10**8)
    n = W * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, W, 3)

def dilate(m, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return cv2.dilate(m.astype(np.uint8), k).astype(bool)

def text_mask(band):
    b = band.astype(np.int16)
    mn, mx = b.min(2), b.max(2)
    white = (mn > 222) & (mx - mn < 30)
    # keep only white pixels that have a dark shadow pixel 2-4px down-right (caption signature)
    lum = b.mean(2)
    sh = np.zeros_like(white)
    for d in (2, 3, 4):
        sh |= np.roll(np.roll(lum, -d, 0), -d, 1) < lum.mean() - 60
    seed = white & dilate(sh, 2)
    if seed.sum() < 40:
        return np.zeros_like(white)
    m = dilate(white & dilate(seed, 12), DIL)
    m[:, :] &= True
    return m

# ---------- pass 1
bands, masks = [], []
for f in frames(f"crop={W}:{BH}:0:{Y0}", BH):
    bands.append(f.copy())
    masks.append(text_mask(f))
bands = np.stack(bands); masks = np.stack(masks)
N = len(bands)
print("frames", N, file=sys.stderr)

# shot detection: robust diff of unmasked band pixels vs previous frame
g = bands.mean(3)
cuts = [0]
for i in range(1, N):
    ok = ~(masks[i] | masks[i - 1])
    d = np.abs(g[i] - g[i - 1])[ok]
    if d.size and np.median(d) > 6:
        cuts.append(i)
cuts.append(N)
shots = [(a, b) for a, b in zip(cuts[:-1], cuts[1:]) if b > a]
print("shots", len(shots), [a for a, _ in shots], file=sys.stderr)

def build_plates(masks):
    plates = np.zeros((N, BH, W, 3), np.uint8)
    for a, b in shots:
        idx = np.arange(a, b)
        if len(idx) > 180:
            idx = idx[np.linspace(0, len(idx) - 1, 180).astype(int)]
        stack = bands[idx].astype(np.float32)
        stack[masks[idx]] = np.nan
        cnt = (~np.isnan(stack[..., 0])).sum(0)
        med = np.nanmedian(stack, axis=0)
        rr, gg, bb = med[..., 0], med[..., 1], med[..., 2]
        skin = (rr > gg + 14) & (rr > bb + 22) & (rr > 120)
        skin = np.nan_to_num(skin, nan=0).astype(bool)
        v = (cnt >= max(4, int(0.2 * len(idx)))) | ((cnt >= 1) & ~skin)
        med = np.nan_to_num(med).astype(np.uint8)
        if (~v).any():
            med = cv2.inpaint(np.ascontiguousarray(med), (~v).astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA)
        plates[a:b] = med
    return plates

# caption region of interest: where strict detections happen within +-10 frames
roi = np.zeros_like(masks)
anym = masks.any((1, 2))
for i in range(N):
    lo, hi = max(0, i - 10), min(N, i + 11)
    if anym[lo:hi].any():
        roi[i] = dilate(masks[lo:hi].any(0), 14)

for it in range(2):
    plates = build_plates(masks)
    soft = np.zeros_like(masks)
    for i in range(N):
        if not roi[i].any():
            continue
        bf = bands[i].astype(np.int16)
        lum = bf.mean(2); sat = bf.max(2) - bf.min(2)
        d = lum - plates[i].astype(np.int16).mean(2)
        sm = roi[i] & (((d > 22) & (sat < 40) & (lum > 150)) | (d < -30))
        if sm.any():
            soft[i] = dilate(sm, 5)
    masks = masks | soft
    print("iter", it, "masked px", int(masks.sum()), file=sys.stderr)
plates = build_plates(masks)
valid = np.ones((N, BH, W), bool)

def diffuse(img, m, init, iters=80):
    out = img.astype(np.float32).copy()
    out[m] = init[m]
    for _ in range(iters):
        avg = (np.roll(out, 1, 0) + np.roll(out, -1, 0) + np.roll(out, 1, 1) + np.roll(out, -1, 1)) / 4
        out[m] = avg[m]
    return out

def clean(band, m, plate, v):
    if not m.any():
        return band
    live = band.astype(np.float32); pl = plate.astype(np.float32)
    ring = dilate(m, 4) & ~m
    # subject present where live differs from plate on unmasked pixels
    diff = np.abs(live - pl).mean(2)
    person = dilate((diff > 28) & ~m & v, 10)
    goodring = ring & ~person & v
    if goodring.sum() > 50:
        gain = live[goodring].mean(0) / np.maximum(pl[goodring].mean(0), 1)
        pl = np.clip(pl * gain, 0, 255)
    use_plate = m & v & ~person
    out = live.copy()
    out[use_plate] = pl[use_plate]
    rest = m & ~use_plate
    if rest.any():
        out = cv2.inpaint(np.ascontiguousarray(out.astype(np.uint8)), rest.astype(np.uint8) * 255, 7,
                          cv2.INPAINT_TELEA).astype(np.float32)
    # smooth fills on flat wall (low local texture in the plate) and add matching grain
    pg = cv2.cvtColor(plate, cv2.COLOR_RGB2GRAY).astype(np.float32)
    var = cv2.blur(pg * pg, (9, 9)) - cv2.blur(pg, (9, 9)) ** 2
    flat = m & (var < 16)
    if flat.any():
        sm = cv2.GaussianBlur(out, (0, 0), 3)
        out[flat] = sm[flat] + RNG.normal(0, 1.2, (int(flat.sum()), 1))
    # feather the seam
    edge = dilate(m, 2) & ~dilate(~m, 2) if False else (dilate(m, 1) & ~m)
    blur = (np.roll(out, 1, 0) + np.roll(out, -1, 0) + np.roll(out, 1, 1) + np.roll(out, -1, 1) + out) / 5
    out[edge] = blur[edge]
    return np.clip(out, 0, 255).astype(np.uint8)

# ---------- pass 2
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                        "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-i", SRC, "-map", "0:v", "-map", "1:a",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
                        "-c:a", "copy", "-movflags", "+faststart", DST], stdin=subprocess.PIPE)
for i, f in enumerate(frames("null", H)):
    if i >= N:
        break
    f = f.copy()
    f[Y0:Y1] = clean(f[Y0:Y1], masks[i], plates[i], valid[i])
    enc.stdin.write(f.tobytes())
enc.stdin.close(); enc.wait()
json.dump({"shots": [a for a, _ in shots], "masked_frames": int(masks.any((1, 2)).sum())},
          open(DST + ".json", "w"))
print("done", file=sys.stderr)
