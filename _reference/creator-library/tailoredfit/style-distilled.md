# @tailoredfit — Style Fingerprint

Rolled up across 3 videos. See `videos/*/analysis.md` for per-video detail. Last distilled: 2026-10-18.

**This is the client's target style.** For this workspace's client builds, it overrides `MOTION_PHILOSOPHY.md` defaults (that file's black-canvas, chrome-text, perspective-grid aesthetic does NOT apply here). Keep only MOTION_PHILOSOPHY's discipline: one idea per beat, stylized transitions at section boundaries, every-frame review.

## The formula (identical script skeleton in all 3)

| Beat | Time | What happens |
|---|---|---|
| 1. Pain hook | 0–5s | "What if I told you…" / "If you have pain…". Pain **visualized on the body** (X-ray, red ring, collapse arrows). Exercise already in motion on frame 1 |
| 2. Promise | 4–8s | "simple / easy / 3× a week". Kinetic word (vertical "EASY"/"FIX"), optional split-screen preview of all exercises |
| 3. Steps | 8–48s | 1–3 exercises. Each one: setup → cue → hold/reps → **why it works** (anatomy overlay) |
| 4. Explainer card | once, mid-video | White grid-paper infographic card that builds element by element (~3–5s) |
| 5. Pattern interrupt | last ~15s | "Oh, and by the way, you and I both know you're gonna save this and forget…" Phone shot, then a self-aware face-cam skit with sticker collage |
| 6. CTA | final ~6s | Phone (mockup or handheld) showing the program. Fixed header **COMMENT "KEYWORD" TO GET STARTED!**, running captions below |

Length: 45–66s. Voice-over drives everything, with a continuous music bed underneath.

## Signature moves (consistent across videos)
- **Hook pattern:** relatable pain question + the pain *drawn on the body part* within 2s. No title card, no intro. Movement from frame 1
- **Caption treatment:** 1–4 word chunks, heavy geometric sans ALL CAPS (Montserrat Black / Poppins ExtraBold feel), white base, soft dark drop shadow, **one active word recolored**. Accent color changes per section and often matches the prop in frame (green band → green words, pink band → pink). Captions sit in negative space, often **in 3D perspective on the floor, wall or bench**. Never over the movement
- **Motion-graphics layer (the big differentiator):**
  - anatomy overlays: glowing red/orange muscles, X-ray bones, heat gradients
  - neon form cues: angle lines (90°), arrows, dashed foot paths, rep numerals, all drawn on with a glow
  - target / ripple rings at pain or contact points (red = pain, green = healthy)
  - callout pills with leader lines ("Patellar Tendon")
  - rounded picture-in-picture context tiles (sprinter, ankle brace, anatomy inset)
  - sticker-label tags ("HOLD")
- **Transition rotation:** hard cuts inside a section. At section changes: motion-blur whip, 3D card flip, white frame flash, punch-in zoom
- **Face treatment:** body-part framing ~65–75% of runtime (feet, shins, knees). Face only in the skit and occasionally in seated demos
- **Footage look:** bright, warm, soft contrast, shallow depth of field, low camera height, side profile for angle-based cues
- **Palette:** #f0a800 orange-yellow (primary accent), #fc3c48 red (pain/cues/CTA), #60cc30 green (healthy/progress), #ffffff, #111111. Optional prop-matched section accent (e.g. #f03060 pink)
- **Energy profile:** breathing. Fast hook, steady educational middle, comedic spike, then a confident CTA

## What to steal (ranked by Hyperframes copy-ability)
1. **Word-highlight phrase captions** with per-section accent color: pure HTML/CSS + GSAP, synced to `transcript.json` word timestamps. *Fully reproducible*
2. **Neon form cues** (arrows, angle lines, dashed paths, rep numerals, ripple rings): SVG + `stroke-dashoffset` draw-on + `filter: drop-shadow` glow. *Fully reproducible*; needs per-shot placement
3. **Kinetic hook words** (vertical letter-stacked "EASY"/"FIX", retro stacked-shadow "BE FIXED"): GSAP stagger. *Fully reproducible*
4. **White explainer card** (grid paper, condensed black headline, red labels, dashed video tiles, branching arrows, line-art) with step-by-step build + 3D card-flip exit: HTML sub-composition. *Fully reproducible* and the strongest "wow" per hour of work
5. **Perspective captions on floor/wall**: CSS 3D transforms per shot. *Reproducible*; static per shot (no camera tracking)
6. **Split-screen exercise preview**, **PiP rounded context tiles**, **phone-mockup CTA** with fixed header: *Fully reproducible*
7. **Callout pills with leader lines**: *Reproducible* for locked-off shots
8. **Anatomy overlays** (glowing muscles / X-ray): *Reproducible* with muscle/bone PNG art (`mix-blend-mode: screen`, glow pulse). Needs an asset per body part, and only works on fairly static shots (no motion tracking in Hyperframes)
9. **Selective background recolor** (pillar turning red): *Hard*. Needs a hand-made mask. Skip for the sample
10. **Sticker collage skit**: reproducible if the client films a skit. Use original or royalty-free stickers

## Don't copy
- "LONGEVITY" keyword, TailoredFit app screens, "12-week routine free for 30 days" offer → swap in the client's own keyword and offer
- The exact skit script ("social media onset ADHD") → keep the *structure* (self-aware "you'll save this and forget" interrupt), rewrite the words
- Third-party IP stickers (Squidward, betting-app logos, podcast thumbnails)
- @tailoredfit's face, gym and branded equipment

## Videos studied
- [deuxfa4bj5r](videos/deuxfa4bj5r/analysis.md): 3 exercises for tight/unstable ankles, 66s. Richest motion-graphics example (X-ray, split-screen, card flip)
- [dd7kwt6p-e4](videos/dd7kwt6p-e4/analysis.md): patellar tendon knee program, 46s. Symptom-montage hook, angle-guide lines, program card
- [dbzxkqdbnpw](videos/dbzxkqdbnpw/analysis.md): one exercise for collapsing ankles / flat feet, 50s. Prop-matched pink accent, neon foot path, branching explainer card
