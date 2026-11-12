#!/usr/bin/env bash
# Composite the transparent GSAP overlay over the base footage, add the mix.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=${1:-final.mp4}
ffmpeg -y -v error -i renders/base.mp4 -thread_queue_size 64 -framerate 30 -i renders/ovl/%05d.png -i renders/mix.wav \
  -filter_complex "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]" -map "[v]" -map 2:a \
  -c:v libx264 -preset slow -crf 17 -profile:v high -c:a aac -b:a 192k -movflags +faststart -shortest "$OUT"
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact "$OUT"
