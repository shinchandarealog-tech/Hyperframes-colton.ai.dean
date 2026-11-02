#!/usr/bin/env bash
# Build edited masters from the client's "Sequence 01_1.mp4" (Drive id 16PnRO70Xsqygd4bATquhktQCx7YEmfOJ).
# Closes the 5 black/silent gaps, drops Teacher 2's first take, trims Teacher 3's silent head,
# conforms 100fps -> 30fps, applies a light grade, levels audio to -14 LUFS. No speech inside a kept range is altered.
set -euo pipefail
SRC="${1:?path to Sequence 01_1.mp4}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; OUT="$ROOT/assets"; TMP="$OUT/src/tmp"; mkdir -p "$TMP"
GRADE="eq=contrast=1.08:saturation=1.18:brightness=0.012:gamma=0.97,unsharp=5:5:0.35"
build () { # name "s1 e1,s2 e2,..."
  local name=$1 segs=$2 i=0; : > "$TMP/$name.txt"
  IFS=',' read -ra arr <<< "$segs"
  for seg in "${arr[@]}"; do
    read -r s e <<< "$seg"; local d; d=$(python3 -c "print(round($e-$s,3))")
    ffmpeg -loglevel error -y -ss "$s" -i "$SRC" -t "$d" -vf "fps=30,$GRADE" \
      -af "afade=t=in:d=0.015,afade=t=out:st=$(python3 -c "print(round($d-0.015,3))"):d=0.015" \
      -c:v libx264 -preset fast -crf 14 -pix_fmt yuv420p -c:a pcm_s16le -ar 48000 "$TMP/$name-$i.mov"
    echo "file '$TMP/$name-$i.mov'" >> "$TMP/$name.txt"; i=$((i+1))
  done
  ffmpeg -loglevel error -y -f concat -safe 0 -i "$TMP/$name.txt" \
    -af "highpass=f=80,acompressor=threshold=-22dB:ratio=3:attack=5:release=120:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=6" \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT/$name.mp4"
  echo "$name: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/$name.mp4")s"
}
# Full: T1+kids | T2 take 2 | Tip1 | Tip2 | Tip3 | artists+recycling | CTA (+outro hold)
build full  "0.25 12.34,20.75 28.90,32.20 40.55,43.12 52.10,54.32 61.85,63.55 79.66,94.75 107.75"
# Short: hook+kids | T2 intro | Tip1 line | Tip2 line | artists/vases line | CTA
build short "0.25 12.34,20.75 28.60,32.36 35.64,43.30 46.55,66.10 74.30,99.55 107.40"
rm -rf "$TMP"
