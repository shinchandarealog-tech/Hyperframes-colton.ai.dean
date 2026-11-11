# Transition Overlay Library — Asset Index

Source: the creator's own "Transition PACK" (`_source/transition-pack.mp4`, 1080×1920 @ 60fps, 23.9s), split into 10 standalone clips with the label cards removed. Every clip is **1080×1920, 60fps, H.264, no audio track**. Where the pack had a sound baked in, it's saved as a matching `.mp3` next to the clip.

All clips are **light-on-black overlays**: the black parts disappear when you composite with `mix-blend-mode: screen`, so the effect sits on top of whatever is underneath. No alpha channel needed.

## Quick pick — by vibe

| Transition | File | Length | Peak (cut here) | SFX | Energy | Looks like / use for |
|---|---|---|---|---|---|---|
| Red light leak | `red-light-leak.mp4` | 1.10s | 0.47s | `red-light-leak.mp3` | calm | Soft orange-red glow with a thin light filament. Warm, gentle scene change, story beats, intros |
| Film burn 01 | `film-burn-01.mp4` | 0.92s | 0.07s (hits immediately) | `film-burn-01.mp3` | high | Big yellow→red orb floods the frame instantly, then fades out. Punchy cut on a beat drop |
| Lite burn | `lite-burn.mp4` | 0.77s | 0.27s | — | medium | Creamy white/beige light flare that washes the frame. Bright "flash" cut, before/after reveals |
| Spinning shape | `spinning-shape.mp4` | 1.05s | 0.87s (expands at end) | — | medium | Small rotating crosshair/bracket reticle (white + green) that spins and grows. Focus/target moments, "zoom into this" beats, tech/AI topics. **Does not cover the frame** — pair with a cut or zoom underneath |
| Fast streak | `fast-streak.mp4` | 1.08s | 0.22s | — | high | Gray/white horizontal speed streaks + halftone texture, full frame. Fast-paced edits, whip-style cuts. Has a small `@hamz…` watermark in the bottom-right corner (see notes) |
| Burning overlay | `burning-overlay.mp4` | 1.43s | 1.00s | — | high | Flying sparks/embers build into a fiery flash. Hype moments, "this is fire", aggressive reveals |
| Film burn 02 | `film-burn-02.mp4` | 1.52s | 1.18s | `film-burn-02.mp3` | medium | Orange film-edge burn with sprocket-hole texture, two pulses. Vintage/cinematic scene change |
| Mix film burn | `mix-film-burn.mp4` | 1.90s | 1.87s (several flashes) | `mix-film-burn.mp3` | high | Rapid sequence of yellow/orange film-burn flashes (~0.3s, ~1.0s, ~1.75–1.9s). Montage/flashback, multi-cut sections |
| Old film | `old-film.mp4` | 1.53s | — (texture) | — | calm | Very subtle dust specks + scratches on black. Not a cut. Lay it over a scene for a vintage/nostalgic texture (loop or stretch) |
| Glitch | `glitch.mp4` | 0.90s | 0.60s | — | high | White digital dash lines, a scan-bar burst, then a full white flash. Tech/AI topics, "error"/"system" beats. Pair with `sfx/transitions/glitch.mp3` |

"Peak" = the brightest frame (most coverage). **Line up the peak with the scene cut** so the flash hides the switch: overlay `data-start` = `cut time − peak`.

## How to use in a Hyperframes composition

1. Copy the clip (and its `.mp3` if it has one) into the project:
   ```bash
   cp ../../assets/transitions/film-burn-01.{mp4,mp3} assets/
   ```
2. Put the overlay on a track above the scenes. Screen-blend it, and don't give the `<video>` `class="clip"`:
   ```html
   <style>
     .fx-overlay { position:absolute; inset:0; width:100%; height:100%; object-fit:cover;
                   mix-blend-mode:screen; pointer-events:none; z-index:50; }
   </style>

   <!-- scene cut at 1.40s, film-burn-01 peaks at 0.07s → start at 1.33 -->
   <video id="fx-burn-1" class="fx-overlay" src="assets/film-burn-01.mp4" muted playsinline
          data-start="1.33" data-duration="0.92" data-track-index="5"></video>
   <audio id="sfx-burn-1" src="assets/film-burn-01.mp3"
          data-start="1.33" data-duration="0.92" data-track-index="6"></audio>
   ```
3. Every element needs a unique `id` (lint enforces it on media). Use a different `id` for each placement.

Verified: a test render (blue scene → green scene with `film-burn-01` screen-blended over the cut) rendered cleanly with `npx hyperframes render`. The burn showed over the scenes and the black parts of the clip didn't show. Lint passed with 0 errors.

## Notes + gotchas

- **Screen blend only brightens.** On a pure-white scene the overlay won't show. These work best on mid-to-dark footage, which is the workspace default (black canvas per `MOTION_PHILOSOPHY.md`).
- **Recolor**: the burns are warm orange. To match a cooler brand accent, put `filter: hue-rotate(…)` on the `<video>`. Don't animate the video's size or position. Wrap it in a `<div>` if it has to move.
- **Fast streak watermark**: the original pack has an `@hamz…` handle burned into the bottom-right of the fast-streak clip. To hide it, scale the clip up slightly (e.g. `transform: scale(1.06)` on a wrapper `<div>`, `transform-origin: top left`) to push the mark off-frame.
- **Licensing**: the creator confirmed they have permission to use everything in this pack, including in monetized posts.
- **60fps source, 30fps renders**: fine. Hyperframes samples the frame at each render timestamp. Render at `--fps 60` to keep every frame of the faster ones (fast-streak, glitch).
- **Re-cutting**: the untouched pack is in `_source/`. The clips were cut on these exact source frame ranges (60fps): red-light-leak 85–150, film-burn-01 235–289, lite-burn 369–414, spinning-shape 480–542, fast-streak 607–671, burning-overlay 737–822, film-burn-02 888–978, mix-film-burn 1044–1157, old-film 1222–1313, glitch 1377–1431. The label cards overlap the first ~0.1–0.25s of some effects (film-burn-01, lite-burn), so those clips start just after the label clears and open a little brighter than in the pack.
