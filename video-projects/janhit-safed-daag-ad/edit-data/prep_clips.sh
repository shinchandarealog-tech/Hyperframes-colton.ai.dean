#!/usr/bin/env bash
# Usage: prep_clips.sh <dir with c01..c26.mp4>
# Trims, retimes, crops out burned-in text, grades brighter (Look B) and scales to 1080x1920.
set -euo pipefail
SRC=$1; OUT=assets/clips; mkdir -p $OUT
GRADE="eq=contrast=1.10:saturation=1.22:brightness=0.025:gamma=1.04,unsharp=5:5:0.6"
# name src in out outdur crop(w:h:x:y or -)
prep(){ local n=$1 c=$2 a=$3 b=$4 d=$5 cr=${6:--}
  local f; f=$(python3 -c "print(($b-$a)/$d)")
  local vf="delogo=x=568:y=1128:w=66:h=66,trim=$a:$b,setpts=(PTS-STARTPTS)/$f"
  [ "$cr" != "-" ] && vf="$vf,crop=$cr"
  vf="$vf,scale=720:1280:flags=lanczos"
  if python3 -c "import sys;sys.exit(0 if $f<0.9 else 1)"; then vf="$vf,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1"; else vf="$vf,fps=30"; fi
  vf="$vf,scale=1080:1920:flags=lanczos,$GRADE,trim=duration=$d"
  ffmpeg -v error -y -i $SRC/$c.mp4 -an -vf "$vf" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -movflags +faststart $OUT/$n.mp4
  echo "$n $(ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT/$n.mp4)"
}
prep s01 c16 0.0 1.90 3.30 &
prep s02 c25 0.0 1.40 1.80 &
prep s03 c04 1.4 3.00 2.20 405:720:190:470 &
prep s04 c03 0.0 1.85 3.05 &
wait
prep s05 c23 1.5 4.03 2.85 &
prep s06 c21 0.0 4.03 5.15 &
prep s07a c16 0.3 1.90 3.40 520:924:120:60 &
prep s07b c09 0.0 1.90 2.80 &
wait
prep s08 c20 1.4 4.03 2.60 &
prep s09a c12 0.0 2.20 2.20 576:1024:72:0 &
prep s09b c26 1.6 4.03 2.15 &
prep s09c c24 0.0 2.50 2.50 &
prep s11 c22 1.6 3.40 1.80 &
prep s12a c13 1.0 4.40 3.40 495:880:112:20 &
wait
# Beat 4 reference-style red: blocky posterized red version of s04 (3 tones), hard-snapped in the composition
ffmpeg -v error -y -i $OUT/s04.mp4 -vf "format=gray,eq=contrast=1.25,scale=90:160:flags=area,scale=1080:1920:flags=neighbor,format=rgb24,lutrgb=r='if(gt(val\,150)\,214\,if(gt(val\,78)\,150\,62))':g='if(gt(val\,150)\,14\,if(gt(val\,78)\,8\,6))':b='if(gt(val\,150)\,26\,if(gt(val\,78)\,16\,10))',format=yuv420p" -c:v libx264 -preset medium -crf 19 -movflags +faststart $OUT/s04red.mp4
