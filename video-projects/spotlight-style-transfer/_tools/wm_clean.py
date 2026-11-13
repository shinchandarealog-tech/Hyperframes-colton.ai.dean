# Remove the Gemini sparkle watermarks from the A-roll frames (aroll/f -> aroll/fc).
# Static sparkle at (899,1739); a smaller one drifts from (1000,1849) to off-frame bottom-right.
# Mask = bright top-hat pixels inside each sparkle's box, dilated; filled by inpainting + matched grain.
import cv2, numpy as np, os
N = 216; os.makedirs('aroll/fc', exist_ok=True); rng = np.random.default_rng(7)
def find_moving(th):
    # th: top-hat of the region x>=940, y>=1790
    b = (th > 25).astype(np.uint8); n, lab, st, cen = cv2.connectedComponentsWithStats(b)
    best = None
    for k in range(1, n):
        if st[k, 4] >= 20 and (best is None or st[k, 4] > st[best, 4]): best = k
    return None if best is None else (int(cen[best][0]) + 940, int(cen[best][1]) + 1790)
last = None; log = []
for i in range(1, N + 1):
    im = cv2.imread(f'aroll/f/a_{i:04d}.jpg'); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    th = g.astype(np.float32) - cv2.medianBlur(g, 61).astype(np.float32)
    mask = np.zeros(g.shape, np.uint8)
    boxes = [(899, 1739, 46)]
    mv = find_moving(th[1790:, 940:])
    if mv: last = mv
    elif last and i < 185: mv = last          # keep masking through a missed detection
    if mv: boxes.append((mv[0], mv[1], 28))
    for cx, cy, r in boxes:
        y0, y1, x0, x1 = max(0, cy - r), min(1920, cy + r), max(0, cx - r), min(1080, cx + r)
        mask[y0:y1, x0:x1] = (th[y0:y1, x0:x1] > 6) * 255
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    out = cv2.inpaint(im, mask, 7, cv2.INPAINT_TELEA)
    # match the footage grain inside the patch so it doesn't read as a smooth blob
    sd = float(np.std(th[1650:1700, 950:1000][np.abs(th[1650:1700, 950:1000]) < 10]))
    noise = rng.normal(0, sd, g.shape).astype(np.float32)
    m = cv2.GaussianBlur(mask, (7, 7), 0).astype(np.float32)[..., None] / 255
    out = np.clip(out + noise[..., None] * m, 0, 255).astype(np.uint8)
    cv2.imwrite(f'aroll/fc/a_{i:04d}.jpg', out, [cv2.IMWRITE_JPEG_QUALITY, 97])
    log.append((i, mv))
print([l for l in log if l[0] % 12 == 1]); print('missing moving from frame', next((i for i, m in log if m is None), None))
