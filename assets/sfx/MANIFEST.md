# SFX + Music Library — Asset Index

Source: Pixabay (CC0-equivalent — free commercial use, no attribution) for the original kit, and Mixkit (Mixkit Sound Effects Free License — free commercial use, no attribution) for the expansion pack. Both are safe for monetized TikTok + Instagram.

All paths below are **relative to `assets/`** so they match `<audio src="...">` values when a Hyperframes project symlinks or copies this folder.

## Quick pick — by purpose

| Moment in video | Best SFX | Path | Duration |
|-----------------|----------|------|----------|
| Scene cut / whip transition | whoosh | `sfx/transitions/whoosh.mp3` | 0.57s |
| Whip transition, airy & short (peak ~0.7s) | whoosh-03 | `sfx/transitions/whoosh-03.mp3` | 1.96s |
| Whip transition, quick (peak ~0.74s) | whoosh-06 | `sfx/transitions/whoosh-06.mp3` | 2.30s |
| Whip transition (peak ~0.87s) | whoosh-07 | `sfx/transitions/whoosh-07.mp3` | 2.56s |
| Whip transition (peak ~0.96s) | whoosh-05 | `sfx/transitions/whoosh-05.mp3` | 2.12s |
| Whip transition, loudest/punchiest (peak ~1.0s) | whoosh-01 | `sfx/transitions/whoosh-01.mp3` | 2.67s |
| Whip transition, longer swell (peak ~1.11s) | whoosh-02 | `sfx/transitions/whoosh-02.mp3` | 2.41s |
| Soft/subtle whoosh, under-the-voice (peak ~0.89s, quiet) | whoosh-04 | `sfx/transitions/whoosh-04.mp3` | 2.85s |
| Big cinematic whoosh into a title / reveal (peak ~0.48s) | cinematic-whoosh | `sfx/cinematic/cinematic-whoosh.mp3` | 2.95s |
| Side-to-side swipe transition | swipe | `sfx/transitions/swipe.mp3` | 1.06s |
| Digital/tech transition, data reveal | glitch | `sfx/transitions/glitch.mp3` | 2.64s |
| Hard snap on a beat drop | hard-cut | `sfx/transitions/hard-cut.mp3` | 0.20s |
| Button press, caption reveal, UI action | click | `sfx/ui/click.wav` | 0.46s |
| Emoji / sticker / bubble pop-in | pop | `sfx/ui/pop.mp3` | 0.72s |
| iMessage/Slack-style ping | notification | `sfx/ui/notification.mp3` | 0.50s |
| Text typing on screen | keyboard-typing *(loop — see note)* | `sfx/ui/keyboard-typing.mp3` | 19.59s |
| Hit-enter / send-prompt beat | send-message | `sfx/ui/send-message.mp3` | 1.06s |
| Quick electric punctuation / chip pop-in | zap | `sfx/ui/zap.mp3` | 0.92s |
| "Wrong way" / pre-AI / fail beat | error | `sfx/ui/error.mp3` | 2.55s |
| Logo slam, title stamp, emphatic hit | slam | `sfx/impact/slam.mp3` | 1.22s |
| Cinematic intro punch | boom | `sfx/impact/boom.mp3` | 2.78s |
| Musical emphasis stab on a key word | stinger | `sfx/impact/stinger.mp3` | 5.63s |
| Sub-bass drop after a reveal lands | bass-drop | `sfx/impact/bass-drop.mp3` | 1.10s |
| Building tension into reveal | riser | `sfx/cinematic/riser.mp3` | 4.03s |
| "AI activates" / energizing build | power-up | `sfx/cinematic/power-up.mp3` | 2.00s |
| Text glint / "wow" / magic moment | sparkle | `sfx/cinematic/sparkle.mp3` | 2.04s |
| List item / page turn / reveal | paper-flip | `sfx/cinematic/paper-flip.mp3` | 2.61s |
| Room tone under tech/server visuals | ambient-hum *(loopable)* | `sfx/ambient/ambient-hum.mp3` | 62.85s |
| Darker tech drone bed | tech-drone *(short — repeat or crossfade)* | `sfx/ambient/tech-drone.mp3` | 10.03s |
| Music bed under a full video | cinematic-tech | `music/music-bed-cinematic-tech.mp3` | 122.91s |

> **More music:** a saved library of 20 copyrighted tracks (not royalty-free; see licensing notes) is indexed in `music/library/MANIFEST.md`.

## Usage notes + gotchas

- **`hard-cut.mp3` was trimmed** from the original 8s (which had 7.8s of dead air tail) down to 0.2s with the snap hitting at ~23ms. Drop it in with `data-duration="0.2"` and it'll fire cleanly on the beat. The untrimmed source is kept alongside as `hard-cut.original.mp3` in case you ever want to re-trim differently.
- **Creator whoosh pack (`whoosh-01`…`whoosh-07`, `cinematic-whoosh`)** — supplied by the creator from their own Google Drive. Each whoosh builds up *before* its loudest point, so **start the audio clip ≈ peak-time earlier than the cut** (e.g. a cut at 4.0s with `whoosh-05` → `data-start="3.04"`). Peak times are in the quick-pick table. Rotate through the seven so back-to-back cuts don't sound identical. `whoosh-04` is ~10 dB quieter than the rest, so it fits under speech. `cinematic-whoosh.mp3` was trimmed: 1.0s of silence removed from the start, the tail cut at 2.9s with a 0.2s fade. The untrimmed source is `cinematic-whoosh.original.mp3`. (The Drive folder had two copies of the cinematic whoosh with identical audio, so only one was kept.)
- **`keyboard-typing.mp3` is a ~20s continuous loop** of fast laptop keys. For typing that lasts N seconds, set `data-start` where the typing begins and `data-duration` to match the typing length — the mixer will truncate naturally. Pair with `<audio>` not `<video>`.
- **`click.wav` is WAV** (uncompressed, ~80KB). All other SFX are MP3. Hyperframes' mixer handles both — no conversion needed.
- **Loopable beds**: `ambient-hum.mp3` (62.85s) and `music-bed-cinematic-tech.mp3` (122.91s) are long enough to cover most shorts without a loop seam being audible. For videos longer than the bed's duration, crossfade a second copy at `(duration - 1s)` with a 1s overlap.
- **Level discipline**: SFX should sit **-12 to -18 dB under the speaking voice**, music bed **-18 to -24 dB under**. Mix the voice as loudest element — never let SFX or music fight the user's speech.
- **No double-hits**: on a single beat, pick ONE SFX (e.g. whoosh OR slam, not both). Layering is for specific craft moments, not every cut.


## Creator starter kit — `sfx/kit/`

93 sounds the creator picked themselves. They come from the Drive folder `sound effect important 2.0` plus the 10 sounds from a second Drive link, which were extracted from .mp4 to .mp3. Names were cleaned to kebab-case, and the original filename is noted in `library/catalog.json` (`kit` field). One exact duplicate was dropped: `Loading - Sound Effect.mp3` is identical to `number-increasing.mp3`.

**Use these before reaching for the full Drive library.**

### transitions/ — whooshes, swooshes, whips, glitch, flash

`bass-whoosh.mp3` 2.86s · `deep-whoosh.mp3` 3.7s · `fast-glitch-1.mp3` 1.06s · `fast-swoosh.mp3` 0.56s · `fast-whip.wav` 1.6s · `fast-whoosh.mp3` 0.48s · `flash.mp3` 1.9s · `fly-by.mp3` 3.53s · `low-whoosh.mp3` 1.94s · `slow-down.mp3` 2.33s · `swoosh-short-2.mp3` 0.36s · `swoosh-short-3.mp3` 0.24s · `swoosh-short.mp3` 0.29s · `whoosh-main.wav` 0.31s

### impact/ — hits, smashes, bass, snaps, blasts

`bomb-blast.mp3` 6.6s · `brick-hit.mp3` 0.22s · `crack-crunch-celery.mp3` 0.6s · `dart-hard-hit-board-2.mp3` 0.34s · `dart-hard-hit-board.mp3` 0.39s · `deep-bass.mp3` 1.18s · `gun-clock.mp3` 2.16s · `impact-glass-smash.mp3` 1.42s · `impact-mirror-smash.mp3` 1.59s · `impact-pickaxe-2.mp3` 0.22s · `impact-pickaxe.mp3` 0.72s · `impact.wav` 2.85s · `ink-splash.mp3` 1.39s · `iron-man-blaster.mp3` 1.04s · `knife-scrape.mp3` 0.46s · `metallic-hit.mp3` 2.38s · `neck-break.mp3` 0.46s · `snap.mp3` 0.26s

### risers/ — build-ups and risers into a reveal

`buildup.mp3` 2.66s · `charge.mp3` 2.47s · `gear-riser.mp3` 2.38s · `number-increasing.mp3` 18.42s · `riser-3.mp3` 2.32s · `riser-base.mp3` 7.31s · `riser-question.mp3` 3.21s · `riser.mp3` 3.31s · `suspense-riser.mp3` 1.8s

### ui/ — clicks, pops, beeps, dings, notifications, camera, pen

`adding-machine.mp3` 0.27s · `alarm-beep.mp3` 0.39s · `apple-notification.mp3` 0.99s · `arcade-game-coin.mp3` 0.65s · `beep-sound.mp3` 2.57s · `beep.mp3` 0.15s · `bell-4.mp3` 2.6s · `button-mechanical-2.mp3` 0.1s · `button-mechanical-3.mp3` 0.1s · `button-mechanical.mp3` 0.27s · `camera-shutter.mp3` 0.34s · `camera.mp3` 0.42s · `chime-hit-bell.mp3` 0.94s · `chime-synth-high.mp3` 0.22s · `click-07.wav` 0.5s · `click-09.wav` 0.5s · `click-15.wav` 0.5s · `click-sequence-2.mp3` 0.25s · `click-sequence.mp3` 17.11s · `da-digital-click-1.mp3` 0.58s · `da-digital-click-2.mp3` 0.53s · `da-digital-click-8.mp3` 0.36s · `ding.mp3` 0.55s · `discord-join.mp3` 2.95s · `discord-leave.mp3` 2.38s · `elevator-bell-ding.mp3` 2.02s · `fairy-magic-sparkle.wav` 1.3s · `highlighter-marker.mp3` 11.11s · `iphone-receive.wav` 0.79s · `iphone-send.wav` 0.66s · `mouse-click-2.mp3` 0.37s · `mouth-pop.mp3` 0.15s · `multimedia-beep-2.mp3` 0.15s · `multimedia-beep-3.mp3` 0.15s · `multimedia-beep.mp3` 0.12s · `pen-click.mp3` 0.48s · `pop-2.mp3` 1.78s · `pop-loud.mp3` 0.17s · `pop-low.mp3` 0.15s · `radio-beep.mp3` 0.46s · `sfx-1.wav` 0.98s · `sfx-2.mp3` 1.27s · `sfx-3.mp3` 0.58s · `sfx-4.mp3` 4.0s · `snd-start.wav` 0.51s · `snd-stop.wav` 0.5s · `ui.wav` 0.08s

### foley/ — real-world texture (crowd, heels, clock wind)

`alarm-clock-wind-2.mp3` 0.82s · `alarm-clock-wind.mp3` 1.11s · `crowd-cheer-in-school-auditorium.mp3` 17.04s · `high-heels.mp3` 0.27s · `insect-claw-grab.mp3` 0.34s

Gotchas: `ui/click-sequence.mp3` (17s) and `ui/highlighter-marker.mp3` (11s) are long takes, so set a short `data-duration`. `risers/number-increasing.mp3` (18s) is a counting/loading loop that you trim to the counter's length. `foley/crowd-cheer-in-school-auditorium.mp3` is 17s.

## Full creator library — `sfx/pack/`, `sfx/reel-pack/`, `music/<genre>/`

The creator's whole pack is in the repo with duplicates removed: **5251 SFX** in 73 categories (`pec-premium/` = UI-heavy premium pack, `sfx/pack/whoosh/`, `glitch/`, `cinematic-hub/`, `risers/`, `notifications/`, `meme-sfx/`…), **39 reel-cut SFX** (`sfx/reel-pack/`), and **391 music tracks** across 28 genres (`music/motivational/`, `music/mystery/`, `music/reel-bgm/`…). All MP3. See `library/README.md` for the category list and full track list, and `library/catalog.json` to search by name, including original filenames.

## Folder structure (actual)

```
assets/
├── sfx/
│   ├── transitions/    whoosh.mp3  swipe.mp3  glitch.mp3  hard-cut.mp3
│   │                   whoosh-01.mp3 … whoosh-07.mp3  (creator pack)
│   ├── ui/             click.wav   pop.mp3    notification.mp3  keyboard-typing.mp3
│   │                   send-message.mp3  zap.mp3  error.mp3
│   ├── impact/         slam.mp3    boom.mp3   stinger.mp3   bass-drop.mp3
│   ├── cinematic/      riser.mp3   sparkle.mp3  paper-flip.mp3  power-up.mp3
│   │                   cinematic-whoosh.mp3  (creator pack)
│   ├── ambient/        ambient-hum.mp3  tech-drone.mp3
│   ├── kit/            creator starter kit — transitions/ impact/ risers/ ui/ foley/  (93 files)
│   ├── pack/           full creator SFX pack, 73 category folders (5251 files, incl. pec-premium/)
│   ├── reel-pack/      39 SFX cut from a pack-preview reel
│   └── MANIFEST.md     (this file)
├── music/              music-bed-cinematic-tech.mp3 + <genre>/ folders (391 tracks)
├── library/            catalog.json + duplicates-removed.json + README.md — index of the full library
└── _inbox/             (staging — empty after sort)
```

## Expanding the library

To add more SFX later:
1. Search Pixabay at `https://pixabay.com/sound-effects/search/<term>/`
2. Download to `~/Downloads/` with a descriptive filename
3. Drop it in `assets/_inbox/` (or leave in Downloads — the assistant can find it)
4. Tell the assistant what it is ("add a glass-shatter SFX I just downloaded") and it'll sort + index + update this manifest.

License:
- Pixabay assets — Pixabay Content License (free commercial use, no attribution required).
- Mixkit assets (`keyboard-typing`, `send-message`, `zap`, `error`, `stinger`, `bass-drop`, `power-up`) — Mixkit Sound Effects Free License (free commercial use, no attribution required, cannot be redistributed as a standalone sound pack).
- Creator whoosh pack (`whoosh-01`…`whoosh-07`, `cinematic-whoosh`) — supplied by the creator from their own Google Drive; the creator is responsible for confirming usage rights.
