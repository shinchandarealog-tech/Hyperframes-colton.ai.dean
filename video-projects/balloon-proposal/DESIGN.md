# DESIGN — Balloon Proposal (one take)

## Style Prompt

Previs mannequin look (reference: `assets/style-ref-previs.jpg`). Two featureless capsule-limbed figures with soft volume shading lit from the sunrise side: him in solid blue, her in red-orange with long hair and a gown. The camera starts at eye level inside a dark wooden basket, framed by the corner posts against a slate-blue to orange horizon. It is one continuous camera move: he kneels with the ring box, she says yes, they hug, she shoves him over the side, and the camera follows his slow, tumbling fall down onto a cloud, where the ring's glint becomes a star.

## Colors

| Role | Hex | Meaning |
|------|-----|---------|
| Him | `#2a55d8` (shade `#16308a`, light `#5a84ff`) | the blue mannequin |
| Her | `#b3432a` (shade `#6e2414`, light `#e06a44`) | the red-orange mannequin |
| Sky | `#3f5283` → `#f0903a` horizon | dawn |
| Basket | `#4c3a28` / `#2c261b` | the set |
| Ring | `#ffd27a` + white glint | the callback object |

Type is cream `#fff3e2` with a warm halo.

## Typography

- **Cormorant Garamond**, italic, lowercase. All on-screen words.

## Motion rules

- One take. No cuts. The camera move is the edit.
- Parallax depth: sky 0.15×, far clouds 0.5×, world 1×, foreground clouds 1.4×.
- Fall: flung out fast, then a decelerating, floaty descent with one constant lazy spin. The follow-cam tracks his body centre.
- Callback: the ring glints three times, and the last glint becomes a star.

## What NOT to Do

- No faces or detail on the mannequins. Keep it previs-simple.
- No hard cuts or black frames.
- No names or handles on screen (per CREATOR.md).
