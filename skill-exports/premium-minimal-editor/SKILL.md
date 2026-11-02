---
name: premium-minimal-editor
description: Plan and design short-form talking-head / podcast edits in the "premium minimal" educational style (the Arthur Brooks look): one oversized hero word per caption (bold sans for facts, serif italic for feelings), white text on footage and blue on white, classical paintings, paper textures, thin blue line graphs, timelines and clean cards, cut on the stressed word. Runs the plan-first workflow (transcript → silence cut → beat-by-beat edit plan the user picks from → build → revisions → sound) and can teach Claude any new editing style from reference videos. Use when the user says "premium minimal", "minimal animation style", "Arthur Brooks style", "clean educational edit", "paper texture edit", "plan my edit", "edit plan", "make this podcast clip premium", "learn this editing style", or hands over a talking-head / podcast clip and wants a high-end educational short. Works with any editor (CapCut, Premiere, After Effects, DaVinci, Remotion, HTML/GSAP).
---

# Premium Minimal Editor

A self-contained skill for the **premium minimal** short-form style, learned from a 21-minute tutorial ("how I created a viral minimal talking-head edit using only Claude") and calibrated against 4 real @arthurcbrooks reels studied frame by frame.

It does three jobs:

1. **Style:** how the look is built (section A, plus `references/style-fingerprint.md`).
2. **Workflow:** plan first, then build, revise and add sound (section B, plus `references/edit-plan-template.md`).
3. **Training:** how to teach Claude any new style (section C).

Load on demand:

| File | Read when |
|---|---|
| `references/style-fingerprint.md` | Before planning any edit in this style (full rules from the real channel) |
| `references/animation-library.md` | When recommending designs per beat (27 reusable animations, with build notes) |
| `references/edit-plan-template.md` | When producing the edit-plan document |
| `references/tutorial-notes.md` | For the tutorial's exact prompts, worked example and time budget |

**Tool-agnostic:** describe every design in plain editor terms (layers, keyframes, eases, durations), so it can be built in CapCut, Premiere, After Effects, DaVinci, Remotion or HTML/GSAP. If the user names a tool, translate the notes into that tool's terms. If you can run code and render video yourself, build it; otherwise hand over a precise build sheet.

---

## A. The style

> **Premium = restraint + texture + typographic hierarchy.** Three colors, two fonts, one hero word per phrase, paper grain on white, cut on the stressed word.

### Tokens

| Role | Value |
|---|---|
| Near-black (pause cards, dark scenes) | `#0B0B0D` |
| White canvas / paper | `#FAFAFA` (paper tint `#F2F2F4`) |
| **Royal blue accent** (the only accent) | `#1F4FD8` (flat full-screen blue cards: `#0A47FF`) |
| Ink (text on white) | `#0B0B0D` |
| Captions on footage | `#FFFFFF` (small satellite words at ~80% opacity) |
| Sans (facts, numbers, concrete nouns) | **Inter** 500 for small words, 800 for hero words (tracking −0.03em) |
| Serif (feelings, abstractions, names) | **Playfair Display Italic** 700 |

One-off accents (yellow highlighter, an orange word, deep red) appear **once per video** at most.

### The five rules that make it look premium

1. **One hero word per phrase.** The phrase (≤5–8 words) is laid out as small satellite words (≈25% of hero size) tucked tight above, below or beside ONE oversized hero word (2–3× bigger).
2. **Font by meaning.** Concrete nouns, facts and numbers get the bold sans hero (**£15**, **eight**, **Rolex**). Feelings, abstractions and names get the serif italic hero (*infatuated*, *journey*, *favourite*). A sans-only version is also valid.
3. **White on footage, blue on white.** Captions over video are white with only a soft shadow: no stroke, pill, box or karaoke color swap. Blue only appears on white or paper cards, flat blue cards, lines, markers, name tags and circle callouts.
4. **Words build in fixed slots.** Lay out the whole phrase first, then fade each word in at its transcript time where it will sit. No re-flowing and no bouncing.
5. **Cut on the stressed word.** Cut away every 1.5–3s and never hold the face more than ~6s without a cutaway. Cuts are mostly hard (or a 0.3s scale 1.06→1 with a blur settle). The variety comes from *where* you cut to.

### Caption placement

- Over the chest / center-lower-middle (≈ y 1050–1350 on a 1080×1920 frame). **Never in the bottom ~350px** (platform UI).
- Top satellite aligned to the hero's left edge, bottom satellite to its right edge.
- Motion: satellites fade in with a 14px rise over 0.25s (`power2.out`); the hero scales 0.94→1 with blur 6px→0 over 0.4s (`expo.out`). Footage gets a slow 1.00→1.05 push-in through each stretch.

### Textures

- **Paper grain** on every white canvas (fine fractal noise, multiplied at ~10–15%).
- **Film grain** over everything at ~6–8%.
- **Darkened, slightly blurred edges** on b-roll and paintings so the eye goes to the subject.
- Textures move with the camera. A static overlay on a moving shot looks fake.

### Scene archetypes (what you cut to)

| Archetype | Use it for |
|---|---|
| Talking head + captions | Announcing a new idea; reconnecting with the speaker |
| **Painting + giant hero word** | Abstract nouns and big ideas (Arthur's #1 cutaway) |
| Cinematic b-roll + text | Concrete scenarios being described |
| **Breath card** (black or white, ONE serif word, 0.5–1.5s) | A pause after a big claim |
| **Paper graph** (thin blue line climbing out of frame, blue ball at its head) | Numbers, growth, "progress" |
| **Life timeline** (thin line, ticks, small-caps labels, blue marker) | Personal journeys, ages, careers |
| **Polaroid collage on white** | Personal story, first purchases, credentials |
| **Name / object callout** (thin curved line plus a blue name box) | A named person or a specific object |
| Flat blue claim card → research paper with yellow highlighter | "Studies show…" evidence beats |
| Rounded inset b-roll on black | Intimate or introspective lines |
| Blue quote card with big quotation marks | Turning points, quotes |
| Blue-on-white summary card | Endings |

Full details, durations and build notes are in `references/animation-library.md` (A01–A27).

### Scene-choice logic (script → scene)

- **New idea announced → stay on the face.** **Idea described → show it.**
- Abstract noun → painting. Concrete scenario → b-roll. Number → graph. Person → callout. Personal history → timeline or polaroids. List of 3 → one cutaway per item. Big claim → breath card next. "Studies show" → evidence beat.
- First second: a visual lands on the first loaded word (either a hard cut to art or b-roll, or a hero caption on the face). Never a title card or logo.
- Never use the same archetype twice in a row. Aim for roughly 40% face, 60% cutaways.
- **Ending:** a blue-on-white summary card, a painting bookend, or the face with a serif "Thank you". No CTA graphics. Hold the last frame ≥1s.

---

## B. The workflow (plan first)

> "Lazy inputs get lazy results." "If you let AI do the planning on its own, it's not creative enough." **The human plans; Claude builds.**

### B1. Intake
Get the clip and confirm: the speaker's name and handle (only if they should appear), the platforms (default 9:16 1080×1920 30fps), whether the clip is raw or already edited, and whether there are any brand colors that should replace the blue.

### B2. Transcript + silence cut
- Make a **word-level transcript** with millisecond timestamps (Whisper or any word-timestamp ASR).
- **Only if the clip is raw and the user allows it:** remove pauses over ~0.3s, keeping **30ms of padding** around speech. Find pauses from the audio itself (e.g. ffmpeg `silencedetect`, about −38dB, 0.18s), not just transcript gaps, and put tiny audio fades on each cut.
- Re-transcribe the edited version. **All timing lives in edited time.**
- Note Whisper mistakes (brand names, numbers) and fix them in the captions.
- Check the source for burned-in text or logos that a 9:16 crop would slice in half. Plan a full-screen scene over them.

### B3. The edit-plan document (deliver BEFORE building)
Follow `references/edit-plan-template.md`:
- One **beat** per spoken thought (~2–5s): timestamp, exact script line, thumbnail if possible.
- **3 design options (A/B/C)** per beat. Each has the archetype, exactly what animates, *why it fits* (the scene-choice logic) and a reference animation ID (A01–A27).
- Mark your suggestion, but **the user chooses**.
- **Make choosing easy for the user.** If they're on a phone or chat app, ask beat by beat as multiple choice (a few beats per question batch) instead of sending an HTML file they can't interact with.
- **Stop and wait** for their picks. Don't build from your own picks unless they say "use your picks".

### B4. Build
1. Write the approved plan down (a beat table).
2. **Asset list:** every clip, photo, painting and font. Prefer the client's own footage first. Reusing their footage creatively (e.g. a slowed close-up of an object from another moment) often beats stock. Otherwise use free-for-commercial sources (Mixkit / Pexels video; Wikimedia Commons public-domain or CC images; Google Fonts). **Log every source and license**; CC BY / BY-SA images need a credit line in the post caption. Never use copyrighted film clips for client work.
3. Lay out every scene's final ("hero") frame first, then add entrances.
4. Captions across all face and b-roll stretches, then each cutaway scene.
5. Reframe 16:9 sources to 9:16 per camera angle (keep the face in the upper ~45%). Never show a slowed-down shot with visible lips moving.

### B5. Self-review, then revisions
- Before showing ANY render, look at every frame (or a dense sample on long videos). Check for: empty or near-empty frames longer than ~0.5s, captions off their word, text overflow, cropped faces, burned-in source text showing, callouts not lined up with their target, half-transitions.
- Expect the first draft to be **60–70% there**. Ask for **numbered revisions with timestamps**.
- Common revisions to pre-empt: a weak lockup (hero word missing), a rough cut between two animations (hold the outgoing scene until the incoming one lands), a texture too heavy or static, a payoff not held long enough (hold ≥1s), and missing quotation marks on a quote ending.
- Then ask: **"Ready for sound design, or more revisions?"**

### B6. Sound design (last)
- One understated cinematic music bed, ducked under the voice (about −18 to −22dB below dialogue).
- Soft **clicks/ticks** for words or cards landing, **pencil or highlighter** sounds for line draws, **soft whooshes** for camera slides and scene changes, a light **paper or photo drop** for polaroids. Subtle: they punctuate the edit, they don't carry it.
- Final loudness about −14 LUFS integrated for social platforms; dialogue clean.

Time budget from the tutorial: cuts + plan 15 min · human planning 15 min · build ~60 min · revisions 10 min · sound 15 min.

---

## C. Teaching Claude any new editing style

1. Collect **~20 of the best videos** in the style (one creator).
2. For each one: a word-level transcript plus a **frame-by-frame breakdown** (at least 2 fps; read every frame, don't just list files).
3. For every scene ask: **why this scene, why this design, why these colors, why these effects, why this animation?**
4. Build an **inspiration board** of ~100+ screenshots of the best scenes and sort them into archetypes. For each archetype note the fonts, colors, sizes, layout and textures. Ask the user for their board (Figma or a folder) if they have one; it's the most valuable input.
5. Study three things: **placement** (which kind of line triggers which scene), **composition** (what each design is made of) and **animation logic** (durations, eases, camera moves, feel).
6. Build a **reference library**: every distinct animation gets an ID, source timestamp, duration, trigger phrase and build notes (see `references/animation-library.md` for the format).
7. Write it up as a skill in this file's order: tokens → caption logic → archetypes → scene-choice logic → workflow → checklist.

> The reference videos teach the **logic**; the board teaches the **design**. You need both. Watch for differences between what a tutorial *says* and what the real channel *does*; trust the real videos.

---

## Pre-flight checklist

- [ ] Only black, white/paper and one blue (natural photo and painting tones are fine, toned down)
- [ ] Inter + Playfair Display Italic only; every phrase has exactly one hero word; font matches meaning
- [ ] White on footage, blue only on white or flat cards; no strokes, pills or karaoke colors
- [ ] Captions over the chest, never in the bottom 350px; words build in fixed slots
- [ ] Cut on stressed words; a cutaway every 1.5–3s; no archetype twice in a row
- [ ] Face when a new idea is announced; a visual when it's described
- [ ] No near-empty frames over ~0.5s; payoffs held ≥1s; ending held ≥1s
- [ ] Burned-in source text never visible after reframing
- [ ] Every asset licensed for commercial use and logged; credit lines handed to the user
- [ ] The user approved the edit plan before the build; sound added last
