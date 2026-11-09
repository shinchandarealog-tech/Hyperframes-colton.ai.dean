# DfRgEzoN7v- (Find My: "Finding Keys") — @themilesholden

**Source:** https://www.instagram.com/reel/DfRgEzoN7v-/ (inferred from the uploaded file name)
**Duration:** 16.14s
**Aspect:** 9:16
**Resolution:** 720x1280 @ 30fps
**Studied:** 2026-11-09
**Engagement (at time of study):** not available. This was a local upload with no info JSON.
**Sample rate:** I read every frame at 2fps (32 frames) on timecoded 4×4 contact sheets and checked frame 14 at full resolution.

## Hook (0–2s)
- **0.0s:** The full layout is on screen from frame 1 with no build-in. The left panel is labelled **"Drawing"** and shows a hand-sketched app icon (radar rings). The right panel is labelled **"✳ Opus 5.5"** and shows a polished 3D **Find My** icon on light grey. A **Comment "OPUS" for guide** line sits under both panels.
- **0.5s:** The camera pushes into the icon. Its green radar ring fills the panel and the blue location dot grows.
- **1.0–1.5s:** The blue dot becomes a map pin, and the shot drops into a photoreal aerial view of a European city at golden hour. The drawing panel switches to a matching sketched street map.
- The hook works on contrast: a 2-second doodle becomes a cinematic 3D world. There's no talking and no face, only the reveal of what the drawing turned into.

## Pacing
- Total scenes (beats): 9. These are continuous camera moves, not hard cuts. Scene detection at a 0.25 threshold found zero cuts.
- Average beat length: about 1.8s
- Shortest / longest: about 1.0s (the "Here" green disc) / about 3.0s (the keys-on-table orbit)
- Distribution feel: one continuous "camera flight" of medium beats
- Pace shifts: the countdown (12m → 10m → 6m → 3m → 2m → 1m) speeds up the beats. The orbit around the keys slows down for the payoff, then it pulls back fast to the logo.

## Captions
- Style: no spoken captions. There's one **persistent static CTA**, **Comment "OPUS" for guide**, for the whole duration.
- Font feel: a geometric/grotesk sans (Google Sans / Product Sans feel). The labels are white, medium–bold weight.
- Active-word treatment: none. "OPUS" is just tinted pink (#f8b0be) inside curly quotes.
- Position: the CTA sits at about y=80% and the panel labels sit above each panel.
- Size: medium (about 34px on a 1280-tall frame)
- **In-content UI text** carries the story: "Keys · Avenue Marceau · 14 m", "Finding Keys", "12 m ahead", "Here", "Find My". The large white distance numerals are the closest thing to kinetic typography.

## Scene types
1. **0.0–1.0 Product/UI showcase:** the Find My app icon pushes in (zoom through the icon)
2. **1.0–2.0 Map fly-in:** a photoreal aerial city with a blue dot and a pin
3. **2.0–4.5 UI overlay on 3D:** an iOS-style "Keys" bottom sheet with Play Sound and Find buttons. The camera tilts down the boulevard and green radar rings pulse.
4. **4.5–5.5 Camera dive:** from top-down to street level, with the blue dot as a puck on the sidewalk
5. **6.0–8.5 AR wayfinding:** street-level café terrace, a "Finding Keys" header, a big arrow and a distance readout counting down (12 → 10 → 6 → 3 → 2 → 1 m)
6. **9.0–9.5 Arrival:** a green disc with **"Here"**. It scales up on the café table.
7. **10.0–12.0 Hero orbit:** an orbit around the keys with an AirTag on the table, with green rings rippling out
8. **12.5 Whip/zoom-out:** the shot zooms into the AirTag's white surface (a match cut) …
9. **13.0–16.1 Logo outro:** … then out to the Find My icon, which settles with a **"Find My"** wordmark under it. It's held for about 2.5s.

The drawing panel (Archetype: **split-screen / side-by-side comparison**) stays in sync with every beat: a sketched version of each shot appears at the same moment.

## Transitions
- Flavors: **continuous camera zoom-through** (icon to map), **tilt/dolly** (aerial to street), **match-cut on shape** (AirTag disc to icon circle), **scale-up overlay** ("Here" disc)
- Rotation cadence: always "zoom through an object into the next world". There are no hard cuts.
- Signature: the opening and closing beats both run through the **app icon**, so the video starts on the icon and ends on it.

## Face treatment
- Mode: none. It's faceless.
- Grading: warm golden-hour photoreal renders (amber/stone) against the cool neutral sketch panel
- Camera motion: constant. Every beat has a push, orbit or tilt.
- Framing: the same 2-panel layout throughout

## Audio reactivity
- I couldn't see any text pulsing on the beat. The layout chrome is completely static.
- I couldn't verify whether the audio is music only (see the transcript note).

## Palette
- **#0a0a0a / #131313**: canvas (a radial dark-grey vignette, lighter in the centre)
- **#e07e52**: Claude-orange asterisk next to "Opus 5.5"
- **#f8b0be**: pink "OPUS" keyword in the CTA
- **#ffffff**: labels and the CTA
- **#34c759-ish green / #0a84ff-ish blue**: the subject brand (Find My). This changes per video.
- Sketch panel: off-white paper **#f7f6f2** with black ink

## Signature move
A rough pen sketch of an app on the left plays in perfect sync with a polished, cinematic AI-generated version of the same storyboard on the right, framed as "Drawing → Opus 5.5".

## What to steal (actionable for Hyperframes builds)
- **Fixed two-panel comparison shell.** On a 720×1280 frame: a small left panel (about 216×384 at x=50, y=490) and a big right panel (about 380×675 at x=287, y=297). Both are 9:16 and offset vertically, and each has a label above it. Build it as a root composition with two `<div>` wrappers, each holding a `<video>` (muted, no `class="clip"`) and an `<h3>` label.
- **Persistent CTA line** ("Comment "KEYWORD" for guide") at y≈80%, with the keyword in an accent colour. You can reuse this on any comment-to-DM funnel video.
- **Zoom-through transitions instead of cuts.** For HTML-native builds, use `cinematic-zoom` or `transitions-scale` between beats.
- **Start and end on the app icon** for a bookend loop.
- **Countdown numerals** (12m → 1m) as a built-in progress bar that builds anticipation.

## What's creator-specific (don't copy literally)
- The "✳ Opus 5.5" label, the Claude asterisk and the "Comment OPUS" lead magnet belong to his funnel.
- Apple Find My branding and UI are third-party IP. Use your own subject.

## Transcript
Not transcribed: `npx hyperframes transcribe` could not download its Whisper model because this environment blocks the Hugging Face host. Nothing on screen points to a voiceover (no presenter, no spoken captions), so the audio is **probably** a music bed, but that is unverified. Re-run transcription where the model can download.
