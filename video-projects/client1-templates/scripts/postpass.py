"""Post-pass on the HyperFrames render (whole frame incl. captions), only inside full-screen b-roll runs:
 1. frame holds copied from the reference's measured unique-frame map (scripts/holdmap.json, ~8 new frames per 17 = 14.12 fps)
 2. scanline overlay: horizontal sine, period 5.294 px, +-3 luma, screen-fixed, peaks at y = 5.294k - 0.04 (spec S02)
usage: postpass.py in.mp4 out.mp4"""
import cv2, numpy as np, sys, json, subprocess, os
src, dst = sys.argv[1:3]
HERE = os.path.dirname(os.path.abspath(__file__))
hold = {int(k): v for k, v in json.load(open(os.path.join(HERE, "holdmap.json"))).items()}
y = np.arange(1920, dtype=np.float32)
scan = (3.0 * np.cos(2 * np.pi * (y + 0.04) / 5.294)).reshape(1920, 1, 1)
cap = cv2.VideoCapture(src); cache = {}
tmp = dst + ".video.mp4"
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "30", "-i", "-",
                      "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
f = 0
while True:
    ok, fr = cap.read()
    if not ok: break
    cache[f] = fr
    for k in [k for k in cache if k < f - 8]: del cache[k]
    if f in hold:
        fr = np.clip(cache[hold[f]].astype(np.float32) + scan, 0, 255).astype(np.uint8)
    p.stdin.write(fr.tobytes()); f += 1
print("frames", f)
p.stdin.close(); p.wait()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-i", src, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", dst], check=True)
os.remove(tmp); print("wrote", dst)
