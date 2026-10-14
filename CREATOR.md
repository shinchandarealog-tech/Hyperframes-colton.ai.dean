# Creator Profile — Video Editor (client work)

Your identity, positioning, and workflow for video work in this workspace. **Read this before every video task** (alongside `PREFERENCES.md`). Use it for on-screen text, niche framing, and workflow assumptions.

## Identity

- **Role**: video editor — mostly makes videos **for clients**, may make some personal ones later. Currently experimenting.
- **Name on-screen**: none. Do **not** put the editor's name or handles on screen.
- **Handles**: — (none for now)

Each client video uses **that client's** name, handles, logo and CTA. Ask for them at the start of a project; never invent them.

## Platform priority

**Cross-post to all** — TikTok, Instagram Reels, and YouTube Shorts. Default format: **9:16 vertical, 1080×1920**, 30fps.

## Content niche

**Everything** — no single niche. Ask about the topic for each new video rather than assuming one.

## On-camera mix

**Both** — some videos are face-cam, some are faceless. Confirm which mode at the start of each video.

- **Face-cam** → use `/short-form-video` face-mode choreography (BOTTOM / FULLSCREEN modes).
- **Faceless** → motion graphics + AI TTS narration (`npx hyperframes tts`) or screen-recordings.

## Workflow — division of labor

**Mix of both** — varies per video. Ask at the start of each video which mode applies:

- **You record + pre-edit your own speaking video** → it's the source of truth; the assistant builds the visual layer on top and does NOT cut your audio, remove pauses, or change your pacing.
- **You build from scratch with the assistant** → motion graphics, TTS narration, screen-recordings assembled together.

## Brand identity

**Per project.** Colors, fonts and logo come from the client's brand, or from the mood of that video. Ask at the start of each project and put them in that project's own `assets/brand-tokens.css`. The workspace-level `assets/brand-tokens.css` is only a neutral fallback.

## Inspiration creators

See [`_reference/creator-library/INDEX.md`](_reference/creator-library/INDEX.md) for the full list. Add new creators via `/study-creator <url>` (or upload a video file).

**Current favorite: @barsolmedia's caption style** — words that type in one by one and pile up along a curving spiral around the speaker. See [their analysis](_reference/creator-library/barsolmedia/videos/nobody-cares-about-your-logo/analysis.md), "Captions" section.

## Posting cadence & length defaults

- _Cadence_: varies by client.
- _Default length_: 15–45s short-form vertical is a common sweet spot. Adjust per video.
- _Default fps_: 30 (matches TikTok + Instagram defaults).

## Project slug convention

**Topic-only, kebab-case.** Each video gets a new subfolder under `video-projects/<topic-slug>/`. Examples: `ai-agents-intro`, `prompting-101`, `tool-of-the-week`. Keep slugs short and descriptive — scannable at a glance in `ls video-projects/`.

---

*This file is updated as your creator profile evolves. Major changes (new handles, platform shifts, workflow changes) can be edited here directly.*
