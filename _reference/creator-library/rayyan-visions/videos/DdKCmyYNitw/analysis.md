# DdKCmyYNitw — @rayyan-visions (text-animation reference)

**Source:** Instagram Reel, uploaded by the user as a local file (`Video_by_rayyan_visions_DdKCmyYNitw.mp4`)
**Duration:** 26.27s · 9:16 · 720x1280 @ 30fps
**Studied:** 2026-10-29, scoped to the **caption/text animation**, which is what the user asked to copy.
**Sample rate:** 4fps across the whole video, plus every frame (30fps) for 5 caption builds (0.2–1.1s, 0.95–2.05s, 16.4–17.4s, 22.75–23.55s, 24.0–25.2s).

Like the @daniel-hee reel, this is an editing-service ad wrapper ("Raw" vs "Final Edit" cards, blue gradient canvas, "DM me to work together"). Only the inner Final Edit card is the edit.

## Text animation (the signature move)
- **Word-by-word on the spoken beat.** Each word appears on its own timestamp. Phrases build to 1–2 lines ("IF YOU NEED / CONTENT IDEAS", "ALL YOU NEED / TO DO", "YOU WILL GET / 10 CONTENT IDEAS", "WITH THIS DONE").
- **Fly-in:** each word starts at ~25–40% opacity, grey/desaturated, blurred, ~1.2–1.3x scale, offset ~80–100px (1080 scale) up-right, up, up-left or right. It travels to its slot in ~5–7 frames (≈0.2s) with a strong ease-out and lands sharp. Direction varies word to word. Words on line 2 often fly in over line 1.
- **Look:** Montserrat-style heavy italic caps. Line 1 is white with a soft white glow; line 2 is the accent colour (purple/violet gradient) with a soft glow. Sits center frame at chest/mic height.
- Earlier words stay put while the next one arrives (the line re-centres slightly as it grows).
- Clears with a hard cut to the next phrase.

## Other moves (not requested)
Icon pops (Instagram/TikTok/YouTube, ChatGPT logo) under the caption, phone-UI typing screens, a red flash glitch, thumbnail montage cutaways.

## What to steal (approved version, used in `video-projects/10-80-style-edit`)
The user signed off on this exact recipe. Reuse it when they ask for "the rayyan text animation":
- **Per-word drop-in** on each word's spoken timestamp: starts ~230px above its slot (1080 scale) with a slight sideways drift (±50px), opacity 0, scale 1.06, plus a **vertical motion-blur streak** (SVG feGaussianBlur stdDeviation "1.5 16" → "0 0"). Lands in 0.17s, power2.out. See `flyIn()` in that project's `index.html`.
- **Flat baseline.** Every word rests on the same line. The user explicitly rejected staggered "bouncy" word heights.
- **Line 1:** heavy italic caps (Montserrat 800 italic) in white with a soft white glow.
- **Line 2 / keywords:** same treatment in the accent colour. The user chose orange over the reference's purple.
- Phrases of 1–2 lines that build word by word, then hard-cut to the next phrase.

## Don't copy
The ad wrapper, the purple palette (the user chose orange), and the creator's handle and branding.
