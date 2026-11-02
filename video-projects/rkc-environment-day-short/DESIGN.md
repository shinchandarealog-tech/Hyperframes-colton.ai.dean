# DESIGN: Rhyming Kid's Corner · Environment Day reel

## Style Prompt
Live-action preschool reel with Hinglish voice. It uses the **hybrid** of the two studied references (`_reference/creator-library/_style-specs/hinglish-agency-offer-reel.md`): ref A's calm single-family typography and single accent, ref B's letter-drop keyword motion and one-idea-per-shot cutting. Every spoken phrase appears as a **keyword lockup**: one huge keyword plus small white connector words. On teacher shots the keyword sits **behind the teacher's head** (person matte). Nouns become objects popping around the head: earth, sapling, dustbin, bottle cards, recycle symbol, comment bubble. Sections are stitched with a **warm leaf-green light-leak flash**. The palette is pulled from the school's own backdrop logo. The mood is bright, warm, playful, and premium rather than cartoonish.

This spec overrides `MOTION_PHILOSOPHY.md`'s black-canvas / grid / chrome-text defaults for this format: it is a live-action presenter reel, not an abstract motion spot. It keeps the discipline (one idea per beat, motion on every transition, callbacks, rule of threes).

## Colors (5 hues, each with a meaning)
| Role | Hex | Meaning |
|---|---|---|
| Leaf green | `#3FAE3A` → light `#8BD94A` | nature / the main keyword colour / flashes |
| Sunshine yellow | `#FFC93C` | numbers & tips (TARIKA 1/2/3, "3" counter) |
| Brand pink → purple | `#E8336E` → `#6B3FB8` | the school name only (from the backdrop logo) |
| White | `#FFFFFF` | connector words, pills text |
| Deep ink | `#16240F` (88% alpha) | pill/badge backgrounds, text shadow |

## Typography
- **Poppins** only. Keywords 800, size 120–170px (6–9% of 1920). Connectors 600, 44–52px. Badges 700, 38px.
- Case: Title case. ALL CAPS only for the CTA name and the tip badges.
- Text shadow on every word: `0 6px 24px rgba(10,20,5,.55)` (legibility over busy backgrounds).

## Motion
- Keyword entrance: **letter-drop** (each letter from y −90px, scaleY 1.6→1, 1 frame stagger, `expo.out` 0.35s), or **slide-in** from off-frame (`expo.out` 0.25s), alternating, never the same pattern twice in a row.
- Connectors: word-by-word rise (y 24px, `power2.out` 0.2s) on their spoken word.
- Objects: `back.out(1.6)` pop 0.35s; tilted cards rotate ±8°.
- Section flash: radial leaf-green/white light leak, 0.4s, cut hidden at the peak.
- Teacher shots: punch-in 1.32× (wrapper transform) + slow 3% push across the shot (camera never sleeps).

## Layout
- Keyword band: y 14–32% (behind head on teacher shots). Connector band: y 34–40% or 52–60%.
- Never place text in the bottom 18% (IG/TikTok UI) or the right 12% from y 55–85% (action buttons).

## What NOT to Do
- No cyan, no lime `#B4FC54`. Those belong to the references.
- Don't copy either reference agency's logos, presenters, price lines or music.
- Don't cover a child's face with any graphic.
- Don't caption words we're unsure of (e.g. the "please …" tail at the end of the CTA).
- No pure-black frames anywhere (the source's black gaps were removed).
