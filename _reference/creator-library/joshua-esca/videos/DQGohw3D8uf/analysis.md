# DQGohw3D8uf — @joshua-esca (text-animation reference)

**Source:** Instagram Reel, uploaded by the user as a local file (`Video_by_joshua.esca_DQGohw3D8uf_1.mp4`)
**Duration:** 8.89s · 4:3 crop of a vertical edit · 960x720 @ 30fps
**Studied:** 2026-10-29, scoped to **text animation**, which is what the user asked to apply.
**Sample rate:** 4fps across the whole clip, plus every frame (30fps) of 8 text moments.

## Text system (three looks, mixed)
1. **Giant word BEHIND the speaker:** huge white heavy grotesk (Helvetica/Inter Black, tight tracking), placed at head height and occluded by his head and body (person matte). Enters with either a horizontal sweep plus heavy horizontal motion blur ("JUST"), or a scale-down from blur ("NO", "Well"). Lands in ~5–6 frames, then holds.
2. **Italic serif accent word in FRONT:** high-contrast italic serif (Instrument Serif–like) under the giant word ("fees", "courses", "straight", "asking"). Rises in from a vertical smear blur in ~6 frames. A new serif word hard-swaps the previous one in place (fees → courses).
3. **Small words:** bold sans lowercase words popped in one by one with a blur-in, spread across a row ("let me *show* you", with one word in italic serif). There's also a low subtitle line where each word sharpens in from blur ("I'm going to break it down for you").

## Extras
- **3D word spiral:** words on a helix orbiting the speaker ("how do you do that text effect"). Words on the far side are mirrored and pass behind him, and words blur at the edges of the orbit.
- **Red circle glitch transition:** a red disc with a cyan/red chromatic rim sweeps across, blows out to white, cut.

## Applied in `video-projects/10-80-style-edit` (user-approved scope)
- Replaces all captions. The user chose: all three looks, plus the spiral and the red circle glitch; serif words keep a soft orange glow (no pure-white-only).
- Implementation: a person matte (MediaPipe selfie segmenter) → `assets/fg-cutout.webm` (VP9 with alpha) layered above `#behind` inside the face transform stack, so the giant words sit behind her and move with every punch-in.
- Fonts: Inter 900 (giant), Instrument Serif Italic (bundled, OFL), Inter 700/600 (small/subtitle).

## Don't copy
His handle, the "how do you do that text effect" content, and the 4:3 framing.
