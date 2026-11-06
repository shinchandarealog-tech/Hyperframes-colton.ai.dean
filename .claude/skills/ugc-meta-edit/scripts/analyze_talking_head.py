"""Analyze a talking-head clip before editing a UGC Meta ad.

Reports leftover pauses, hard (jump) cuts, audio clicks and where the speaker's
face sits, so captions can be placed just below the chin and every jump cut can
be covered with B-roll.

Usage (run with -I, pass paths as arguments):
  python3 -I analyze_talking_head.py <talking-head.mp4> <words.json>

<words.json> is a whisper word list: [{"text","start","end"}, ...] as written by
`npx hyperframes transcribe` or by whisper-cli -ml 1 -sow (see SKILL.md).
Needs ffmpeg, numpy, and opencv-python-headless<5 (for the face check).
"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

video, words_path = sys.argv[1], sys.argv[2]
W = json.load(open(words_path))
tmp = tempfile.mkdtemp()


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


# 1. Pauses between words
gaps = [(W[i]["text"], W[i + 1]["text"], round(W[i + 1]["start"] - W[i]["end"], 2))
        for i in range(len(W) - 1) if W[i + 1]["start"] - W[i]["end"] > 0.35]
print("PAUSES > 0.35s between words:", gaps or "none")

# 2. Hard cuts (frame-difference spikes)
ff("-i", video, "-vf", "scale=108:192,format=gray", "-f", "rawvideo", f"{tmp}/v.gray")
N = 108 * 192
a = np.fromfile(f"{tmp}/v.gray", np.uint8).reshape(-1, N).astype(float)
d = np.abs(np.diff(a, axis=0)).mean(1)
med = np.median(d)
cuts = [(i + 1, round((i + 1) / 30, 3)) for i, v in enumerate(d) if v > max(6, 4 * med)]
print("HARD CUTS (frame, seconds) -> each must be covered by B-roll:", cuts or "none")

# 3. Audio clicks at joins (big sample jump relative to local level)
ff("-i", video, "-vn", "-ac", "1", "-ar", "48000", "-f", "s16le", f"{tmp}/a.raw")
s = np.fromfile(f"{tmp}/a.raw", "<i2").astype(float)
jump = np.abs(np.diff(s))
clicks = []
for i in np.argsort(jump)[-30:]:
    loc = s[max(0, i - 480):i + 480]
    if jump[i] / (np.sqrt(np.mean(loc ** 2)) + 1) > 6:
        clicks.append(round(i / 48000, 3))
print("POSSIBLE CLICKS (s):", sorted(set(clicks)) or "none")

# 4. Face position (for caption placement)
try:
    import cv2
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    ff("-i", video, "-vf", "fps=5,scale=540:960", "-q:v", "3", f"{tmp}/f-%04d.jpg")
    rows = []
    for f in sorted(os.listdir(tmp)):
        if not f.startswith("f-"):
            continue
        g = cv2.cvtColor(cv2.imread(f"{tmp}/{f}"), cv2.COLOR_BGR2GRAY)
        faces = casc.detectMultiScale(g, 1.1, 6, minSize=(90, 90))
        if len(faces):
            x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
            top, chin = y * 2, int((y + h * 1.15) * 2)  # 1080x1920 coords
            if chin < 1500:  # ignore false hits on hands / bottles low in frame
                rows.append((int(f[2:6]) / 5, top, chin))
    if rows:
        chins = sorted(r[2] for r in rows)
        p98 = chins[int(len(chins) * 0.98) - 1]
        print(f"FACE: top min {min(r[1] for r in rows)}px | chin max {max(chins)}px | chin p98 {p98}px "
              f"({len(rows)} frames)")
        print(f"  -> caption top suggestion: {p98 + 20}px (must stay <= 1185 so the line ends by 1250)")
    else:
        print("FACE: none detected; check frames by eye")
except ImportError:
    print("FACE: opencv not installed (pip install 'opencv-python-headless<5')")
