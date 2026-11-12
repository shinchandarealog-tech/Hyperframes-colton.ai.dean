# CUTS.md — reference "09 Glucose.mp4"

**Basics (ffprobe):** 1080×1920, **23.976 fps (24000/1001)**, 788 frames = 32.87 s, AAC stereo. Mix −14.2 LUFS.
**Method:** per-frame mean-abs-diff + 8³ RGB histogram correlation on 270×480 cache, full/top/bottom halves (`spec/_tools/cuts.py`, data `an/ref_diff.json`).

## Cadence (measured)
- Speaker shots: every frame new (true 23.976 fps).
- **All full-screen b-roll pages, including their text, update on TWOS** (new picture on every 2nd frame → 11.99 fps). Diff pattern `.X.X.X…` in 105-159, 311-353, 423-549. Copy this: b-roll segments are rendered with `stepF(f)=f-(f%2)`.

## Shot table
| # | first | last | t (s) | len f | type | content | in-transition | graphics |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 62 | 0.00 | 62 | speaker A | podcast guest (host) | – | IG profile card, sans words, GLUCOSE serif on dark box, OVERWHELMING orange gradient |
| 2 | 63 | 104 | 2.59 | 42 | speaker B | main guest | hard cut | IG profile card (2nd person), "so glucose is your body's" + "Energy" yellow italic; ends with blur-out f99-104 |
| 3 | 105 | 127 | 4.38 | 23 | b-roll still (cut-out on brown) | brain | blur-in f105-110 | "all of our" + BRAINS cream pill |
| 4 | 128 | 159 | 5.34 | 32 | b-roll still (product photo) | sugar cubes, light | hard cut | "are using" + giant gradient "glucose" BEHIND cubes + "to think" |
| 5 | 160 | 310 | 6.67 | 151 | speaker B | | hard cut | pages S05-S08 (hard page swaps at 203, 241, 269) |
| 6 | 311 | 353 | 12.97 | 43 | b-roll still (photo) | bowl + fork, shadow | hard cut | grey label box, "foods", "contain" serif, drawn circle |
| 7 | 354 | 422 | 14.76 | 69 | speaker B | | hard cut | carbs bar; TWO CATEGORIES pill; blur-out f417-422 |
| 8 | 423 | 440 | 17.64 | 18 | b-roll still (photo) | spoons of flour | blur-in f423-429 | "STARCHES" engraved serif; page shrinks to card f437-441 |
| 9 | 441 | 498 | 18.39 | 58 | b-roll carousel | bread / pasta / rice / potatoes cards | card-shrink | italic serif labels above cards, slide left |
| 10 | 499 | 524 | 20.81 | 26 | b-roll cut-out diagram | sugar cubes on light grey | hard cut | "and then sugars." + 4 italic labels |
| 11 | 525 | 549 | 21.90 | 25 | b-roll grid | 3×3 dessert photos, tilted | hard cut | "so anything sweet" |
| 12 | 550 | 714 | 22.94 | 165 | speaker B | | hard cut | S16-S18; push-in f692-714; blur-out f709-714 |
| 13 | 715 | 788 | 29.82 | 74 | speaker B (2nd angle) | | blur-in f715-723 | "and that's where THE GLUCOSE gets brought to all of our cells" |

**Screen time:** speaker 563 f = 71 %, b-roll 225 f = 29 %. Longest speaker stretch 165 f (6.9 s) + 74 f — carried by caption pages that swap every 1.1-2.2 s.
**False cuts dropped:** 126 (page zoom), 203/246-248/268-274/599-603 (fast hand motion), 425-437/443-493 (b-roll on twos).
