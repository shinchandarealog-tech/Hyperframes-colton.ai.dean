# de1ub-sj8m8 — @edita.visuals ("Welcome to the attention economy")

**Source:** https://www.instagram.com/reel/De1uB_sJ8M8/ (uploaded file, not downloaded)
**Duration:** 24.52s
**Aspect:** 9:16
**Resolution:** 720x1280 showcase; inner edit card ≈ 360x642
**Studied:** 2026-10-29
**Engagement (at time of study):** n/a (local upload)
**Sample rate:** every frame at 2fps (49 frames), storyboard at 1fps, a 10fps strip across 2.2–3.2s, and a spectrogram.

## Wrapper
Same before/after showcase as every @edita.visuals post: a "Storyboard" pencil card behind the final card, the "Opus 5.5" pill and the "Follow & comment CLAUDE" CTA. See `../det-wsmtgue/analysis.md`.

## Hook (0–2s)
- 0.0: A **purple gradient wipe** sweeps off a white frame (a diagonal light streak), revealing the speaker (Lara Acosta, a YouTuber-style setup with a cobalt-blue backlight).
- 0.5: Caption "And I know this" in clean white **geometric sans (Poppins-like)**, with a thin swoosh underline drawing in under it.
- 1.0–2.0: "because I used to" → "to spend all of **my time**". "my time" is in purple. A **progress-bar slider** (line + white dot knob) scrubs left to right under the text: a visual pun on "time".

## Pacing
- Total scenes: ~12
- Average scene length: ~2.0s
- Shortest / longest: 0.3s (flash frames) / ~4s (face-cam)
- Distribution: medium. Alternates face-cam (with captions) and a full-screen graphic every 2–4s.

## Captions
- Style: phrase chunks (2–4 words) that replace each other. One keyword per phrase is coloured **purple (#8B5CF6)** and slightly bigger/bolder.
- Font: geometric sans, medium weight, white. Purple accent keyword.
- Active-word treatment: the keyword fades and slides in. Decorative micro-graphics hang on the caption itself: a swoosh underline, a slider knob, a "skip ▶|" icon after "Skip", bullet checkmarks for "Mistake ×3".
- Position: centre / lower-centre (about 45–55%).
- Size: medium.

## Scene types
1. Face-cam fullscreen, cobalt-blue grade, with captions + micro-icons
2. **Flash-flicker transition** (2.3–2.9s at 10fps): purple flash → white → purple → white, then the face video **shrinks into a rounded card** on white
3. **YouTube-channel mock**: avatar + "Lara Acosta · 32.8k Subscribers" header over the video card, captioned "Watching **Videos**"
4. White canvas, "Looking for an **answer**" + a gradient progress bar under it
5. The face-cam card slides in from the right on white, then re-expands to fullscreen
6. Face-cam with a "help you **Skip ▶|** through" icon caption
7. A list build: "all of the **Mistakes**" with three ◉ "Mistake" bullets stacking
8. **Quiz/worksheet mock**: a lavender card "1. Question" with dotted answer lines, plus "and get right to the answers that you're looking for" on a white canvas with a big lavender arc
9. A purple flash to a dark grid-background scene: a white **"Blueprint" card** with checklist items (Content, Distribution, Sales) popping in one by one, and blurred purple orbs in the corners
10. Face-cam with a **handwritten script overlay** (Content / Distribution / Sales on a blue banner card) sliding up from the bottom
11. Face-cam with a white circle icon badge (a box/product icon) on a dashed curved path — "products aren't hard, **distribution** is"
12. Face-cam + a giant "**The Attention Economy**" title in purple-white, with a translucent blue band at the bottom scrolling the oversized text "...ention Econ..." sideways (a ticker/marquee)

## Transitions
- Flavors: **colour-flash flicker** (purple/white alternating frames, ~0.1s each), **video-to-card shrink** (fullscreen → rounded card on white), **slide-in card**, **light-streak wipe**, hard cuts.
- Rotation: flicker → shrink → hard cut → slide → flash. Graphic scenes always enter via a flash or shrink, never a plain cut.
- Signature: **the face-cam shrinking into a UI card** (YouTube player, then a floating card), so the talking head becomes an object inside a mock interface.

## Face treatment
- Fullscreen and card-in-canvas modes. Card mode is ~70% width with a rounded corner radius and a soft shadow on white.
- Grade: deep cobalt-blue backlight, crushed blacks, warm skin.
- A subtle blur pulse on punch-ins (6.5s is a heavy defocus into "This").

## Audio reactivity / SFX
- ~34 broadband transients in 24.5s. The spectrogram shows a **rapid tick cluster at 1.0–1.6s** (a run of short clicks under the slider scrub, like a "scrub/tick" SFX), a tonal **chime/sparkle** at ~17.3–17.6s (a 13kHz tone line as the handwritten overlay lands) and dense swooshes at every graphic entrance.
- Low hits at 0.2s (opening wipe), 1.0/1.9s and 7.2s (Skip).
- Light music bed is barely audible. Speech + SFX dominate.

## Palette
- #7C3AED / #8B5CF6 purple — dominant accent (keywords, flashes, Blueprint title)
- #1E2BFF-ish cobalt blue — the footage backlight
- #FFFFFF / #F8F7FC white & lavender-white canvases
- #E9E3FB lavender cards
- #0B0B0F near-black grid background

## Signature move
**The talking head turns into an object inside a mocked UI** (YouTube channel card, floating card), with purple flash-flicker transitions in and out.

## What to steal
- **Flash-flicker transition**: 3–4 alternating frames of accent colour / white at 0.1s each, then land on the new scene. Easy in GSAP with a full-frame div `opacity` timeline (`steps`). Pair with `sfx/transitions/glitch.mp3` (trimmed) or `whoosh`.
- **Face → card shrink**: animate a wrapper div (never the `<video>` itself) from full-bleed to a 70% rounded card with `border-radius` + `box-shadow`, then add a header (avatar + name + subscriber count) above it.
- **Caption micro-icons**: attach a tiny SVG to the keyword that acts out the word (a slider for "time", ▶| for "skip", a check bullet for list items).
- **Checklist card build** (Blueprint: Content → Distribution → Sales), one `pop.mp3` per item. Maps to `short-form-video` list archetypes.
- **Oversized marquee text band** under the final title for the outro.

## What's creator-specific
- The speaker's channel name/subscriber count; the wrapper chrome.

## Transcript
See `transcript.json`. Whisper heard "in hot distribution" for "and distribution". The caption on screen reads "in hot distribution" too, so the editor kept the mistranscription.
