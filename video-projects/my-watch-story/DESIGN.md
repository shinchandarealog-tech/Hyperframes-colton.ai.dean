# My Watch Story — Design

Source: the storyboard brief (Nov 2026). Explicit user direction overrides MOTION_PHILOSOPHY defaults
(hard cuts kept, flat white type, no grid texture).

## Style Prompt
Quiet luxury. Black letterbox around a centred 16:9 shot (y 656–1264). White type only, one soft
rose-gold accent taken from the 5711R for lines, lit dots and glints. Everything glides in with
8–12 frame ease-outs; only the WATCH ROLL label and the Argos map pin bounce.

## Colors
- `#000000` canvas / letterbox
- `#FFFFFF` all type (dim state 45% white)
- `#E3AD97` rose gold — lines, lit timeline dots, glints, ring strokes
- `rgba(12,11,12,.58)` card fill, 1.5px `rgba(255,255,255,.86)` outline, 18px radius

## Typography
- Playfair Display — header lines, card names, numbers, caption key word (italic)
- Inter 600 — captions, tracked caps labels

## Safe zones
No text above y 230. Nothing below y 1560. Nothing in x > 950 for y > 960.

## What NOT to Do
- No second accent colour, no gradients on type
- No bounce/overshoot except WATCH ROLL label and map pin
- Don't touch the speaker's audio or the camera cuts
- Never let the burned-in "PATEK PHILIPPE NAUTILUS" lower third (28.0–32.55 s, source y ≥ 900) show:
  the 125% punch-in is top-anchored so it stays out of frame
