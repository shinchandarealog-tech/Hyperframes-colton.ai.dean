---
name: edit-from-reference
description: Study any reference video a client sends (any niche — real estate, fitness, tech, podcasts, luxury, food, faceless, talking-head), break down EVERYTHING about how it is edited (structure, hook, pacing, cut points, captions, typography, color grade, graphics, transitions, camera moves, b-roll choices, sound design, and which script moments trigger which visuals), turn that into a reusable style spec, then plan and edit the client's own footage to match it — with a plan-first workflow (breakdown → style spec → beat-by-beat edit plan the user picks from → build → side-by-side check against the reference → revisions → sound). Use whenever a user shares a reference/inspiration video or link and wants their video edited "like this", asks to analyze or break down an edit, wants to copy/learn an editing style, or wants a premium short-form edit planned. Includes universal short-form principles as an analysis lens and a fallback when no reference exists. Works with any editing tool.
---

# Edit From Reference

**What this skill does:** a client sends a reference ("make my video like this"). You **study it until you could rebuild it from memory**, write down its rules as a **style spec**, then **plan and edit the client's footage to follow that spec**. The niche doesn't matter: the method is the same for a real-estate walkthrough, a gym reel, a podcast clip or a product ad.

```
Reference(s) ─► 1 STUDY ─► 2 BREAKDOWN ─► 3 STYLE SPEC ─► 4 MAP TO CLIENT FOOTAGE ─► 5 EDIT PLAN (user picks)
            ─► 6 BUILD ─► 7 CHECK SIDE-BY-SIDE vs REFERENCE ─► 8 REVISIONS ─► 9 SOUND ─► export
```

| File | Read when |
|---|---|
| `references/breakdown-checklist.md` | **Always**, while studying a reference: everything to observe and measure, with commands |
| `references/breakdown-template.md` | Writing the per-video breakdown and the style spec |
| `references/edit-plan-template.md` | Producing the beat-by-beat plan |
| `references/animation-patterns.md` | Naming what you see (shared vocabulary) and proposing designs |
| `references/principles.md` | The universal "why it works" lens; also the fallback rules when there's no reference |
| `references/niche-presets.md` | No reference given: starting brand slots per niche |
| `references/example-real-estate.md` | A worked example of the full method (breakdown → spec → mapping → plan) |

---

## 1. Study: get the reference into a form you can analyze

1. **Get the file.** Download it (yt-dlp, a direct link, or a cloud-drive "export=download" link; large files may need a confirm token) or ask the user to upload it. If a link fails (private, login wall), say so and ask for the file. **Never invent an analysis from a title or thumbnail.**
2. **Probe it:** duration, resolution, aspect, fps, audio.
3. **Transcribe word by word** with timestamps (Whisper or similar). With no speech, note that and analyze the visuals and music only.
4. **Detect cuts** automatically (scene-change detection) to get a shot list with timestamps.
5. **Extract frames** at ≥2 fps (every frame for key moments like the hook, transitions and graphics). Make timestamped contact sheets.
6. **Actually look at every frame.** Read the images; don't just list files. For long references (>90s), sample at 1 fps and say so.
7. Measure what you can: colors (sample pixels), caption sizes relative to frame height, loudness, music presence.

All commands are in `references/breakdown-checklist.md`.

## 2. Breakdown: answer the editor's questions for every scene

For each shot or scene write down **what** is on screen, **when** (timestamp and the exact word it lands on), **how** it moves, and **why** it's there. The key question is always:

> **Why this visual, with this design, these colors, this effect and this animation, at this word?**

Cover every layer (the full checklist is in `breakdown-checklist.md`):

- **Format & structure:** aspect, length, sections (hook, body beats, payoff, CTA), where the energy rises and falls.
- **Hook (0–3s):** first frame, first words, first visual change, the open loop.
- **Pacing:** number of shots, average and min/max shot length, where cuts speed up or slow down.
- **Cut logic:** what triggers each cut (a word, a beat in the music, an action, a sentence end).
- **Captions & typography:** on or off, words per caption, font family and weight, size, case, color, position, emphasis method (size, color, font switch, box), entrance animation, timing tightness.
- **Graphics:** lower thirds, callouts, numbers, maps, icons, progress bars, logos; how each enters and exits.
- **Footage & camera:** shot types (wide, detail, drone, gimbal, talking head), camera motion (push, pan, orbit, speed ramp), framing rules, how 16:9 becomes 9:16.
- **Transitions:** types used, how often, rotation.
- **Color & texture:** grade (warm/cool, contrast, saturation), palette hex values, grain, vignette, overlays.
- **Script → visual mapping:** which kinds of lines trigger which visuals. This is the most reusable insight.
- **Sound:** music genre, BPM and energy curve, whether cuts hit the beat, SFX types and density, voice treatment, ducking, silence used as an effect.
- **Ending:** payoff, CTA style, hold length, loop-back to the start.

## 3. Style spec: turn observations into rules

Convert the breakdown into **rules someone else could follow**, using `breakdown-template.md`:

- Say **what's consistent** (do this every time) separately from **what varies** (options).
- Give **numbers**: "cut every 1.2–1.8s", "captions 2–4 words, Montserrat 800, 7% of frame height, white, lower-middle", "music ducks −18dB under voice".
- Write the **script → visual table**.
- List **signature moves** (the 1–3 things that make it recognizably *that* style).
- List **don't copy** items: the creator's logo, handles, personal assets, catchphrases, copyrighted music or film clips.
- With **multiple references:** list what all of them share (the core) and what's specific to each (variants). Ask the user which variant they prefer if it matters.
- **Show the spec to the user** in short form before planning ("Here's what I learned from your reference: …"). They may correct it, and that's cheap now and expensive later.

## 4. Map the style onto the client's footage

The client's footage is never identical to the reference. Bridge the gap explicitly:

| Situation | What to do |
|---|---|
| Same type of footage (e.g. both walkthroughs) | Match the spec directly: shot lengths, moves, captions, grade |
| Reference is talking head, client has no face (or the reverse) | Keep the rhythm, caption system, graphics and grade; swap the "face" anchor for the client's strongest recurring shot |
| Reference uses visuals the client doesn't have | Find the nearest equivalent: client's own b-roll first, then licensed stock, then graphics |
| Different length | Keep the **ratios** (hook %, shots per second, graphic density), not the absolute timings |
| Different niche | Keep the editing grammar; switch brand slots (colors, fonts, cutaway sources) to the client's brand |
| Burned-in text or logos in the client's footage | Plan full-screen scenes or crops that hide them |

Also: silence-cut raw speech (keep ~30ms of padding) **only if** the user wants it, and re-transcribe so all timing is in edited time.

## 5. Edit plan (the human chooses)

Use `references/edit-plan-template.md`: one beat per spoken thought or shot group, each with **3 options (A/B/C)** grounded in the spec, and **citing the reference timestamp** that inspired each ("like ref @0:07, drone reveal with price card"). Mark your suggestion and let the user choose. On phone or chat apps, ask as multiple-choice questions a few beats at a time. **Stop and wait for the picks.**

## 6. Build

- Asset list: client footage first, then licensed stock and fonts. **Log every source and license**; give CC-BY credits to the user.
- Lay out each scene's final frame first, then add motion. Follow the spec's numbers.
- Describe or execute it in the user's tool (CapCut, Premiere, After Effects, DaVinci, Remotion, HTML/GSAP).

## 7. Check side by side against the reference (before the user sees anything)

- Look at every frame of your render (or a dense sample on long videos).
- Put **your render next to the reference** at matching moments (hook, a typical caption, a graphic, a transition, the ending). Compare caption size and position, pacing, grade, motion feel and graphic style. Write down each mismatch and fix it, or explain why it's intentional.
- Also check: near-empty frames, captions off their word, text outside safe zones, cropped faces, visible burned-in source text, misaligned callouts, slowed footage with moving lips.

## 8–9. Revisions and sound

- Expect the first draft to be 60–70% there. Ask for **numbered changes with timestamps**, then "Ready for sound, or more changes?"
- Sound follows the spec (genre, energy, beat-sync, SFX density). Final loudness about −14 LUFS for social platforms.

## When there's no reference

Use `references/principles.md` (universal rules) plus `references/niche-presets.md`, and say that you're doing so. Offer to study a reference if the user can find one; it's the fastest way to hit their taste.

## Save what you learn

Save each breakdown and style spec (e.g. `references-library/<creator-or-client>/`). After 3+ references from the same source, merge them into one fingerprint. Over time this becomes a library of styles you can apply on request ("edit this like the luxury-realtor style").
