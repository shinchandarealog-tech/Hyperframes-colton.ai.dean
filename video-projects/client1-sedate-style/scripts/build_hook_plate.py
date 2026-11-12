"""S01 hook plate for client 1: source 0.00-3.80 s (cut inside the 3.75-3.89 s silence after "community"),
29.97 -> 30 fps by nearest source frame, zoom 1.15->1 circ.out 31 f about (540,960) (spec S01),
white silhouette strobe on frames 1,3,5 = person matte, gaussian sigma 40, gain 1.6 (fitted on the reference)."""
import cv2, numpy as np, sys, math, subprocess, mediapipe as mp
from mediapipe.tasks import python as mpp
from mediapipe.tasks.python import vision
rawdir, model, out = sys.argv[1:4]
N = 114  # 3.80 s at 30 fps
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(base_options=mpp.BaseOptions(model_asset_path=model), output_confidence_masks=True))
def circ(u): u = min(max(u, 0), 1); return math.sqrt(1 - (u - 1) ** 2)
def matte(img):
    r = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
    b = ((1 - r.confidence_masks[0].numpy_view()) > 0.5).astype(np.uint8)
    b = cv2.morphologyEx(b, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61)))
    h, w = b.shape; ff = b * 255; m = np.zeros((h + 2, w + 2), np.uint8); cv2.floodFill(ff, m, (0, 0), 128); cv2.floodFill(ff, m, (w - 1, 0), 128)
    return np.clip(cv2.GaussianBlur((ff != 128).astype(np.float32), (0, 0), 40) * 1.6, 0, 1)[..., None]
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "30", "-i", "-",
                      "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for f in range(N):
    k = int(round(f / 30 * 30000 / 1001)); img = cv2.imread(f"{rawdir}/f{k+1:04d}.jpg")
    s = 1 + 0.15 * (1 - circ(f / 31)); M = np.float64([[s, 0, 540 - 540 * s], [0, s, 960 - 960 * s]])
    fr = cv2.warpAffine(img, M, (1080, 1920), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    if f in (1, 3, 5):
        a = matte(fr); fr = (fr * (1 - a) + 255 * a).astype(np.uint8)
    p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait(); print("plate", N, "frames")
