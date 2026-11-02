# Universal short-form principles (analysis lens + fallback)

Use these two ways:
1. **As a lens while studying a reference:** they explain *why* a reference works, so your style spec captures intent, not just surface.
2. **As the fallback** when there's no reference (pair them with `niche-presets.md`).

**A reference always overrides these.** If the reference uses karaoke captions, boxes, constant zooms or no captions at all, the spec follows the reference, not this file.

## 1. The core idea

> **Premium = restraint + hierarchy + intent.** Few colors, two fonts, one idea per beat, one hero word per phrase, and every cut lands on purpose.

Cheap-looking edits do the opposite: every word captioned the same size, five colors, random zooms, stock clips that don't match the words, effects with no reason.

## 2. Brand slots (fill these per client or niche first)

| Slot | Rule | Fill from |
|---|---|---|
| **Base dark** | Near-black, never pure flat #000 with banding | Brand or preset |
| **Base light** | Off-white or paper, never pure #FFF glare | Brand or preset |
| **One accent** | ONE saturated color. It carries all emphasis: lines, markers, highlight boxes, key words on light backgrounds | Brand color, or the niche preset |
| **Rare accent** (optional) | Used at most **once per video** for a special moment | Preset |
| **Sans font** | Clean grotesk (Inter, Helvetica, SF, Manrope…) for facts and small words | Brand or preset |
| **Display / emotion font** | ONE contrasting face: a serif italic (classic, emotional), a condensed bold (energetic), or a mono (technical) | Niche preset |
| **Texture** | ONE texture family: paper grain, film grain, clean digital, or halftone | Niche preset |
| **Cutaway language** | Where visuals come from: paintings, cinematic b-roll, product shots, UI and screen recordings, diagrams, archival photos | Niche preset |

If the client has a brand, use it. If not, pick a preset from `niche-presets.md` and confirm it with the user in one line.

## 3. Caption principles

1. **One hero word per phrase.** A phrase (≤5–8 words) is laid out as small satellite words (≈20–30% size) tucked tight around ONE oversized hero word (2–3× bigger). Viewers read the hero word first; it carries the meaning even with the sound off.
2. **Pick the hero by meaning:** the word that would survive if you could only keep one (the number, the noun, the turn of the sentence). Never filler.
3. **Font by meaning:** facts, numbers and concrete nouns go in the bold sans hero. Feelings, abstractions and names go in the display/emotion font. Stay consistent across the video.
4. **Fixed slots, no re-flow.** Lay out the whole phrase, then reveal each word at its spoken timestamp where it will sit. Words never jump around as new ones arrive.
5. **Legibility without decoration.** Light text on footage, dark or accent text on light cards. Use a soft shadow or local darkening for contrast, not strokes, pills or boxes (unless the brand specifically uses a box style).
6. **Placement:** center to lower-middle (over the chest on a talking head). **Never in the bottom ~18% or the far right edge** (platform UI). Keep the face clear.
7. **Accent color is rare.** On footage, captions stay neutral. The accent belongs to graphics and light cards, so when it appears it means something.
8. **Motion:** small words fade and rise ~14px over 0.25s; the hero word scales 0.94→1 with a blur-in over ~0.4s, ease-out. No bounces or wiggles unless the niche preset says "playful".

## 4. Cutting principles

1. **Cut on the stressed word.** A cut lands on the word that carries the meaning, not on a pause.
2. **Cadence:** a visual change every **1.5–3s**; never hold the same shot more than ~6s. Faster for hype niches, slower for calm or luxury niches (see presets).
3. **Variety comes from the destination, not the effect.** Mostly clean cuts (or a 0.3s scale-and-blur settle). Rotate *what* you cut to: face → visual → card → graph. Never use the same scene type twice in a row.
4. **Motion in every shot:** slow push-ins (1.00→1.05) on footage, drawing lines, drifting cards. No frame should look frozen for more than ~0.5s.
5. **Reframing 16:9 to 9:16:** set a crop per camera angle, keep the face in the upper ~45%, and push-in by scaling a wrapper or adjustment layer.

## 5. What to show for each line (scene-choice logic)

The most important principle: **announce = face, describe = show.**

| Script moment | Show |
|---|---|
| A new idea / section is announced | The speaker's face (reconnect) |
| Something is described or given as an example | A visual that **literally** shows it (b-roll, photo, product, UI) |
| An abstract idea (freedom, discipline, risk) | A **visual metaphor** from the niche's cutaway language |
| A number, price, growth, comparison | A **graph or big-number** card; animate the number when it's spoken |
| A list of 2–4 items | One cutaway per item, or a single list graphic that builds |
| A person or a product is named | A **callout** (line + label/name tag) on a photo or the footage |
| A personal story or timeline | **Timeline** and/or **photo collage** that carries across beats |
| "Studies show" / proof / a screenshot | An **evidence beat**: claim card, then the source with a highlight sweep |
| A big claim lands | A **breath card** (one word, plain background, 0.5–1.5s) right after |
| A question the audience asks | A **chat / comment / DM** recreation |
| A quote or turning point | A **quote card** |
| The ending | A **summary card** in the accent, a callback to the hook visual, or the face with a final hero word. Hold ≥1s. No cluttered CTA. |

Aim for roughly 40% face and 60% cutaways on talking-head content. On faceless content, swap "face" for a recurring anchor shot or host graphic.

## 6. Hook and ending

- **First second:** a visual or hero word lands on the first loaded word. Either open on a striking visual carrying the thesis word, or show the face with a big hero caption and cut away within 1s. Never a logo, title card or "hey guys".
- **First 3 seconds:** the viewer should know the topic and why to stay (a tension, a number, a contrarian line).
- **Ending:** close the loop with a callback to the hook, a clean summary card, or the strongest line held on screen. Let it breathe ≥1s.

## 7. Sound principles

- The voice is king: clean, consistent, and never ducked by effects.
- One music bed matching the niche's energy, sitting about 18–22dB under the dialogue.
- SFX **punctuate**, they don't carry: soft ticks for words or cards landing, pencil or swipe sounds for line draws, soft whooshes for scene changes, a drop or paper sound for photos, a riser into a big reveal. If you notice an effect, it's too loud.
- Final loudness about −14 LUFS integrated for social platforms.
