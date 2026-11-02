# Creator Profile — Client Editor

Your identity, positioning, and workflow for video work in this workspace. **Read this before every video task** (alongside `PREFERENCES.md`). Use it for on-screen text, niche framing, and workflow assumptions.

> The user is a **freelance video editor working for clients**. The speaker, handles and niche change per project — always ask for them at the start of each video.

## Identity

- **Name on-screen**: **per client** — ask for the speaker's name at the start of every project. Never put the editor's own name on screen.
- **Instagram**: per client (ask)
- **TikTok**: per client (ask)
- **YouTube**: per client (ask)
- **X / other**: per client (ask)

When putting handles on-screen (lower-thirds, outros, end-cards), use the **client's** handle for that project, exactly as they give it. Record it in the project's `meta.json` / `DESIGN.md`. If unknown, leave handles off-screen and ask.

## Platform priority

**Cross-post to all** — Instagram Reels, TikTok and YouTube Shorts. Default **9:16 vertical, 1080×1920, 30fps**. Keep key text inside the safe zone (avoid the bottom ~350px and right ~150px where platform UI sits).

## Content niche

**All niches** — varies per client. At the start of each project, confirm the client's niche and preferred style (e.g. `/premium-minimal-edit` for educational/podcast clips) instead of assuming.

## On-camera mix

**Other people's clips** — mostly podcast / interview / talking-head footage of the client or a guest speaker. Usually landscape source that needs a 9:16 reframe on the speaker.

- **Face-cam** → use `/short-form-video` face-mode choreography (BOTTOM / FULLSCREEN modes).
- **Faceless** → motion graphics + AI TTS narration (`npx hyperframes tts`) or screen-recordings.

## Workflow — division of labor

**Mode: raw footage in → full edit out.** The user sends raw client footage; the assistant cuts silences/retakes (default: keep ~30ms padding around speech), reframes to 9:16, and builds the full visual layer, captions and sound design. Plan the edit first (edit-plan document) and get the user's picks before building. Do not change the meaning or order of what the speaker says without asking.

_(Reference — the two common modes:)_

- **You record + pre-edit your own speaking video** → it's the source of truth; the assistant builds the visual layer on top and does NOT cut your audio, remove pauses, or change your pacing.
- **You build from scratch with the assistant** → motion graphics, TTS narration, screen-recordings assembled together.

## Brand identity

**Per client.** Each project gets its own `assets/brand-tokens.css` (copied from the workspace default, then adjusted to the client's brand). The workspace default in `assets/brand-tokens.css` is the **premium minimal / Arthur Brooks look**: near-black #0B0B0D, white #FAFAFA, royal blue #1F4FD8 (flat cards #0A47FF), Inter + Playfair Display Italic. Text is white on footage, blue on white.

## Inspiration creators

See [`_reference/creator-library/INDEX.md`](_reference/creator-library/INDEX.md) for the full list. Add new creators via `/study-creator <url>` (links or uploaded files).

- **@arthurcbrooks**: the user's main reference style (premium minimal educational). Use it for podcast/talking-head client clips unless the client wants something else. Fingerprint: [`style-distilled.md`](_reference/creator-library/arthurcbrooks/style-distilled.md); build with `/premium-minimal-edit`.

## Posting cadence & length defaults

- _Cadence_: per client
- _Default length_: 15–45s short-form vertical is a common sweet spot. Adjust per video.
- _Default fps_: 30 (matches TikTok + Instagram defaults).

## Project slug convention

**Topic-only, kebab-case.** Each video gets a new subfolder under `video-projects/<topic-slug>/`. Examples: `ai-agents-intro`, `prompting-101`, `tool-of-the-week`. Keep slugs short and descriptive — scannable at a glance in `ls video-projects/`.

---

*This file is updated as your creator profile evolves. Major changes (new handles, platform shifts, workflow changes) can be edited here directly.*
