# Two Timelines — 30s motion graphic reel (Remotion)

A 1080×1920, 30 fps, 900-frame (30 s) reel. The top half is **THE HARD WAY** and the bottom half is **THE SMART WAY**. The same editor works through script → cuts → captions → B-roll. The smart side exports first, wipes over the frame and lands on "Work smarter, not longer."

> This project uses **Remotion (React)**, not the HyperFrames HTML pipeline the rest of this workspace uses. Run the commands below from this folder.

## Preview

```bash
npm install
npm run dev          # Remotion Studio → http://localhost:3000, composition "TwoTimelines"
```

## Render

```bash
npm run build        # out/two-timelines.mp4  (H.264, CRF 18, AAC)
npm run cover        # out/cover.png          (frame 670)
npm run stills       # QA stills → out/stills/ (frames 30,100,200,300,420,500,600,670,800,880)
npm run stills -- 120,240,672   # any frames you like
npm run lint         # TypeScript check
```

## Drop-in media (all optional; files are detected automatically)

| What | Where | Behaviour |
|---|---|---|
| Claude screen recordings | `public/recordings/prompt1.mp4` … `prompt4.mp4` | Plays inside the shot's white chat card, cropped to fill and sped up so it runs from the start of typing to the end of the shot. A missing file falls back to the animated placeholder chat. |
| Music | `public/music.mp3` | Plays for the whole video. It's positioned so its beat drop lands on frame 660 (see below). |
| SFX | `public/sfx/<name>.mp3` | Each cue in `src/sfx.ts` plays only if its file exists. |
| Fonts | `public/fonts/inter-latin-var.woff2`, `caveat-700.woff2` | These are self-hosted copies of Inter and Caveat, so renders work offline. Delete them to fall back to `@remotion/google-fonts`. |

The `public/music.mp3` and `public/sfx/*` files that ship here come from the workspace's royalty-free library (`../../assets/sfx`, `../../assets/music`; Pixabay and Mixkit licences, free for commercial use). A few are trimmed variants. `tick`, `tick-loop` and `bonk` were synthesised with ffmpeg. Replace any of them with your own files of the same name.

After adding or removing files in `public/`, restart Studio (the file list is read at bundle time).

## What to tweak

**`src/theme.ts`**
- `COLORS`: page/panel backgrounds, green, red, text colours
- `LAYOUT`: panel bounds, label/timer/step-tag positions, safe-zone numbers
- `TYPE`: font sizes
- `COPY`: hook lines, labels, the end message, CTA lines and handle (`@hey.rishish`)
- `HARD_FILTER`, `GRAIN_OPACITY`: the hard-way grade

**`src/timing.ts`**
- `SHOTS`: start and end frame of each of the 10 shots
- `TIMER_KEYS`: timer keyframes as `[frame, top minutes, bottom minutes]`
- Per-shot blocks (`SCRIPT`, `CUTS`, `CAPTIONS`, `BROLL`, `GRIND`, `EXPORT`, `MESSAGE`, `CTA`): every animation frame from the brief
- `WIGGLE`: camera-wiggle amplitude (2px, rising to 4px in shot 7) and frequency
- Music:
  - `MUSIC_DROP_IN_TRACK_FRAMES`: where the drop sits inside `music.mp3`. It's 633 for the bundled bed (~21.1 s).
  - `MUSIC_DROP_TARGET`: the video frame the drop should hit (660).
  - `MUSIC_OFFSET_FRAMES`: a manual nudge (+ is later, − is earlier).
  - `MUSIC_VOLUME`, `SFX_VOLUME`: levels.

**`src/sfx.ts`**: every sound cue (file, frame, optional length or volume).
**`src/prompts.ts`**: the four prompt texts.

## Structure

```
src/
  index.ts, Root.tsx        composition + detection of optional media (calculateMetadata)
  TwoTimelines.tsx          main composition: panels, wiggle, wipe, one <Sequence> per shot
  theme.ts, timing.ts, sfx.ts, prompts.ts
  shots/Shot01Hook … Shot10Cta.tsx   one component per shot (split shots render the top or bottom half)
  components/               Panel, Label, Timer, StepTag, WhiteCard, ChatCard, Character, ProgressBar,
                            Chip, Check, Note, Grain, HardGrade, Glow, PaperBall, ShotHalf, Soundtrack
  lib/anim.ts               pop / smooth / jerky / typing / fall / noise helpers
```

## Choices where the brief left room or conflicted

- **Bottom step tags** sit under the label (y 1100), so the chat cards start at y 1160. Card text stays inside the y 1080–1500 safe zone. The card backgrounds (e.g. the 920×420 card in shot 3) and the phone mock-up extend below y 1500, but they hold no text there.
- **Card UI text** (the chat bubbles and idea cards) is dark on white, because white text would be invisible on a white card. Every overlay label still follows the white / `#06210F`-on-green rule.
- **Captions landing in the phone** use `#06210F` on green to match the global text rule, instead of white on green.
- **Red accents on the hard side** (the timer, playhead, wavy underline and "12%… still rendering") sit outside the desaturating grade so they stay red.
- **No Claude logo or brand mark** anywhere. The chat uses a plain grey "Claude" text label.
