# Home tour reel — 37 s, 1080x1920, 24 fps

Source: karine.homes house tour (720x1280, 24 fps, 120 s). Output frames map 1:1 to source frames (24 fps kept on purpose).
Voice = Demucs vocal stem, -14 LUFS; bed = the source's own music stem (continuous, ~-31 LUFS); 6 whooshes, 12 soft ticks.

| # | Out frames | Source frames | Beat |
|---|---|---|---|
| 1 | 0–54 | 0–54 | Hook: blurred rounded card on white sharpens, coral chip "CUSTOM-BUILT" tracked to chest |
| 2 | 55–172 | 55–172 | Card expands full-frame; "EXECUTIVE HOME / COMPLETED IN [2025]" + icon chips |
| 3 | 173–299 | voice 14.00–19.29 s | White scene: "STEP INSIDE TO OVER" + coral "3,300 SQ FT", photo cards flip |
| 4 | 300–421 | 593–714 | Kitchen b-roll, coral gradient rises, small white line |
| 5 | 422–546 | top 715–839, bottom 1154–1278 | Split screen, caption + coral chip between cards |
| 6 | 547–599 | 1509–1561 | Definition tag: coral asterisk, "Walkout basement", chips |
| 7 | 600–696 | 1562–1658 (UI card) | Light gradient: coral headlines, cut-out, stars, UI cards |
| 8a | 697–790 | 2078–2171 | Drone b-roll, coral check + "1.2 PRIVATE ACRES" |
| 8b | 791–887 | 2172–2268 | Presenter: "REACH OUT TODAY TO" + coral box "BOOK YOUR PRIVATE SHOWING" |

## Rebuild
```
python3 -m demucs -n htdemucs --two-stems=vocals -o assets/stems assets/src/raw.wav
# extract source frames listed above to renders/srcframes/f%05d.jpg (ffmpeg select + -frame_pts 1)
python3 scripts/build_audio.py          # renders/mix.wav
./scripts/render_parallel.sh            # renders/video_only.mp4 (headless Chromium, 180° shutter)
python3 scripts/qc.py renders/video_only.mp4 renders/qc   # jump / freeze / 1:1 checks + segment stills
ffmpeg -i renders/video_only.mp4 -i renders/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k renders/final.mp4
```
