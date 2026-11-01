"""Frame-to-frame motion QC on a rendered reel.
 - per-frame mean abs difference; flags spikes that are not planned cuts
 - flags frozen/duplicated frames inside video segments
 - 1:1 check: once a full-frame segment has settled, the rendered frame must
   match its mapped source frame better than the source neighbours (n-1, n+1)
 - writes one still per segment + a contact sheet
usage: python qc.py renders/video_only.mp4 renders/qc_final
"""
import sys, pathlib, subprocess, numpy as np, cv2
R = pathlib.Path(__file__).resolve().parent.parent
vid, outdir = sys.argv[1], pathlib.Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
CUTS = {55, 117, 173, 300, 316, 365, 422, 490, 503, 547, 600, 666, 697, 791}
SEG = {"1 hook": (0, 55), "2 captions": (55, 173), "3 white": (173, 300), "4 b-roll": (300, 422),
       "5 split": (422, 547), "6 definition": (547, 600), "7 light": (600, 697),
       "8a check": (697, 791), "8b end": (791, 888)}
# full-frame segments and their source offset (output n -> source m)
FULL = [(318, 422, 593 - 300), (560, 600, 1509 - 547), (712, 791, 2078 - 697), (806, 888, 2172 - 791)]
cap = cv2.VideoCapture(vid); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(cv2.resize(f, (270, 480), interpolation=cv2.INTER_AREA).astype(np.float32))
N = len(frames); print("frames:", N, "(expected 888)")
d = np.array([0] + [np.abs(frames[i] - frames[i-1]).mean() for i in range(1, N)])
issues = []
for i in range(2, N - 2):
    if i in CUTS: continue
    loc = np.median(np.r_[d[max(1, i-6):i], d[i+1:i+7]])
    if d[i] > max(3.0 * loc, loc + 6):
        issues.append(f"jump  frame {i} (t={i/24:.2f}s) diff {d[i]:.1f} vs local {loc:.1f}")
for name, (a, b) in SEG.items():
    if name in ("3 white",): continue
    for i in range(a + 1, b):
        if d[i] < 0.05: issues.append(f"freeze frame {i} ({name}) diff {d[i]:.3f}")
# 1:1 mapping check against source
src = cv2.VideoCapture(str(R / "assets/src/raw.mp4")); srcf = {}
need = {i + off + k for a, b, off in FULL for i in range(a, b) for k in (-1, 0, 1)}
m = 0
while True:
    ok, f = src.read()
    if not ok: break
    if m in need:
        g = cv2.resize(f, (720, 1280))
        # same framing as the settled scene: scale 1.025 about centre, cropped to 9:16
        g = cv2.resize(g, None, fx=1.025 * 1.5, fy=1.025 * 1.5)
        h, w = g.shape[:2]; y0, x0 = (h - 1920) // 2, (w - 1080) // 2
        srcf[m] = cv2.resize(g[y0:y0+1920, x0:x0+1080], (270, 480), interpolation=cv2.INTER_AREA).astype(np.float32)
    m += 1
bad = 0; checked = 0
for a, b, off in FULL:
    for i in range(a, b):
        s = i + off
        e = {k: np.abs(frames[i] - srcf[s + k]).mean() for k in (-1, 0, 1) if s + k in srcf}
        checked += 1
        if min(e, key=e.get) != 0 and abs(e[0] - min(e.values())) > 0.3:
            bad += 1; issues.append(f"map   frame {i} best matches src {s+min(e, key=e.get)} not {s}")
print(f"1:1 mapping: {checked - bad}/{checked} settled full-frame frames match their source frame")
for k, (a, b) in SEG.items():
    n = b - 6 if k != "8b end" else 885
print("\n".join(issues) if issues else "no jumps / freezes / mapping errors")
np.save(outdir / "diffs.npy", d)
# stills of each segment (late in the segment, after every element has landed)
picks = [(k, (b - 6) if k != "8b end" else 884) for k, (a, b) in SEG.items()]
for k, n in picks:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-vf", f"select=eq(n\\,{n})", "-vsync", "0",
                    "-frames:v", "1", str(outdir / f"seg_{k.split()[0]}.png")], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-pattern_type", "glob", "-i", str(outdir / "seg_*.png"),
                "-vf", "scale=360:-1,tile=5x2:padding=6:color=gray", "-frames:v", "1",
                str(outdir / "segments_sheet.jpg")], check=True)
