# DESIGN — iman-watch-collection (premium minimal / @arthurcbrooks reference)

## Style Prompt
Calm, literary, expensive. A talking-head clip of a luxury-watch collector, cut on the stressed word to cinematic b-roll, white paper canvases and black pause cards. White captions over footage with ONE oversized hero word per phrase: bold sans for facts and numbers, serif italic for feelings and names. A single royal blue accent lives only on white paper (lines, markers, serif words, name tags). Fine film grain on footage, paper grain on white. Motion is restrained: soft settles, slow push-ins, lines that draw.

## Colors
| Role | Hex |
|---|---|
| Near-black (pause cards, inset backgrounds) | `#0B0B0D` |
| White canvas / paper | `#FAFAFA` (paper tint `#F2F2F4`) |
| Royal blue accent (only on white / name tag) | `#1F4FD8` |
| Ink (text on white) | `#0B0B0D` |
| Caption white on footage | `#FFFFFF` (satellites at 80% opacity) |
| Hairlines (timeline, polaroid border shadow) | `#D9D9E0` |

## Typography
- **Inter** 500 (satellite words), 800 (sans hero words, tracking −0.03em).
- **Playfair Display Italic** 700 (serif hero words).
- Hero 120–190px, satellites 34–44px (≈25% of hero). Locally embedded in `assets/fonts/`.

## Layout rules
- 1080×1920. Captions on A-roll sit at y ≈ 1050–1350 (over the chest), never in the bottom 350px.
- Lockups: satellites tucked tight above/below the hero, aligned to the hero's left or right edge.
- Words appear one at a time in fixed slots, timed to the transcript. No re-flow, no karaoke color swap.

## Motion
- Cutaways enter with a quick settle (scale 1.06→1, blur 8px→0, 0.35s, `expo.out`) instead of a bare jump cut.
- Satellite words: opacity + 14px rise, 0.25s `power2.out`. Hero words: scale 0.94→1 + blur 6→0, 0.4s `expo.out`.
- Footage gets a slow push-in (1.00→1.05, linear) through each segment.
- Lines draw with `stroke-dashoffset`, `power2.inOut`. Polaroids drop with `back.out(1.4)` from −8° rotation.

## What NOT to Do
- No blue text over footage; no karaoke highlights, strokes, pills or boxes behind captions.
- No chrome text, perspective grids, whip-streaks or glitch transitions (MOTION_PHILOSOPHY defaults are overridden by this style).
- No more than ONE hero word per phrase; never two serif heroes stacked.
- No bottom-edge captions; no handles or CTA graphics on screen.
- Never show the burned-in source title (26.0–30.0s) — beat 8 covers the full frame.
