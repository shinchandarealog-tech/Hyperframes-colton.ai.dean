#!/usr/bin/env bash
# Bake the teacher punch-ins into the footage (the renderer ignores CSS transforms on <video> wrappers).
# Run AFTER prep.sh. Rewrites assets/full.mp4 (zoom + slow push on T1/T2/T3), regenerates assets/short.mp4's
# video from the zoomed full master (frame-exact, keeps short's audio), then re-mattes the teachers on zoomed footage.
# usage: scripts/punchin.sh <python-with-onnxruntime> <rvm_mobilenetv3_fp32.onnx>
set -euo pipefail
PY="${1:?python}"; MODEL="${2:?rvm onnx}"
cd "$(dirname "$0")/.."; A=assets; mkdir -p $A/src
[ -f $A/src/full-unzoomed.mp4 ] || cp $A/full.mp4 $A/src/full-unzoomed.mp4
[ -f $A/src/short-unzoomed.mp4 ] || cp $A/short.mp4 $A/src/short-unzoomed.mp4
# frame ranges (30 fps, full-master): T1 0-244, T2 363-607, T3 1837-2227 ; zoom s0->s1 about origin (50%, oy)
Z="if(lte(in,244),1.32+0.05*in/244,if(between(in,363,607),1.32+0.05*(in-363)/244,if(gte(in,1837),1.12+0.05*(in-1837)/390,1)))"
OY="if(lte(in,244),0,if(between(in,363,607),576,if(gte(in,1837),1459.2,0)))"
ffmpeg -loglevel error -y -i $A/src/full-unzoomed.mp4 -filter_complex \
  "[0:v]scale=2160:3840:flags=lanczos,zoompan=z='$Z':x='1080-1080/zoom':y='($OY)-($OY)/zoom':d=1:s=1080x1920:fps=30[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a copy -movflags +faststart $A/full.mp4
echo "full: $(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 $A/full.mp4) frames"
# short = frame-exact picks from zoomed full: [fullStartFrame, nFrames]
SEGS=("0 363" "363 236" "613 98" "864 98" "1431 246" "1981 236")
fc=""; cat=""; i=0
for s in "${SEGS[@]}"; do read -r st n <<< "$s"; fc+="[0:v]trim=start_frame=$st:end_frame=$((st+n)),setpts=PTS-STARTPTS[v$i];"; cat+="[v$i]"; i=$((i+1)); done
ffmpeg -loglevel error -y -i $A/full.mp4 -i $A/src/short-unzoomed.mp4 -filter_complex "${fc}${cat}concat=n=$i:v=1:a=0[v]" \
  -map "[v]" -map 1:a -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 30 -c:a copy -movflags +faststart -shortest $A/short.mp4
echo "short: $(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 $A/short.mp4) frames"
for r in "t1 0 8.2" "t2 12.1 8.2" "t3 61.2 13.2"; do set -- $r; "$PY" scripts/matte.py "$MODEL" $A/full.mp4 $2 $3 $A/matte-$1.webm; done
