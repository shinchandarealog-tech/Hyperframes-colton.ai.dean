# Creator Profile

Your identity, positioning, and workflow for video work in this workspace. **Read this before every video task** (alongside `PREFERENCES.md`). Use it for on-screen text, niche framing, and workflow assumptions.

## Identity

- **Name on-screen**: — (not set; client ads carry the client's branding)
- **Instagram**: —
- **TikTok**: —
- **YouTube**: —
- **X / other**: —

When putting handles on-screen (lower-thirds, outros, end-cards), use the platform-appropriate handle.

## Platform priority

**Reels-first** (Instagram). Default **9:16 vertical, 1080×1920, 30 fps**. Keep text and UI inside Meta's Reels ad safe zone (x 65–1015, y 269–1248).

## Content niche

**Client ads / brand spots**: short motion-graphic ads built to a client's render spec (e.g. the KFC "v11" spot). Each project's brand comes from its client spec, not from a personal brand.

## On-camera mix

**Both**: depends on the video. Client spots are usually faceless motion graphics.

- **Face-cam** → use `/short-form-video` face-mode choreography (BOTTOM / FULLSCREEN modes).
- **Faceless** → motion graphics + AI TTS narration (`npx hyperframes tts`) or screen-recordings.

## Workflow — division of labor

**Build from scratch with the assistant**: motion graphics, audio cues and any TTS are built from the spec or brief.

- **You record + pre-edit your own speaking video** → it's the source of truth; the assistant builds the visual layer on top and does NOT cut your audio, remove pauses, or change your pacing.
- **You build from scratch with the assistant** → motion graphics, TTS narration, screen-recordings assembled together.

## Brand identity

Workspace default in `assets/brand-tokens.css`: off-white `#F6F5F1` background, `#111111` ink for all type, one red accent `#E4002B` that never touches text; Inter Tight (display), Inter (UI), JetBrains Mono (labels). Client projects override this with their own spec.

## Inspiration creators

_(Studied creators live in [`_reference/creator-library/`](_reference/creator-library/). Paste a TikTok / Instagram Reel / YouTube Short URL and run `/study-creator <url>` to add one. At build time, name a creator — "build this like @handle" — to apply their style fingerprint to the visual layer. /setup seeds your first few here.)_

None studied yet (skipped during setup). Until then, builds use `MOTION_PHILOSOPHY.md` defaults, or the client spec where one is given.

## Posting cadence & length defaults

- _Cadence_: _(TBD — set during /setup)_
- _Default length_: 15–45s short-form vertical is a common sweet spot. Adjust per video.
- _Default fps_: 30 (matches TikTok + Instagram defaults).

## Project slug convention

**Topic-only, kebab-case.** Each video gets a new subfolder under `video-projects/<topic-slug>/`. Examples: `ai-agents-intro`, `prompting-101`, `tool-of-the-week`. Keep slugs short and descriptive — scannable at a glance in `ls video-projects/`.

---

*This file is updated as your creator profile evolves. Major changes (new handles, platform shifts, workflow changes) can be edited here directly.*
