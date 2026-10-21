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

**Reels-first** (Instagram Reels is the priority; cross-post to TikTok / Shorts is fine). Default aspect: **9:16 vertical, 1080×1920**. Keep key text inside Reels safe zones (clear of the bottom caption/UI area and right-side action rail).

## Content niche

**Business / finance** — entrepreneurship, money, marketing. When planning a new video, assume this niche unless told otherwise.

## On-camera mix

**Both** — some videos are face-cam, some are faceless. Confirm which mode at the start of each project.

- **Face-cam** → use `/short-form-video` face-mode choreography (BOTTOM / FULLSCREEN modes).
- **Faceless** → motion graphics + AI TTS narration (`npx hyperframes tts`) or screen-recordings.

## Workflow — division of labor

**Depends on the video.** Ask at the start of each project which mode applies. When the user supplies their own pre-edited speaking video, treat it as the source of truth (rule 1 below). Otherwise build from scratch (rule 2).

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
