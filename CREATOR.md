<!-- HYPERFRAMES_SETUP_INCOMPLETE -->
<!-- ^ Leave this marker until /setup is complete. It tells Claude to greet a new user
     and run onboarding before any video work. The setup skill removes it when finished. -->

# Creator Profile — _(your name)_

Your identity, positioning, and workflow for video work in this workspace. **Read this before every video task** (alongside `PREFERENCES.md`). Use it for on-screen text, niche framing, and workflow assumptions.

> 🚧 **This file is a blank template.** Run `/setup` (or just tell Claude "help me get set up") and it will fill these sections in from a short interview. You can also edit it by hand any time.

## Identity

- **Name on-screen**: _(your display name)_
- **Instagram**: _(@handle or "—")_
- **TikTok**: _(handle or "—")_
- **YouTube**: _(handle or "—")_
- **X / other**: _(handle or "—")_

When putting handles on-screen (lower-thirds, outros, end-cards), use the platform-appropriate handle.

## Platform priority

**Instagram Reels first.** Default: **9:16 vertical, 1080×1920, 30fps.**

## Content niche

**Jewellery brand content**: product showcases and brand reels. Default vibe: **luxury & elegant** (slow smooth moves, light sweeps/shimmer on metal and stones, serif type, generous breathing room). Note: this overrides MOTION_PHILOSOPHY.md's chrome/grid/fast-whip texture. Keep the discipline but use a softer luxury palette and pacing.

## On-camera mix

**Faceless / product-led**: raw product footage plus a supplied voiceover.

- **Face-cam** → use `/short-form-video` face-mode choreography (BOTTOM / FULLSCREEN modes).
- **Faceless** → motion graphics + AI TTS narration (`npx hyperframes tts`) or screen-recordings.

## Workflow — division of labor

**Active mode: the user supplies a voiceover (which is also the script) and raw footage.** The voiceover is the source of truth: never cut it, re-time it, or change its pacing. Cut and sync the footage and text to it. **Captions: key phrases only** (minimal elegant text, not word-by-word karaoke).

Reference modes:

- **You record + pre-edit your own speaking video** → it's the source of truth; the assistant builds the visual layer on top and does NOT cut your audio, remove pauses, or change your pacing.
- **You build from scratch with the assistant** → motion graphics, TTS narration, screen-recordings assembled together.

## Brand identity

Starter luxury palette in `assets/brand-tokens.css`: black `#0b0a08`, gold `#c9a45c`, ivory `#f5efe3`. Display font: Cormorant Garamond (serif); body: Inter. Logo: TBD (supplied per project).

## Inspiration creators

_(Studied creators live in [`_reference/creator-library/`](_reference/creator-library/). Paste a TikTok / Instagram Reel / YouTube Short URL and run `/study-creator <url>` to add one. At build time, name a creator — "build this like @handle" — to apply their style fingerprint to the visual layer. /setup seeds your first few here.)_

## Posting cadence & length defaults

- _Cadence_: _(TBD — set during /setup)_
- _Default length_: 15–45s short-form vertical is a common sweet spot. Adjust per video.
- _Default fps_: 30 (matches TikTok + Instagram defaults).

## Project slug convention

**Topic-only, kebab-case.** Each video gets a new subfolder under `video-projects/<topic-slug>/`. Examples: `ai-agents-intro`, `prompting-101`, `tool-of-the-week`. Keep slugs short and descriptive — scannable at a glance in `ls video-projects/`.

---

*This file is updated as your creator profile evolves. Major changes (new handles, platform shifts, workflow changes) can be edited here directly.*
