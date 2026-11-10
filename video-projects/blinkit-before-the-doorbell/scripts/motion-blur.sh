#!/usr/bin/env bash
# Render at 60fps, then blend each pair of frames into one 30fps frame (180° shutter motion blur).
# Usage: scripts/motion-blur.sh <quality: draft|standard|high> <output.mp4>
set -euo pipefail
Q="${1:-draft}"; OUT="${2:-renders/blinkit-${Q}.mp4}"
TMP="renders/_60fps-${Q}.mp4"
npx hyperframes render --quality "$Q" --fps 60 --output "$TMP"
CRF=$([ "$Q" = draft ] && echo 23 || echo 16)
ffmpeg -loglevel error -y -i "$TMP" \
  -vf "tmix=frames=2:weights='1 1',select='not(mod(n\,2))',setpts=N/(30*TB)" -r 30 \
  -c:v libx264 -preset slow -crf "$CRF" -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"
rm -f "$TMP"
echo "wrote $OUT"
