"""A-roll plates for the reel. reel frame f -> source time t = f/30 + offset (pauses removed), nearest 29.97 source frame.
plate_aroll.mp4: full frame, all 554 reel frames (used for speaker B: S06, S17).
plate_split.mp4: frames 232-342 (speaker A) scaled 0.974 into the split's bottom panel (14,974,1052x930), raw rows 120-1075."""
import cv2, numpy as np, sys, subprocess
rawdir = sys.argv[1]
def src_t(f):
    t = f / 30
    if t < 3.80: return t
    if t < 7.405: return t + 0.055
    if t < 16.045: return t + 0.325
    return t + 0.615
def frame(f): k = min(572, int(round(src_t(f) * 30000 / 1001))); return cv2.imread(f"{rawdir}/f{k+1:04d}.jpg")
def enc(out): return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "30", "-i", "-",
    "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
p = enc("assets/plate_aroll.mp4")
for f in range(554): p.stdin.write(frame(f).tobytes())
p.stdin.close(); p.wait()
s = 930 / 955; M = np.float64([[s, 0, 14 + (1052 - 1080 * s) / 2], [0, s, 974 - 120 * s]])
p = enc("assets/plate_split.mp4")
for f in range(232, 343): p.stdin.write(cv2.warpAffine(frame(f), M, (1080, 1920), flags=cv2.INTER_LANCZOS4).tobytes())
p.stdin.close(); p.wait(); print("ok")
