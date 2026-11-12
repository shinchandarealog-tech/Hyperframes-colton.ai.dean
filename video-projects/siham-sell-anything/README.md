# Siham — "How I learned to sell anything" (32.5 s, 1080×1920, 30 fps)

Entirely code-built: footage in ffmpeg + Python/OpenCV, every caption/card/graphic in HTML/CSS + one GSAP
timeline rendered frame-by-frame in headless Chrome (transparent PNGs), composited with ffmpeg.

Deliverables: `final.mp4` (the edit), `showcase.mp4` (1080×1350, raw B&W vs final, CTA). QC stills: `qc/lines/` (one per line).

## Rebuild
Large media is not in git (`raw-media/` is gitignored): put the take at `raw-media/raw/take.mp4` (+ `take.wav`, 16 kHz mono)
and the Mixkit clips below at `raw-media/broll/<id>.mp4`.
```bash
python3 scripts/plan.py                 # cut list + word timings -> scripts/timeline.json
python3 scripts/base.py                 # graded/cropped footage, B-roll, collage -> renders/base.mp4
node scripts/capture.mjs                # GSAP overlay -> renders/ovl/*.png (+ qc.json, sfx.json)
python3 scripts/audio.py                # voice -14 LUFS, ducked bed, whooshes/pops -> renders/mix.wav
scripts/composite.sh final.mp4
python3 scripts/qc.py <blaze_face_short_range.tflite>   # safe area / overlaps / text-vs-face
```
Tools: faster-whisper small.en + medium.en (transcript), MediaPipe face detector (crop tracking, QC),
MediaPipe selfie_multiclass segmentation (installed; not needed — no room photo was supplied), GSAP 3.12.5 local copy.

## Editorial notes
- On-screen wording = Siham's actual delivery ("panic", "Ask before you pitch.", "Here's three", "fundamental"), per the client.
- The source has burned-in captions at chest height; every Siham crop stays above source row 1685 so they never show.
- Name card title is a placeholder (no names.txt): "Sales Manager · Fintech · SaaS · Real Estate".

## Stock (Mixkit free licence, assets.mixkit.co)
39815 young woman ending a call · 39790 worried woman on a phone call · 42655 woman writing in a spiral notebook ·
collage: 35902, 5461, 6367, 21780, 1728, 5454, 382, 40549, 12877.
Music/SFX from the workspace library: `assets/music/pop/es-upbeat-electronic-pop-indie-pop-version-gavin-luke.mp3`, whoosh-03/04/06, whoosh, pop.
