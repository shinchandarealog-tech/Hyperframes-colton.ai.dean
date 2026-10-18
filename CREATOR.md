# Creator Profile — Client (workout niche, anonymous for now)

> **Context:** this workspace is run by a video editor building a *pitch sample* for a fitness client. The client's reference videos (3 @tailoredfit reels, analyzed in `_reference/creator-library/tailoredfit/`) define the target style. Goal: a sample edit the client loves enough to hire us.

Your identity, positioning, and workflow for video work in this workspace. **Read this before every video task** (alongside `PREFERENCES.md`). Use it for on-screen text, niche framing, and workflow assumptions.


## Identity

- **Name on-screen**: — (anonymous — no name on screen until the client provides one)
- **Instagram**: —
- **TikTok**: —
- **YouTube**: —
- **X / other**: —

**Never put a handle or name on screen** in the sample unless the client supplies one.

When putting handles on-screen (lower-thirds, outros, end-cards), use the platform-appropriate handle.

## Platform priority

**Cross-post all** (Reels + TikTok + Shorts). Default **9:16 vertical, 1080×1920, 30fps**. Keep text and key action inside the safe zone that works for every platform (avoid the bottom ~20% and right ~12% where UI overlays sit).

## Content niche

**Fitness / workout** — exercise demos, gym content, training tips.

## On-camera mix

**Mix / TBD.** It depends on the footage the client sends (raw workout clips, talking-head + B-roll, or both).

- **Face-cam** → use `/short-form-video` face-mode choreography (BOTTOM / FULLSCREEN modes).
- **Faceless** → motion graphics + AI TTS narration (`npx hyperframes tts`) or screen-recordings.

## Workflow — division of labor

**Mix / not sure yet.** Decide per delivery once the client's footage arrives. Default rule: if the client is **speaking** in the footage, never cut their words or change what they're saying. Raw workout B-roll can be cut and paced freely to match the reference style.

- **You record + pre-edit your own speaking video** → it's the source of truth; the assistant builds the visual layer on top and does NOT cut your audio, remove pauses, or change your pacing.
- **You build from scratch with the assistant** → motion graphics, TTS narration, screen-recordings assembled together.

## Brand identity

Placeholder palette derived from the @tailoredfit references: orange-yellow `#f0a800` accent, red `#fc3c48` cues, green `#60cc30` progress, white/near-black. Heavy geometric sans ALL CAPS captions. See `assets/brand-tokens.css`. **Replace with the client's real brand colors/logo if they have them.**

## Inspiration creators

**Client reference videos** are the primary style target. Their analyses live in [`_reference/creator-library/`](_reference/creator-library/), and they **override `MOTION_PHILOSOPHY.md` defaults** for this client's builds.

- **[@tailoredfit](_reference/creator-library/tailoredfit/style-distilled.md)** — client's target style (3 reels studied). **Build every client video "like @tailoredfit".**

See [`_reference/creator-library/INDEX.md`](_reference/creator-library/INDEX.md) for the full list. Add new creators via `/study-creator <url>`.

## Posting cadence & length defaults

- _Cadence_: TBD (client project)
- _Default length_: 15–45s short-form vertical is a common sweet spot. Adjust per video.
- _Default fps_: 30 (matches TikTok + Instagram defaults).

## Project slug convention

**Topic-only, kebab-case.** Each video gets a new subfolder under `video-projects/<topic-slug>/`. Examples: `ai-agents-intro`, `prompting-101`, `tool-of-the-week`. Keep slugs short and descriptive — scannable at a glance in `ls video-projects/`.

---

*This file is updated as your creator profile evolves. Major changes (new handles, platform shifts, workflow changes) can be edited here directly.*
