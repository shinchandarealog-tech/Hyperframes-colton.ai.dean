import sys, json, subprocess, cv2, numpy as np, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
W, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
cap = cv2.VideoCapture(src); Wd, Ht = 720, 1280
# --- phone-number mask, taken from the black logo-outro frame ---
cap.set(cv2.CAP_PROP_POS_MSEC, 53000); _, ref = cap.read()
mask = np.zeros((Ht, Wd), np.uint8)
x0, y0, x1, y1 = 195, 1030, 530, 1110
roi = ref[y0:y1, x0:x1].max(axis=2)
mask[y0:y1, x0:x1] = (roi > 35).astype(np.uint8) * 255
mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
cv2.imwrite(out + '/callmask.png', mask)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=W + '/models/selfie_multiclass_256x256.tflite'), output_confidence_masks=True))
def ff(path, pix, crf):
    return subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', pix, '-s', f'{Wd}x{Ht}', '-r', '30', '-i', '-',
                             '-c:v', 'libx264', '-preset', 'medium', '-crf', str(crf), '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
pc = ff(out + '/clean_noaudio.mp4', 'bgr24', 14); pm = ff(out + '/matte.mp4', 'gray', 12)
faces = []; prev = None; prevsmall = None; n = 0
while True:
    ok, fr = cap.read()
    if not ok: break
    b_, g_, r_ = [fr[..., c].astype(np.int16) for c in range(3)]
    red = ((r_ > 150) & (r_ - g_ > 60) & (g_ < 130)).astype(np.uint8); red[:820] = 0; red[1260:] = 0
    cnt = int(red.sum()); inside = int((red & (mask > 0)).sum())
    fm = np.zeros_like(mask)
    if inside > 150: fm |= mask
    ys_, xs_ = np.nonzero(red)
    okbox = cnt > 40 and (xs_.max() - xs_.min()) < 430 and (ys_.max() - ys_.min()) < 220
    if okbox: fm |= cv2.dilate(red, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))) * 255
    if n < 26:  # fade-in: faint, low-saturation text
        faint = ((r_ - g_ > 18) & (r_ > 120) & (r_ - b_ > 8)).astype(np.uint8); faint[:980] = 0; faint[1160:] = 0
        faint[:, :150] = 0; faint[:, 570:] = 0
        faint = cv2.morphologyEx(faint, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
        fm |= cv2.dilate(faint, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))) * 255
    clean = cv2.inpaint(fr, fm, 7, cv2.INPAINT_TELEA) if fm.any() else fr
    pc.stdin.write(clean.tobytes())
    rgb = cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)
    r = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
    cm = [np.squeeze(m.numpy_view()) for m in r.confidence_masks]
    person = 1.0 - cm[0]
    small = cv2.resize(fr, (64, 112)).astype(np.float32)
    cut = prevsmall is None or np.abs(small - prevsmall).mean() > 28
    if prev is not None and not cut: person = 0.55 * person + 0.45 * prev   # temporal smoothing, reset on cuts
    prev = person; prevsmall = small
    pm.stdin.write(np.clip(person * 255, 0, 255).astype(np.uint8).tobytes())
    head = ((cm[3] > 0.5) | (cm[1] > 0.5)).astype(np.uint8)
    k, lab, st, _ = cv2.connectedComponentsWithStats(head)
    box = None
    if k > 1:
        i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        if st[i, cv2.CC_STAT_AREA] > 150:
            x, y, w, h = st[i, :4]; box = [round(x / Wd, 4), round(y / Ht, 4), round((x + w) / Wd, 4), round((y + h) / Ht, 4)]
    faces.append(box); n += 1
    if n % 200 == 0: print('frames', n, flush=True)
pc.stdin.close(); pm.stdin.close(); pc.wait(); pm.wait(); seg.close()
json.dump({'fps': 30, 'frames': faces}, open(out + '/faces.json', 'w'))
print('done', n)
