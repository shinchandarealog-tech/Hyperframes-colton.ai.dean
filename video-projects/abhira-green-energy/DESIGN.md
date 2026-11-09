# DESIGN — Abhira Green Energy (solar promo reel)

## Style Prompt
Warm, optimistic, premium solar-energy reel. AI-generated cinematic footage (rooftop
panels, homes at golden hour, glowing energy lines) carries the image; bold Hindi
kinetic typography carries the message. Type is lit, not flat: white with a soft
green halo, key words punched in sun-gold. Every cut hides inside a quick light
flash or a blur/zoom push. Subtle grain + vignette on everything. The Abhira logo
lives in the top-right corner for the whole video.

## Colors (taken from the logo)
| Role | Hex | Meaning |
|---|---|---|
| Text base | `#FFFFFF` | body words |
| Leaf green | `#7ED321` | halo/glow, "green / savings" accents |
| Deep green | `#0F5A1E` | text shadow / underline bars |
| Sun gold | `#FFB52E` | hero key-word highlight (bill, subsidy, solar) |
| Sky blue | `#2E8BFF` | used sparingly (light-flash tint only) |

## Typography
- Poppins 800 (Devanagari + Latin, self-hosted woff2 in `assets/fonts/`) for kinetic words
- Poppins 600 for small supporting lines

## Motion
- Words enter with scale + blur + y (expo.out / back.out), staggered per word
- Cuts: 0.25s white-gold light flash or zoom-blur push
- Footage always slowly pushes in (Ken Burns 1.0 → 1.08)

## What NOT to Do
- No text in the top 14% (logo zone) or bottom 20% (platform UI)
- No text over the AI clips' own baked-in cards (subsidy card, address card, contact card, end logo) — those beats get minimal/no kinetic type
- No more than ~4 words on screen at once
- No hard jump cuts
