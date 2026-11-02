"""Presenter cut-out (RGBA WebM) via RobustVideoMatting ONNX.
usage: python matte.py <model.onnx> <in.mp4> <start_s> <dur_s> <out.webm>
Output: VP9 yuva420p WebM, same size/fps as input, presenter only (alpha = matte)."""
import sys, subprocess, numpy as np, onnxruntime as ort
model, src, ss, dur, out = sys.argv[1:6]
W, H, FPS = 1080, 1920, 30
sess = ort.InferenceSession(model, providers=["CPUExecutionProvider"])
rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4
dr = np.array([0.25], np.float32)
dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", ss, "-i", src, "-t", dur,
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
                        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libvpx-vp9",
                        "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "30", "-row-mt", "1",
                        "-deadline", "good", "-cpu-used", "4", "-auto-alt-ref", "0", out], stdin=subprocess.PIPE)
n = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    x = (img.astype(np.float32) / 255.0).transpose(2, 0, 1)[None]
    fgr, pha, *rec = sess.run(None, {"src": x, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3], "downsample_ratio": dr})
    a = np.clip(pha[0, 0], 0, 1)
    a = np.where(a < 0.04, 0, a)  # kill faint halos
    rgba = np.dstack([img, (a * 255).astype(np.uint8)])
    enc.stdin.write(rgba.tobytes()); n += 1
enc.stdin.close(); enc.wait(); dec.wait()
print(f"{out}: {n} frames")
