---
name: premium-minimal-edit
description: Edit a talking-head / podcast clip in the "premium minimal" educational animation style (paper textures, Inter + Playfair-italic cinematic text, one cobalt-blue accent, line/illustration/painting scenes) — and run the plan-first workflow that gets good edits out of Claude (transcript → silence cut → beat-by-beat edit-plan document the user picks from → build → revise → sound design). Also contains the method for training Claude on ANY new editing style from reference videos. Use when the user says "premium minimal", "minimal animation style", "Arthur Brooks style", "clean educational edit", "paper texture edit", "make an edit plan", "plan the edit first", "train you on a new style", or hands over a raw podcast/talking-head clip and wants a high-end educational short.
---

# Premium Minimal Edit

Learned from a 21-min tutorial (Ultimate Editors — "how I created this viral minimal talking-head edit using only Claude"). Source notes, full beat plan and timings: `references/tutorial-notes.md`.

The tutorial teaches three things. This skill encodes all three, translated from the tutorial's Remotion pipeline into **HyperFrames** (this workspace's pipeline):

1. **The style** — 10 design principles (section A)
2. **The edit workflow** — plan first, then build, then revise, then sound (section B)
3. **The training method** — how to teach Claude any new style (section C)

**Always invoke `/hyperframes` first** (framework rules) and read `/short-form-video` for the vertical scaffold, audio-sync protocol and verification gate. This skill replaces only the *look* (captions, background, transitions, scene archetypes) — the render contract, preview gates and every-frame review in `CLAUDE.md` still apply.

### Precedence / conflicts

- `CREATOR.md` + `PREFERENCES.md` still win. If `CREATOR.md` says the user pre-edits their own speaking video, **skip the silence cut** (B2) — never cut their audio.
- Choosing this style is an explicit aesthetic override of `MOTION_PHILOSOPHY.md` defaults: **no chrome-gradient text, no perspective grid, no whip-streak transitions, no karaoke Montserrat captions, no navy ambient stack.** Keep the discipline (one idea per beat, payoffs held ≥1s, callbacks, no dead frames, breathing outro).

---

## A. The style — 10 principles

> The core idea: **premium = restraint + texture + typographic hierarchy.** Three colors, two fonts, paper grain on everything, one blue line that the camera follows.

### Global tokens

```css
:root {
  --pm-paper:   #ECECF2;   /* off-white paper, slightly cool */
  --pm-ink:     #0B0B0D;   /* near-black text / dark scenes */
  --pm-dark:    #101012;   /* flat dark background (graph + line scenes) */
  --pm-blue:    #1E3BF0;   /* the ONE accent: cobalt / Klein-ish blue — lines, illustrations, blue scenes */
  --pm-white:   #FFFFFF;
  --pm-sans:    "Inter", system-ui, sans-serif;            /* main text */
  --pm-serif:   "Playfair Display", Georgia, serif;         /* special words — ITALIC */
}
```

- Fonts: load **Inter** (400/600/800) and **Playfair Display Italic** (600/800) from Google Fonts. Embed locally into `assets/fonts/` for deterministic renders.
- Palette is **3 colors + paper**: white/paper, black, blue. Nothing else except the natural colors of paintings/B-roll (which get desaturated toward the palette).
- If the user's `brand-tokens.css` has an accent, it may replace `--pm-blue` — ask once.

### Textures (on EVERY scene — the #1 "premium" tell)

| Texture | Use | HyperFrames recipe |
|---|---|---|
| Light paper grain | all backgrounds, B-roll, paintings | SVG `feTurbulence` (baseFrequency ~0.8, numOctaves 3) as a `mix-blend-mode: multiply` overlay at 8–15%. Fixed `seed` — deterministic. |
| Rough paper / canvas | text-centric + painting scenes | Same turbulence, lower frequency (~0.04) + `feDisplacementMap` blotches, 20–30%. |
| Rough painted / cloth | illustration figures, half-circles | Fill the figure with `--pm-blue`, mask with a turbulence-displaced edge so edges are ragged and "bleed" into the paper. |
| Halftone dots | paper backgrounds, edges | `radial-gradient` dot pattern at 4–6% fading toward the center. |
| Edge darken + blur | B-roll, paintings | inset vignette `box-shadow` + a blurred duplicate masked to the edges so the eye goes to the focal point. |

Textures should **move** with the camera (tutorial revision #3: "paint texture too heavy and didn't move with the animation"). Put the texture inside the camera-moved wrapper, not as a static screen overlay, and keep it at half strength over paintings.

### Cinematic text logic (principle 1 — used in EVERY scene)

1. Take the spoken line (≤5 words).
2. Pick the **1–2 most important words** → **big + bold**, centered. Either bold sans (Inter 800, tight tracking −0.03em) or bold *serif italic* (Playfair 800 italic). Alternate between the two across the video.
3. The remaining words go **small** (Inter 400–600) in the gaps **above or below** the big word — tucked against it, left- or right-aligned to its edge. Small text ≈ 25–35% the size of the big word.
4. No fixed pattern — but always: one hero word, small satellites, tight lockup.
5. On A-roll: no pill, no stroke box. A soft dark radial behind the lockup for legibility. White text on footage, ink text on paper.
6. Words appear in sync with speech: small words fade/rise in (0.25s, `power2.out`), the hero word lands with a soft scale 0.96→1 + blur 6px→0 (0.4s, `expo.out`).

Example lockups: `in the business` / ***of life.*** · `there's` / **linears** / `who just kind of` · `I'm a big fan of` / ***unhappiness***

### Scene archetypes (principles 2–10)

| # | Archetype | Background | Composition | Motion |
|---|---|---|---|---|
| 2 | **B-roll + text** | B-roll that literally shows the line | paper grain + darkened, slightly blurred edges; cinematic text on top describing it | slow push-in 1.00→1.06 |
| 3 | **Painting + text** | public-domain painting that shows the idea | paint + rough-paper texture over it; cinematic text placed around the main subject | **quick camera slide-in** (x 8%→0 or y, 0.6s `expo.out`) then slow drift |
| 4 | **Line + text** | black OR white paper | a thin `--pm-blue` line draws, is *interrupted* by text, continues to the next related text | camera **tracks the line head** (animate the world wrapper opposite to the line) |
| 5 | **Line + illustrations** | same | line draws horizontally with a **white dot** marking an object; or zig-zags with camera panning to reveal objects on both sides (= progression/phases); or leads straight up to the subject | stroke-dashoffset draw + camera follow |
| 6 | **Text-centric** | white OR blue, very rough paper | two quotation marks around center, cinematic text in the middle | quotes fade in, text writes on |
| 7 | **Center illustration** | white paper | a blue rough-textured illustration fills the lower half and bleeds into the middle (abstract ragged edges); cinematic text above. Variants: top-down brain, circular thin-line pattern, side-profile head with cloth texture | slow rise + scale 1.04→1 |
| 8 | **Side illustration + text** | paper | figure on one side, text on the other; or a half-circle (cloth texture) on one edge with clean text orbiting it — use when **two elements** must be shown at once | figure slides from its edge |
| 9 | **Object + text** | paper | a single element/photo with text around it as part of the story | rough reveal (masked wipe with ragged edge) |
| 10 | **Graph / statistic** | flat dark + texture | thin white glowing grid lines; a **blue ball** is the line's head | camera follows the ball; one step per spoken beat |

Plus **A-roll + captions** — the base layer. Face full-frame 9:16, light grade, cinematic text captions (principle 1).

Illustrations: generate as SVG/paths in-house (blue fill + turbulence mask) or source a silhouette PNG and recolor to `--pm-blue` with `filter`/`mix-blend-mode`. Paintings: Wikimedia Commons public domain. B-roll: Pexels. Never hotlink at render time — download to `assets/` first (determinism rule).

### Scene-choice logic (how the tutorial picks scenes)

- **Announcing a new idea / category → stay on A-roll.** The viewer reconnects with the speaker.
- **Describing / giving an example → show it** (painting, B-roll, illustration).
- **Numbers, growth, comparisons → graph scene.** Sync steps to repeated words ("up… up… up").
- **A person being described → character/side illustration callout.**
- **Personal story → object callout with real photos of the speaker.**
- **A list of options → center illustration with options cycling around it.**
- **The big thesis → line + text, the line running through the key words.**
- **Final line → text-centric scene with quotation marks.** Hold it.
- First 1–2s: A-roll so the viewer meets the face, then the first visual must be a strong hook.
- Rotate archetypes — never the same archetype twice in a row; balance face time vs cutaways (~40/60).

### Calibration from the real channel (4 reels studied, 2026-11-02)

The tutorial's paper-and-illustration scenes are the "animated" end of the style. The real @arthurcbrooks reels are **mostly A-roll + fast cutaways**, with the illustrated scenes used as accents. **Read `_reference/creator-library/arthurcbrooks/style-distilled.md` before planning.** It has the full scene-choice table and an **animation library (A01–A27)** to recommend from in the edit plan. Rules that override the defaults above:

- **Text is white on footage, blue on white.** Blue only lives on paper/white cards, flat blue cards, lines, markers and callouts, never as caption color over footage.
- **Font by meaning:** concrete nouns/facts → bold sans hero; emotion/abstract/names → Playfair italic hero. A sans-only version is valid too (reel DXcF).
- **Captions sit center / lower-middle (over the chest), never at the bottom edge.** Satellites are tiny (20–30% of the hero). Words build **one at a time in fixed slots**: no re-flow, no karaoke color swap, no stroke or pill.
- **Cut on the stressed word.** A cutaway every 1.5–3s; A-roll never more than ~6s without one. Mostly hard cuts; the variety comes from *where* you cut to.
- **Breath cards** (black or white, one serif word, 0.5–1s) after big claims.
- **Paintings are the #1 cutaway** for abstract nouns. Cinematic b-roll for concrete scenarios.
- **Endings:** blue-on-white summary card, a painting bookend, or A-roll with a serif "Thank you". No CTA graphics.
- Long-form/biographical clips: use the **life timeline** (A20) and **Polaroid collage** (A15) as the spine.
- One-off accents (yellow highlighter, orange word, deep red illustration): max once per video.

---

## B. The edit workflow (plan first — this is the important part)

> "Lazy inputs with AI get you lazy results." "If you let AI do the planning on its own, it's not creative enough." The plan is the human's job; the build is Claude's.

### B1. Intake
- Raw clip in `video-projects/<slug>/assets/`. Read `CREATOR.md`/`PREFERENCES.md`. Probe duration + resolution. If landscape podcast, plan a 9:16 crop on the speaker.

### B2. Transcript + silence cut (only if the clip is raw and CREATOR.md allows cutting)
```bash
npx hyperframes transcribe assets/raw.mp4 --model small.en --json
```
- Find gaps between words > ~0.25s. Keep **30 ms of padding** on each side of speech. Build an ffmpeg `select`/`aselect` (or concat list) to cut them, export `assets/<name>-edit.mp4`, then **re-transcribe the edited file** — all timing lives in edited-time (see `/short-form-video` audio-sync protocol).

### B3. Edit-plan document (deliver this BEFORE building anything)
Write `video-projects/<slug>/EDIT_PLAN.html` (or publish as an artifact) with:
- Header: clip, length, number of beats, a beat timeline bar.
- **One card per beat** (a beat = one spoken thought, ~2–5s): timestamp range; **script on the right** (with an embedded player seeked to the beat); on the left a free-text notes box + **3 recommended designs (A/B/C)** — each with archetype name, one-line description of exactly what animates, and *why it fits* (using the scene-choice logic above + any studied references in `_reference/creator-library/`). Cite the reference animation ID and source timestamp (e.g. "A04 paper graph — like DP7eSmPADaD @11.0s") and show a thumbnail from that reel's `frames/` folder when it exists locally.
- Mark Claude's suggested pick, but the **user chooses**. A "copy plan" button that exports the choices as text.

Then **stop and wait** for the user's filled-in plan. Do not build from your own picks unless they explicitly say "use your picks."

### B4. Build
1. Parse the plan → list of scenes.
2. **Asset list** — every painting, B-roll clip, photo, font needed. Fetch them (Wikimedia/Pexels/Google Fonts), save to `assets/`, note license/source in `assets/SOURCES.md`. Ask the user for anything you can't find.
3. A-roll captions across the full video first (cinematic text logic).
4. Then build each scene as its own sub-composition `compositions/beatNN-<archetype>.html`, local timing, padded to slot duration.
5. Lint → Studio preview gate → draft render → every-frame review (per `CLAUDE.md`).

Expect the first draft to be **60–70% there.**

### B5. Revisions
Ask the user for numbered, specific revisions (scene + timestamp + what's wrong). Typical ones from the tutorial — check these yourself before showing a draft:
- weak text lockup in a scene (missing the hero word on screen)
- rough cut between two animations → hold the previous scene until the next lands, then cut on motion
- texture too heavy / not moving with the camera
- bad cut at a specific second
- payoff not held long enough
- missing quotation marks on the final text scene

After revisions, ask: **"Ready for sound design, or more revisions?"**

### B6. Sound design (last)
- One cinematic, understated music bed (ducked under voice, ~−20 dB).
- **Clicks / soft ticks** for text appearing, **highlighter/scribble** for graph & line draws, **soft whooshes** for camera slides & transitions. Subtle — they punctuate, they don't carry.
- Source from `assets/sfx/` (see `MANIFEST.md`) and `assets/music/`.
- If reference videos for this style are in `_reference/creator-library/`, match their SFX density.

Rough time budget from the tutorial: cuts + plan doc 15 min · human planning 15 min · build ~60 min · revisions 10 min · sound 15 min.

---

## C. Training Claude on ANY new style (the method)

Use when the user says "learn this style", "train you on @creator", "make a skill for this look".

1. **Collect ~20 of the best videos** in the style (one creator). Run `/study-creator <url>` on each — word-level transcript + frame-by-frame breakdown.
2. For every scene ask the editor's questions: **why this scene? why this design? why these colors? why these effects? why this animation?**
3. **Inspiration board** (~100+ screenshots of the best scenes). Ask the user for theirs (Figma link / folder) — it's the most important input. If none, build one: a contact sheet per scene type from the extracted frames.
4. **Categorize** the board into principles/archetypes; for each: fonts, colors, sizes, layout pattern, textures.
5. Study three things from the videos:
   - **Placement** — where animations sit relative to the script (what kind of line triggers what kind of scene)
   - **Composition** — what elements make up each design
   - **Animation logic** — durations, eases, camera moves, how it *feels*
6. **Build a reference library**: every distinct animation saved as `_reference/creator-library/<handle>/animations/<id>/` with a keyframe contact sheet + a `notes.md` (archetype, duration, trigger phrase). The tutorial's version had 225 animations from 20 videos — this library is what makes later design recommendations good.
7. Package it as a skill (`.claude/skills/<style>/SKILL.md`) following this file's layout: tokens → textures → text logic → archetypes → scene-choice logic → workflow.

> The reference videos teach the **logic**; the board teaches the **design**. You need both.

---

## Pre-flight checklist (premium minimal)

- [ ] Only paper/white, black, one blue (+ natural tones of paintings/B-roll, toned down)
- [ ] Inter + Playfair italic only; every lockup has one hero word
- [ ] Paper texture on every scene, moving with the camera
- [ ] Edges darkened/blurred on B-roll and paintings
- [ ] Camera motion in every cutaway (slide-in, track the line, follow the ball, slow push)
- [ ] Face shown when a new idea is announced; visuals when it's described
- [ ] No archetype twice in a row
- [ ] Final scene: text-centric with quotation marks, held ≥2s
- [ ] Sound added last, subtle
- [ ] Edit plan was approved by the user before building
