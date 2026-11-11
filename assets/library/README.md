# Creator audio library

The creator's full SFX + music pack (from their Google Drive), **imported into the repo, with duplicates removed**: 5251 SFX in `assets/sfx/pack/`, 39 SFX cut from a pack-preview reel in `assets/sfx/reel-pack/`, and 391 music tracks in `assets/music/<genre>/`.

- `catalog.json`: every file with its `path` (relative to `assets/`), `dur` (seconds), and `orig` (the original filename in the Drive pack).
- `duplicates-removed.json`: the 717 files that were skipped as duplicates, and which kept file each one matches.

**Check the curated sets first:** `assets/sfx/MANIFEST.md` (quick-pick table + the creator's starter kit in `sfx/kit/`). Dig into `sfx/pack/` when you need something specific.

## Finding a sound

```bash
ls assets/sfx/pack/                       # categories
ls assets/sfx/pack/whoosh/                # browse one
grep -i 'cash' assets/library/catalog.json  # search names (current + original)
```

Copy the file into the project's `assets/` and reference it from an `<audio>` element.

## How it was built

- Source: the Drive folder's one-click zip (6,134 audio files), plus the 10 sounds from the second link and the reel from the third link. The Drive folders are listed in git history (`assets/library/catalog.json` before this import).
- **Format:** WAV / AIFF / FLAC / M4A / MP4 were converted to **MP3 320 kbps**. MP3s were copied as-is. Names are kebab-case.
- **Duplicates removed (717):** exact copies, the same file under a different name (very common in this pack, e.g. SoundSnap vs Epidemic vs `@adobebasics` re-uploads), and the same recording with a different trim or fade. Each candidate was confirmed by comparing waveforms. Different takes of similar sounds (`gear-metal-459` vs `460`, `typewriter-2` vs `3`) were **kept**.
- **PEC Premium SFX.zip** (added later): 278 sounds → 226 imported into `sfx/pack/pec-premium/`. 52 were duplicates: 33 were already in the library and 19 were repeated inside the pack.
- Not imported: 2 corrupt files (`Beep/BeepShort_S011SF.148.mp3`, `Percussion/MultimediaPercussive_S011TE.681.mp3`, which don't decode in the source), Sound Forge `.sfk` peak files, `.DS_Store`, and a tutorial video (`Everything You Need to Know About Sound Design in 2025!`).

## SFX pack categories (`assets/sfx/pack/`)

| Folder | Files |
|---|---|
| `action-sound` | 83 |
| `alarm-chime` | 31 |
| `ambience` | 15 |
| `animals` | 53 |
| `arcade-noises` | 9 |
| `beep` | 183 |
| `bell` | 56 |
| `bugs` | 37 |
| `build-up` | 7 |
| `button` | 272 |
| `camera` | 38 |
| `chime` | 227 |
| `cinematic-hub` | 206 |
| `clicks` | 22 |
| `clock` | 7 |
| `construction-tools` | 48 |
| `crowd-people` | 7 |
| `digital` | 24 |
| `electric` | 31 |
| `epic-cinematic-trailer-impact-pack-2` | 5 |
| `error` | 2 |
| `esfx` | 10 |
| `evolve-audio-essential-transitions-free` | 6 |
| `explosions` | 24 |
| `fart` | 18 |
| `feeling` | 6 |
| `fire-fireworks` | 27 |
| `firearms` | 20 |
| `food` | 8 |
| `fw-sounds` | 30 |
| `games` | 14 |
| `gear` | 147 |
| `glitch` | 86 |
| `hits` | 45 |
| `horn` | 16 |
| `i-phone` | 5 |
| `keyboard-mouse` | 46 |
| `knife` | 3 |
| `liquid` | 5 |
| `logo-animation` | 5 |
| `mechanical` | 10 |
| `meme-sfx` | 64 |
| `miscellaneous` | 5 |
| `money` | 9 |
| `musical` | 92 |
| `negative` | 355 |
| `notifications` | 260 |
| `other` | 1048 |
| `paper-sound-effects` | 20 |
| `pen-click` | 5 |
| `percussion` | 213 |
| `pec-premium` | 226 (PEC Premium SFX: UI, notifications, cash, wink, games, whooshes, risers, all-use) |
| `phone` | 1 |
| `pitched` | 24 |
| `pop` | 6 |
| `positive` | 93 |
| `ringtones` | 58 |
| `risers` | 23 |
| `sci-fi` | 117 |
| `shining` | 3 |
| `sports` | 2 |
| `swishes` | 15 |
| `switch` | 168 |
| `swoosh` | 28 |
| `tone` | 18 |
| `transition-sound-effects` | 135 |
| `ui-sound` | 29 |
| `vehicles` | 56 |
| `vibes` | 6 |
| `water` | 42 |
| `whoosh` | 168 |
| `wind` | 24 |
| `wooshes` | 44 |

`pitched/` holds key-matched ping-booms and deep-breath risers (one per musical key). Use the one that matches the music bed's key.

## Reel pack (`assets/sfx/reel-pack/`)

Cut from a 48s pack-preview reel. Each label on screen was matched to its sound, and silence was trimmed. **⚠ = cut from a stretch where sounds overlap, so it may carry a little bleed from the neighbouring sound.** Prefer a `sfx/pack/` equivalent for hero moments.

`bloop-cartoon.mp3` 0.21s · `bubble-pop-2.mp3` ⚠ 1.36s · `bubble-pop.mp3` 0.44s · `camera-click.mp3` 0.24s · `camera-flash.mp3` 1.41s · `camera-rec.mp3` ⚠ 1.15s · `camera-shutter.mp3` 1.57s · `camera-transition.mp3` ⚠ 1.25s · `cash-register.mp3` 0.81s · `click-1.mp3` 0.91s · `click-2.mp3` 0.18s · `click-3.mp3` 0.18s · `click-glitch.mp3` ⚠ 1.25s · `clock-ticking.mp3` ⚠ 0.99s · `deep-riser.mp3` ⚠ 1.25s · `digital-counting.mp3` 0.81s · `ding.mp3` ⚠ 1.25s · `echo.mp3` ⚠ 1.25s · `evoy.mp3` 0.34s · `film-burn.mp3` ⚠ 1.25s · `gear-up.mp3` 0.6s · `marker.mp3` 0.89s · `mechanical-gear-up.mp3` ⚠ 1.44s · `mechanical-keyboard.mp3` ⚠ 1.07s · `message.mp3` 0.34s · `ni-interface.mp3` 0.89s · `ni-soft-ui.mp3` 0.97s · `overlay-switch.mp3` ⚠ 1.25s · `phill.mp3` 0.63s · `riser.mp3` ⚠ 1.25s · `slice.mp3` 0.73s · `soft-gear-up.mp3` 1.07s · `tick.mp3` 1.02s · `typing.mp3` 0.55s · `ui-6.mp3` 0.91s · `ui-bubble-pop.mp3` 0.1s · `ui-click.mp3` 0.24s · `ui-pop.mp3` 0.63s · `yt-click.mp3` 0.18s

## Music (`assets/music/<genre>/`)

### adventure (29)

- `andalucia-max-ll-musicbed-licensed.mp3` — 3:38
- `es-a-fly-on-the-wall-raymond-grouse.mp3` — 1:52
- `es-a-million-upheavals-edgar-hopp.mp3` — 2:46
- `es-a-true-hero-edgar-hopp.mp3` — 3:59
- `es-across-the-ocean-bonnie-grace.mp3` — 2:07
- `es-allegiances-hampus-naeselius.mp3` — 2:13
- `es-apollo-dream-cave.mp3` — 2:21
- `es-can-t-dampen-my-spirit-adriel-fair.mp3` — 2:27
- `es-conquest-dragon-tamer-1.mp3` — 2:39
- `es-crank-it-sage-oursler.mp3` — 2:02
- `es-crusaders-adriel-fair.mp3` — 1:43
- `es-forever-to-run-howard-harper-barnes.mp3` — 2:34
- `es-globetrotter-adriel-fair.mp3` — 2:03
- `es-highland-hymn-bonnie-grace.mp3` — 3:08
- `es-keep-close-to-the-guide-philip-ayers.mp3` — 2:21
- `es-knight-s-templar-adriel-fair.mp3` — 1:34
- `es-look-see-max-anson.mp3` — 1:52
- `es-medieval-adventure-bonnie-grace.mp3` — 2:01
- `es-peacekeepers-dream-cave.mp3` — 2:06
- `es-plains-of-illeyneth-dragon-tamer.mp3` — 3:13
- `es-playing-with-thunder-max-anson.mp3` — 2:01
- `es-ropes-away-adriel-fair.mp3` — 1:43
- `es-skilled-in-the-arts-yi-nantiro.mp3` — 2:13
- `es-the-eye-of-the-storm-edward-karl-hanson.mp3` — 1:55
- `es-the-traveller-christoffer-moe-ditlevsen.mp3` — 2:53
- `es-truce-no-more-dream-cave.mp3` — 1:56
- `es-valley-of-drakes-dragon-tamer.mp3` — 2:02
- `es-victory-theme-max-anson.mp3` — 2:05
- `galway-clover-by-c-k-martin-artlist.mp3` — 2:59

### alternative (26)

- `big-shot-instrumental-irontom-musicbed-licensed.mp3` — 3:39
- `call-me-the-west-irontom-musicbed-licensed.mp3` — 3:15
- `cheers-by-rex-banner-artlist.mp3` — 1:56
- `es-a-most-violent-man-lofive.mp3` — 3:00
- `es-baby-don-t-care-mike-stringer.mp3` — 1:51
- `es-cassandra-i-really-know-you-marc-torch.mp3` — 1:44
- `es-illusion-instrumental-version-coma-svensson.mp3` — 2:53
- `es-just-say-when-the-grateful-7.mp3` — 1:56
- `es-smokey-goodbye-modal-youth.mp3` — 2:27
- `es-stay-true-instrumental-version-lars-eriksson.mp3` — 3:32
- `es-the-end-of-me-gaillardia.mp3` — 2:46
- `es-the-whole-nine-yards-another-notion.mp3` — 1:59
- `es-we-re-not-the-same-good-song-audio-extracted-1.mp3` — 0:01
- `es-we-re-not-the-same-good-song.mp3` — 2:15
- `filthy-instrumental-moony-musicbed-licensed.mp3` — 2:39
- `full-moon-instrumental-irontom-musicbed-licensed.mp3` — 3:12
- `keep-movin-along-no-lead-vocals-by-milano-artlist.mp3` — 2:08
- `let-em-talk-instrumental-lone-waves-musicbed-licensed.mp3` — 3:06
- `loverboy-instrumental-irontom-musicbed-licensed.mp3` — 3:38
- `never-wanted-your-love-instrumental-nevada-wild-musicbed-licensed.mp3` — 3:23
- `perfect-day-for-a-party-by-custommelody-artlist.mp3` — 1:51
- `rush-hour-by-dan-zeitune-artlist.mp3` — 2:31
- `the-gemberzee-instrumental-lovedrug-musicbed-licensed.mp3` — 3:34
- `way-back-when-before-instrumental-version-by-con-davison-artlist.mp3` — 3:45
- `well-keep-running-instrumental-version-by-to-the-valley-artlist.mp3` — 2:51
- `when-a-dickhead-dies-instrumental-irontom-musicbed-licensed.mp3` — 2:50

### ambient (30)

- `boot-sequence-by-jimmy-svensson-artlist.mp3` — 1:56
- `es-a-closer-look-charles-holme.mp3` — 2:00
- `es-and-behold-awlee.mp3` — 4:09
- `es-atlas-light-farrell-wooten.mp3` — 2:21
- `es-cold-war-games-gabriel-lewis.mp3` — 2:21
- `es-detector-max-anson.mp3` — 1:46
- `es-digital-future-christoffer-moe-ditlevsen.mp3` — 2:18
- `es-divine-comedy-oh-the-city.mp3` — 3:11
- `es-enter-the-realm-of-shadows-christoffer-moe-ditlevsen.mp3` — 3:02
- `es-feeling-new-max-anson.mp3` — 1:58
- `es-floating-variables-isaac-larson.mp3` — 0:33
- `es-forest-sunrise-marten-moses.mp3` — 1:50
- `es-formations-van-sandano.mp3` — 3:26
- `es-in-cinemas-pulsed.mp3` — 1:55
- `es-in-obscurity-lies-the-gate-christoffer-moe-ditlevsen.mp3` — 2:46
- `es-leaving-traces-gettz-g.mp3` — 2:29
- `es-path-to-the-abyss-christoffer-moe-ditlevsen.mp3` — 2:42
- `es-tension-2-fredrik-ekstrom.mp3` — 1:42
- `es-thirty-fourth-window-heath-cantu.mp3` — 1:46
- `es-trembling-anticipation-dream-cave.mp3` — 1:57
- `es-true-stories-farrell-wooten.mp3` — 1:46
- `father-son-makeup-and-vanity-set-musicbed-licensed.mp3` — 7:14
- `fearful-continuity-by-josh-mccausland-artlist-1.mp3` — 2:14
- `first-try-by-neon-ridge-artlist.mp3` — 4:00
- `free-radicals-by-stanley-gurvich-artlist.mp3` — 4:41
- `into-the-storm-no-drums-by-ian-post-artlist.mp3` — 2:24
- `k-i-t-t-vs-k-a-r-r-by-ian-post-artlist.mp3` — 1:21
- `mayhem-by-ian-post-artlist.mp3` — 1:25
- `the-harvest-by-dan-mayo-artlist.mp3` — 5:03
- `unknown-darkness-by-jimmy-svensson-artlist.mp3` — 3:40

### chamber-music (11)

- `es-a-delightful-evening-francis-wells.mp3` — 1:32
- `es-a-swallow-s-escape-fabien-tell.mp3` — 1:36
- `es-errands-fabien-tell.mp3` — 1:41
- `es-highest-gear-brightarm-orchestra.mp3` — 1:35
- `es-life-in-pieces-howard-harper-barnes.mp3` — 3:10
- `es-refined-enlightenment-howard-harper-barnes.mp3` — 2:23
- `es-rememberance-fabien-tell-1.mp3` — 1:35
- `es-sudden-escape-brightarm-orchestra.mp3` — 1:43
- `es-we-must-be-prepared-brightarm-orchestra.mp3` — 1:53
- `immaterial-by-anbr-artlist.mp3` — 4:10
- `run-with-the-wolves-by-ardie-son-artlist.mp3` — 2:04

### classical (15)

- `es-a-brand-new-sunset-modern-version-joe-e-lee.mp3` — 2:12
- `es-agrumes-ch-ntarelle.mp3` — 2:48
- `es-fly-baby-fly-fabien-tell.mp3` — 1:39
- `es-kinderszenen-op-15-no-1-a-curious-story-traditional.mp3` — 1:52
- `es-paidias-pledge-golden-anchor.mp3` — 2:30
- `es-run-and-hide-philip-ayers.mp3` — 2:04
- `es-suite-bergamasque-l-75-iii-clair-de-lune-intro-traditional.mp3` — 2:08
- `es-the-barber-of-seville-traditional.mp3` — 1:42
- `es-the-farewell-serenade-howard-harper-barnes.mp3` — 2:02
- `es-the-nutcracker-op-71-th-14-act-2-no-12d-trepak-russian-dance-traditional.mp3` — 1:05
- `es-william-tell-overture-traditional.mp3` — 1:05
- `farewell-by-maya-belsitzman-matan-ephrat-artlist.mp3` — 1:56
- `rain-by-anbr-artlist.mp3` — 2:19
- `the-day-before-by-maya-belsitzman-matan-ephrat-artlist-1.mp3` — 1:48
- `this-way-by-biba-dupont-artlist.mp3` — 1:42

### clock-timed (3)

- `es-abandoned-houses-wendel-scherer.mp3` — 1:54
- `es-in-timely-manner-guy-copeland.mp3` — 1:49
- `es-it-is-set-wendel-scherer.mp3` — 1:58

### drones (4)

- `es-did-they-lose-us-experia.mp3` — 1:50
- `es-hidden-output-ethan-sloan.mp3` — 1:43
- `es-natural-cause-ethan-sloan.mp3` — 1:45
- `es-radiant-shore-cobby-costa.mp3` — 1:59

### drum-n-bass (8)

- `es-catrine-power-druid.mp3` — 2:37
- `es-monologue-splasher.mp3` — 2:25
- `es-now-agst.mp3` — 2:49
- `es-paradigm-raccy.mp3` — 3:08
- `es-paralysed-agst.mp3` — 3:53
- `es-wanna-go-back-squiid.mp3` — 2:51
- `es-you-give-me-feelings-house-of-say.mp3` — 3:30
- `es-zanobi-catiso.mp3` — 2:39

### eccentric (36)

- `es-a-cradle-song-mary-riddle.mp3` — 2:25
- `es-a-faint-touch-ethan-sloan.mp3` — 1:52
- `es-afternoon-tea-galore-magnus-ringblom.mp3` — 1:56
- `es-afternoon-tea-in-polynesia-3-martin-gauffin.mp3` — 2:15
- `es-appeased-soundscape-03-august-wilhelmsson.mp3` — 2:04
- `es-beach-grave-dj-denz-the-rooster.mp3` — 3:46
- `es-caught-in-the-net-jon-bjork.mp3` — 1:34
- `es-cinematic-latin-flavours-2-magnus-ringblom.mp3` — 2:09
- `es-coconut-monkey-anders-ekengren.mp3` — 1:32
- `es-crossing-states-3-magnus-ringblom.mp3` — 2:13
- `es-dangerous-fling-alexandra-woodward.mp3` — 2:15
- `es-dizzy-mind-stationary-sign.mp3` — 2:02
- `es-duck-confit-alexandra-woodward.mp3` — 2:05
- `es-festive-riot-harper-rey.mp3` — 2:03
- `es-goofy-moments-17-magnus-ringblom.mp3` — 2:01
- `es-hangover-weekend-stationary-sign.mp3` — 2:11
- `es-high-heels-walkabout-1-magnus-ringblom.mp3` — 1:53
- `es-latin-orchestra-2-magnus-ringblom.mp3` — 2:07
- `es-lawnmower-trouble-stationary-sign.mp3` — 2:06
- `es-mambo-lounge-9-martin-gauffin.mp3` — 2:21
- `es-mario-paint.mp3` — 1:52
- `es-national-anthem-sweden-8-traditional.mp3` — 1:42
- `es-odd-coincidence-kikoru.mp3` — 2:06
- `es-playful-mischief-josef-falkenskold.mp3` — 1:50
- `es-second-toe-to-the-left-3-peter-sandberg.mp3` — 1:57
- `es-sneaking-into-the-kitchen-arthur-benson.mp3` — 2:04
- `es-the-juice-jam-arthur-benson.mp3` — 2:54
- `es-the-king-of-thieves-christoffer-moe-ditlevsen.mp3` — 2:29
- `es-the-kook-marc-torch.mp3` — 2:12
- `es-tiptoeing-2-valdemar-hansen.mp3` — 2:08
- `es-tongue-twister-white-bones.mp3` — 1:58
- `es-trainee-day-stationary-sign.mp3` — 2:04
- `es-whacky-theater-4-magnus-ringblom.mp3` — 2:01
- `es-whimsical-and-playful-2-gavin-luke.mp3` — 2:20
- `es-wives-club-4-gunnar-johnsen.mp3` — 2:16
- `es-work-these-shoes-medite.mp3` — 2:12

### experimental (15)

- `boom-clap-instrumental-chair-model-musicbed-licensed.mp3` — 2:40
- `chocolate-brownie-instrumental-version-by-ian-post-artlist.mp3` — 3:11
- `drift-instrumental-peached-musicbed-licensed.mp3` — 3:30
- `entertain-you-instrumental-bronze-radio-return-musicbed-licensed.mp3` — 3:37
- `es-dot-real-heroes.mp3` — 2:14
- `ganga-sun-instrumental-version-by-omri-smadar-artlist.mp3` — 5:22
- `healthier-instrumental-moony-musicbed-licensed.mp3` — 2:33
- `hey-you-instrumental-chair-model-musicbed-licensed.mp3` — 2:29
- `hot-for-a-min-instrumental-version-by-captain-qubz-artlist.mp3` — 2:59
- `id-rather-cry-instrumental-version-by-jane-the-boy-artlist.mp3` — 2:56
- `nonsense-by-raw-artlist.mp3` — 3:24
- `poolside-retreat-by-marc-robillard-artlist.mp3` — 1:32
- `rue-de-jaffa-instrumental-version-by-a-m-beef-artlist.mp3` — 3:30
- `we-the-ones-with-oohs-ahhs-instrumental-mf-graves-musicbed-licensed.mp3` — 3:11
- `what-ya-want-instrumental-hipz-musicbed-licensed.mp3` — 2:28

### extra (1)

- `es-accident-scene-sfx-producer.mp3` — 0:45

### funk (3)

- `es-my-rama-dama-doo-sven-lindvall.mp3` — 4:04
- `es-rain-checking-ote.mp3` — 3:18
- `es-the-setup-gerhard-feng.mp3` — 1:54

### funny (32)

- `cat-walk-by-roie-shpigler-artlist.mp3` — 1:51
- `es-a-dolphin-serenade-josef-bel-habib.mp3` — 2:03
- `es-bathtub-ballpoint.mp3` — 2:33
- `es-be-nice-twice-mac-taboel.mp3` — 2:03
- `es-becoming-mr-bossa-redeemin.mp3` — 2:05
- `es-bird-watching-justnormal.mp3` — 2:15
- `es-bop-it-jules-gaia.mp3` — 2:50
- `es-bringing-the-groove-arthur-benson.mp3` — 2:04
- `es-bubble-bee-the-fly-guy-five.mp3` — 2:07
- `es-feeling-alright-gavin-luke.mp3` — 2:17
- `es-flying-pillows-mike-franklyn.mp3` — 1:53
- `es-go-after-them-harry-edvino.mp3` — 2:01
- `es-i-could-stay-forever-modern-version-joe-e-lee.mp3` — 2:07
- `es-incidental-encounter-arthur-benson.mp3` — 2:26
- `es-it-s-not-me-arthur-benson.mp3` — 2:01
- `es-jubilation-jules-gaia.mp3` — 3:19
- `es-mama-swing-lucas-pittman.mp3` — 2:52
- `es-midnight-swing-jules-gaia.mp3` — 2:18
- `es-muffin-cuffin-martin-klem.mp3` — 2:01
- `es-people-falling-down-arthur-benson.mp3` — 2:29
- `es-simple-pleasantries-arthur-benson.mp3` — 2:10
- `es-skipping-class-birdies.mp3` — 2:08
- `es-the-director-stationary-sign.mp3` — 2:16
- `es-when-the-final-bell-rings-mike-franklyn.mp3` — 1:50
- `es-wild-slide-jules-gaia.mp3` — 2:51
- `es-yellow-light-arthur-benson.mp3` — 2:10
- `low-puddles.mp3` — 1:47
- `on-the-tip-of-my-toes-by-roie-shpigler-artlist.mp3` — 2:24
- `quick-party-before-the-end-of-the-world-by-francesco-dandrea-artlist.mp3` — 2:03
- `the-kings-parade-by-francesco-dandrea-artlist.mp3` — 2:24
- `wag-the-tail-by-roie-shpigler-artlist.mp3` — 2:14
- `white-russian-rag-by-the-bottlesnakes-artlist.mp3` — 2:52

### happy (14)

- `es-a-tiny-tumble-josef-falkenskold.mp3` — 2:08
- `es-african-food-truck-sahara-skylight.mp3` — 1:58
- `es-day-at-the-fair-the-fly-guy-five.mp3` — 1:51
- `es-dime-a-dozen-esme-cruz.mp3` — 1:54
- `es-forest-bugs-stationary-sign.mp3` — 2:02
- `es-in-the-name-of-z-real-heroes.mp3` — 1:47
- `es-pigeons-on-a-train-harry-edvino.mp3` — 3:12
- `evermore-feat-jordan-critz-roary-musicbed-licensed.mp3` — 4:09
- `flight-hannah-parrott-musicbed-licensed.mp3` — 3:14
- `lie-in-the-sun.mp3` — 2:29
- `march-of-toys.mp3` — 2:46
- `oasis-by-milano-artlist.mp3` — 2:10
- `temptation-instrumental-version-by-ride-free-artlist.mp3` — 2:39
- `wannabe-instrumental-version-by-g9-artlist.mp3` — 3:03

### jazz (3)

- `es-common-language-vendla.mp3` — 4:37
- `es-eye-hara-noda.mp3` — 3:30
- `es-yurei-sugoi.mp3` — 5:36

### jungle (7)

- `energetic-percussion-by-infraction-no-copyright-drum-music-the-rhythm.mp3` — 0:49
- `es-encountering-the-unknown-zauana.mp3` — 2:20
- `es-hidden-and-ready-zauana.mp3` — 2:13
- `es-in-the-amazonas-kikoru.mp3` — 2:02
- `es-snake-trails-experia.mp3` — 2:07
- `es-through-deep-forests-experia.mp3` — 1:31
- `es-when-warriors-align-zauana.mp3` — 2:30

### master-plan (5)

- `come-in-instrumental-kaina-musicbed-licensed.mp3` — 5:34
- `continent-by-anbr-artlist.mp3` — 1:28
- `jane-austens-fight-club-steven-gutheinz-musicbed-licensed.mp3` — 3:00
- `solving-puzzles-alistair-sung-musicbed-licensed.mp3` — 2:59
- `tv-drama-theme.mp3` — 1:40

### motivational (17)

- `avengers-artlist.mp3` — 4:15
- `es-and-the-sky-shall-unfold-1-johannes-bornlof.mp3` — 2:21
- `es-army-of-angels-edgar-hopp.mp3` — 2:22
- `es-dungeon-dream-cave.mp3` — 2:32
- `es-first-shooter-bonnie-grace.mp3` — 2:04
- `es-on-a-hunt-philip-ayers.mp3` — 2:01
- `es-one-last-battle-edgar-hopp.mp3` — 2:23
- `es-power-squad-adriel-fair.mp3` — 2:05
- `es-roaming-the-island-adriel-fair.mp3` — 1:34
- `es-tense-excitement-1-johannes-bornlof.mp3` — 2:05
- `es-termination-1-johannes-bornlof.mp3` — 1:36
- `es-termination-2-johannes-bornlof.mp3` — 1:49
- `es-the-crew-adriel-fair.mp3` — 1:40
- `es-treasure-hunter-5-johannes-bornlof.mp3` — 2:10
- `es-unstoppable-3-johannes-bornlof.mp3` — 1:40
- `es-watchdogs-jo-wandrini.mp3` — 2:18
- `vortex-by-shahead-mostafafar-artlist.mp3` — 2:37

### mystery (17)

- `es-ancient-discoveries-gabriel-lewis.mp3` — 3:20
- `es-backdoor-exit-max-anson.mp3` — 2:04
- `es-carabiner-max-anson.mp3` — 1:52
- `es-commando-max-anson.mp3` — 2:15
- `es-desert-mirage-colors-of-illusion.mp3` — 1:54
- `es-destiny-unfolds-max-anson.mp3` — 2:05
- `es-detective-work-v-v-campos.mp3` — 2:19
- `es-electric-spark-sight-of-wonders.mp3` — 1:40
- `es-follow-every-move-radio-night.mp3` — 2:03
- `es-in-the-outskirts-of-buenos-aires-harper-rey.mp3` — 2:00
- `es-mysterious-madeleine-lucas-pittman.mp3` — 2:02
- `es-mystery-box-stationary-sign.mp3` — 1:58
- `es-mystical-tension-dream-cave.mp3` — 2:31
- `es-nothing-can-conquer-us-now-christian-andersen.mp3` — 1:47
- `es-private-detective-ch-ntarelle.mp3` — 3:06
- `es-the-unveiling-christoffer-moe-ditlevsen.mp3` — 3:31
- `es-through-space-and-time-etienne-roussel.mp3` — 2:08

### other-music (28)

- `late-night-snack-gunnar-olsen.mp3` — 3:19
- `mixkit-aggressive-beast-roar-13.mp3` — 0:01
- `mixkit-big-fire-spell-burning-1332.mp3` — 0:04
- `mixkit-cinematic-drama-anticipation-795.mp3` — 0:10
- `mixkit-cinematic-glass-hit-suspense-677.mp3` — 0:04
- `mixkit-cinematic-orchestra-chaos-639.mp3` — 0:04
- `mixkit-cinematic-transition-swoosh-heartbeat-trailer-488.mp3` — 0:08
- `mixkit-cinematic-tunnel-reverb-woosh-1486.mp3` — 0:06
- `mixkit-classic-alarm-995.mp3` — 0:05
- `mixkit-clock-countdown-bleeps-916.mp3` — 0:05
- `mixkit-crickets-and-insects-in-the-wild-ambience-39.mp3` — 0:26
- `mixkit-eating-crispy-cookies-122.mp3` — 0:16
- `mixkit-epic-orchestra-transition-2290.mp3` — 0:07
- `mixkit-fast-small-sweep-transition-166.mp3` — 0:00
- `mixkit-game-show-suspense-waiting-667.mp3` — 0:41
- `mixkit-keyboard-typing-1386.mp3` — 0:26
- `mixkit-light-rain-loop-2393.mp3` — 0:15
- `mixkit-little-birds-singing-in-the-trees-17.mp3` — 0:08
- `mixkit-rain-and-thunder-storm-2390.mp3` — 0:29
- `mixkit-sad-game-over-trombone-471.mp3` — 0:05
- `mixkit-swallowing-a-water-drink-in-the-throat-150.mp3` — 0:02
- `mixkit-tick-tock-clock-timer-1045.mp3` — 0:16
- `mixkit-vacuum-swoosh-transition-1465.mp3` — 0:02
- `new-tires-silent-partner.mp3` — 2:06
- `not-for-nothing-otis-mc-donald.mp3` — 1:58
- `shoulder-closures-gunnar-olsen.mp3` — 2:38
- `the-charmer-s-call-hanu-dixit.mp3` — 2:26
- `tropic-fuse-french-fuse.mp3` — 1:49

### pop (20)

- `anthem-of-a-quirky-hipster-by-rex-banner-artlist-1.mp3` — 1:00
- `better-than-ever-instrumental-lady-bri-musicbed-licensed.mp3` — 3:18
- `breaking-out-instrumental-prty-anml-musicbed-licensed.mp3` — 2:50
- `es-being-nostalgic-flyin.mp3` — 2:21
- `es-don-t-bore-me-alberto-harry-edvino.mp3` — 2:25
- `es-mexican-standoff-walt-adams.mp3` — 1:54
- `es-new-dawn-is-rising-instrumental-version-stonekeepers.mp3` — 2:58
- `es-new-location-flyin.mp3` — 2:55
- `es-silver-bullet-elliot-holmes.mp3` — 1:59
- `es-slap-act-white-bones.mp3` — 2:06
- `es-upbeat-electronic-pop-indie-pop-version-gavin-luke.mp3` — 1:44
- `es-zoot-suit-elliot-holmes.mp3` — 1:44
- `freewheel-by-rex-banner-artlist-1.mp3` — 1:28
- `i-feel-free-instrumental-jamie-lono-musicbed-licensed-1.mp3` — 3:04
- `i-got-it-instrumental-juliet-roberts-musicbed-licensed.mp3` — 2:03
- `locktup-instrumental-version-by-lone-wild-artlist.mp3` — 3:51
- `move-your-body-by-rocknstock-artlist-1.mp3` — 2:00
- `ready-to-go-instrumental-louis-ii-musicbed-licensed.mp3` — 3:47
- `solid-gold-instrumental-goldenface-musicbed-licensed.mp3` — 2:11
- `work-feat-kvlvnv-instrumental-cass-xq-musicbed-licensed.mp3` — 2:43

### quirky (5)

- `es-extra-fries-the-fly-guy-five.mp3` — 2:00
- `es-healthy-throat-martin-landstrom.mp3` — 2:55
- `es-how-to-tango.mp3` — 2:22
- `es-out-of-order-the-fly-guy-five.mp3` — 1:50
- `es-when-the-cats-away-the-fly-guy-five.mp3` — 1:57

### reel-bgm (15)

- `caleb-arredondo-feeling-blue.mp3` — 1:47
- `echo-sax-end-looped-by-caleb-arredondo.mp3` — 5:05
- `flawed-mangoes-dramamine-visualizer.mp3` — 3:25
- `kendrick-lamar-instrumental-eduardo.mp3` — 4:35
- `le-monde.mp3` — 2:14
- `lindsey-stirling-carol-of-the-bells-official-music-video.mp3` — 3:06
- `mary-j-blige-family-affair-instrumental.mp3` — 3:35
- `nightcrawler-instrumental.mp3` — 1:00
- `ogryzek-empire-slowed.mp3` — 1:55
- `ogryzek-glory-slowed-reverb.mp3` — 2:29
- `sae4-elveda.mp3` — 2:46
- `synthwave-goose-blade-runner-2049.mp3` — 3:48
- `until-i-found-you-stephen-sanchez-em-beihold-karaoke-version.mp3` — 3:06
- `vj-x-narvent-memory-reboot-slowed.mp3` — 3:56
- `whats-app-video-2025-05-07-at-3-21-03-pm-1.mp3` — 2:45

### retro (8)

- `a-moon-walk-instrumental-version-by-yehezkel-raz-artlist.mp3` — 8:26
- `do-you-instrumental-kena-musicbed-licensed.mp3` — 2:18
- `es-agent-getaway-elliot-holmes.mp3` — 1:45
- `es-bubble-beam-soara.mp3` — 1:56
- `es-kind-of-real-soara.mp3` — 2:08
- `es-megapixel-lasse-lyx.mp3` — 2:05
- `lemon-popsicle-by-randy-sharp-artlist.mp3` — 2:03
- `starsky-by-alex-keren-artlist.mp3` — 3:39

### sad (21)

- `calm-mind-feat-harshini-iyer-no-lead-vocals-by-prashant-naidu-artlist.mp3` — 4:39
- `domine.mp3` — 5:08
- `es-a-common-memory-trevor-kowalski.mp3` — 2:59
- `es-a-whisper-in-the-dark-gavin-luke.mp3` — 2:19
- `es-burned-letters-johannes-bornlof.mp3` — 3:01
- `es-can-you-hear-me-breathing-tides.mp3` — 1:52
- `es-ether-jakob-ahlbom.mp3` — 3:09
- `es-exile-lo-mimieux.mp3` — 2:35
- `es-like-home-jakob-ahlbom.mp3` — 2:34
- `es-miss-everything-instrumental-version-mindme.mp3` — 2:58
- `es-onthou-ever-so-blue.mp3` — 2:08
- `es-sad-news-emily-rubye.mp3` — 2:09
- `es-secrets-of-the-earth-lama-house.mp3` — 2:24
- `es-shadowman-s-waltz-franz-gordon.mp3` — 2:42
- `es-spring-queen-dew-of-light.mp3` — 2:53
- `es-stay-wide-open-instrumental-version-loving-caliber.mp3` — 3:46
- `es-valleys-harbours-oceans.mp3` — 3:05
- `es-whisper-of-the-pines-howard-harper-barnes.mp3` — 2:24
- `life.mp3` — 3:27
- `the-bannered-mare.mp3` — 2:30
- `winter.mp3` — 3:18

### samba (13)

- `es-balcony-music-timothy-infinite.mp3` — 2:08
- `es-bateria-brasileira-redeemin.mp3` — 2:07
- `es-heist-music-nightcap.mp3` — 2:52
- `es-music-box-rachel-meyer.mp3` — 1:39
- `es-samba-amigo-tiki-tiki.mp3` — 2:06
- `es-samba-del-sol-el-equipo-del-norte.mp3` — 2:58
- `es-samba-no-pe-ruben-cortes.mp3` — 2:07
- `es-samba-party-tiki-tiki.mp3` — 2:06
- `es-samba-piano-el-equipo-del-norte.mp3` — 3:23
- `es-samba-triste-instrumental-version-clara-mendes.mp3` — 3:08
- `es-samba-vibes-riverworn.mp3` — 2:00
- `es-the-music-box-ave-air.mp3` — 3:17
- `es-turtleneck-music-sarah-the-illstrumentalist.mp3` — 2:11

### spy (4)

- `cant-stop-with-oohs-ahhs-instrumental-reagan-james-musicbed-licensed.mp3` — 3:08
- `es-a-deal-with-the-devil-white-bones.mp3` — 1:49
- `es-spy-spring-gang.mp3` — 2:57
- `meidum-spy-action-detective.mp3` — 2:23

### suspense (1)

- `es-charged-alec-slayne.mp3` — 2:01
