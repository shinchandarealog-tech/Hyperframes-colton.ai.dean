# @edita.visuals — Style Fingerprint

Rolled up across 6 videos. See `videos/*/analysis.md` for per-video detail. Last distilled: 2026-10-29.

---

## Part 1 — How the storyboard ("before") works

Every post is a **before/after showcase**. The "before" card, labelled **Storyboard**, is a **pencil line-art version of the finished edit, frame-synced to it**. Reading it as a process gives this workflow:

1. **The storyboard is the edit's skeleton, drawn per shot.** Each scene in the final edit has a matching sketch panel: same framing, same subject pose, same layout. Face-cam shots are traced portraits. B-roll is traced objects (clock, brain, phone, shelves, flowers).
2. **Text is planned as placeholder boxes, not written out.** Wherever a caption or graphic will go, the storyboard shows a hand-drawn rectangle labelled **"Text"**, sized and positioned exactly where the final caption lands. Big hero words (SAY THAT, BRAINS, Social media., BLOOD STREAM, PAID OFF) are sometimes **traced as outlined lettering** to lock in the typographic scale.
3. **Graphic layouts are blocked out as wireframes.** UI mocks appear as outline cards with "Text" slots: the chat input, the Blueprint checklist, the toggle pills, the poll chips, the Polaroid sticker, the phone with app icons. The storyboard decides *what kind* of graphic goes on each line, *where* it sits and *how big* it is before any styling.
4. **Timing is decided at the storyboard stage.** The sketch changes exactly when the edit cuts, so the cut points (one per phrase / noun) are fixed during storyboarding, not during polish.
5. **What the storyboard does NOT decide:** colour, fonts, glow, grade, SFX, easing. Those are the polish layer. That's why one storyboard language produces six very different-looking finals (orange serif, purple sans, terracotta caps, lime glow, cobalt italic, brown editorial).

**Practically:** the storyboard is a **shot-by-shot list keyed to the transcript**. For every phrase it answers: (a) what's on screen (face / B-roll / UI mock / kinetic text), (b) where the text box goes, (c) which word is the keyword. The look comes later.

### Why the "after" is so good (the polish layer on top of the storyboard)
- **Every concrete noun gets a visual.** Years → clock, companies → logo wall, brains → 3D brain, starches → spoons, lawsuit → courtroom, social media → phone. The storyboard forces this question for every line.
- **Abstract ideas become UI.** "Can you program this for me?" → a chat input with a send click. "Go viral" → a TikTok post button + view counter. "Paid off" → a progress bar filling to 99%. "Pros/cons" → ✓/✕ pills.
- **One accent colour, everywhere.** Keyword, chips, glow, flash transitions and cards all share one hue matched to the footage's lighting.
- **Hierarchy in every caption.** Small lead-in + big keyword, so the eye reads the keyword first.
- **Sound on every event.** ~1–1.3 SFX per second: a swoosh per cut, a pop per chip, a click per cursor, a riser into reveals, a low thump on punch words.
- **Nothing static for >2s.** Even "long" face-cam runs have captions building word by word, punch-ins, blur resets or chips stacking.

---

## Part 2 — Signature moves (consistent across all 6)

- **Hook pattern:** 0–0.5s face-cam already captioned (no title card). By 1.0–2.5s the **first graphic interruption** lands (clock B-roll, progress card, profile card, "Social media." product layout, supplement shelf). Speaker identity is established in the first 3s with a **name chip / IG profile card / channel header / typewriter lower-third**.
- **Caption treatment:** a **two-tier "lead-in + keyword"** system. Lead-in: small, white, thin or medium sans, often ALL CAPS, built word by word. Keyword: 3–4× larger, in **the video's single accent colour**, in a contrasting face (italic serif, condensed heavy caps, or bold italic sans), revealed with a letter-by-letter wipe/blur or pop. Captions sit centre-low on the chest and never cover the face.
- **Caption decorations:** micro-graphics tied to the word (underline swoosh, slider knob, ▶| skip icon, ✦ sparkle bullets, floating "?" marks, hand-drawn arrows, circle highlight rings).
- **Chip / pill vocabulary:** rounded pills with icons for lists and verdicts. ! = problem, + = item, ✓ = benefit, ✕ = rejected, ★ = hero claim, 🛡 = protection, emoji = emotion. Chips **stack** and **persist across B-roll cuts**.
- **Transition rotation:** mostly **hard cuts on the word**. Graphic scenes enter with one of: colour-flash flicker, light-sweep flash, video-to-card shrink, 3D card swing, push-in zoom on text, card slide-up, defocus-blur reset, torn-paper frame. The same fancy transition never appears twice in a row.
- **Face treatment:** fullscreen face-cam is the home base (≈50–60% of runtime). It's regularly **turned into an object**: a rounded card on a white canvas, a stacked top/bottom split, inside a YouTube/TikTok/app UI, or a square app-icon tile. A bottom dark gradient keeps captions legible.
- **Graphic-scene look:** white / off-white / light-gradient canvases, rounded 16px cards, soft drop shadows, frosted glass, gradient-mesh blobs, dotted grids, all in the accent hue. Reads like a modern SaaS landing page.
- **Palette:** **one accent per video**, picked to match the footage: #E8552B orange (AI interview), #8B5CF6 purple (blue-lit creator), #C8673A terracotta (warm podcast), #D7F542 lime (neutral daylight), #2F6BFF cobalt (blue suit / blue foreground), #9E2B1E + #E9A23B red/gold on beige (warm podcast). Constants: white #FFFFFF, near-black #0B0B0F, off-white #F4F4F4.
- **Energy profile:** sustained high. Front-loaded hook burst, then a graphic interruption every 2–4s, a big set-piece in the middle (UI mock / carousel / montage), and a strong final keyword. No breathing outro: the clip ends on the last punch word.
- **SFX profile:** 0.9–1.3 broadband transients/sec (swoosh/click/pop) layered under the voice. Low thumps on punch words and scene entrances. Risers into reveals (progress bars, logo walls). Tick clusters under scrubs/counters. A paper wash for paper-themed transitions. The music bed is very quiet or absent (one video has a soft ~106 BPM bed). The voice always dominates.

## What to steal (ranked by Hyperframes copy-ability)
1. **Two-tier caption component** (lead-in sans + accent keyword with per-letter blur/wipe-in). Pure HTML/CSS + GSAP stagger. Use on every build.
2. **Storyboard-first workflow**: before authoring, write a shot list from `transcript.json`. For each phrase: scene type, keyword, text-box position, B-roll/UI noun. (We can render our own sketch-storyboard card by running an edge-detect filter over draft frames for the same before/after look.)
3. **HTML UI mock scenes**: chat input + cursor click + send (`keyboard-typing` + `click.wav`), progress bar filling (`riser`), toggle pills, poll chips, profile cards, platform post UI with a view counter. HyperFrames is HTML, so these are native.
4. **Chip/pill system with icon semantics**, stacking and persisting over B-roll cuts (`pop.mp3` per chip).
5. **Face → card transformations**: animate a wrapper div to a rounded card on white, a stacked split, or a 3D swing (`perspective` + `rotateY`). Never animate the `<video>` itself.
6. **Literal-noun B-roll cut-ins**, 0.5–1.2s each, graded to the face-cam palette.
7. **Transition kit**: colour-flash flicker (3–4 frames), light-sweep flash, push-in on text, defocus-blur reset, carousel push. Map to `whoosh`, `glitch`, `hard-cut`, `swipe`.
8. **One accent colour per video**, sampled from the footage's dominant light (respects `PREFERENCES.md` / brand tokens first).
9. **SFX density target**: ~1 SFX per visual event, voice -12 to -18 dB above SFX (per `assets/sfx/MANIFEST.md` level discipline).

## Don't copy
- The promo wrapper itself ("Opus 5.5" pill, "Follow & comment CLAUDE", Claude asterisk background, @edita.visuals handle). That's their marketing frame, not the edit style. If the user wants a before/after showcase of their own, build an original wrapper with their handle.
- Other people's interview footage, names, and composited images of real people (the courtroom shot).
- Real platform stats or UI presented as genuine. Mocks are fine as obvious illustration.

## Videos studied
- [det-wsmtgue](videos/det-wsmtgue/analysis.md) — AI interview; orange italic-serif keywords, literal B-roll cut-ins, chat-UI mock with cursor send
- [de1ub-sj8m8](videos/de1ub-sj8m8/analysis.md) — creator talking head; purple accent, flash-flicker transitions, face shrinks into YouTube card, Blueprint checklist
- [dfahrx6pxz5](videos/dfahrx6pxz5/analysis.md) — health podcast; editorial magazine serif type, IG profile cards, photo carousel, text behind subject
- [demwl0ottd8](videos/demwl0ottd8/analysis.md) — wellness podcast (51s); terracotta pills, icon-chip semantics over plant montage, stacked split-screen
- [derbe18txng](videos/derbe18txng/analysis.md) — business talking head; lime glow keywords, 3D card swing with icon orbit, TikTok post-UI with cursor + view counter
- [dewlyzsncme](videos/dewlyzsncme/analysis.md) — insurance agent; cobalt italic caps, frosted-glass UI (progress, toggles, poll), emoji chips, defocus-blur resets
