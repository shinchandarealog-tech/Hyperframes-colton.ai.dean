# Footage prep (re-create assets/clips/ from the originals)

Real footage (WhatsApp 480p) → `assets/raw/<date>-<seq>.mp4`; AI clips (Gemini, 720x1280, 4s) → `assets/raw-ai/aiNN.mp4` in the order received.

```bash
G="eq=contrast=1.06:saturation=1.05,unsharp=5:5:0.6"
# AI clips: crop bottom 152px to remove the Gemini ✦ watermark, upscale, then 0.8x slow-mo
for f in assets/raw-ai/*.mp4; do n=$(basename $f .mp4)
  ffmpeg -i $f -an -vf "crop=634:1128:43:0,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p" -c:v libx264 -crf 18 assets/clips/$n.mp4
  ffmpeg -i assets/clips/$n.mp4 -vf "setpts=1.25*PTS,minterpolate=fps=30:mi_mode=blend,format=yuv420p" -c:v libx264 -crf 18 assets/clips/$n-s.mp4
done
# Real clips: upscale + light grade (20261023-0009 is landscape → blurred-fill background)
for f in assets/raw/*.mp4; do n=$(basename $f)
  ffmpeg -i $f -an -vf "scale=1080:1920:flags=lanczos,$G,fps=30,format=yuv420p" -c:v libx264 -crf 18 assets/clips/r$n
done
```

Music: `assets/music-diwali.mp3` is synthesized (tanpura drone, temple bells, bansuri-style melody) — fully original, no licensing.
Edit: `scripts/shots.json` (shot list) → `python3 scripts/build.py` → `index.html`.
