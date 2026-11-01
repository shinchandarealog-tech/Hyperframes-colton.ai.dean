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

**Cross-post to all three**: TikTok, Instagram Reels and YouTube Shorts. Default canvas is **9:16 vertical, 1080×1920, 30 fps**. Keep text inside the safe zone that works on all three (avoid the bottom ~320px and right ~140px, where the UI overlays sit).

## Content niche

**Real estate**: buying and selling homes, inspections vs. appraisals, contracts, and agent tips. Assume this niche unless told otherwise.

## On-camera mix

**Both.** Some videos are face-cam talking heads with graphics on top, and some are faceless (motion graphics + TTS or screen recordings). Ask which mode at the start of each video if it isn't obvious.

- **Face-cam** → use `/short-form-video` face-mode choreography (BOTTOM / FULLSCREEN modes).
- **Faceless** → motion graphics + AI TTS narration (`npx hyperframes tts`) or screen-recordings.

## Workflow — division of labor

**Mixed — confirm per video.** When the user supplies their own speaking video, treat it as the source of truth (don't cut audio or change pacing unless asked). For faceless videos, build from scratch. The two modes:

- **You record + pre-edit your own speaking video** → it's the source of truth; the assistant builds the visual layer on top and does NOT cut your audio, remove pauses, or change your pacing.
- **You build from scratch with the assistant** → motion graphics, TTS narration, screen-recordings assembled together.

## Brand identity

_(Colors, fonts, logo. Often a blank slate at the start — `assets/brand-tokens.css` fills in over time. Set initial values during /setup.)_

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
