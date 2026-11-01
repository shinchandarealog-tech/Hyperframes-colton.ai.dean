"""QC for rendered templates: frame-to-frame jump check on the alpha .mov (graphics only, so background
cuts don't count) plus a sampled frame sheet of each preview. usage: python qc_library.py [slugs...]"""
import sys, pathlib, subprocess, numpy as np, cv2
R = pathlib.Path(__file__).resolve().parent / "renders"; Q = R / "qc"; Q.mkdir(exist_ok=True)
slugs = sys.argv[1:] or sorted(p.stem for p in R.glob("*.mov"))
for s in slugs:
    # decode true RGBA (OpenCV drops alpha) and compare premultiplied colour, so invisible pixels don't count
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(R / f"{s}.mov"), "-vf", "scale=270:480", "-f", "rawvideo",
                          "-pix_fmt", "rgba", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 480, 270, 4).astype(np.float32)
    pm = fr[..., :3] * fr[..., 3:4] / 255.0
    d = [np.abs(pm[i] - pm[i - 1]).mean() for i in range(1, len(pm))]
    d = np.array(d); flags = []
    for i in range(3, len(d) - 3):
        loc = np.median(np.r_[d[i-4:i], d[i+1:i+5]])
        if d[i] > max(3 * loc, loc + 4): flags.append(f"f{i+1}:{d[i]:.1f}/{loc:.1f}")
    n = len(d) + 1
    step = max(1, n // 24)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(R / f"{s}_preview.mp4"), "-vf",
                    f"select='not(mod(n\\,{step}))',scale=120:213,drawtext=text='%{{eif\\:n*{step}\\:d}}':fontcolor=yellow:fontsize=12:box=1:boxcolor=black,tile=12x2:padding=2",
                    "-frames:v", "1", str(Q / f"{s}_sheet.jpg")], check=True)
    print(f"{s:10s} frames {n:3d} max-diff {d.max():5.1f}  spikes: {', '.join(flags) or 'none'}")
