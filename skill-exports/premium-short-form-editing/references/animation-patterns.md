# Animation patterns (P01–P30)

Niche-independent building blocks. Cite the ID in edit-plan options ("P08 graph line"). Colors and fonts come from the brand slots. Durations are typical on-screen times. Build notes are tool-agnostic.

**Default motion vocabulary**
- *Scene settle:* scale 1.06→1 with blur 8px→0 over 0.35s, ease-out. Use it instead of a bare jump cut.
- *Small word in:* opacity with a 14px rise over 0.25s, ease-out. *Hero word in:* scale 0.94→1, blur 6px→0, 0.4s, ease-out.
- *Slow push:* 1.00→1.05 across the shot, linear.
- *Line draw:* stroke reveal (trim path / dash offset), ease in-out.
- *Photo drop:* from −90px, ±14° rotation and 0 opacity, landing over 0.55s with a slight overshoot.

## Captions & text

| ID | Pattern | Duration | Use for | Build notes |
|---|---|---|---|---|
| P01 | **Hero-word caption** | per phrase | Default on the face or b-roll | Phrase pre-laid out; small words above/below the hero; each word revealed at its timestamp; no re-flow. |
| P02 | **Breath card** | 0.5–1.5s | Pause after a big claim | Plain dark or light card, ONE word or short phrase in the emotion font. Nothing else. |
| P03 | **Summary / end card** | 1.5–3s | Endings, key takeaway | Light card; accent-colored emotion-font hero; small ink satellites; hold ≥1s. |
| P04 | **Claim card** | 1–2s | Restating a claim in 4–6 words | Full-bleed accent color, light text, one bold hero. |
| P05 | **Quote card** | ~1.5s | Quotes, turning points | Dark or accent radial background; oversized quotation marks scale in; emotion-font line between them. |
| P06 | **Ghost/echo word** | ~1s | Motion words (faster, backwards, drift) | 3–4 offset copies with falling opacity, sliding. |
| P07 | **Hold one hero word across a montage** | ~3s | A theme word over several clips | The caption stays still while 3–4 clips (0.5–0.8s each) cut underneath. |

## Data & structure

| ID | Pattern | Duration | Use for | Build notes |
|---|---|---|---|---|
| P08 | **Graph line** | 2–3.5s | Growth, decline, "progress" | Faint grid; thin accent line draws and **exits the frame** (implies it continues); a glowing dot rides its head; the number lands big when spoken. |
| P09 | **Big-number card** | 1–2s | A single stat or price | The number in huge bold sans (counts up, or slams in on the word); unit and context small beside it. |
| P10 | **Timeline** | recurring | Ages, years, steps, history | Thin line, ticks, small-caps labels; the marker stays centered while the track slides to the next tick. Reuse it as a semi-transparent overlay on the face so progress stays visible. |
| P11 | **Building list** | 2–4s | 2–4 items | Items appear one by one on the spoken word; earlier items dim to ~40%. |
| P12 | **Comparison split** | 1–3s | A vs B, before/after | Two halves (left/right or top/bottom), a label each, a divider line that draws. |
| P13 | **Diagram draw-on** | 2–4s | Processes, systems, anatomy, floor plans | Thin strokes drawing in sequence with the narration; labels pop at their nodes. |
| P14 | **Kaleidoscope / shard list** | ~4s | Lists of 3 with images | A triangle or shard mask holds an image; it rotates to the next image per item. |

## Callouts & proof

| ID | Pattern | Duration | Use for | Build notes |
|---|---|---|---|---|
| P15 | **Name / object callout** | 1–2s | A named person, product or detail | A ring draws around the target, then a thin curved line to a label: small-caps line plus a name on an accent box that grows left-to-right with the text revealed letter by letter. |
| P16 | **Hand-drawn circle** | ~1.5s | Point at something in a photo | Slightly wobbly ellipse stroke draws around the subject. |
| P17 | **Highlighter sweep on a document** | 3–5s | "Studies show", headlines, contracts | Real screenshot of the source; highlight bars sweep line by line (scaleX from the left). |
| P18 | **Spec / form label** | ~1s | Facts about an object or person | Small-caps label with an accent highlight ("PRICE: £15", "BEDS: 4"). |
| P19 | **Recreated chat / DM / comment** | 2–4s | Audience questions, social proof | Rebuild the UI (never screen-record private accounts); text types out; blurred surroundings. |
| P20 | **Recreated UI / cursor zoom** | 2–4s | Software, websites, apps | Clean screen capture; the virtual camera zooms to where the cursor clicks; shallow blur outside. |

## Images & footage

| ID | Pattern | Duration | Use for | Build notes |
|---|---|---|---|---|
| P21 | **Visual metaphor + hero word** | 0.8–3s | Abstract ideas | Full-bleed image from the niche's cutaway language; slow push; darkened edges; the hero word in the image's empty space. |
| P22 | **Literal b-roll + caption** | 1–3s | Concrete descriptions | B-roll that shows exactly what's said; the caption continues over it. |
| P23 | **Photo collage drop-ins** | 1–3s per photo | Personal stories, first purchases, credentials | White-bordered photos with soft shadows drop in rotated; accent labels in the emotion font. |
| P24 | **Rounded inset footage on dark** | 2–3s | Intimate lines; landscape footage in vertical | Footage in a rounded card at ~90% width (no upscaling needed); text above or below. Great for reusing a landscape crop of the client's footage. |
| P25 | **Reuse client footage as b-roll** | 1–5s | Showing the actual object or place | Pull a moment from elsewhere in the clip (e.g. a close-up of the product), crop out faces, optionally slow to 0.5–0.7× from 60fps sources. |
| P26 | **Punch-in on the key word** | ~0.5s | Emphasis inside a shot | Scale 1.0→1.3–1.6 on the stressed word (scale a wrapper or adjustment layer, not the clip's size). |
| P27 | **Grainy B&W treatment + icon** | 1–3s | Memory, struggle, stopping/starting | Desaturate, contrast up, heavy grain or halftone; an optional play/pause or arrow icon pops on the word. |
| P28 | **Split-screen images** | 0.5–1s | "Multiple areas", variety | 2 images stacked; one caption across the seam. |
| P29 | **Product / cover flick montage** | ~2s | "Everything I've built", collections | Covers or products flick past with a slight tilt and focus blur, quick cuts. |
| P30 | **Light-leak flash** | ~0.5s | Rare rhythm break | Warm gradient with blur. Max once per video. |

## Code-based notes (HTML/GSAP, Remotion, Lottie)

- Captions: one element per word with its start time; show the group over its window; tween each word in at `wordStart − 0.04s`.
- Line draws: SVG path with `strokeDasharray = length`, tween `strokeDashoffset` to 0; for a dot on the line, tween a 0→1 progress and place the dot with `getPointAtLength(progress × length)`.
- Use seeded noise for grain so renders are deterministic. Animate wrappers, never a video element's width or height.
