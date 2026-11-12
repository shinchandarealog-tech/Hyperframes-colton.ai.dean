"""Automated QC over every frame: safe area, overlaps between text blocks, text vs faces."""
import json, os, subprocess, sys, numpy as np, cv2
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = sys.argv[1]   # blaze_face_short_range.tflite
SAFE = (72, 220, 944, 1480)   # x0, y0, x1, y1 (Reels/Shorts: top bar, right buttons, bottom caption area)
qc = json.load(open(os.path.join(ROOT, "renders/ovl/qc.json")))
det = vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(
    base_options=BaseOptions(model_asset_path=MODEL), min_detection_confidence=0.5))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, "renders/base.mp4"), "-vf", "scale=270:480",
                      "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
issues = []; faces = {}
n = 0
while True:
    buf = p.stdout.read(270 * 480 * 3)
    if len(buf) < 270 * 480 * 3: break
    img = np.frombuffer(buf, np.uint8).reshape(480, 270, 3)
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(img)))
    fb = []
    for d in r.detections:
        b = d.bounding_box
        # bbox -> output px; extend down to the chin (blaze box stops near the mouth)
        x0, y0, w, h = b.origin_x * 4, b.origin_y * 4, b.width * 4, b.height * 4
        fb.append((x0, y0 - 0.15 * h, x0 + w, y0 + 1.12 * h))
    faces[n] = fb
    n += 1

def inter(a, b, pad=0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])

for k, rects in qc.items():
    f = int(k); t = f / 30
    R = [(r["x0"], r["y0"], r["x1"], r["y1"], r["g"], r["txt"]) for r in rects]
    for r in R:
        if r[2] - r[0] < 2: continue
        if r[0] < SAFE[0] - 0.5 or r[1] < SAFE[1] - 0.5 or r[2] > SAFE[2] + 0.5 or r[3] > SAFE[3] + 0.5:
            issues.append((t, "outside safe area", r[5], [round(v) for v in r[:4]]))
        for fb in faces.get(f, []):
            if inter(r[:4], fb) and r[4] != "card_polaroid":
                issues.append((t, "touches face", r[5], [round(v) for v in fb]))
    for i in range(len(R)):
        for j in range(i + 1, len(R)):
            if inter(R[i][:4], R[j][:4], pad=8):
                issues.append((t, "overlap", R[i][5] + " | " + R[j][5], ""))

# collapse consecutive duplicates
seen = {}
for t, kind, txt, extra in issues:
    key = (kind, txt)
    seen.setdefault(key, []).append(t)
for (kind, txt), ts in sorted(seen.items(), key=lambda x: x[1][0]):
    print(f"{kind:18s} {ts[0]:6.2f}-{ts[-1]:6.2f}s ({len(ts)} fr)  {txt}")
print("frames checked:", len(qc), "faces found in", sum(1 for v in faces.values() if v), "frames")
