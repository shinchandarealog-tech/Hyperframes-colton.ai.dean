# Template library: Hook & Captions pack

All 20 templates from the licensed After Effects pack (15 captions, 5 hooks), rendered without
After Effects by `tools/aep_port`. See that folder's README for how the engine works.

## Use a template

1. Look it up in `CATALOG.md` to find its text keys, colours and media slots.
2. Write `texts/<slug>.json`, e.g. `texts/caption03.json`:
   ```json
   {"Text 01/Text": "Most", "Text 02/Text": "buyers", "Text 03/Text": "miss", "Text 04/Text": "this detail",
    "@Control Text 04/Text 04 Color": [0.878, 0.333, 0.227, 1]}
   ```
3. Render:
   ```bash
   python3 render_library.py "Caption 03"
   ```
   Output: `renders/caption03.mov` (transparent ProRes 4444, for dropping over your footage in any editor) and
   `renders/caption03_preview.mp4` (over sample footage). Hooks put `assets/media_porch.mp4` in their
   media slots. Change it in `render_library.py`, or call `tools/aep_port/render.py` directly with
   `--media "Media 01=your_clip.mp4"`.
4. QC: `python3 qc_library.py caption03` runs a frame-to-frame jump check on the graphics and writes a frame
   sheet to `renders/qc/`.

Captions render 3.5 s by default: every entrance has finished by then and the text holds. Pass `--duration` to
`render.py` to change it.

## Notes

- **Fonts.** Neue Haas Grotesk is replaced by Inter Display Bold. Playfair Display (italic, bold italic) is the
  real font, bundled in `tools/aep_port/fonts` under the OFL licence.
- **Template quirks kept as-is:**
  - Caption 08 and Hook 03's last line carry a leftover typewriter expression with no controls. After Effects
    errors on it too and shows the static text.
  - The "7" in Hook 05 deliberately overlaps "Advices".
- **Hook 03 judgement call.** Its six typed lines had chained track mattes that would hide all of them, so those
  mattes are ignored.
- `renders/` and `assets/` are gitignored, and the `.aep` and specs stay private under `_reference/templates/`.
