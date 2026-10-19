# Creator Profile

Your identity, positioning, and workflow for video work in this workspace. **Read this before every video task** (alongside `PREFERENCES.md`). Use it for on-screen text, niche framing, and workflow assumptions.

## Identity

- **Name on-screen**: — (no name/handle on screen by default)
- **Instagram**: —
- **TikTok**: —
- **YouTube**: —
- **X / other**: —

When putting handles on-screen (lower-thirds, outros, end-cards), use the platform-appropriate handle.

## Platform priority

Short-form vertical — **9:16, 1080×1920** default. No single platform prioritized yet.

## Content niche

Not fixed yet. First project: a dreamy, surreal animated story short (hot-air-balloon proposal).

## On-camera mix

Undecided ("no idea" at setup). Default to **faceless animated motion graphics** until told otherwise.

- **Face-cam** → use `/short-form-video` face-mode choreography (BOTTOM / FULLSCREEN modes).
- **Faceless** → motion graphics + AI TTS narration (`npx hyperframes tts`) or screen-recordings.

## Workflow — division of labor

Undecided at setup — default to **building from scratch with the assistant**. Ask before assuming a speaking video exists. Two common modes:

- **You record + pre-edit your own speaking video** → it's the source of truth; the assistant builds the visual layer on top and does NOT cut your audio, remove pauses, or change your pacing.
- **You build from scratch with the assistant** → motion graphics, TTS narration, screen-recordings assembled together.

## Brand identity

Blank slate — "let each video decide." `assets/brand-tokens.css` holds neutral defaults; per-video palettes are fine.

## Inspiration creators

None yet (skipped at setup). Studied creators live in [`_reference/creator-library/`](_reference/creator-library/); add one any time with `/study-creator <url>`.

## Posting cadence & length defaults

- _Cadence_: _(TBD — set during /setup)_
- _Default length_: 15–45s short-form vertical is a common sweet spot. Adjust per video.
- _Default fps_: 30 (matches TikTok + Instagram defaults).

## Project slug convention

**Topic-only, kebab-case.** Each video gets a new subfolder under `video-projects/<topic-slug>/`. Examples: `ai-agents-intro`, `prompting-101`, `tool-of-the-week`. Keep slugs short and descriptive — scannable at a glance in `ls video-projects/`.

---

*This file is updated as your creator profile evolves. Major changes (new handles, platform shifts, workflow changes) can be edited here directly.*
