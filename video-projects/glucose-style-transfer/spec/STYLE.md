# STYLE.md — the reference's style system ("09 Glucose")

## Canvas
1080×1920, **23.976 fps**. Speaker shots at full rate; **every full-screen b-roll page (incl. its text) on twos**.

## Fonts (NCC on ink, rendered in the same Chromium — `spec/_tools/fontcand.js`, `track.js`, `ncc.py`)
| Role | Font | Weight / style | Tracking | NCC |
|---|---|---|---|---|
| Lead-in words (small) | **Outfit** | 300 (400 for pill text / CAPS sub-lines) | **−0.06 em** | 0.92 ("and you have"), 0.81 |
| Accent words | **DM Serif Display** | 400 regular, italic, CAPS | **−0.04 em** | 0.82 (BLOOD), 0.71 (sugars.), 0.72 (sweet), 0.58 (GIVE YOUR BODY) |
| IG card | system UI sans (Outfit 600 used) | 600 handle / 400 stats | 0 | – |
Runner-up rejected: Playfair Display (0.77 / 0.51 / 0.48), Urbanist (0.84 / 0.76), Questrial.

## Typography sizes (px on 1080 wide; % of width)
| Use | Size | % W |
|---|---|---|
| sans lead on speaker | 82-90 | 7.6-8.3 |
| sans lead on b-roll page | 118 | 10.9 |
| sans sub-line (small, under accent) | 60-64 | 5.6-5.9 |
| serif accent on box / CAPS line | 91-132 | 8.4-12.2 |
| serif accent italic hero | 141-243 | 13-22.5 |
| giant title behind speaker | 315 | 29 |

## Palette
| Role | Hex |
|---|---|
| caption white | #fffaf6 |
| cream (serif / underline) | #f9e6c0 |
| cream pill | #fbf1d6 / #fcedda |
| pill ink (on cream) | #825d54 |
| rust (bars, boxes, CAPS titles) | #8f2e1e (title ink #88291d-#8f2f1f) |
| rust dark text | #7e2019 / #721d15 |
| dark-brown box / pill | #4a1c14 (hook) / #441611 |
| orange gradient | #e07a1f → #f6a944 (vertical) ; #f19428 → #f5c84a (horizontal) |
| yellow gradient | #f7e98a → #e9c74a ; pale #f9e2b0 → #e9c27a |
| gold gradient (big word on photo) | #c88d5a → #e9c8a0 → #b07040 |
| peach decoration (?) | #e8b39a |
| b-roll grounds | brown #7b5a52, cream #f1e6c8, grey #eeeeee→#d6d6d6 |
| grey label box | #8a8a8a α0.85 |

## Components (canonical motion — all measured, see S-files)
| # | Component | Motion |
|---|---|---|
| 1 | **wordBlur** (sans word) | blur 10→0 px + opacity 0→1, 4 f power2.out; centred line re-centres circ.out 8 f |
| 2 | **stackRise** | when a line joins, the stack moves up dy +36→0, back.out(1.7) ~10 f |
| 3 | **letterBlur** (serif) | letters L→R, stagger 1.5 f, each blur 14→0 + x −12→0 + opacity, 6 f power2.out |
| 4 | **letterFlicker** (serif CAPS) | letters in random order over 5-6 f, each opacity 0→1 in 1-2 f |
| 5 | **gradient fill** | orange / yellow / gold background-clip text gradients |
| 6 | **boxWipeL** (dark box / rust bar behind word) | scaleX 0→1 from left, 7-10 f power3.out, radius 14 (box) / 0 (bar) |
| 7 | **pillGrowC** (cream or rust pill) | 6 px line at centre → full width, 8-12 f power3.out, text clipped |
| 8 | **maskWipeLR** (dark pill + text together) | clip-path reveal L→R 12 f power2.out |
| 9 | **underline** | 3-4 px line, scaleX 0→1 from left, circ.out 12 f |
| 10 | **lineToBox** | line grows L→R 4 f, then height 6 px → box 6 f power3.out |
| 11 | **drawStroke** (circle / arrow) | stroke-dash 0→100 %, power2.out 12-14 f |
| 12 | **IG profile card** | blur 18→0 + opacity + y +40→0, power2.out 10 f |
| 13 | **? decorations** | 3 serif "?" peach α0.8, ±12°, blur-fade in, float ±6 px |
| 14 | **titleBehind** | giant rust CAPS behind the person (person matte on top), letterFlicker |
| 15 | **labelBox** | grey box appears empty, the word lands inside it |
| 16 | **blur-through transition** | out: blur 0→15-21 px, 6 f power2.in; in: 15-40→0 px, 6-8 f |
| 17 | **cardShrink → carousel** | page scales 1→0.42 in 4 f into a card; cards slide 1/14 f, power3.inOut 8 f |
| 18 | **photo grid pop** | tiles back.out(1.7) 6 f, random order, stagger 1 f, grid −2° |
| 19 | **cut-out page** | object cut-out on flat colour, scale 0.82→1 circ.out 42 f, page rotate 0→−3° |
| 20 | **text-behind-object** | giant word between photo and its own cut-out foreground |

## Camera
- Hook: zoom-out 1.28→1.00 circ.out 50 f. New speaker: zoom-out 1.058→1 sine.out 14.5 f.
- Normal speaker shots: slow push-in ≈ 1.00→1.12 over ~150 f (linear-ish).
- Emphasis: push-in 1.00→1.18 circ.out 32.5 f (with the giant title).
- B-roll pages: slow push-in 1.00→1.04-1.08 linear, cut-out pages also rotate 0→−3°.

## Global rules
- No background panels, no gradients over the footage; the grade is warm peach, untouched.
- Caption page = 1-3 lines: small sans lead + ONE serif accent (box / bar / pill / gradient word / giant title). Page lasts 25-60 f; hard page swaps, **no exits** (exceptions: S17 fade-out 4 f, blur-through between shots).
- Text zone on the speaker: either below the chin (y 1180-1435) or above the head (y 150-560) — never over the face.
- Text appears on the voice: sans words median **0-2 f** before the word, serif accents **6-15 f** before (median lead over all = 5.6 f).
- Speaker 71 % / b-roll 29 %; b-roll comes in blocks of 2-5 pages (2.3-5.3 s), separated by 4-7 s of speaker with frequent page swaps.
