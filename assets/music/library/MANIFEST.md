# Music Library — Your Saved Tracks

Tracks you saved for future edits. Paths are **relative to `assets/`** (e.g. `music/library/ryan-taubert-marvel.mp3`). To use one, copy it into the project's `assets/` and reference it from an `<audio>` element per the render contract.

> ⚠️ **These are NOT royalty-free.** Unlike `music/music-bed-cinematic-tech.mp3` and the `sfx/` kit, most of these are commercial, copyrighted songs or instrumentals (The Weeknd, Lady Gaga, Arctic Monkeys, Steve Lacy, JVKE, etc.).
> - **Baking one into a rendered MP4** can get the post muted, blocked, or demonetized — especially on YouTube Shorts and on business/creator accounts with restricted music libraries.
> - **Safer pattern for trending sounds:** use the track to *time the edit* (sync cuts to its beats), render the video **without** it, and add the same sound in-app on TikTok/Instagram so it's licensed through the platform.
> - **The audio files are gitignored** (this repo is public, and pushing the files would redistribute copyrighted music). Only this manifest is committed. Keep your own copy of the MP3s; drop them back into this folder in a new session.

## Tracks

Vibe/use notes come from what these tracks are generally known for — nobody has listened to every file yet. Confirm by ear before building around one (especially the vocals column).

| File | Track | Length | Vibe | Good for | Vocals? |
|------|-------|--------|------|----------|---------|
| `gibran-alcocer-idea-10.mp3` | Gibran Alcocer — Idea 10 | 2:06 | Soft solo piano, nostalgic | Emotional / reflective edits, storytelling | No |
| `tys-as-time-flies.mp3` | Tys — As Time Flies (special version) | 1:02 | Reflective cinematic piano | Recaps, "a year ago vs now", short emotional beats | No |
| `neheart-reidenshi-snowfall.mp3` | Neheart × Reidenshi — Snowfall | 2:03 | Calm lo-fi, airy | Chill tutorials, calm explainers, study vibe | No |
| `emile-mosseri-jacob-and-the-stone.mp3` | Emile Mosseri — Jacob and the Stone (*Minari* OST) | 1:40 | Warm, wistful, gentle | Personal story, origin story, heartfelt intro | No |
| `joel-sunny-luminary.mp3` | Joel Sunny — Luminary | 3:09 | Ambient, uplifting, cinematic | Inspirational builds, reveals | Check |
| `jvke-golden-hour-instrumental.mp3` | JVKE — golden hour (instrumental) | 3:30 | Romantic piano-pop, uplifting | Feel-good moments, aesthetic montages | No |
| `ryan-taubert-marvel.mp3` | Ryan Taubert — Marvel | 3:26 | Epic neoclassical orchestral, big build | Hype reveals, big announcements, launches | No |
| `will-van-de-crommert-to-concerto-grosso.mp3` | Will Van De Crommert — To Concerto Grosso | 3:48 | Classical / baroque orchestral, elegant | Premium / luxury feel, "sophisticated" edits | No |
| `flawed-mangoes-swimming.mp3` | Flawed Mangoes — Swimming | 3:08 | Motivational, dreamy electronic build | Motivation, grind / progress edits | Check |
| `flawed-mangoes-dramamine.mp3` | Flawed Mangoes — Dramamine | 3:26 | Hazy, dreamy, atmospheric | Aesthetic b-roll, late-night moods | Check |
| `the-weeknd-take-my-breath-instrumental.mp3` | The Weeknd — Take My Breath (instrumental) | 3:40 | 80s synthwave / disco, high energy | Fast-cut hype edits, product showcases | No |
| `the-weeknd-after-hours-instrumental.mp3` | The Weeknd — After Hours (instrumental) | 6:01 | Dark synth, cinematic, slow build | Moody cinematic intros, tension | No |
| `lady-gaga-bloody-mary-x-dum-dum-edit.mp3` | Lady Gaga — Bloody Mary (inst.) × Dum Dum Da-Di-Da (edit audio) | 1:42 | Dark pop, trendy, punchy | Trend edits, transformations, beat-synced cuts | Check |
| `gijuri-scheming-slowed.mp3` | Gijuri — Scheming (slowed instrumental) | 1:12 | Dark, moody, slowed | Sad / dramatic edits, "villain arc" | No |
| `arctic-monkeys-505-instrumental.mp3` | Arctic Monkeys — 505 (instrumental) | 4:10 | Brooding indie rock, builds to a climax | Build-then-drop edits, emotional payoff | No |
| `the-rare-occasions-notion-filtered-instrumental.mp3` | The Rare Occasions — Notion (filtered instrumental) | 3:20 | Driving indie rock, filtered/lo-fi intro | Trendy montages, energetic storytelling | No |
| `steve-lacy-dark-red.mp3` | Steve Lacy — Dark Red (David Dean Burkhart upload) | 2:55 | Lo-fi indie, groovy but melancholic | Aesthetic edits, vibe montages | Likely yes |
| `kehlani-nights-like-this-instrumental.mp3` | Kehlani — Nights Like This (instrumental) | 1:24 | Smooth R&B, late-night | Chill lifestyle, aesthetic edits | No |
| `thee-sacred-souls-will-i-see-you-again.mp3` | Thee Sacred Souls — Will I See You Again? | 4:01 | Vintage soul, warm, nostalgic | Throwbacks, retro-styled edits | Yes |
| `dana-and-alden-dragonfly.mp3` | Dana and Alden — Dragonfly | 5:58 | Mellow jazz, sophisticated | Calm explainers, cafe / lifestyle feel | Check |

## Quick pick — by energy

- **Calm / emotional:** Idea 10, As Time Flies, Snowfall, Jacob and the Stone, golden hour
- **Epic / inspirational:** Marvel, Luminary, Swimming, To Concerto Grosso
- **High-energy / hype:** Take My Breath, Bloody Mary × Dum Dum, Notion
- **Dark / moody:** After Hours, Scheming (slowed), 505, Dramamine
- **Groove / lifestyle:** Dark Red, Nights Like This, Will I See You Again, Dragonfly

## Mixing

Follow the level discipline in `sfx/MANIFEST.md`: music sits **-18 to -24 dB under the voice** in talking-head videos. In faceless or music-only edits the track can be the lead. Most of these are full songs, so trim with `data-media-start` / `data-duration` to the section you want (the drop, the build) instead of starting at 0:00.
