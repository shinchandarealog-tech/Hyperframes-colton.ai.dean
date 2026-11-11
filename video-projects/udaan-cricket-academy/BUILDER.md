# Udaan Reel Builder

Live, editable reel builder for this project. What you see in the builder is what renders.

```bash
cd video-projects/udaan-cricket-academy
node builder/server.cjs 3010        # → http://localhost:3010
```

- **Timeline strip** (bottom): every beat, coloured by scene. Click to jump.
- **Per beat**: ≥3 headline designs + ≥4 motion-graphic accents (cards), headline text,
  shot motion, transition in, footage source / in-point / framing, split-screen layout.
- **Pacing**: change a cut point, *Split at playhead* (faster cuts), *Merge with next*.
- **Save & update render** writes `edit-data/beats.json` (previous version kept in
  `edit-data/history/`) and regenerates `index.html`.

Files:
- `builder/designs.js` — the design engine (designs, accents, motions, transitions). Shared by builder + render.
- `edit-data/beats.json` — the edit (source of truth).
- `scripts/build_index.cjs` — beats.json → index.html (also run by Save).

## Artifact version (claude.ai)
Published at https://claude.ai/artifact/NKTtsCnpRS5f3ey6WvpiJQ — same engine, proxy footage (≤540px).
Its **Save** writes the edit to the artifact database (`edits/current`); Claude pulls it into
`edit-data/beats.json` and regenerates `index.html`. Rebuild the page: `node scripts/build_artifact.cjs <outDir>`
(proxies must be in `<outDir>/assets/`).
