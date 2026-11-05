
# Creator Profile

Your identity, positioning, and workflow for video work in this workspace. **Read this before every video task** (alongside `PREFERENCES.md`). Use it for on-screen text, niche framing, and workflow assumptions.

## Identity

- **Name on-screen**: —
- **Instagram**: —
- **TikTok**: —
- **YouTube**: —
- **X / other**: —

**No handle / name on screen** — the user chose not to set one. Do not put any name, handle, or end-card identity text on screen unless asked.

## Platform priority

**Instagram Reels first** (cross-post to TikTok/Shorts optional). Default canvas: **9:16 vertical, 1080×1920, 30fps**. Keep captions/text inside Reels safe zones (avoid bottom ~20% UI and right-side action rail).

## Content niche

**AI / tech** — AI tools, tech tips, automation.

## On-camera mix

**Face-cam** — appears on camera in own recorded footage.

- **Face-cam** → use `/short-form-video` face-mode choreography (BOTTOM / FULLSCREEN modes).
- **Faceless** → motion graphics + AI TTS narration (`npx hyperframes tts`) or screen-recordings.

## Workflow — division of labor

**Mode: records + pre-edits own speaking video.** The footage is the source of truth — build captions + motion graphics on top. **Never cut the audio, remove pauses, restructure speech, or change pacing.** Sync visuals to the footage timing.

Reference (both modes):

- **You record + pre-edit your own speaking video** → it's the source of truth; the assistant builds the visual layer on top and does NOT cut your audio, remove pauses, or change your pacing.
- **You build from scratch with the assistant** → motion graphics, TTS narration, screen-recordings assembled together.

## Brand identity

Starting look: **dark + electric-blue accent, white text** (see `assets/brand-tokens.css`). Evolves via `/feedback`.

## Inspiration creators

See [`_reference/creator-library/INDEX.md`](_reference/creator-library/INDEX.md) for the full list. Add new creators via `/study-creator <url>`.

- @simar-visuals — editorial two-voice captions, blue-violet accent
- @vyron-media — gold glowing hero-word slams, warm grade

## Posting cadence & length defaults

- _Cadence_: not set
- _Default length_: 15–45s short-form vertical is a common sweet spot. Adjust per video.
- _Default fps_: 30 (matches TikTok + Instagram defaults).

## Project slug convention

**Topic-only, kebab-case.** Each video gets a new subfolder under `video-projects/<topic-slug>/`. Examples: `ai-agents-intro`, `prompting-101`, `tool-of-the-week`. Keep slugs short and descriptive — scannable at a glance in `ls video-projects/`.

---

*This file is updated as your creator profile evolves. Major changes (new handles, platform shifts, workflow changes) can be edited here directly.*
