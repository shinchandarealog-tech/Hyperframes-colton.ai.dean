# DESIGN — Balloon Proposal (one take)

## Style Prompt

A dreamy, surreal sunrise told in a single unbroken camera move. Characters are backlit silhouettes with a warm gold rim light. The world is soft pastel dawn: a lavender sky melting into peach and gold, a cloud sea, and a hot-air balloon in rose and gold. The camera rises out of the clouds, pushes in on the basket for the proposal, holds through the "yes" and the hug, then pulls back as he is shoved over the edge. It follows his slow, spinning fall down into the clouds, where he lands softly on his back with the ring held up to the sky. The ring's glint drifts up and becomes a star. Nothing is ever static: clouds parallax, motes drift, the vignette breathes.

## Colors (5 symbolic hues)

| Role | Hex | Meaning |
|------|-----|---------|
| Plum silhouette | `#2a1b3d` | the two of them / the night that is ending |
| Dawn lavender | `#6c5aa8` → `#c98bb0` | the dream / the fall |
| Peach | `#ffc58f` | the sunrise / warmth |
| Gold | `#ffd27a` | the ring, the sun, the star (one object, three times) |
| Rose | `#e0607e` | her / love (ribbon, hearts, balloon stripes) |

Type is cream `#fff3e2` with a gold halo.

## Typography

- **Cormorant Garamond**, italic, lowercase. All on-screen words.

## Motion rules

- One take. **No cuts, no scene transitions.** The camera move is the edit.
- Parallax depth: sun 0.15×, far clouds 0.5×, world 1×, foreground clouds 1.4×.
- Slow motion during the fall: a 7s sine.inOut descent with one full lazy spin.
- Callback: the ring glints three times (proposal, mid-fall, landing), and the final glint becomes a star.
- Unifying texture (instead of MOTION_PHILOSOPHY's grid): warm vignette, CSS grain, and drifting light motes on every frame.

## What NOT to Do

- No hard cuts and no black frames. It is one shot.
- No flat white text; always cream with a gold halo.
- No slapstick SFX. The shove is a soft whoosh; the tone stays dreamy.
- No names or handles on screen (per CREATOR.md).
- No neon, cyan or pure black.
