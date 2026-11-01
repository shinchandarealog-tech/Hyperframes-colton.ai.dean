#!/usr/bin/env bash
# Render reel.html in 4 parallel chunks, then join losslessly (stream copy).
set -e
cd "$(dirname "$0")/.."
B=(0 222 444 666 888)
for i in 0 1 2 3; do
  python3 scripts/render_video.py renders/chunk$i.mp4 ${B[$i]} ${B[$((i+1))]} > renders/chunk$i.log 2>&1 &
done
wait
printf "file 'chunk%d.mp4'\n" 0 1 2 3 > renders/chunks.txt
ffmpeg -v error -y -f concat -safe 0 -i renders/chunks.txt -c copy renders/video_only.mp4
tail -qn1 renders/chunk*.log
