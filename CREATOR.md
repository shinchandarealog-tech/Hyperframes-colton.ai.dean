# Creator Profile — Client (no on-screen name)

Your identity, positioning, and workflow for video work in this workspace. **Read this before every video task** (alongside `PREFERENCES.md`). Use it for on-screen text, niche framing, and workflow assumptions.

## Identity

- **Name on-screen**: none: do not put a name or handle on screen
- **Instagram**: —
- **TikTok**: —
- **YouTube**: —
- **X / other**: —

When putting handles on-screen (lower-thirds, outros, end-cards), use the platform-appropriate handle.

## Platform priority

**Cross-post all** (Instagram Reels + TikTok + YouTube Shorts). Default: **9:16 vertical, 1080×1920, 30fps**; keep text inside the shared safe zone (avoid top ~220px and bottom ~380px platform UI).

## Content niche

**AI / tech**: AI tools, automation, tech explainers.

## On-camera mix

**Face-cam.** The client records talking-head clips; premium b-roll + Apple-style motion graphics are layered on top.

- **Face-cam** → use `/short-form-video` face-mode choreography (BOTTOM / FULLSCREEN modes).
- **Faceless** → motion graphics + AI TTS narration (`npx hyperframes tts`) or screen-recordings.

## Workflow — division of labor

**Client records + pre-edits their own speaking video. Keep their audio exactly as-is.** Never cut their speech, remove pauses, or change pacing; sync b-roll, captions and animations to their timing.

- **You record + pre-edit your own speaking video** → it's the source of truth; the assistant builds the visual layer on top and does NOT cut your audio, remove pauses, or change your pacing.
- **You build from scratch with the assistant** → motion graphics, TTS narration, screen-recordings assembled together.

## Brand identity

Navy-glass + light-blue/cyan accent palette derived from the @alihassan-works reference, set in `assets/brand-tokens.css`. Display font: Inter / SF Pro Display. Premium, clean, Apple-style.

## Inspiration creators

See [`_reference/creator-library/INDEX.md`](_reference/creator-library/INDEX.md) for the full list. Add new creators via `/study-creator <url>`.

- **Client's primary style reference: @alihassan-works**: Apple-style blur-focus text + glass UI chips + checklist ticks, plus premium b-roll per the client brief.

## Posting cadence & length defaults

- _Cadence_: _(TBD — set during /setup)_
- _Default length_: 15–45s short-form vertical is a common sweet spot. Adjust per video.
- _Default fps_: 30 (matches TikTok + Instagram defaults).

## Project slug convention

**Topic-only, kebab-case.** Each video gets a new subfolder under `video-projects/<topic-slug>/`. Examples: `ai-agents-intro`, `prompting-101`, `tool-of-the-week`. Keep slugs short and descriptive — scannable at a glance in `ls video-projects/`.

---

*This file is updated as your creator profile evolves. Major changes (new handles, platform shifts, workflow changes) can be edited here directly.*
