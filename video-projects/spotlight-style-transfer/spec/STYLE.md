# STYLE.md — reference "You're not competing on price." (@aslaniedits)

Source measured: ONE still frame (720x1280, upscaled x1.5 to 1080x1920 for measuring).
All px are on the 1080x1920 canvas. Tools: spec/_tools/measure_ref.py, font_ncc.py, font_calib.js, script_calib.js.

## What a still CAN'T give us (marked ESTIMATED everywhere it is used)
- cuts / cadence (CUTS.md), motion curves + timings (S01.md), camera moves, SFX/music (AUDIO.md).
- These are exposed as live controls in the builder with premium defaults (skill rule 6). They get
  replaced with measured numbers as soon as the reference VIDEO is supplied.

## Palette (measured hex)
| role | hex | where measured |
|---|---|---|
| accent yellow (crosses, dot) | #F7F64E (big + #FAFA47, small + #F5F652) | connected components, H 20-40 |
| script yellow (antialiased ink mean) | #E4E85E → use #F2F24E core | "competing" |
| small line white | #E3E3E2 | "You're not" ink mean |
| big word | vertical gradient #FFFFFF → #EDEDED (45%) → #A0A0A0 (100%) | per-row p10 224 → 146 |
| background | #070707-#0A0A0A (A-roll's own black; untouched) | |
| glass card fill | white ≈ 5-7% (bg 8 → card 17-27 luma) | |
| glass card rim | white ≈ 10% 1.5 px + bottom inner glow 15 px (luma 35-38) | |
| notch pill | #FFFFFF solid | |

## Typography (calibrated in Chromium, NCC vs reference ink)
| line | font | weight | size px | % of W | tracking | NCC |
|---|---|---|---|---|---|---|
| small line ("You're not", "on") | Inter Tight (Helvetica Neue look-alike) | 300 | 65.8 | 6.1% | -0.08em | 0.878 / 0.861 |
| script accent ("competing") | Italianno | 400 | 127 | 11.8% | 0 | 0.801 (next best 0.419) |
| big word ("price") | Inter Tight | 600 | 203.6 | 18.9% | -0.06em | 0.891 |
| period after big word | yellow circle Ø24 px, 11 px after last glyph, sitting on baseline | | | | | |

## Layout at rest (reference)
- Text block centred on x≈540 (line1 ink 407-647, big word 332-730+dot 741-765).
- Baselines: line1 480, script/"on" line 553, big word 720.  Gaps: 73 / 167.
- Script word + small word share a baseline; small word follows the script with ~13 px gap.
- Glass card: x 229-852, y 223-1163 (623 x 940), radius ≈ 98 px. Speaker sits IN FRONT of it
  (suit luma 4 inside card < card 24) → needs a person matte.
- Notch pill: x 472-607, y 258-289 (135 x 31, r 15.5), centre x 540.
- Crosses (rounded "+", bars with round caps, rotated ≈ -22°):
  big Ø100 thick 41.5 @ centre (852,628) | mid Ø48 thick 20.4 @ (232,428) | tiny Ø22 thick 11.6 @ (323,841)
  → thickness = 0.42 x size, always.
- Cursor: white rounded-triangle arrow 48x44 at (865,202), pointing up-left, soft white glow.
- Spotlight cone from top (part of the footage, not a graphic).

## Rules derived
- Accent system per page: ONE small line + ONE script word (yellow) + ONE big metallic word with yellow dot.
- Everything else is decoration from the same kit: 3 crosses (big/mid/tiny), cursor, card + notch.
- Text sits ABOVE the speaker's head (in the dark empty space under the spotlight), never on the face.
- Our A-roll framing: hair top y≈640 (ref ≈705) → whole layout shifts -80 px (builder: "Layout Y").
- IG safe zone x 84-900, y ≤ 1520: the reference's big cross (to 915) and cursor (to 913) are pulled
  inside to ≤ 900 in our build.
