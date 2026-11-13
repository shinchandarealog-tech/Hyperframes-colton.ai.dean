# Composite the edit: A-roll (camera move) -> card layer -> speaker (matte, same camera) -> graphics layer.
# Writes vid/comp/f_%04d.png. Camera = builder zoomAt() (same numbers).
import cv2, numpy as np, json, os, sys
FPS = 24; N = 216; FC = (550, 745); SRC = os.environ.get('AROLL', 'aroll/f')  # aroll/fc = watermark-cleaned
ZK = [1.10, 1.08, 1.00, 1.12, 1.02, 1.12, 1.08]
cam = json.load(open(sys.argv[1]))['style'].get('camera', 1) if len(sys.argv) > 1 else 1
edl = json.load(open('aroll/edl.json'))['edl']
SH = [[e[2], e[2] + e[1] - e[0]] for e in edl]
def zoom(t):
    i = next((k for k, s in enumerate(SH) if t < s[1]), len(SH) - 1)
    a, b = SH[i]; p = min(1, max(0, (t - a) / (b - a))); p = -(np.cos(np.pi * p) - 1) / 2
    z = ZK[i] + (ZK[i + 1] - ZK[i]) * p; return 1 + (z - 1) * cam
def warp(im, z):
    M = np.float32([[z, 0, FC[0] * (1 - z)], [0, z, FC[1] * (1 - z)]])
    return cv2.warpAffine(im, M, (1080, 1920), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
def over(base, rgba):
    a = rgba[..., 3:4].astype(np.float32) / 255
    return base * (1 - a) + rgba[..., :3].astype(np.float32) * a
os.makedirs('vid/comp', exist_ok=True)
for f in range(1, N + 1):
    t = (f - 1) / FPS; z = zoom(t)
    A = warp(cv2.imread(f'{SRC}/a_{f:04d}.jpg'), z).astype(np.float32)
    M = warp(cv2.imread(f'aroll/m/m_{f:04d}.png', 0), z).astype(np.float32)[..., None] / 255
    C = cv2.imread(f'vid/card/c_{f:04d}.png', cv2.IMREAD_UNCHANGED)
    G = cv2.imread(f'vid/gfx/g_{f:04d}.png', cv2.IMREAD_UNCHANGED)
    out = over(A, C)                 # glass card over the background
    out = A * M + out * (1 - M)      # speaker in front of the card
    out = over(out, G)               # text, crosses, cursor on top
    cv2.imwrite(f'vid/comp/f_{f:04d}.png', np.clip(out, 0, 255).astype(np.uint8))
print('done', N)
