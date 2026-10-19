# client-reel-01 — "The silent ad auction" — Storyboard

Source: `assets/raw.mp4` (32.2s, 720x1280 @25fps, single take on blue backdrop). Output: 1080x1920 @30fps.
Style: @alihassan-works (blur-focus text, navy glass pills, ticking checklists, mock-UI CTA) + premium b-roll + Apple-style animation.
**Audio is untouched.** Every beat is timed to `assets/transcript.json`.

| # | Time | Spoken | Visual |
|---|------|--------|--------|
| 1 | 0.0–2.3 | "Every time you tap an ad on your phone," | Face full screen. Blur-in kinetic text "Every time you **tap an ad**". Glass iPhone mockup slides up with a finger-tap ripple on an ad card. |
| 2 | 2.3–5.1 | "a silent war happens in less than a second." | **B-roll cut:** dark, premium shot (server racks / data streams). Apple-style headline "A silent war." + a "< 1 sec" counter ticking 0.000 → 0.97s. |
| 3 | 5.1–9.5 | "When you click, 50 different companies bid against each other…" | Face returns, slow push-in. A grid of 50 glowing glass company chips cascades in; bid tags flicker up ($0.42, $1.10…). Gradient count-up "50". |
| 4 | 9.5–12.4 | "But the winner is not the one with the biggest budget." | Numbered glass pill "Biggest budget" gets a strike-through and fades to grey. Blur-text "≠ winner". |
| 5 | 12.4–16.0 | "The AI picks the ad that users actually watch and share." | **B-roll cut:** abstract AI/neural b-roll. Checklist ticks in on the spoken words: ✓ Watched ✓ Shared. |
| 6 | 16.0–21.5 | "If your ad is boring, the AI taxes you… five times more expensive." | Face. Red-tinted glass card "Boring ad", CPC price counter climbs to **5×** with a shake. |
| 7 | 21.5–25.5 | "If your ad holds attention, the platform gives you a massive discount." | Mirror card in blue: "Holds attention", price drops with a "−80%" discount tag (Apple-store price-drop animation). |
| 8 | 25.5–28.1 | "Stop blaming the algorithm. Fix your creative hook." | Big kinetic slam: "Stop blaming the algorithm." → "Fix your **hook**." (light-blue gradient, 3D extrude on "hook"). |
| 9 | 28.1–32.2 | "Comment 'auction' below and I'll send you five winning ad hook templates." | Mock-UI CTA: comment bubble typing "AUCTION" → send → DM notification card "Here are your 5 winning hook templates" (no name/handle shown). |

Throughout: soft vignette plus light grain on the face-cam, and a subtle teal/blue grade to match the brand palette. Text stays in the chest zone (y 45–78%) and never covers the face.

Notes: Whisper heard "ad hook" as "ad-hoc". The CTA uses "ad hook templates".

## Build notes
- Scenes are authored in `src/scenes/` with shared `src/fx.css` + `src/fx.js`; run `python3 scripts/build-comps.py` to regenerate `compositions/`.
- `assets/face.mp4` (gitignored, derived) = 1080x1920@30 upscale of `assets/raw.mp4`:
  `ffmpeg -i assets/raw.mp4 -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.4,fps=30" -c:v libx264 -preset medium -crf 17 -pix_fmt yuv420p -c:a copy -movflags +faststart assets/face.mp4`
- Final scene timing (s): s1 0–2.3 · s2 2.3–5.1 · s3 5.1–9.45 · s4 9.45–12.65 · s5 12.65–15.95 · s6 15.95–21.45 · s7 21.45–25.75 · s8 25.75–28.45 · s9 28.45–32.17
