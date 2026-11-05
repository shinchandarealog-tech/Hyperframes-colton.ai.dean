# My Watch Story — build notes

35.8 s total (35.3 s footage + 0.5 s last-frame hold), 1080x1920, 60 fps. Shot at y 656–1264.

## Camera cuts (measured, kept as hard cuts)
2.333 (A→B) · 12.767 (B→A) · 22.133 (A→B) · 26.433 (B→A)

## Hits, snapped to the audio (onsets + silence gaps; whisper alone drifted up to 1 s)
| Beat | Hit | Time |
|---|---|---|
| 02 | "abroad" flight path | 3.05 |
| 02 | "watch roll" ring + label | 5.58 |
| 03 | "eight" dot 1 | 9.95 |
| 03 | "first Timex" card | 11.82 |
| 04 | "£15" price tag | 12.98 |
| 04 | "Argos" map pin | 14.58 |
| 05 | 14 X's + ticks | 16.80 → 18.10 |
| 06 | "18" dot 2 | 20.32 |
| 06 | "first Rolex" card + glint | 21.27 / 21.55 |
| 07 | counter 0 → 50, "+" and dot 3 | 22.2 → 24.95 |
| 08 | punch 125% + ring | 27.2 / 27.3 |
| 08 | "favorite" line | 27.86 |
| 08 | PATEK PHILIPPE / Nautilus / 5711R | 29.42 / 30.42 / 30.98, fade 32.2 |
| 09 | "one watch" big 1, dot 4, underline | 33.38 / 33.42 / 33.52 |
| 09 | "this" punch 135% + glint ping | 34.90 |

## Burned-in lower third
The raw footage carries the old "PATEK PHILIPPE NAUTILUS" two-bar lower third from 28.0 to 32.55 s,
in source y ≥ 900 px. The 125% punch-in uses transform-origin 0 0, so the visible window is source
y 0–864 and the old bars never show. The zoom eases back out at 32.6 s, after they've gone.

## Caption note
Three Whisper passes (small, segment, medium) hear "on the wrist **at my** moment". The captions
say "at the moment", as the brief suggests. Listen at ~27.0 s to confirm.

## v2 — 3D rebuild
Real 3D (three.js r147, `assets/scene3d.js`, HDRI-lit PBR, rendered on `#gl` over the shot):
spinning Timex (leather strap) and Rolex (fluted bezel, Oyster links) in their cards, 3D plane on a
3D dotted flight path, torus rings round the watch roll and the lifted 5711R (ring keyframes measured
from the rendered footage), swinging extruded price tag with 3D "£15", lathed rose-gold map pin with one
bounce, extruded Playfair counter 0→50 + "+", ten spinning mini watches, extruded "1".
2.5D: header words flip up, timeline stands up from flat and dots spin when lit, cards swing in on a
hinge, calendar cells flip, captions tilt up. Argos logo (Simple Icons) under the pin; 5711R photo
(cropped from the footage) on the Patek card. Look unchanged: white + one rose-gold accent.
Assets and licences: see CREDITS.md.
