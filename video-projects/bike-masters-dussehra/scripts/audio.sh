#!/usr/bin/env bash
# Builds renders/mix.wav (23.0 s): VO cut to the same two source ranges as the picture, cleaned,
# loudness-normalized to -14 LUFS, plus whooshes on the four whips, soft ticks on key-word pops,
# and a quiet music bed.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=assets/source.mp4
SFX=../../assets/sfx
MUSIC=../../assets/music/music-bed-cinematic-tech.mp3
mkdir -p renders

# 1) VO: reel 0-18.60 = src 0-18.60, reel 18.60-23.00 = src 40.50-44.90.
#    The second range is faded out at src 44.10, before "terms and conditions" starts (shown on screen instead).
CLEAN="highpass=f=80,afftdn=nf=-28,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2"
ffmpeg -v error -y -i "$SRC" -filter_complex "
  [0:a]atrim=0:18.60,asetpts=PTS-STARTPTS,afade=t=out:st=18.585:d=0.015[a];
  [0:a]atrim=40.50:44.90,asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st=3.60:d=0.10[c];
  [a][c]concat=n=2:v=0:a=1,aformat=sample_rates=48000:channel_layouts=stereo,$CLEAN[vo]" \
  -map "[vo]" renders/vo-raw.wav

# two-pass loudnorm to -14 LUFS
M=$(ffmpeg -v info -i renders/vo-raw.wav -af loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$M" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i renders/vo-raw.wav -af "loudnorm=I=-14:TP=-1.5:LRA=9:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true,aresample=48000" renders/vo.wav

# 2) SFX: whoosh peak is ~0.17 s into the file -> start 0.17 s before each whip center.
W=() ; for c in 3.10 6.60 12.40 18.60; do W+=("$(python3 -c "print(int(($c-0.17)*1000))")"); done
T=() ; for c in 1.24 4.00 8.70 10.76 17.10 21.12; do T+=("$(python3 -c "print(int(($c-0.01)*1000))")"); done

FC="[1:a]volume=-16dB,asplit=4[w0][w1][w2][w3];"
for i in 0 1 2 3; do FC+="[w$i]adelay=${W[$i]}|${W[$i]}[wd$i];"; done
FC+="[2:a]atrim=0:0.25,afade=t=out:st=0.12:d=0.13,volume=-22dB,asplit=6[t0][t1][t2][t3][t4][t5];"
for i in 0 1 2 3 4 5; do FC+="[t$i]adelay=${T[$i]}|${T[$i]}[td$i];"; done
FC+="[3:a]atrim=0:23,volume=-22dB,afade=t=in:d=0.8,afade=t=out:st=21.8:d=1.2[mus];"
FC+="[0:a][wd0][wd1][wd2][wd3][td0][td1][td2][td3][td4][td5][mus]amix=inputs=12:normalize=0:duration=first,alimiter=limit=0.89:level=false,atrim=0:23[out]"

ffmpeg -v error -y -i renders/vo.wav -i "$SFX/transitions/whoosh.mp3" -i "$SFX/ui/click.wav" -i "$MUSIC" \
  -filter_complex "$FC" -map "[out]" -ar 48000 -ac 2 renders/mix-pre.wav
# vo.wav is 22.90 s of content; pad to exactly 23.0 s
ffmpeg -v error -y -i renders/mix-pre.wav -af "apad=whole_dur=23" -t 23 renders/mix.wav
for f in vo mix; do
  echo "$f: $(ffmpeg -i renders/$f.wav -af loudnorm=print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' | python3 -c "import json,sys;d=json.load(sys.stdin);print('I',d['input_i'],'LUFS  TP',d['input_tp'],'dBTP')")"
done
