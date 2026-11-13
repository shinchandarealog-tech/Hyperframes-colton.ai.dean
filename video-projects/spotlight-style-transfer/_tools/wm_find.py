# Find the Gemini sparkle watermark(s) in the A-roll frames: one static, one that moves.
# Writes aroll/wm.json {frame: [[cx, cy, r], ...]}.
import cv2, numpy as np, json
N = 216; Y0, X0 = 1450, 600
def tophat(i):
    g = cv2.cvtColor(cv2.imread(f'aroll/f/a_{i:04d}.jpg'), cv2.COLOR_BGR2GRAY)[Y0:, X0:].astype(np.float32)
    return g - cv2.medianBlur(g.astype(np.uint8), 51).astype(np.float32)
out = {}
for i in range(1, N + 1):
    d = tophat(i); b = (d > 25).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(b)
    hits = []
    for k in range(1, n):
        x, y, w, h, a = st[k]
        if a < 30 or w > 140 or h > 140: continue
        fill = a / (w * h)                  # 4-point star fills ~0.3-0.45 of its box
        if not (0.2 < fill < 0.6 and 0.75 < w / h < 1.33): continue
        hits.append([int(cen[k][0] + X0), int(cen[k][1] + Y0), int(max(w, h) / 2), round(fill, 2)])
    out[i] = hits
json.dump(out, open('aroll/wm.json', 'w'))
for i in range(1, N + 1, 6): print(i, out[i])
