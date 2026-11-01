#!/usr/bin/env bash
# boat launch promo — full build: sub-frame render → motion-blur average → audio mix → final.mp4
#   ./scripts/build.sh            # full pipeline
#   ./scripts/build.sh audio      # audio mix only
#   ./scripts/build.sh mux        # re-mux existing blurred video + audio
set -euo pipefail
cd "$(dirname "$0")/.."
HF="npx -y hyperframes@0.8.225"
SFX=../../assets/sfx
MUSIC=../../assets/music/music-bed-cinematic-tech.mp3
DUR=13
SUB=8          # sub-frames captured per output frame (240 fps)
SHUTTER=4      # sub-frames averaged per output frame (4/8 = 180° shutter)
mkdir -p renders

video() {
  # 1. capture the GSAP timeline at 240 fps (8 sub-frames per 30 fps frame), near-lossless
  $HF render --fps $((30 * SUB)) --crf 8 --output renders/sub240.mp4 --quiet
  # 2. average the first SHUTTER sub-frames of every frame (frame time → +180° shutter), keep 30 fps
  ffmpeg -v error -y -i renders/sub240.mp4 \
    -vf "tmix=frames=${SHUTTER},select='eq(mod(n\,${SUB})\,$((SHUTTER - 1)))',setpts=N/30/TB" \
    -r 30 -an -c:v libx264 -preset slow -crf 10 -pix_fmt yuv420p renders/blurred.mp4
}

audio() {
  # cue: file  start(s)  trim-in(s)  gain(dB)
  local CUES=(
    "impact/bass-drop.mp3     0.05 0.0 -10"   # glow blooms
    "ui/pop.mp3               0.62 0.0  -8"   # icon tile lands
    "transitions/whoosh.mp3   1.80 0.0  -4"   # push through icon
    "ui/click.wav             2.58 0.0 -10"   # chips reveal
    "transitions/swipe.mp3    3.62 0.0  -6"   # flash to black
    "ui/pop.mp3               4.18 0.0 -12"   # "Just Ask"
    "transitions/whoosh.mp3   5.42 0.0  -6"   # phones fly in
    "ui/pop.mp3               5.80 0.0 -12"   # "See The Magic"
    "transitions/whoosh.mp3   7.38 0.0  -3"   # tunnel push-through
    "ui/send-message.mp3      7.85 0.0  -6"   # pill reveal
    "ui/click.wav             9.20 0.0 -10"   # 100%
    "transitions/whoosh.mp3   9.36 0.0  -9"   # flash to black
    "ui/pop.mp3               9.60 0.0 -14"   # tagline
    "cinematic/riser.mp3      9.00 1.5  -8"   # riser into logo (peaks 10.95)
    "impact/slam.mp3         10.82 0.0  -5"   # logo hit
  )
  local inputs=() chains="" labels="" i=0
  for c in "${CUES[@]}"; do
    read -r f st tr g <<<"$c"
    inputs+=(-i "$SFX/$f")
    local ms; ms=$(awk "BEGIN{printf \"%d\", $st*1000}")
    chains+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=$tr,asetpts=PTS-STARTPTS,volume=${g}dB,adelay=${ms}|${ms}[s$i];"
    labels+="[s$i]"; i=$((i + 1))
  done
  ffmpeg -v error -y "${inputs[@]}" -filter_complex \
    "${chains}${labels}amix=inputs=$i:normalize=0:duration=longest,apad,atrim=0:$DUR[out]" \
    -map "[out]" -ar 48000 renders/sfx-bus.wav
  ffmpeg -v error -y -i "$MUSIC" -af "aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$DUR,afade=t=in:d=0.6,afade=t=out:st=$(awk "BEGIN{print $DUR-1.4}"):d=1.4" renders/music-bus.wav

  lufs() { ffmpeg -hide_banner -nostats -i "$1" -af ebur128 -f null - 2>&1 | awk '/Integrated loudness/{f=1} f&&/I:/{print $2; exit}'; }
  local SI MI; SI=$(lufs renders/sfx-bus.wav); MI=$(lufs renders/music-bus.wav)
  # effects bus → -16 LUFS, music bed → -31 LUFS (15 LU under the effects)
  local SG MG; SG=$(awk "BEGIN{print -16-($SI)}"); MG=$(awk "BEGIN{print -31-($MI)}")
  ffmpeg -v error -y -i renders/sfx-bus.wav -i renders/music-bus.wav -filter_complex \
    "[0]volume=${SG}dB[a];[1]volume=${MG}dB[b];[a][b]amix=inputs=2:normalize=0[m]" -map "[m]" renders/premix.wav
  local PI; PI=$(lufs renders/premix.wav)
  local PG; PG=$(awk "BEGIN{print -14-($PI)}")
  ffmpeg -v error -y -i renders/premix.wav -af "volume=${PG}dB,alimiter=limit=0.84:level=false" -ar 48000 renders/mix.wav
  echo "sfx bus ${SI} LUFS → -16 | music ${MI} LUFS → -31 | premix ${PI} → mix $(lufs renders/mix.wav) LUFS"
}

mux() {
  ffmpeg -v error -y -i renders/blurred.mp4 -i renders/mix.wav -map 0:v -map 1:a \
    -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -profile:v high -c:a aac -b:a 256k \
    -movflags +faststart -t $DUR final.mp4
  echo "→ final.mp4"
}

case "${1:-all}" in
  video) video ;;
  audio) audio ;;
  mux) mux ;;
  all) video; audio; mux ;;
esac
