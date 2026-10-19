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

**Cross-post all** — TikTok, Instagram Reels, and YouTube Shorts equally. Default canvas: **9:16 vertical, 1080×1920, 30fps**. Keep captions and key text inside the safe zone that works on all three platforms (avoid the bottom ~20% and the right-edge button rail).

## Content niche

**Mix of everything** — no single niche. Ask about the topic for each video and don't assume one.

## On-camera mix

**Both** — depends on the video. Ask (or infer from the footage) which mode each video uses.

- **Face-cam** → use `/short-form-video` face-mode choreography (BOTTOM / FULLSCREEN modes).
- **Faceless** → motion graphics + AI TTS narration (`npx hyperframes tts`) or screen-recordings.

## Workflow — division of labor

**The assistant edits everything.** The user hands over raw footage (or a URL) and the assistant is the full short-form editor: cuts, crop, mix, captions, titles, and render. Unlike the "pre-edited" mode, the assistant **may** cut audio, remove silences/filler, tighten pacing, and restructure for the hook.

Editing toolchain (pipeline the user specified):

- **FFmpeg** — every cut, crop, mix, mute, and render ([FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg))
- **faster-whisper** (runs OpenAI's [Whisper](https://github.com/openai/whisper) models) — word-level transcription; every cut is placed against these timestamps ([SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper))
- **yt-dlp** — downloads source videos from URLs ([yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp))
- **OpenCV + contrib** — follows whoever is talking when cropping landscape footage to vertical ([opencv/opencv](https://github.com/opencv/opencv), [opencv/opencv_contrib](https://github.com/opencv/opencv_contrib))
- **Headless Chrome (Puppeteer-style)** — renders captions and titles to video; in this workspace that's the Hyperframes renderer ([puppeteer/puppeteer](https://github.com/puppeteer/puppeteer))

Cut rule: cut on word boundaries from the transcript, never mid-word. Keep a little padding (~0.1s) around speech so cuts don't clip breaths into pops.

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
