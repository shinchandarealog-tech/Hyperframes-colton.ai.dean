"""Composite overlay PNGs over base.mp4 at given frames -> QC stills + a contact sheet."""
import sys, os, glob, subprocess, numpy as np, cv2
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base, ovl, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
files = sorted(glob.glob(os.path.join(ovl, '*.png')))
tiles = []
for f in files:
    n = int(os.path.basename(f)[:5])
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', f'{n/30:.4f}', '-i', base, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'])
    b = np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3).astype(np.float32)
    o = cv2.imread(f, cv2.IMREAD_UNCHANGED).astype(np.float32)
    a = o[..., 3:4] / 255
    img = (b * (1 - a) + o[..., :3] * a).astype(np.uint8)
    if '--safe' in sys.argv:
        cv2.rectangle(img, (72, 220), (940, 1480), (0, 0, 255), 2)
    cv2.putText(img, f'{n/30:.2f}s', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 255), 3)
    cv2.imwrite(os.path.join(out, f'{n:05d}.jpg'), img, [cv2.IMWRITE_JPEG_QUALITY, 88])
    tiles.append(cv2.resize(img, (270, 480)))
cols = 6
while len(tiles) % cols: tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
cv2.imwrite(os.path.join(out, 'sheet.jpg'), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
