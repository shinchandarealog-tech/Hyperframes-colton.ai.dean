"""Cut + upscale the A-roll from edl.json.
usage: assemble.py <src> <edl.json> <out_video.mp4> <out_audio.m4a> [--audio-only]"""
import json, subprocess, sys

src, edl_path, out_v, out_a = sys.argv[1:5]
audio_only = "--audio-only" in sys.argv
segs = json.load(open(edl_path))["segments"]
FADE = 0.012  # de-click each audio edge

parts, vlabels, alabels = [], [], []
for i, s in enumerate(segs):
    a, b = s["src_in"], s["src_out"]
    d = b - a
    parts.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,"
                 f"afade=t=in:d={FADE},afade=t=out:st={d - FADE:.3f}:d={FADE}[a{i}]")
    alabels.append(f"[a{i}]")
    if not audio_only:
        parts.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}]")
        vlabels.append(f"[v{i}]")
n = len(segs)
parts.append("".join(alabels) + f"concat=n={n}:v=0:a=1,"
             "loudnorm=I=-15:TP=-1.5:LRA=9[aout]")
if not audio_only:
    # 832x464 -> 1920x1080: lanczos upscale, mild sharpen, gentle contrast/sat lift, 30fps
    parts.append("".join(vlabels) + f"concat=n={n}:v=1:a=0,fps=30,"
                 "scale=1936:1080:flags=lanczos,crop=1920:1080,"
                 "unsharp=5:5:0.6:5:5:0.0,eq=contrast=1.04:saturation=1.05,format=yuv420p[vout]")
fc = ";".join(parts)
cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", fc,
       "-map", "[aout]", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", out_a]
if not audio_only:
    cmd += ["-map", "[vout]", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
            "-movflags", "+faststart", "-an", out_v]
subprocess.run(cmd, check=True)
print("ok")
