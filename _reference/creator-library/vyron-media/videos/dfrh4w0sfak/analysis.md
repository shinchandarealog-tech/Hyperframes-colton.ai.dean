# dfrh4w0sfak — @vyron-media

**Source:** https://www.instagram.com/reel/DfRh4w0SfAk/
**Duration:** 29.85s
**Aspect:** 9:16
**Resolution:** 1076x1914 @ 25fps
**Studied:** 2026-11-05
**Engagement (at time of study):** 713 likes · 543 comments (comment-bait CTA; views not exposed)
**Sample rate:** extracted 60 frames at 2fps; reviewed at 1fps (every 2nd frame, 30 frames) via labeled contact sheets.

> Format note: **#ad for "Montage AI"** — white canvas, the edited talking-head plays in a large rounded card (right), a small pencil-sketch "Storyboard" card (left) previews each beat, pill tag "Montage AI/$1.6" above, persistent CTA below: Comment "**Montage AI**" for the tool link. The analysis describes the edit inside the main card.

## Hook (0–2s)
- 0.0s: talking-head (bald, beard, cream jacket, warm brick-wall set). Small white words "Discipline … is the … long" float in; an empty dark **progress-bar pill with a 🔥 emoji** sits mid-frame.
- 1.0s: "**Secret**" slams in huge — heavy rounded sans, **yellow→orange gradient fill with glow**, small "Discipline / is the" words around it; the progress bar fills orange; a white pill "long" drops under it.
- First words: "Discipline is the secret for long-term success." — a statement hook delivered with a big single-word slam.

## Pacing
- Total scenes: ~14 visual beats in 30s
- Average scene length: ~2.1s
- Shortest / longest: ~1s / ~3s (pill-stacking "Face Challenge / Get Tired / Lose the initial spark" 9–11s)
- Distribution feel: short-chopped, sustained high energy.
- Every new sentence = new graphic gesture; no beat lasts more than ~3s without a change.

## Captions
- Style: **phrase chunks with one HERO word**; supporting words tiny and scattered around the hero word (above-left, right, below).
- Font feel: hero word = heavy rounded geometric sans, **gold gradient (#ffd21f → #ff9e0b) with outer glow**; support words = small white medium sans.
- Active-word treatment: hero word scales/slams in with blur → sharp, glow bloom; sometimes the word is masked behind the speaker (depth layering — "Gym", "Test" sit behind his shoulder).
- Position: center to lower-center, sometimes upper-right negative space.
- Size: hero word large (~8–12% frame height), support ~2.5%.

## Scene types
1. 0–1s talking-head + emoji progress bar (🔥) filling.
2. 1–2s kinetic slam "Secret" gold gradient.
3. 2–3s cutaway b-roll (him at desk with laptop) → "My **Agency**" huge white with **yellow light-streak swoosh** across.
4. 4–5s full graphic: black + **glowing yellow bar** rising, "ON **Motivation**", then "TO GET ME THROUGH THE **EARLY STAGES**" condensed caps.
5. 6–7s talking-head + **photo pop-ups** (stills of him waking up / at gym) springing in as framed cards.
6. 8s "But then **Something** would happen" over glass cards.
7. 9–11s **white UI pills stacking** one per phrase: "Face Challenge" → "Get Tired" → "Lose the initial Spark".
8. 12s "And **suddenly**" gold.
9. 13s b-roll (head in hand at laptop) + "Didn't **WORK!** Feel like" big white with yellow glow halo.
10. 14s b-roll hoodie guy with teal/neon light + yellow swoosh line, "It's like starting a…"
11. 16–18s talking-head + gold hero words "Motivation", "Gym" (behind shoulder), "All in".
12. 19–20s **dark calendar strip** Mon–Sun with days 5/6/7 glowing red → "Novelty wears off".
13. 21–22s orange progress bar draining with 🔥 → "Starts to fade".
14. 24–26s **glass comparison card**: 💵 "Just like IN FITNESS" vs 🔴 "business SUCCESS", gold underline → "doesn't come from **motivation alone**".
15. 27–29s talking-head, "Up **Everyday**", "Even when you are **Feeling** it" gold.

## Transitions
- Flavors observed: hard cuts on the word, blur-in slams, light-streak swoosh, glass cards sliding/stacking, b-roll cutaways.
- Rotation cadence: rotates freely; motion lives *inside* the beat rather than in transitions.
- Signature: **gold light-streak swoosh** curving across frame behind the hero word.

## Face treatment
- Mode mix: fullscreen talking-head ~70%, b-roll/graphic cutaways ~30%.
- Grading: **warm cinematic** — amber/teal, crushed blacks, bottom vignette fade to black.
- Camera motion: occasional punch-in (≈1.15×) on hero words.
- Framing: centered medium shot, headroom kept for upper text.

## Audio reactivity
- Text pulses on beat: no (hero-word slams on stressed syllables)
- Background reactivity: no
- Synced to a specific syllable: yes — every hero word lands exactly on the spoken word.

## Palette
- `#ffd21f` gold yellow (dominant accent, hero words)
- `#ff9e0b` orange (gradient end, progress bar)
- `#ffffff` white support text / pills
- `#0b0b0b` black (graphic takeovers, vignette)
- `#e0393e` red (calendar warning, sparing)

## Signature move
**One gold-gradient glowing hero word per sentence**, slammed in on the stressed syllable with tiny white support words orbiting it.

## What to steal (actionable for Hyperframes builds)
- **Hero-word captions**: support words small white, hero word heavy rounded sans with `linear-gradient(#ffd21f,#ff9e0b)` + `background-clip:text` + `drop-shadow` glow; GSAP `fromTo` scale 1.4→1, blur 12px→0, 0.25s `back.out`.
- **Emoji progress bar** (🔥 pill filling/draining) for any "rise/fade" line — simple div `scaleX` tween.
- **Stacking UI pills** one per listed item (rule of threes).
- **Calendar strip** with highlighted days for time-based claims.
- **Depth-masked word** behind the speaker (needs a matte — skip unless a segmentation mask exists).
- **Warm grade + bottom vignette** on the face cam.

## What's creator-specific (don't copy literally)
- The Montage AI ad framing (storyboard card, price tag pill, "Comment Montage AI" CTA).
- The pencil-sketch storyboard previews.

## Transcript
See `transcript.json` in this folder.
