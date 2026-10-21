# DESIGN — Apple-style UI over talking head

## Style Prompt

Apple keynote / iOS UI language layered on a bright, real-world talking-head clip. Frosted "liquid glass" cards, Dynamic-Island pills and iOS notification banners spring in around the speaker's face, never over it. A single system-blue accent marks the one thing that matters in each beat. Motion is calm and physical: spring overshoots, soft blur-ins, no glitch or neon.

## Colors

| Role | Hex | Use |
|---|---|---|
| Glass dark | `rgba(28,28,30,0.72)` (`#1c1c1e`) | Card / pill fill over the bright room |
| Text | `#f5f5f7` | All text on glass |
| Secondary | `#a1a1a6` | Labels, sub-lines (brightened from `#86868b` for contrast on glass) |
| Accent | `#0a84ff` | The one key word/number per beat, active caption word, progress rings |
| Warm highlight | `#ff9f0a` | Festive / offer beat only (the "25% OFF" moment) |

## Typography

- Display + UI: **Inter** (SF Pro stand-in, embeds reliably), weights 600–800, tight tracking (-0.02 to -0.04em).
- Numbers: `font-variant-numeric: tabular-nums`.

## Motion

- Entrances: spring (`back.out(1.4–1.8)`), `expo.out` blur-ins, iOS banner drop from top (`power3.out`).
- Exits: scale-down + blur to 0 (`power2.in`, 0.25–0.3s) — Dynamic-Island "collapse".
- Ambient: subtle 1.00 → 1.03 Ken Burns on the face; glass cards float ±6px (`sine.inOut`).

## Adaptations from MOTION_PHILOSOPHY.md

The source is a bright, real-room talking head (pre-edited, source of truth), so the black canvas / perspective grid are not used. Kept: one idea per beat, light glows on glass edges, vignette + faint grain on the frame, motion-led transitions, callback (the Bike Masters pill returns at the outro), outro hold.

## What NOT to Do

- No overlays covering the face (eyes/mouth zone ≈ y 420–900 at 1080×1920).
- No neon, chromatic glitch or heavy shaders — this is Apple-calm.
- No more than one accent color per beat; orange only for the offer beat.
- Never cut, trim or re-time the speaker's audio.
- Nothing inside the Reels bottom UI zone (bottom ~280px) or the right action rail.
