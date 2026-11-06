"""Verify a rendered UGC ad before sending it.

Usage:
  python3 -I verify_render.py <render.mp4> <talking-head.mp4> [cut_frame ...] [--sheet out.jpg]

Checks: duration/frames, black or frozen frames, loudness, which ranges are B-roll
vs talking head (any shot under 0.5s is flagged as a flash), and whether each given
jump-cut frame (from analyze_talking_head.py) is covered by B-roll. With --sheet,
writes a 4fps contact sheet to look at by eye.
"""
import subprocess
import sys
import tempfile

import numpy as np

args = sys.argv[1:]
sheet = None
if "--sheet" in args:
    k = args.index("--sheet")
    sheet = args[k + 1]
    del args[k:k + 2]
render, head, cut_frames = args[0], args[1], [int(x) for x in args[2:]]
tmp = tempfile.mkdtemp()


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stderr


print(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,nb_frames,duration",
                      "-of", "compact", render], capture_output=True, text=True).stdout.strip())
out = run(["ffmpeg", "-i", render, "-vf", "blackdetect=d=0.03:pix_th=0.08,freezedetect=n=0.002:d=0.5",
           "-an", "-f", "null", "-"])
print("black/frozen events:", out.count("black_start") + out.count("freeze_start"))
loud = [l.strip() for l in run(["ffmpeg", "-i", render, "-af", "ebur128=framelog=quiet", "-f", "null", "-"]).splitlines()
        if l.strip().startswith("I:")]
print("loudness:", loud[-1] if loud else "?", "(target about -16 LUFS)")

N = 108 * 192
for name, src in (("r", render), ("h", head)):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", "scale=108:192,format=gray", "-f", "rawvideo",
                    f"{tmp}/{name}.gray"], check=True)
r = np.fromfile(f"{tmp}/r.gray", np.uint8).reshape(-1, 192, 108).astype(float)
h = np.fromfile(f"{tmp}/h.gray", np.uint8).reshape(-1, 192, 108).astype(float)
n = min(len(r), len(h))
# compare the top 57% of the frame (captions sit lower) to tell B-roll from the speaker
broll = np.abs(r[:n, :110] - h[:n, :110]).mean((1, 2)) > 12
sw = [i for i in range(1, n) if broll[i] != broll[i - 1]]
print("shots:", [(round(i / 30, 2), "broll" if broll[i] else "speaker") for i in sw])
if sw:
    runs = [sw[0]] + [b - a for a, b in zip(sw, sw[1:])] + [n - sw[-1]]
    print(f"shortest shot: {min(runs)} frames" + ("  <-- FLASH, fix it" if min(runs) < 15 else ""))
for f in cut_frames:
    ok = f < n and broll[f - 1] and broll[f]
    print(f"jump cut at frame {f} ({f / 30:.2f}s): {'covered' if ok else 'NOT COVERED'}")

if sheet:
    from PIL import Image, ImageDraw
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", render, "-vf", "fps=4,scale=180:320", "-q:v", "3",
                    f"{tmp}/s-%04d.jpg"], check=True)
    import glob
    fs = sorted(glob.glob(f"{tmp}/s-*.jpg"))
    im = Image.new("RGB", (16 * 180, ((len(fs) + 15) // 16) * 338))
    dr = ImageDraw.Draw(im)
    for i, f in enumerate(fs):
        x, y = (i % 16) * 180, (i // 16) * 338
        im.paste(Image.open(f), (x, y + 18))
        dr.text((x + 2, y + 2), f"{i / 4:.2f}s", fill="yellow")
        for yy in (270, 1250):  # safe-area lines
            dr.line([(x, y + 18 + yy / 6), (x + 180, y + 18 + yy / 6)], fill=(255, 0, 0))
    im.save(sheet, quality=82)
    print("contact sheet:", sheet)
