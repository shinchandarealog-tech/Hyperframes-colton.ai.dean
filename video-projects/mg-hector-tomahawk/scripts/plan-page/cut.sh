#!/usr/bin/env bash
# Cut per-beat preview clips (+posters) and web-sized full reels from the three option renders.
set -euo pipefail
R=/home/user/Hyperframes-colton.ai.dean/video-projects/mg-hector-tomahawk/renders
OUT=/tmp/claude-0/-home-user-Hyperframes-colton-ai-dean/f6779b87-beee-57e6-8876-1b99715add69/scratchpad/plan/site
mkdir -p "$OUT/clips" "$OUT/full"
for o in A B C; do
  ffmpeg -v error -y -i "$R/option-$o-draft.mp4" -vf scale=360:-2 -c:v libx264 -preset veryfast -crf 27 \
    -c:a aac -b:a 96k -movflags +faststart "$OUT/full/option-$o.mp4"
  ffmpeg -v error -y -ss 1.2 -i "$R/option-$o-draft.mp4" -frames:v 1 -vf scale=360:-2 -q:v 4 "$OUT/full/option-$o.jpg"
done
python3 -I - "$OUT" <<'EOF'
import json, subprocess, sys
out = sys.argv[1]
R = "/home/user/Hyperframes-colton.ai.dean/video-projects/mg-hector-tomahawk/renders"
beats = json.load(open(out + "/../beats.json"))
for b in beats:
    s = max(0, b["s"] - 0.25); d = min(55.2, b["e"] + 0.35) - s
    for o in "ABC":
        src = f"{R}/option-{o}-draft.mp4"; base = f"{out}/clips/{b['id']}-{o}"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.2f}", "-i", src, "-t", f"{d:.2f}",
            "-vf", "scale=360:-2", "-c:v", "libx264", "-preset", "veryfast", "-crf", "26",
            "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", base + ".mp4"], check=True)
        pt = min(b["e"] - 0.05, b["s"] + 0.6)   # poster: card fully landed
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{pt:.2f}", "-i", src, "-frames:v", "1",
            "-vf", "scale=360:-2", "-q:v", "5", base + ".jpg"], check=True)
print("clips done")
EOF
du -sh "$OUT"
