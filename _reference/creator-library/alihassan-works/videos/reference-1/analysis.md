# reference-1 ("These are the 5 fonts") — @alihassan-works

**Source:** user upload — `Video_by_alihassan.works_DaxYgjjoA_f.mp4` (Instagram Reel, @alihassan.works)
**Duration:** 50.56s
**Aspect:** 9:16
**Resolution:** 720x1280, 30fps
**Studied:** 2026-10-19
**Engagement (at time of study):** n/a (uploaded file, no metadata)
**Sample rate:** extracted at 2fps (101 frames); every frame reviewed via timestamped contact sheets, plus 3 full-res detail frames.

## Hook (0–2s)
- 0.0s: single static medium shot of the creator, chest-up, warm practical lamp top-left, dark gaming chair, concrete wall. Speaker already smiling and talking. No cold-open graphic.
- 0.0–0.5s: "These are the" fades in **word by word with a blur→sharp reveal**, centred over the chest.
- 0.5–1.0s: "5 Fonts" slams in under it, big, in a **light-blue → cyan gradient fill with soft glow**. It reveals letter by letter, with blur and a slight scale.
- 1.0–2.0s: a numbered list of 5 **glassy navy pill rows** (1 Inter Font … 5 Tempting Font) cascades down one after another. Each row comes in as a glowing bright-cyan bar, then settles into a dark-navy glass pill.
- The full list holds ~1.5s, then dissolves (blur-out) at ~3.2s.
- Formula: **the spoken promise, set as a "table of contents" overlay on the chest.** The viewer sees the whole payoff structure in the first 2 seconds.

## Pacing
- One continuous take with no visual cuts. Pacing comes entirely from overlay beats.
- Overlay beats: ~25 across 50s, so a new graphic event every ~2s.
- Repeating 5-part module per item (~8s each): **pill label → big font name → one-line description → 3-item checklist ticking on → dissolve**.
- Shortest beat ~0.5s (pill pop); longest ~4s (completed checklist hold).
- The pace speeds up at the CTA (46–50s): Follow button → click → chat bubble typing → DM notification, each ~0.7s.

## Captions
- Not karaoke subs. **Selective kinetic captions**: only key phrases are set, written as designed text blocks rather than transcription.
- Font feel: clean geometric sans (Inter / SF Pro-like), white with a soft drop shadow, semibold to bold. The headline word is huge (~2.5x the body).
- Reveal: **per-word blur-in with a slight upward drift and scale** (Apple keynote "focus-in"). Exit: the whole block blurs and fades out together.
- Accent: an occasional word is tinted light blue during its reveal and settles to white.
- Position: centre-left to centre, over the chest/torso (y ≈ 50–75% of frame). Always clear of the face.
- Size: headline large (~10% of width per char cluster), body medium.

## Scene types
1. 0–3.3s: talking-head (fullscreen) + kinetic-type title "These are the **5 Fonts**" + 5-row glass-pill list (stagger cascade)
2. 3.5–4.5s: glass pill "1 Inter Font" drops in; big "Inter" headline rises beneath it
3. 5–10s: headline moves up/left. "It's a modern and minimal font used in:" + **checklist**: each item is a dashed spinning circle that resolves to a filled blue ✓ while the label blurs in (UI Designs → Motion Graphics → Clean Subtitles)
4. 10.5–12s: phrase caption "Perfect for professional **Tech Style Look**" (gradient-blue emphasis line)
5. 12.5–18s: pill "2 Clash Display" → headline → "This font is used in:" → checklist (Cinematic Edits / Posters / High-End Visuals)
6. 18.5–21s: two-line phrase captions ("If you want a bold and stylish look?" / "Then this font is perfect for you")
7. 21.5–29.5s: pill 3 SF Pro Display → headline → "This is Apple's signature font" → checklist (UI Animation / Minimal Designs / Apple Style Edits)
8. 29.5–37.5s: pill 4 Helvetica → headline → description → checklist (Subtitles / Minimal Edits / Clean Motion Graphics)
9. 38–46s: pill 5 Tempting (rendered in the script face itself) → description → checklist (Cinematic Titles / Aesthetic Videos / Fashion Edits)
10. 46–47s: "And if you want these **Fonts?**" with **3D extruded blue gradient** headline, letters bouncing on a wave
11. 47–48.4s: UI showcase: blue **Follow** button, cursor clicks, morphs to grey "Following ⌄"
12. 48.5–49.2s: UI showcase: iMessage-style input bubble with avatar typing "F… Font" and a blue send arrow
13. 49.5–50.5s: UI showcase: DM notification card (avatar + "alihassan.works / Here's your 5 best fonts") + caption "And I'll send it to you"

No b-roll cutaways. 100% face-cam with overlays.

## Transitions
- No camera cuts. Overlay transitions only:
  - **Blur-in / blur-out** (dominant; on every text block)
  - Stagger cascade (list rows, checklist items)
  - Glow-flash entry: element enters as an over-bright cyan bar, then cools to its final colour
  - Morph: Follow → Following button state change
- Rotation: the same vocabulary repeats on every item. Consistency is the style.

## Face treatment
- Fullscreen, static locked-off tripod, centred, head in the top third and chest left free as the "graphics canvas".
- Grade: warm practicals vs teal-blue shirt (teal/orange). Slightly lifted shadows, soft vignette, shallow DOF background.
- No punch-ins, no Ken Burns. A subtle camera breathe at most.

## Audio reactivity
- None visible. Overlays sync to **spoken words**: each checklist item ticks exactly as it is said.

## Palette
- `#FFFFFF` text (dominant)
- `#1E3A8A` → `#152B6B` navy glass pill fill (semi-opaque, inner highlight, soft outer glow)
- `#4FC3F7` / `#7DD3FC` light-blue → cyan gradient on headline emphasis
- `#3B82F6` check-badge blue, `#4F46E5` follow-button indigo
- `#2A2A2E` dark-grey UI chip ("Following", DM card)

## Signature move
Apple-keynote-style **blur-focus kinetic text and glass UI chips (numbered pills, ticking checklists, Follow/DM mock-UI) floating on the speaker's chest**, synced word by word to their speech.

## What to steal (actionable for Hyperframes builds)
- **Blur-focus word reveal**: GSAP `from({filter:'blur(12px)', opacity:0, y:14, scale:0.96}, stagger 0.06)` per word; exit = whole block `to({filter:'blur(10px)', opacity:0})`. Use for every caption block.
- **Numbered glass pill**: rounded-full navy pill, `backdrop-filter`-style look faked with a semi-opaque gradient + 1px inner highlight + cyan outer glow. Enter as a glow flash (brightness 2 → 1).
- **Animated checklist**: dashed SVG circle rotates while the label blurs in, then morphs to a filled blue circle with a stroke-drawn ✓. Time each tick to the transcript word.
- **Gradient emphasis word** (light-blue → cyan) on the 1–2 key words per section. Use a 3D extrude (stacked text-shadows) only on the final CTA word.
- **UI-mock CTA**: Follow button + cursor click → "Following", then a typing chat bubble, then a DM notification card. Maps loosely to `instagram-follow` / `macos-notification` blocks; custom HTML is more faithful.
- **"Table of contents" hook**: show the whole list structure in the first 2s.
- Keep graphics in the chest zone (y 45–78%); never cover the face.

## What's creator-specific (don't copy literally)
- The handle "alihassan.works", the avatar, and "Here's your 5 best fonts" DM copy
- The font-list topic itself
- His exact blue palette can be adapted to the client's brand accent

## Transcript
See `transcript.json` in this folder (148 words, Whisper small.en). Mistranscription: Whisper hears "font" as **"phone"** throughout and "comment" as "come on"; timestamps stay accurate.
