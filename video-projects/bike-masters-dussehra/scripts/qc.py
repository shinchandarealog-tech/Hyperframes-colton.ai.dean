"""QC for a rendered reel.

1. Graphics motion trace: samples every element's pose per frame from overlay.html and flags
   teleports (opacity popping 0 -> visible in one frame) and velocity jumps (jerks).
2. Output frame-to-frame difference: flags spikes outside the planned whip windows.
3. 1:1 mapping proof: on full-frame shots, the untouched top band of each output frame must match
   its expected source frame better than the neighbouring source frames (no skips / duplicates).
4. One still per segment -> renders/qc/.

usage: qc.py RENDER.mp4
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
import render as R

ROOT = R.ROOT
OUT = ROOT / "renders" / "qc"; OUT.mkdir(parents=True, exist_ok=True)
vid = sys.argv[1]
problems = []

def in_whip(t, pad=0.03):
    return any(abs(t - c) <= R.WHIP_D / 2 + pad for c in R.WHIPS)

# ---- 1. graphics trace ----
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    p = b.new_page(viewport={"width": R.W, "height": R.H})
    p.goto((ROOT / "graphics" / "overlay.html").as_uri()); p.evaluate("window.ready")
    trace = p.evaluate(f"(() => {{ const o = []; for (let f = 0; f < {R.N_FRAMES}; f++) o.push(poses(f / 30)); return o; }})()")
    b.close()
ids = sorted({k for fr in trace for k in fr})
for k in ids:
    prev_op, pos = 0.0, []
    for f, fr in enumerate(trace):
        P = fr.get(k)
        op = P["op"] if P else 0.0
        if op - prev_op > 0.5:
            problems.append(f"graphics pop: {k} opacity {prev_op:.2f}->{op:.2f} at frame {f}")
        prev_op = op
        pos.append((P["tx"], P["ty"], P["sc"]) if P and op > 0.02 else None)
    for f in range(2, len(pos)):
        if None in (pos[f], pos[f - 1], pos[f - 2]): continue
        v1 = np.subtract(pos[f - 1], pos[f - 2]); v2 = np.subtract(pos[f], pos[f - 1])
        jerk = np.hypot(*(v2[:2] - v1[:2])) + abs(v2[2] - v1[2]) * 300
        if jerk > 40 and not in_whip(f / 30):
            problems.append(f"graphics jerk: {k} {jerk:.1f}px/frame^2 at frame {f}")

# ---- 2 + 3. output frames ----
def frames(path, vf):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-vf", vf, "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 96, 54).astype(np.float32)

out = frames(vid, "scale=54:96:flags=area")
assert len(out) == R.N_FRAMES, f"render has {len(out)} frames, expected {R.N_FRAMES}"
diff = np.abs(np.diff(out, axis=0)).mean(axis=(1, 2))
for i, d in enumerate(diff):
    f = i + 1
    lo, hi = max(0, i - 8), min(len(diff), i + 9)
    local = np.median(np.r_[diff[lo:i], diff[i + 1:hi]])
    if d > max(4 * local, 3.0) and not in_whip(f / 30):
        problems.append(f"frame jump: {f - 1}->{f} diff {d:.2f} (local median {local:.2f})")

# source at the same downscale; band rows 0..49 (y < 1000: wall + face, where her motion is),
# which graphics never cover except the polaroid's drop-in (skipped below)
src = frames(R.SRC, "scale=54:96:flags=area")
band = slice(0, 50)
checked = bad = 0
for f in range(R.N_FRAMES):
    t = f / 30
    roll, s, _, _ = R.video_pose(t)
    if roll or s < 0.9999 or 3.28 <= t <= 3.90: continue
    e = R.src_index(f)
    cands = [c for c in (e - 1, e, e + 1) if 0 <= c < len(src)]
    errs = [np.abs(out[f, band] - src[c, band]).mean() for c in cands]
    checked += 1
    if cands[int(np.argmin(errs))] != e and max(errs) - min(errs) > 0.15:
        bad += 1; problems.append(f"mapping: out frame {f} best matches src {cands[int(np.argmin(errs))]}, expected {e}")
print(f"1:1 mapping check: {checked} full-frame output frames compared, {bad} mismatches")

# ---- 4. a still per segment ----
segs = {"1-hook": 2.6, "2-polaroid": 5.6, "3-offer": 9.2, "4-stores": 11.9, "5-discount": 17.9, "6-card": 21.6, "7-endcard": 22.8}
for name, t in segs.items():
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", vid, "-frames:v", "1", str(OUT / f"seg{name}.png")])

json.dump({"diff": diff.round(3).tolist()}, open(OUT / "diff.json", "w"))
print(f"{len(problems)} problems")
for p_ in problems[:80]: print("  ", p_)
