# DESIGN — Bike Masters Festive Offer

## Style Prompt
Bright, high-energy Indian agency-ad edit on top of a seated talking-head presenter, blending two studied references:
**@escapemedia.in**: giant bold red hero words placed in the upper third and composited *behind* the presenter, with props bursting toward camera.
**@fobet.media**: two-tier caption lockups (small setup words + one huge condensed keyword) and frosted-glass number boxes that act as receipts for every claim (the offer %, the service list).
The source video is the source of truth: no cuts to her speech, the visuals sync to it. Festive (Diwali-season) warmth comes from the gold accent and a few sparkles, not from clutter.

## Colors
- `#E3121B` Festive red: hero words, the offer, the brand name (meaning: *the offer / Bike Masters*)
- `#FFB703` Marigold gold: festive accent, "25%" glow, sparkles (meaning: *festive season / savings*)
- `#FFFFFF` White: captions and setup words
- `#0B0B0F` Ink: glass-box tint, caption stroke, end-card background
- `#1A1A22` Ink-2: card surfaces

## Typography
- **Anton**: hero words and big keywords (condensed, uppercase)
- **Poppins 800**: captions (rounded geometric, mixed case, like escapemedia)

## Motion
- Hero words: scale 1.35→1 with `expo.out` 0.35s, and a letter-by-letter build on the brand name
- Captions: 2–3-word phrase chunks, word-by-word pop (`back.out(2)` 0.14s). The active word turns gold.
- Transitions between beats: whip blur + red/gold colour flash (fobet glue) and a white light-streak
- Face: gentle grade + a 1.00→1.04 Ken Burns, with punch-ins (1.12×) on key beats

## What NOT to Do
- Never cut or re-time her speech
- Never cover her face with text (her head sits at y≈600–1000 of 1920); hero words go in the upper wall area (y≈140–600), captions at y≈1450–1700 over her lap
- No more than 4 colours; no cyan or blue (that's fobet's brand)
- No flat dark background slabs over the video for more than the end card
- No `-webkit-text-stroke`; use layered text-shadow
