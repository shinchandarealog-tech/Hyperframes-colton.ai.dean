# STORYBOARD — "Strip It Down" (Bauhaus explainer)

**Format:** 9:16 Reel, 1080×1920, 25fps · **Length:** ~34s (31.06s clean cut + 3s outro hold)
**Concept:** The video starts out ornate and ends up Bauhaus. The edit acts out the script: decoration comes off, function stays.
**Source:** `assets/talking-head-cut.mp4`. This is a 1216×2160 vertical crop of the 4K raw with every retake and pause removed. Cut list is at the bottom.

## Visual system

| | Act 1 — ORNATE (0–6.4s) | Act 2+ — BAUHAUS (6.4s → end) |
|---|---|---|
| Palette | sepia, oxblood, antique gold `#B8913A` | cream paper `#F2EBDD`, black `#111`, red `#E1251B`, yellow `#F5C400`, blue `#1F4E9C` |
| Type | Playfair Display italic + UnifrakturMaguntia (blackletter) | Futura-style geometric sans (Jost 700/900, uppercase, tight) |
| Frame around speaker | gilded baroque picture frame on damask wallpaper | plain black rectangle → circle/square crops on a strict grid |
| Grade | warm sepia, vignette, heavy grain | clean, neutral, light grain only |
| Motion | slow, floaty, ornamental easing (`sine`) | snappy, mechanical (`expo.out`, `steps`), objects snap to the grid |

**Colors carry meaning:** red = what got removed (decoration, craft) · blue = function / the rule · yellow = impact / today · black = structure.
**Captions:** Hinglish in Roman script, exactly as spoken. Jost 700, black `#111` on a flat yellow block (a Bauhaus "label"), 2–3 words per chunk. One color for the whole video. They sit just below the chin, inside the safe area (y ≤ 1250). They need the block because they sit over his white hoodie.

## Beat sheet (timestamps are in the cut timeline)

| # | Time | VO | Screen | Motion / transition | SFX |
|---|---|---|---|---|---|
| 1 | 0.0–1.0 | "1919 mein…" | **HOOK.** He's inside a gilded baroque frame on damask wallpaper, sepia grade. A giant blackletter **"1919"** fills the top third. | Frame 0 is already full, no fade-in. Slow 3% push-in. Dust motes drift. | gramophone crackle bed |
| 2 | 1.0–2.2 | "…Germany mein ek school shuru hua tha" | Small serif label "Weimar, Germany" swings in on a gold chain. A1 (workshop B-roll) plays as a vintage photo inside a second small ornate frame. | Gentle pendulum swing (`sine.inOut`). | soft chime |
| 3 | 2.2–3.0 | "—**Bauhaus**." | **THE CRACK.** A single flat **red circle** punches through the damask wall behind him and the wallpaper tears around it. **BAUHAUS** stamps in Jost 900, the only clean thing in an ornate frame. | Hard stamp, 2-frame shake. A foreshadow: the future breaking into the old world. | paper punch + low thud |
| 4 | 3.0–4.6 | "The idea was simple: art aur design…" | Split card: **ART** (ornate serif, left) and **DESIGN** (geometric, right), with a thick gold line between them. | The words slide in from opposite sides. | — |
| 5 | 4.6–6.4 | "…ke beech ki line hata do." | On "hata do" the gold line is **erased** by a black-bar wipe and ART + DESIGN slam together into one word: **ART+DESIGN**. | Snap collide, `expo.in`. | eraser swipe → click |
| 6 | 6.4–7.4 | "Bauhaus ne **curves**…" | **THE STRIP BEGINS.** The curly flourishes on the frame peel off and fall off-screen. | Each piece falls with gravity + spin (seeded). | paper rip #1 |
| 7 | 7.4–7.9 | "**detail**…" | The gold filigree and the wallpaper pattern drain to flat cream. | Colour drain sweeps top → bottom. | rip #2 |
| 8 | 7.9–8.8 | "aur **decoration** hata ke" | The whole gilded frame drops out of shot. The sepia grade snaps to clean neutral. **A2 hero shot** (ornate chair morphs into a tubular steel chair) plays full-screen. | Frame falls with `power2.in` and the grade flips on the beat. | big rip + whoosh |
| 9 | 8.8–11.0 | "clean shapes aur function pe focus kiya." | **The Bauhaus world.** Cream paper, a 6-column grid draws itself in black hairlines. He sits in a clean black-bordered rectangle. A **red circle, yellow triangle and blue square** snap to grid points one per word ("clean / shapes / function"). **FORM → FUNCTION** label. | Mechanical `steps(4)` snaps, rule of three. | 3× clicks |
| 10 | 11.0–13.6 | "It was heavily influenced by **modernism**," | Poster layout: **MODERNISM** set vertically up the left edge in black Jost 900. His frame shifts right on the grid. | The type racks in letter by letter like a typewriter carriage. | typewriter clacks (subtle) |
| 11 | 13.6–15.3 | "appreciated for its **simplicity**," | A blue ✓ square and the word **SIMPLICITY** (blue). | Pop from scale 0, `back.out`. | soft pop |
| 12 | 15.3–17.2 | "but criticized for erasing **craftsmanship**." | Cut to **A3** (hands carving ornate wood) in a circle crop. A **red diagonal bar** strikes through **CRAFTSMANSHIP**. | Bar slashes across in 0.25s. A hard emotional beat: show what was lost. | slash |
| 13 | 17.2–20.5 | "Sirf 14 saal chala, par impact aaj bhi hai" | Timeline bar **1919 ━━━━ 1933** draws across; a **"14 YEARS"** counter ticks up. At 1933 the bar stops, then a **yellow circle ripples outward** from the end of the bar past the frame: **→ 2026**. | Line draws (`stroke-dashoffset`), concentric yellow rings. | tick-tick, then a low boom on "impact" |
| 14 | 20.5–21.9 | "Aaj aap **clean layouts**," | Rule-of-three montage, beat 1: **A4** minimalist website on a laptop. | Whip-wipe in on a black bar. | whoosh |
| 15 | 21.9–23.2 | "**simple logos**," | Beat 2: three generic geometric logos built in code (circle, triangle, square marks; no real brands) assemble on cream. | Grid snap. | whoosh |
| 16 | 23.2–24.9 | "aur **minimal buildings** dekhte ho," | Beat 3: **A5** white concrete-and-glass minimal house, slow push-in. | Whip-wipe. | whoosh |
| 17 | 24.9–26.7 | "they are all products of modernism," | The three montage tiles shrink into a 3-up grid, with him back in the centre tile. Label **PRODUCTS OF MODERNISM**. | Tiles fly to grid slots, `expo.out`. | 3 clicks |
| 18 | 26.7–31.06 | "where simplicity, where efficiency often **wins over detail**." | **The balance scale**, built from Bauhaus shapes: a black beam on a triangle pivot. **SIMPLICITY + EFFICIENCY** blocks (blue, yellow) drop on the left and **DETAIL** (a small gold ornate flourish) sits on the right. On "wins" the left side slams down and **DETAIL** is launched off-screen. | Physics-y tilt, `back.out`. The callback: the last ornament leaves the frame. | heavy thunk + whistle |
| 19 | 31.06–34.0 | *(silence + music tail)* | **OUTRO HOLD.** Freeze on his last frame in a clean Bauhaus poster: cream, grid, the three shapes. Bottom-third question: **"Simplicity jeet gayi… par kya humne kuch khoya? 👇"** | Stillness, with a slow shimmer on the shapes. | music resolves |

**Music:** low, warm, slightly vintage piano/pad under Act 1. It becomes tighter and more rhythmic at the strip (beat 8), at ≈0.15 volume under the voice. Pulled from `assets/music/`.

## Assets needed from Google Flow (see prompts in chat)
- **A1** 1920s workshop interior (video, ~4s)
- **A2** ornate chair → tubular steel chair morph (video, ~4s) ← hero shot
- **A3** hands carving ornate wood (video, ~4s)
- **A4** minimalist website on a laptop (video, ~4s)
- **A5** minimal white modernist house (video, ~4s)
- **I1** damask wallpaper texture (image, 9:16)
- **I2** gilded baroque picture frame with an empty centre (image, 9:16)

Everything else (grid, shapes, type, logos, timeline, scale, captions) is built in code.

## Cut list (raw → `talking-head-cut.mp4`)
Crop `1216:2160:1312:0`. Segments (raw seconds): 1.62–4.60 · 4.72–8.40 · 13.02–17.95 · 18.62–24.72 · 27.90–38.40 · 38.85–41.72 → total 31.06s.
Removed: false start "1919 me" · first "Bauhaus ne curves…" take · lean-in reset · first "14 saal" take · 0.8s pause before "where efficiency".
