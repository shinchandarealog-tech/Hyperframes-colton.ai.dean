# boat — launch promo · DESIGN

## Style Prompt
Keynote-style product launch. A black stage lit by one soft, slowly breathing glow
(deep red → orange → cream). Thin white type, wide and calm. Frosted-glass surfaces
(tiles, panels, pills) catch the glow from behind. The motion carries the energy:
spring/expo eases, push-ins with blur, fast flashes to black. Nothing pops.

## Colors
| Role | Hex |
|---|---|
| Stage | `#000000` |
| Glow — deep red (outer) | `#8a0f0c` |
| Glow — orange (mid) | `#ff6a1a` |
| Glow — cream (core) | `#ffe9cc` |
| Accent streak — yellow | `#ffc83d` |
| Type | `#ffffff` (dim: `rgba(255,255,255,.62)`) |

## Typography
- Display + UI: **Inter**, weights 100–300. Headlines 120–150px weight 200, tracking −0.01em.
- Numbers: Inter 100, `tabular-nums`.

## Motion
- Eases: `expo.out` entrances, `expo.in` push-throughs, `back.out(1.4)` / `elastic` only for
  small springy UI (tile, chips, pill overshoot). `sine.inOut` for the breathing glow + orbit.
- Scene changes: push-in + blur, or a 4-frame flash to black (glow keeps breathing beneath).
- Motion blur: averaged sub-frames at render (240 fps capture → 4-sample 180° shutter → 30 fps).

## What NOT to Do
- No hard pops on/off, no number swaps (counts only).
- No bold/heavy type, no more than the 5 colours above.
- No full-screen linear gradients (banding) — radial glows + grain only.
- No perspective grid / chrome text (this brief replaces the house texture).
- Placeholder logo + screens: never imitate any real brand's marks.
