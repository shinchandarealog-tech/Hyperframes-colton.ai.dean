# aep_port: use After Effects templates without After Effects

Reads an `.aep` project directly, then replays its comps in headless Chromium:
keyframes, the template's own expressions, precomps, text animators, Fill and
Transform effects, and media placeholders. It outputs a transparent ProRes 4444 `.mov`
(drop it over any footage in any editor) plus an MP4 preview.

## Pipeline

```
.aep ──extract.py──▶ spec JSON ──compile_expr.mjs──▶ spec + compiled expressions
                                                          │
             texts.json, media clip, fps, motion blur ───▶ render.py ──▶ out.mov (alpha) + out_preview.mp4
                                                          (player.html + player.js in Chromium)
```

## Steps

```bash
cd _reference/templates/hook-captions
# 1. extract the comps you want (the "Render - …" comps are the deliverables)
python3 ../../../tools/aep_port/extract.py "Hook & Captions for Social Media.aep" specs "Render - Hook 01" "Render - Caption 01"
# 2. make the expressions browser-safe (AE allows array math with + - * /)
node ../../../tools/aep_port/compile_expr.mjs "specs/Render - Hook 01.json"
# 3. render with your text and media
python3 ../../../tools/aep_port/render.py "specs/Render - Hook 01.json" out/hook01 \
    --texts my_hook.json --media "Media 01=clip.mp4" --fps 30 --shutter 180 --bg footage.mp4
```

`texts.json` maps `"<chunk comp>/<layer>"` to new text. Use `\n` for line breaks. Keys starting with
`@` set a control instead: `"@<layer>/<effect>"` sets that effect's first value (a colour, slider or checkbox):

```json
{"Text 01/Text": "This home\nchanged how\nI see\nluxury.", "Text 02/Text": "Let's",
 "@Control Text 03/Text 03 Color": [0.878, 0.333, 0.227, 1]}
```

`video-projects/template-library/CATALOG.md` lists every template's keys, original text, colours and media slots.

Useful flags: `--stills 0.5,1.2` (PNG stills only), `--duration 4` (render fewer seconds),
`--shutter 0` (no motion blur, matches the AE comp setting), `--bg "#101010"`.

## How it stays faithful

- **Expressions run verbatim.** Only `+ - * /` and unary minus are rewritten into vector-aware
  helpers. The AE expression API used by the pack is implemented in `player.js`: `thisComp`,
  `layer()`, `effect()()`, `valueAtTime`, `linear`/`ease`, `clamp`, `timeToFrames`, `textIndex`,
  `seedRandom`/`random`, and so on. If an expression throws, the property falls back to its static
  value, which is what After Effects does too.
- **Keyframes.** Linear, hold, and bezier temporal ease (speed and influence), per dimension or
  along the path.
- **Text animators.** Range selectors (square, ramp up, ramp down, triangle, ease high/low) and
  expression selectors, based on characters, words or lines. Supports position, scale,
  rotation, opacity, blur and fill colour.
- **Essential Properties.** Overrides flow from the parent layer into the precomp's
  control effects.
- **Shape layers.** Groups, rectangles (with roundness), fill, stroke (with dashes), offset paths and group
  transforms. Items switched off in AE (eyeball / fx switch) stay off.
- **Track mattes.** Alpha and inverted alpha. A matte layer can be hidden or visible, and matted layers can
  matte others.
- **Effects.** Fill, Transform, Fast Box Blur, Glow (approximate), Linear Wipe. Effects that spread
  (blur, glow) get padded buffers so they are not clipped at the layer edge.
- **Expression extras.** `text.sourceText` (typewriter, number counter), `key()` / `nearestKey()` / `numKeys`,
  `content()` lookups on shape groups, `thisLayer.parent`, `sourceRectAtTime` (tight glyph bounds for text,
  path bounds for shapes).
- **Auto-fit.** Word chunks widen (and grow taller only if glyphs would be cut) to fit new text,
  keeping their alignment. Chunks that share a row reflow with the template's gaps, and rows
  are scaled to stay inside a 6% safe area.

## Known gaps and judgement calls

- **Chained mattes are ignored.** In Hook 03, six copies of a typewriter line are each matted by the layer
  above, starting with a media layer that isn't on screen yet. Taken literally, every copy would be invisible,
  so a matte whose matte layer is itself matted is skipped. Every other matte is honoured.
- **Glow is approximate.** It's a blurred halo behind the layer. AE's threshold and colour options are not modelled.
- **Fonts.** Neue Haas Grotesk Display is Adobe Fonts only. `FONT_MAP` in `player.js` substitutes
  Inter Display Bold. If you have the real font file, install it and change `FONT_MAP`.
- **Unused features.** Layer masks, luma mattes, blend modes other than normal, 3D layers, bezier shape paths,
  ellipses and `wiggle()` are not implemented, because none of the 20 templates use them.
- **Licence.** The `.aep` and the extracted specs are licensed content. They are gitignored and
  must stay private.
