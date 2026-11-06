# Reel Editor (tap-to-edit)

A touch-first editor for any project in `video-projects/`. It works on an iPad, an Android phone or a laptop.

```bash
npm install                                                   # once, from the workspace root
npm run editor -- video-projects/<project>                    # opens on port 3010
npm run editor -- video-projects/<project> --port 4000
node scripts/editor/server.mjs video-projects/<project> --apply   # re-write saved edits into index.html
npm run test:editor -- <copy-of-a-project>                    # touch test (iPad + Android emulation). It WRITES to the project, so run it on a copy.
```

## How it fits the existing pipeline

- **Preview:** the editor plays the project's real `index.html` with Hyperframes' own player and runtime (`node_modules/hyperframes`), the same engine `npx hyperframes render` uses.
- **Saving:** every change is saved two ways:
  - `edit-data/edits.json` holds the list of edits plus each piece of text's original words.
  - `index.html` gets a managed `<style id="hf-edits">` block between `hf-editor:start/end` markers, and changed words are written straight into the element.
  - Studio preview and render read `index.html`, so the export matches the editor.
- **No layout fights:** move, resize and rotate use the CSS `translate`, `scale` and `rotate` properties, and opacity uses `filter: opacity()`. These stack on top of GSAP animations, which write `transform` and `opacity`, instead of replacing them.
- **Fonts:** picking a font copies the font file into `assets/fonts/`, so the preview and the render use the same file.
- **Rebuilt `index.html`:** if Claude regenerates a project's `index.html`, run `--apply` to put your edits back. Keys are element ids, or a child path like `#hook > :nth-child(1)` for things without an id.

## Using it

| Do this | To |
| --- | --- |
| Tap a caption, title, sticker or graphic | Select it (blue box with handles). Playback pauses. |
| Drag it with one finger | Move it. It snaps to the safe-zone edges and the centre lines (pink guide). |
| Drag a corner, or pinch with two fingers | Resize it. Pinching also turns it if you twist. |
| Drag the ⟳ handle | Rotate it. It snaps at 0°, 45°, 90° and so on. |
| Double-tap text, or tap ✎ Text | Type new words in place. Tap "Done typing" when finished. |
| Use the floating panel | Change font, size, colour, bold, outline, shadow and opacity, or delete the item. Reset clears its position and style. |
| Tap ▣ Safe zone | Show Meta's safe area (top 14%, bottom 35%, sides 6%). Anything outside it gets a red box. |
| Tap ↶ / ↷ | Undo or redo any edit, including deletes and text changes. |
| Pinch on empty space | Zoom the preview. Drag with one finger to pan. ⤢ Fit resets the view. |

Keyboard shortcuts (bonus): Ctrl/⌘+Z undo, Shift+Ctrl/⌘+Z or Ctrl+Y redo, Delete removes the item, arrow keys nudge it (Shift for 10 px), Enter edits text, Space plays or pauses, Esc deselects.
