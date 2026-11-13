# Every-frame review: decode every frame of the delivered MP4 and tile them 8x3 per sheet with frame numbers.
import cv2, numpy as np, sys, os
src, tag = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src); fr = []
while True:
    ok, im = cap.read()
    if not ok: break
    fr.append(im)
os.makedirs('an/qc', exist_ok=True)
W, H = 200, 356
for s in range(0, len(fr), 24):
    tiles = []
    for i in range(s, s + 24):
        t = np.zeros((H, W, 3), np.uint8)
        if i < len(fr):
            t = cv2.resize(fr[i], (W, H), interpolation=cv2.INTER_AREA)
            cv2.putText(t, f'{i+1} {i/24:.2f}s', (4, 16), 0, 0.45, (0, 255, 255), 1)
        tiles.append(t)
    cv2.imwrite(f'an/qc/{tag}_{s//24+1:02d}.jpg', np.vstack([np.hstack(tiles[r*8:(r+1)*8]) for r in range(3)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
print(len(fr), 'frames')
