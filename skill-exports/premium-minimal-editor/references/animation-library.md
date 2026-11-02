# Animation library (A01–A27)

Reusable designs observed in the premium minimal style. Cite the ID in edit-plan options ("A04 paper graph"). Durations are typical on-screen times. Build notes use generic editor terms; a code-based equivalent (HTML/GSAP or Remotion) is given where it helps.

Default motion vocabulary:
- **Scene settle:** scale 1.06→1 with blur 8px→0 over 0.35s, ease-out (expo). Use it instead of a bare jump cut.
- **Satellite word:** opacity 0→1 with a 14px rise over 0.25s, ease-out.
- **Hero word:** scale 0.94→1, blur 6px→0 and opacity 0→1 over 0.4s, ease-out (expo).
- **Slow push:** scale 1.00→1.05 across the shot, linear.
- **Line draw:** stroke reveal (trim path / stroke-dashoffset), ease in-out.
- **Photo drop:** from y −90px, rotated ±14°, opacity 0, landing over 0.55s with a slight overshoot (back-out 1.4).

| ID | Animation | Duration | Trigger | Build notes |
|---|---|---|---|---|
| A01 | **Painting + giant hero word** | 0.8–3s | Abstract noun / thesis | Full-bleed painting, slow push 1.00→1.04, darkened edges. Hero word white, 150–190px, satellites 40px. Put the word in the painting's empty space (sky, wall). |
| A02 | **Breath card** | 0.5–1.5s | Pause after a big claim | Solid black (or white) card, ONE serif italic word or short phrase, fade or blur in. Nothing else on screen. |
| A03 | **Blue serif on white paper card** | 1–1.5s | Short emotional line; endings | Off-white paper with grain; blue Playfair italic hero, small ink satellites; words appear in fixed slots. |
| A04 | **Paper graph** | 2–3.5s | Numbers, growth, "progress" | Faint grid on paper; a thin (6–8px) blue zig-zag line draws from bottom-left and **exits the frame top-right**; a blue ball with a soft glow rides the line's head; the number lands huge in black sans when spoken. |
| A05 | **Ghost/echo word** | ~1s | "backwards", "forward", "drift" | 3–4 copies of the word offset along x with falling opacity (0.6→0.1), sliding. |
| A06 | **Grainy B&W halftone b-roll + play/pause icon** | ~3s | Momentum / stopping | Desaturate, contrast up, heavy grain or dither; a white play ▶ or pause ⏸ icon pops center on the matching word. |
| A07 | **Kaleidoscope shard list** | ~4s | List of 3 | White canvas; a downward triangle mask holds a painting; shards rotate to swap paintings per list item; a small metallic 4-point star at the pivot. |
| A08 | **Split-screen stacked paintings** | 0.5–1s | "multiple domains", comparisons | Two paintings stacked top and bottom (1080×960 each), one line of text across the seam. |
| A09 | **Fixed-slot caption on the face** | per phrase | Default caption | The whole phrase pre-laid out; each word fades in at its timestamp; the hero word on its own line. |
| A10 | **Flat blue claim card** | 1–2s | Restating a claim in 4–6 words | Full-bleed `#0A47FF`, white sans, one bold hero word. |
| A11 | **Light-leak flash card** | ~0.5s | Rhythm break | Pink or peach gradient with blur, an optional vertical type fragment. Use rarely. |
| A12 | **Anatomical silhouette with glowing nerve lines** | ~3s | Brain or body science | Dark head silhouette from behind on deep red (`#8B0E0A`); thin pink-white lines draw down the neck with a glow. One-off accent. |
| A13 | **Name / object callout** | 1–2s | Named person or specific object | Thin white curved line drawn from the subject to a label; small-caps brand or line in white; name in white bold sans on a **blue box** that grows left-to-right, with the text revealed letter by letter. Optional ring drawn around the object first. |
| A14 | **Research paper + yellow highlighter** | ~4.5s | "Studies show…" | White page with a real paper's title and abstract; yellow highlight bars sweep line by line (scaleX 0→1 from the left); keyword captions above. |
| A15 | **Polaroid drop-in collage** | 1–3s per photo | Personal story, objects, credentials | Photos with a white border (thick at the bottom) and a soft shadow, dropping in rotated; earlier photos dim to ~40% when a new one lands; blue serif labels. |
| A16 | **Role carousel** | ~3s | "I'm a X, a Y, a Z" | Labels in a row; the active one blue and bold, the others grey and small; photos swap with it. |
| A17 | **Recreated social profile + Follow click** | ~2.5s | "Follow me", social proof | Rebuild the UI (don't screen-record someone else's account); cursor clicks Follow; shallow focus blur. |
| A18 | **DM bubble typing** | ~3.5s | A question people ask | Blue chat bubble typing out the question; blurred UI around it. |
| A19 | **Hand-drawn circle callout** | ~1.5s | Point at a person or detail in a photo | Ellipse stroke draws around the subject, slightly wobbly; white on dark or blue on light. |
| A20 | **Life timeline** | recurring | Ages, careers, journeys | Thin line, ticks, small-caps labels ("8 YEARS — FIRST WATCH"), a blue dot marker held at center while the track slides to the next tick. Use it on a white canvas AND as a semi-transparent overlay on the face (bottom third, above the platform UI) so the story's progress stays visible. |
| A21 | **Form-field label stamp** | ~1s | Facts about a photo | Small-caps label with a blue highlight ("OCCUPATION: MUSICIAN") next to a photo. |
| A22 | **Postage-stamp photo** | ~1.5s | Nostalgic / old photo | Perforated border mask around the photo. |
| A23 | **Blue radial quote card** | ~1.5s | Quote, turning point | Radial gradient from `#1F4FD8` to near-black, oversized white quotation marks scaling in, serif italic line between them. |
| A24 | **Rounded inset b-roll on black** | ~2.5s | Intimate line; a landscape shot in a vertical video | Footage in a rounded card (radius ~40px) at ~90% width on black; text above or below. Great for reusing a landscape crop without upscaling. |
| A25 | **Book / product flick montage** | ~2s | "Everything I've built" | Covers flick past with a slight perspective tilt and focus blur, quick cuts. |
| A26 | **Hold one hero word across a montage** | ~3s | A theme word | The caption layer stays still while 3–4 stock clips (0.5–0.8s each) cut underneath. |
| A27 | **Punch-in on the thesis word** | ~0.5s | The thesis line in a b-roll | Scale the footage 1.0→1.6 on the key word (scale a wrapper, not the clip's size property). |

## Code-based notes (HTML/GSAP, Remotion)

- Captions: one element per word with its start time; set the group visible over its window and tween each word in at `wordStart − 0.04s`.
- Line draws: SVG path with `strokeDasharray = length`, animate `strokeDashoffset` to 0; for a ball on the line, tween a progress value and position the ball with `getPointAtLength(progress × length)` on update.
- Use a seeded noise (fixed seed) for grain so renders are deterministic.
- Animate wrappers, never a video element's width or height.
