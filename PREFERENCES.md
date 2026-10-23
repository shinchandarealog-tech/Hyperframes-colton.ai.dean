# PREFERENCES — Your Video Taste

Your accumulated taste for video work in this workspace. Populated over time via the `/feedback` skill.

**Read this file BEFORE every video task.** Apply the rules as overrides — they win over default skill choices and `MOTION_PHILOSOPHY.md` defaults when there's a conflict. If a section is empty, fall back to skill defaults.

Each bullet should end with a date in parentheses — that traces back to the per-session log under `_reference/feedback-logs/`.

> Seeded with the creative direction approved at `/setup` (2026-10-23). It keeps growing as you finish videos and run `/feedback`.

---

## Creative direction — approved at /setup

**These rules override `MOTION_PHILOSOPHY.md` wherever they conflict.** The goal is a premium, reusable motion graphics language for short-form talking-head videos — inspired by Apple product presentations, sophisticated editorial motion graphics, and thoughtfully designed spatial UI. It must feel professionally art-directed, never like a generic AI tech edit or a collection of premade templates. Tokens live in `assets/brand-tokens.css`.

## Visual style

- Palette: near-black `#0B0B0D`, graphite `#1C1D21`, raised graphite `#2A2C31`, warm white `#F4F1EA`. Electric blue `#3D7BFF` only when it serves the content; warning orange `#FF9F43` rarely. (2026-10-23, setup)
- Preserve the original footage as the visual foundation. Never impose a dark color grade or graphic background on footage just because the palette is dark — change its look only for a specific, justified creative decision. (2026-10-23, setup)
- Dark graphic surfaces are the default; warm-white panels with dark type are allowed when they better serve the footage or concept. (2026-10-23, setup)
- Typography: Geist for headlines and body; Geist Mono only for genuinely technical details (code, values, specs, timestamps). Fonts are self-hosted — copy `assets/fonts/` into each project. (2026-10-23, setup)
- The type scale in `brand-tokens.css` is a flexible starting point. Pick sizes by hierarchy, content, composition, and mobile readability. (2026-10-23, setup)
- Materials: fine hairline borders, realistic but restrained shadows, carefully controlled depth. Glassmorphism is one optional material, never the default UI style. (2026-10-23, setup)
- Use a wide visual vocabulary — editorial typography, anchored labels, inline annotations, structured panels, diagrams, spatial layouts, custom compositions. Do not make every graphic a floating glass card. (2026-10-23, setup)
- Graphics must feel compositionally connected to the speaker and footage (eyelines, gestures, negative space, alignment to the frame), not like unrelated overlays. (2026-10-23, setup)
- Every graphic needs a clear informational, narrative, or visual purpose. If it doesn't earn its place, cut it. (2026-10-23, setup)
- Keep everything readable on a 9:16 phone screen and inside the safe zones (top 220px, bottom 380px, right 140px clear; 64px side margins). (2026-10-23, setup)
- Maintain visual variety without sacrificing consistency — the system is a flexible visual language, not a fixed template. (2026-10-23, setup)

## Pacing

- No arbitrary average scene duration and no mandatory outro hold. Timing follows the script and the actual footage. (2026-10-23, setup)
- Motion uses deliberate timing and excellent easing. Eases: `power3.out` enter, `power2.inOut` move, `expo.out` emphasis, `power2.in` exit. Durations: micro 0.18s, standard 0.45s, structural 0.8s, stagger 0.04–0.08s. Bounce/elastic only when the content calls for it. (2026-10-23, setup)

## Captions

_(style, color, sync tightness, word-by-word vs. phrase chunks — populated by /feedback over time)_

- _no rules captured yet_

## Transitions

- Motion must communicate hierarchy, relationship, emphasis, or meaning — if it doesn't, it doesn't move. (2026-10-23, setup)
- Select the treatment and transition per content beat: masks/reveals, anchored labels drawing in, line/arrow connections, layout morphs, focus pulls, clean cuts on the beat. (2026-10-23, setup)
- Do not apply the same entrance, transition, or layout to every scene. (2026-10-23, setup)
- Avoid unnecessary animation, excessive motion blur (light, only on fast moves), gratuitous particles, and distracting effects. (2026-10-23, setup)

## Audio

_(music vibe, voiceover style, SFX, mix — populated by /feedback over time)_

- _no rules captured yet_

## Brand

_(logo treatment, hashtags, handles, brand-tokens overrides — populated by /feedback over time)_

- _no rules captured yet_

## Avoid

_(anti-patterns to never repeat — populated by /feedback over time)_

- OPT-IN ONLY, never by default: black perspective grid, crosshairs, vignette, grain, chrome-gradient text, glowing text, whip transitions. Use one only when a specific concept justifies it. (2026-10-23, setup)
- Generic AI-tech-edit look and template feel; every graphic as a floating glass card. (2026-10-23, setup)
- Arbitrary scene-length or outro-hold rules imported from `MOTION_PHILOSOPHY.md`. (2026-10-23, setup)
