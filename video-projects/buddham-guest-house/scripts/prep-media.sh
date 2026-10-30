#!/usr/bin/env bash
# Rebuilds the processed clips + audio mix from assets/src and the workspace audio library.
# Run from the project folder: bash scripts/prep-media.sh
set -euo pipefail
cd assets
W=../../../assets
G="eq=contrast=1.06:saturation=1.18:brightness=0.01,unsharp=5:5:0.5,setsar=1,fps=30"
ENC="-c:v libx264 -crf 18 -preset medium -g 15 -pix_fmt yuv420p -movflags +faststart"
# Full-frame framing; the top brand band in index.html covers the old burned-in titles.
ffmpeg -y -v error -i src/clip-buddham.mp4 -an -vf "delogo=x=112:y=640:w=246:h=52,scale=1080:2016:flags=lanczos,crop=1080:1836:0:180,pad=1080:1920:0:0:color=0x0e1646,$G" $ENC buddham.mp4
ffmpeg -y -v error -i src/clip-dipak.mp4 -an -vf "delogo=x=90:y=1012:w=598:h=152,scale=1080:2112:flags=lanczos,crop=1080:1782:0:330,pad=1080:1920:0:0:color=0x0e1646,$G" $ENC dipak.mp4
ffmpeg -y -v error -i src/clip-phulwari.mp4 -an -vf "scale=1080:1920:flags=lanczos,$G" $ENC phulwari.mp4
# Voiceover + music bed + transition SFX.
ffmpeg -y -v error -i voiceover.mp3 -i $W/music/music-bed-cinematic-tech.mp3 -i $W/sfx/transitions/whoosh.mp3 -i $W/sfx/ui/pop.mp3 -i $W/sfx/cinematic/sparkle.mp3 -i $W/sfx/impact/bass-drop.mp3 -filter_complex "\
[0]apad=whole_dur=50.5[vo];\
[1]atrim=0:50.5,volume=0.13,afade=t=in:d=0.6,afade=t=out:st=47.5:d=3[mu];\
[2]asplit=7[w1][w2][w3][w4][w5][w6][w7];\
[w1]adelay=5250:all=1,volume=0.35[a1];[w2]adelay=8550:all=1,volume=0.35[a2];[w3]adelay=17550:all=1,volume=0.35[a3];[w4]adelay=26350:all=1,volume=0.35[a4];[w5]adelay=35250:all=1,volume=0.35[a5];[w6]adelay=40650:all=1,volume=0.4[a6];[w7]adelay=44950:all=1,volume=0.35[a7];\
[3]asplit=4[p1][p2][p3][p4];[p1]adelay=17800:all=1,volume=0.3[b1];[p2]adelay=19300:all=1,volume=0.3[b2];[p3]adelay=21200:all=1,volume=0.3[b3];[p4]adelay=22600:all=1,volume=0.3[b4];\
[4]adelay=45500:all=1,volume=0.35[sp];[5]adelay=40850:all=1,volume=0.45[bd];\
[vo][mu][a1][a2][a3][a4][a5][a6][a7][b1][b2][b3][b4][sp][bd]amix=inputs=15:normalize=0:duration=first,alimiter=limit=0.95[out]" -map "[out]" -c:a aac -b:a 192k -ar 48000 mix.m4a
