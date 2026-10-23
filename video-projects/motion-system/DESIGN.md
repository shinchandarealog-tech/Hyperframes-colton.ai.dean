# Motion System — Phase 1 Design Proposal

**Status: PROPOSAL — awaiting approval. Nothing below is built yet.**
Test case: `assets/sample-home-buying.mp4` ("Are you thinking about buying a home?").
The home-buying clip is the *test bed*, not the system's theme. Every component below is defined generically; the sample-specific usage is listed separately in §5.

Governing docs (precedence): `CREATOR.md` → `PREFERENCES.md` (approved creative direction) → this file → `MOTION_PHILOSOPHY.md` (technical recipes only; its aesthetic defaults are overridden — see §9).

---

## 1. Source footage — what was actually inspected

| Property | Value (verified with ffprobe) |
|---|---|
| File | `assets/sample-home-buying.mp4` (downloaded from the Google Drive link, 47.8 MB) |
| Video | H.264, 1920×1080 (16:9), 30 fps, yuv420p, ~20.5 Mbps |
| Audio | AAC, 48 kHz stereo; mean −23.6 dB, peak −2.3 dB |
| Duration | 18.67 s; speech 0.06 → 18.59 s |
| Edit | One continuous locked-off shot, no cuts. Pre-edited speech: the only gap >0.25 s is a 0.28 s breath at 15.37–15.66 s. |

**How I inspected it:** extracted frames at 2 fps (37 frames, 0.0–18.0 s), viewed 19 of them at 960 px (one per second) plus a timestamped contact sheet of all 37; sampled region colors from a full-res frame at 4.0 s; ran silence detection. I did **not** review all 560 native frames — that review happens on renders, per the workspace rule. I can't listen to audio, so transcript accuracy is checked only against whisper's own segment pass (they agree word-for-word).

### 1.1 Framing (coordinates in source pixels, 1920×1080)

- **Shot:** medium close-up, speaker centered, eye-level, direct address to camera for the entire clip.
- **Head box:** roughly x 800–1160, y 80–600 (hair top ~y 80–110, chin ~y 560–600).
- **Head drift:** horizontal center wanders between ~x 880 (≈3–4 s) and ~x 1080 (≈7 s); mean ≈ x 980. Vertical drift is small (±30 px).
- **Torso:** royal-blue hoodie fills x ≈ 470–1500 from y ≈ 480 to the bottom edge. Chest print reads "GALICI FINANCIAL". Black lav mic at chest left.
- **Eyeline:** to lens throughout. Brief eyes-closed "thinking" beats at ~13.0 s and ~16.0 s.

### 1.2 Gestures (hands enter from the bottom edge)

| Time | Gesture | Region (source px) |
|---|---|---|
| 0.0–2.5 s | Open palm, frame-right | x ≈ 1380–1650, y ≈ 950–1080 |
| 8.5–9.0 s | Both hands low, brief | bottom corners |
| **9.5–10.6 s** | **Both hands open wide** ("Let's break it down") | x ≈ 240–480 and 1360–1640, y ≈ 860–1080 |
| 11.0 s | One hand chopping, lower center-left | x ≈ 560–860, y ≈ 840–1080 |
| 15.5–16.1 s | Both hands low, open | bottom corners |

Rule derived: **the bottom ~22% of the 16:9 frame (y > 840) is a gesture zone** — graphics stay out of it during the windows above.

### 1.3 Negative space and contrast (measured at 4.0 s)

| Region (source px) | Avg color | Warm-white `#F4F1EA` text | Near-black `#0B0B0D` text |
|---|---|---|---|
| Upper-left wall (x 60–620, y 80–440) | `#615850` | **6.2:1** ✓ | 2.8:1 ✗ |
| Left wall mid (x 60–560, y 500–800) | `#594E47` | **7.2:1** ✓ | 2.4:1 ✗ |
| Right shelves/bed (x 1400–1700, y 560–760) | `#4B342A` | 10.3:1 ✓ (but visually busy) | ✗ |
| Floor lamp (x 1760–1900, y 220–400) | `#F9E9B3` | 1.1:1 ✗ | 16:1 |
| Hoodie (x 700–1200, y 760–1010) | `#213590` | 9.5:1 ✓ | ✗ |

Findings that drive the design:
1. **The left third is the primary graphic zone** (x 64–700, y 64–820): plain, mid-dark warm wall, good warm-white contrast. A small bookcase sits at x ≈ 580–860, y ≈ 220–620 — keep type left of x ≈ 620 or on a surface.
2. **The right third is busy** (shelves, books, bright lamp). Type there needs its own surface (panel), and never sits over the lamp.
3. **Dark type directly on the footage fails.** Dark-on-light only inside a warm-white panel.
4. **The hoodie is royal blue (`#213590`) — the same hue family as our accent `#3D7BFF`.** Blue graphics near the torso will visually merge with the clothing. On this footage the accent stays small and away from the torso (see §4.3).
5. Footage is warm and low-key. **No grade, no darkening, no vignette** — the footage is shown as delivered (PREFERENCES rule).

---

## 2. Transcript (local whisper.cpp `small.en`, word-level)

Word-level JSON: `assets/transcript.json` (83 words). Sentence/clause view:

| # | Start – End (s) | Text |
|---|---|---|
| 1 | 0.06 – 2.72 | Are you thinking about buying a new home in the next 10 years? |
| 2 | 2.78 – 4.40 | If you're in your late 20s right now, |
| 3 | 4.40 – 9.69 | I'll show you how to plan your finances over the next 10 years so you can buy a home before you're out of your 30s. |
| 4 | 9.82 – 12.60 | Let's break it down step by step so you can get started today. |
| 5 | 12.66 – 15.61 | Buying a home is one of the biggest financial goals for a lot of people, |
| 6 | 15.61 – 17.06 | but as you're likely aware, |
| 7 | 17.06 – 18.59 | it's gotten pretty pricey. |

Key word timings used below: *buying* 0.90 · *home* 1.40 · *10* 2.13 · *late* 3.40 · *20s* 3.62–3.88 · *now* 4.11 · *plan* 5.14 · *finances* 5.53–5.97 · *10* 6.52 · *years* 6.86–7.10 · *home* 7.76 · *before* 7.98 · *30s* 9.12–9.69 · *break* 10.02 · *step* 10.66 / 10.91 · *today* 12.08–12.60 · *biggest* 13.66 · *financial goals* 14.02–14.74 · *but* 15.61 · *pretty* 17.67 · *pricey* 18.03–18.59.

---

## 3. Content beats

| Beat | Time (s) | Role | What's being said | Visual opportunity (only what the words support) |
|---|---|---|---|---|
| B1 | 0.06 – 2.72 | **Hook / question** | "Are you thinking about buying a new home in the next 10 years?" | Editorial typographic question. Speaker gestures frame-right — type goes frame-left. |
| B2 | 2.78 – 4.40 | **Audience qualifier** | "If you're in your late 20s right now," | Start of a time axis: a "Late 20s / Now" marker. |
| B3 | 4.40 – 9.69 | **Promise** | plan finances · next 10 years · buy a home · before you're out of your 30s | The one diagram the transcript genuinely supports: a **10-year span** from *late 20s* to *end of 30s* with a home marker. Builds on B2 — same object, no scene change. |
| — | 9.69 – 9.82 | breath | | Diagram resolves / exits. |
| B4 | 9.82 – 12.60 | **Roadmap promise** | "break it down step by step … get started today" | Section marker + step rhythm. **The clip never names the steps** — so no numbered list with invented content. Wide hand gesture 9.5–10.6 s must stay clear. |
| B5 | 12.66 – 15.61 | **Context** | "one of the biggest financial goals for a lot of people" | Editorial pull-quote, emphasis on *biggest*. Good place for the light (warm-white) surface variant. |
| B6 | 15.61 – 18.59 | **Tension / pivot** | "but … it's gotten pretty pricey." | Pivot on *but* (natural seam after the 0.28 s breath). Emphasis on *pricey* using the rare warning accent `#FF9F43` — the one place its "caution" meaning fits. **No price figures**: the clip states none (see §8, Q4). |

The clip ends 0.08 s after "pricey" — it is clearly the opening of a longer video. **No outro hold** is added; timing follows the footage.

---

## 4. System architecture (reusable, content-agnostic)

### 4.1 Four layers, kept separate

| Layer | What it is | Changes per video? |
|---|---|---|
| **Tokens** | `assets/brand-tokens.css` (approved) + `assets/fonts/` | No |
| **Components** | Generic HTML/CSS/GSAP building blocks (§5). They know nothing about real estate. | No |
| **Footage map** | Per-clip JSON: head-box keyframes, gesture windows, free zones, contrast notes (§1.1–1.3 encoded). Drives where components may sit. | Yes — authored per clip from analysis |
| **Beat script** | Per-video JSON: each beat = component + variant + text + word-anchored timing + zone. | Yes — the only "content" file |

Content (text, timings, which component) lives only in the beat script. Swapping topics means writing a new beat script and footage map — no component edits. HyperFrames supports `data-composition-variables` + `render --variables-file`, which I intend to use for this (to be verified in Phase 2, §8 T3).

### 4.2 Placement by semantic zone, not pixels

Components ask for a **zone**; each aspect ratio resolves zones to rectangles, then the footage map subtracts the face box and any active gesture window.

| Zone | 16:9 (1920×1080) | 9:16 (1080×1920) |
|---|---|---|
| `primary` | Left column x 96–640, y 120–820 (the speaker's open side; mirrors if a future speaker sits left) | Graphic stage (layout-dependent, §6.2) |
| `secondary` | Right column x 1320–1824, y 120–760 — **surface required** (busy background) | Below primary in the stage |
| `anchor:<target>` | Point on the frame (e.g. beside the head, at the shoulder) + leader line | Same, scaled; only in FULL layout |
| `caption` | Bottom center, max width 1100, baseline ≈ y 1000 | Layout-dependent, always above y 1540 |
| `full` | Whole frame (rare: full-bleed type or diagram moments) | Whole frame |

Safe zones (approved): 9:16 keeps top 220 / bottom 380 / right 140 clear, 64 px side margins. 16:9 uses a 96 px title-safe margin (≈5%) and no platform UI bands.

### 4.3 Global rules applied to every component

- Footage is never graded, darkened, vignetted, or grained. Graphics carry their own contrast (text shadow `0 1px 2px rgba(0,0,0,.45)` on footage, or a surface).
- Dark surfaces default; warm-white surface where it improves contrast or variety.
- Accent `#3D7BFF`: strokes, markers, active states — small areas, never a large fill. **On footage where the subject wears blue (this sample)**: accent stays ≥ 120 px from the torso and never sits on the hoodie.
- `#FF9F43` only for caution/tension meaning, at most once per video unless the script repeats the idea.
- Glass (`--brand-surface-glass`) is allowed for at most one component per video, and only where the footage behind adds value.
- Geist for everything; Geist Mono only for technical facts (numbers with units, years, ages, percentages, labels like `STEP 01`).
- One focal graphic at a time (captions excepted).
- Motion in/out uses the approved tokens. All tween ends snap to 1/30 s. Every timeline is padded to its slot (`tl.set({}, {}, SLOT)`) — the technical laws from `MOTION_PHILOSOPHY.md` that remain in force.

---

## 5. Component list

Each component: **why it exists**, then its spec. Sizes are starting points from the approved scale, chosen per instance.

### C1 — Editorial Headline
**Why:** a hook or thesis line carried by typography alone — the strongest, quietest way to frame a talking-head video. Generic: any question, claim, or title.

- **Variants:** `question` (two lines, the second line dimmer), `statement`, `kicker+headline` (Geist Mono label above, e.g. `CHAPTER 01`).
- **Type:** Geist 600, `--type-headline` (88 px) in 16:9; ~96–112 px in 9:16 stage. Tracking −0.02em, line-height 1.02. Warm white on footage. Max 3 lines, ≤ 22 characters per line.
- **Layout:** left-aligned in `primary`; ragged right; optical left alignment to the 96 px margin.
- **Animation in:** line-by-line **mask reveal** — each line slides up 100% inside an overflow-hidden line box, `power3.out`, 0.45 s, lines staggered 0.08 s. The emphasized word gets a weight shift to Bold or a warm-white→accent color change at its spoken time.
- **Out:** lines slide up out of their masks, `power2.in`, 0.30 s, or hand off to the next component (morph, below).
- **Captions:** suppressed while the headline shows the same words (no duplicate text).

### C2 — Anchored Label
**Why:** ties a fact to something *in* the frame (the speaker, a gesture, an object) so graphics feel attached to the footage, not pasted over it. Generic: names, qualifiers, roles, "this is X".

- **Anatomy:** a 1 px hairline leader (warm white @ 60%) from an anchor dot (6 px, accent) to a label block: optional mono eyebrow (26 px, +2% tracking, dim) + title (Geist 500, 40–56 px).
- **Anchor sources:** footage-map point (e.g. "shoulder-left", "beside-head-left"), tracked with the head-box keyframes so it follows the speaker's drift.
- **Animation in:** the dot scales 0→1 (`expo.out`, 0.18 s) → the leader draws from the anchor outward (`power2.inOut`, 0.35 s) → the label wipes in from the leader end (clip-path, `power3.out`, 0.35 s). Total ≈ 0.6 s; it reads as one gesture.
- **Out:** reverse at 0.6× speed, or the label retargets into another component.
- **Constraint:** the leader never crosses the face box; the label never sits in an active gesture window.

### C3 — Span / Timeline Diagram
**Why:** many scripts talk about time — plans, milestones, "in 5 years", before/after. A horizontal axis with markers and a span bracket makes a spoken time frame instantly visible. Generic: any time span, roadmap, or age/date range.

- **Anatomy:** a hairline axis (1 px warm white @ 40%); **start marker** (accent dot + label); **span bracket** (1.5 px accent line with end caps, duration label in Geist Mono, e.g. `10 YRS`); **end marker** (warm-white ring + label); optional **milestone glyph** (a 1.5 px stroked icon, drawn on).
- **Built progressively, on the words:** each element appears when it's spoken, so the diagram assembles in sync with the sentence instead of appearing all at once.
- **Animation:** axis draws left→right (`power2.inOut`, 0.8 s structural); markers pop (scale 0.6→1 + opacity, `expo.out`, 0.18 s); bracket stroke-draws (`power3.out`, 0.45 s) with its label counting `0 → 10` in mono over the same duration; glyph stroke-draws (0.45 s). Exit: the whole diagram slides left 24 px + fades (`power2.in`, 0.3 s).
- **Surface:** none on clean wall (16:9 left column) — lines and type sit directly on the footage with a soft text shadow. In 9:16 it sits in the stage.
- **No invented data:** labels come only from the script (here: "Late 20s", "10 years", "End of 30s").

### C4 — Section Marker (Step Rail)
**Why:** signals structure ("step by step", "three reasons", "part two") so viewers know the video has a plan. Generic: chapter changes, step counts, agenda.

- **Anatomy:** mono eyebrow (`THE PLAN`, `PART 02`, etc.) + Geist 600 title + a segmented progress rail (n segments, 4 px tall, 8 px gaps; active = warm white, inactive = warm white @ 18%).
- **Rule for this sample:** the clip doesn't say how many steps there are. The rail's segment count comes from the beat script; if unknown, it uses an **unnumbered** rhythm (3 ticks lighting on "step… by… step") rather than inventing "Step 1/5".
- **Animation:** eyebrow fades/slides 12 px (`power3.out`, 0.3 s) → title mask-reveal (as C1) → segments light in sequence on the spoken rhythm (`expo.out`, 0.18 s each). On "today" (or any call to action), the title's last word shifts to accent.
- **Placement:** 16:9 upper-left `primary` (y 120–420) — specifically above the 9.5–10.6 s wide-hands gesture zone.

### C5 — Pull Quote / Emphasis Panel
**Why:** lifts one important phrase from the speech, with emphasis on the key word. It gives the edit an editorial rhythm and a chance to vary material. Generic: any key claim or stat sentence.

- **Variants:** `light` (warm-white panel `--brand-light-surface`, near-black Geist 600 type, 1 px `--brand-light-border`, `--shadow-2`, `--radius-m`) and `dark` (graphite panel, warm-white type). No glass by default.
- **Type:** 56–72 px, line-height 1.1, max 4 lines; the key word is set in Bold with a 3 px accent underline that draws under it at its spoken time.
- **Animation in:** the panel grows from a 2 px hairline to full height (`clip-path inset`, `power3.out`, 0.45 s) while lifting 16 px; text lines mask-reveal 0.08 s after; the underline draws on the key word (`power2.inOut`, 0.35 s).
- **Out:** collapses back to a hairline (`power2.in`, 0.3 s) — a different exit from C1 and C3, for variety.

### C6 — Info Panel (Structured Data)
**Why:** when a script makes a quantitative claim, a structured panel (label, value, unit, source) turns it into evidence. Generic: any figure, comparison, or before/after.

- **Anatomy:** mono label row · large value (Geist 600, tabular numerals via Geist Mono for the digits) · delta chip (↑/↓ + %; `#FF9F43` for adverse, accent for favorable) · source line (Geist Mono 22–26 px, dim). Optional sparkline (1.5 px stroke).
- **Animation:** panel enters as C5; value counts up (`power2.out`, 0.8 s, snapped to whole units); delta chip pops (`expo.out`, 0.18 s) after the count lands; sparkline stroke-draws.
- **Sample status: proposed but NOT used unless you supply a sourced figure.** "It's gotten pretty pricey" contains no number; I won't fabricate one. Without data, B6 uses C7 instead (typographic emphasis).

### C7 — Captions
**Why:** most short-form viewing is sound-off; in 16:9 they're optional. Captions must read as part of the design, not a subtitle track.

- **Style:** Geist 600, warm white, phrase-chunked (≤ 2 lines, ≤ 32 characters per line, broken at clause boundaries from the transcript). Shadow `0 2px 12px rgba(0,0,0,.45)` for legibility — no stroke, no pill, no glass.
- **Active word:** **restrained** — inactive words at 72% opacity, the current word at 100% (0.08 s crossfade). No scale pop, no color flash by default; key words flagged in the beat script may get accent color.
- **Size:** 9:16 ≈ 56–60 px; 16:9 ≈ 44 px.
- **Behavior:** hidden while C1/C5 show the same words; shifted when a gesture window overlaps their box.
- **Placement:** see §6.
- **This overrides** the `short-form-video` skill's karaoke default (Montserrat 900, pop + color, "graffiti" style) per PREFERENCES.

### C8 — Speaker Frame (layout controller)
**Why:** the footage is the foundation. This is the one component that decides how the footage itself is framed per aspect ratio, and it animates layout changes so they read as deliberate camera moves rather than cuts. Generic: any talking-head source.

- 16:9: the footage is full-frame by default. Optional `push-in` (scale 1.00→1.06 over a beat, `power2.inOut`, centered on the head box) for emphasis moments — used sparingly, never as constant drift.
- 9:16: the layout modes in §6.2.
- Mode changes: 0.5 s `power2.inOut` (approved "move" ease), starting 0.25 s before the beat's first word; the outgoing graphic exits during the move.
- **Never** animates `<video>` dimensions — wraps it in a div (render contract).

### C9 — Identity Lower Third *(library only — disabled)*
**Why:** reusable name/handle plate for future videos.
**Disabled until `CREATOR.md` has a name and handles** (it currently says not to show any). Not used in this sample. The hoodie's "GALICI FINANCIAL" is not treated as your brand without confirmation (§8, Q2).

### Transition vocabulary (shared, not a component)
Chosen per beat, never repeated back-to-back: **mask reveal** (C1), **draw-on** (C2/C3), **hairline grow/collapse** (C5/C6), **segment sequence** (C4), **layout move** (C8), **straight cut on a word** (for hard pivots like "but"). Opt-in only, with a concept that justifies them: grid, crosshairs, vignette, grain, chrome/glow text, whip transitions.

---

## 6. Responsive rules: 16:9 vs 9:16

### 6.1 16:9 (1920×1080) — use the width

- The footage stays full-frame; the speaker is centered, so the **left column is the stage** and the right column is secondary (surface required).
- Graphics compose *with* the speaker: left-aligned type aligns its cap height to the speaker's eye line (~y 300) or chin line (~y 580), so text and face read as one composition.
- The wide frame allows **side-by-side** structures (diagram left, speaker center) instead of stacked ones — don't port the vertical stack.
- Captions bottom-center only when enabled; they move up/aside during gesture windows (§1.2).

### 6.2 9:16 (1080×1920) — protect the face, then the stage

The source is 1080 px tall, so **any full-bleed 9:16 crop is a 1.78× upscale** (608×1080 → 1080×1920) and will look softer than the 16:9 version. The system therefore offers two layouts:

| Layout | Footage | Graphics | Use for |
|---|---|---|---|
| **SPLIT (default)** | **Native-res crop 1080×960** of the source (no upscale), centered on the head-box track; placed at y 960–1920. Face lands at ≈ y 990–1500 (clear of the bottom 380 UI band). | Graphic stage y 220–940, x 64–1016 — a clean area for C1/C3/C4/C5/C6. Stage background: graphite `--brand-surface` with a 1 px hairline seam at y 960 (no gradient glow seam). | Diagrams, panels, headlines — most beats. |
| **FULL** | 608×1080 crop, 1.78× upscale, tracking the head box (center x ≈ 980 ± 100 → keyframed). Face ≈ y 160–1070. | C2 anchored labels beside the head; C7 captions over the chest, y ≈ 1300–1480 (warm white on the hoodie measures 9.5:1). | Emotional / direct-address beats where the face *is* the content. Brief. |

- Between layouts: C8 animates the crop window (0.5 s), never a hard cut.
- **Captions in SPLIT** sit at the seam (bottom of the stage, y ≈ 820–930) — near the eyes, above the face, clear of the bottom UI. **In FULL** they sit over the chest (y ≈ 1300–1480).
- Type sizes scale up in 9:16 relative to 16:9 (both are read on a phone): headline 96–112 px, body 44–48 px, mono ≥ 28 px, captions 56–60 px.
- Gestures: the wide 9.5–10.6 s gesture is mostly outside both 9:16 crops (hands at x 240–480 / 1360–1640). Accepted — noted here so nobody "fixes" it by widening the crop past the face.
- Right edge: no text inside x > 940 (right 140 px safe zone).

### 6.3 Per-component adaptation

| Component | 16:9 | 9:16 SPLIT | 9:16 FULL |
|---|---|---|---|
| C1 Headline | Left column, 88 px, ≤ 3 lines | Stage, 96–112 px, ≤ 4 lines, centered vertically in the stage | Not used (would cover the face) |
| C2 Anchored label | Beside the head, leader to the shoulder | Not used (no frame room) | Beside the head, short leader; label inside x 64–940 |
| C3 Timeline | Left column, horizontal axis 520 px wide | Stage, horizontal axis full stage width (952 px) — more room, larger labels | Not used |
| C4 Section marker | Upper-left, above the gesture zone | Stage top | Top band y 220–420, compact |
| C5 Pull quote | Left column panel, ≤ 560 px wide | Stage, full width | Not used |
| C6 Info panel | Right or left column panel | Stage | Not used |
| C7 Captions | Bottom center, optional | Seam, y ≈ 820–930 | Chest, y ≈ 1300–1480 |

---

## 7. Sample application (test case only — not part of the system)

| Beat | Time (s) | 16:9 | 9:16 layout | Component & timing |
|---|---|---|---|---|
| B1 | 0.06–2.72 | C1 `question` left column: "Thinking about buying a home" / "in the next 10 years?" | SPLIT | Line 1 reveals at 0.25 s, line 2 at *next* (1.91 s); "10 years" set in Geist Mono at *10* (2.13 s). Captions suppressed. Exit 2.72–3.0 s. |
| B2→B3 | 2.78–9.69 | C3 builds in the left column | SPLIT | Axis draws from *late* (3.40 s); start marker "Late 20s" at *20s* (3.62 s); "NOW" mono tag at *now* (4.11 s); bracket draws from *next* (6.36 s) with `10 YRS` counting to *years* (7.10 s); home glyph draws at *home* (7.76 s); end marker "End of 30s" at *30s* (9.12 s). Exit 9.69–9.95 s. |
| B4 | 9.82–12.60 | C4 upper-left: `THE PLAN` / "Step by step" / 3-tick rail | FULL (face moment, big gesture) | Eyebrow at *break* (10.02 s); ticks light at *step* 10.66 s, *by* 10.81 s, *step* 10.91 s; "Start today." accent on *today* (12.08 s). Captions on, chest position. |
| B5 | 12.66–15.61 | C5 `light` panel: "One of the biggest financial goals" | SPLIT | Panel grows at *Buying* (12.66 s); underline draws on *biggest* (13.66 s). Out on the breath at 15.37 s. |
| B6 | 15.61–18.59 | Typographic emphasis (C1 `statement`): "It's gotten pretty pricey." — *pricey* in `#FF9F43` | SPLIT | Straight cut in on *but* (15.61 s); line reveals at *it's* (17.06 s); *pricey* color lands at 18.03 s; holds to 18.67 s. C6 replaces this **only** if you provide a sourced figure. |

The variety check: six beats use six different entrances (mask, draw-on, segment sequence, hairline grow, cut, layout move); four different surfaces/materials (bare type, bare lines, light panel, dark stage). No grid, grain, vignette, glow, or whips.

---

## 8. Technical limitations and open questions

### Questions for you
1. **Q1 — Is there a 4K original of this clip, and do you film in 4K?** At 4K, 9:16 FULL becomes a sharp downscale (1215×2160 → 1080×1920) instead of a 1.78× upscale, and SPLIT can crop more tightly. This is the biggest quality lever for vertical.
2. **Q2 — "GALICI FINANCIAL" on the hoodie:** is that your brand? If so, should it go into `CREATOR.md` (name, plus a logo and lower third in C9)? Until you say so, nothing identity-related goes on screen.
3. **Q3 — Should the accent stay `#3D7BFF` when you're wearing that blue hoodie?** My proposal keeps it and applies the distance rule (§4.3). The alternative is warm-white-only graphics for this wardrobe.
4. **Q4 — "Pretty pricey":** do you want a sourced figure (C6) in the full video? If yes, give me the number and its source. Without it, B6 stays typographic.
5. **Q5 — The transcript says "10 years"** (digits) and "20s/30s". Please confirm it matches what you said; I can't listen to the audio.
6. **Q6 — Should 16:9 deliverables have burned-in captions** (YouTube typically uses platform captions), or only 9:16?

### Technical items to resolve in Phase 2 (none verified yet)
- **T1 — Network dependency in the scaffold:** `index.html` loads GSAP from `cdn.jsdelivr.net`. The workspace forbids render-time network fetches, so I'll vendor GSAP into `assets/vendor/` and reference it locally.
- **T2 — Scaffold vs. workspace render contract:** `init` put `class="clip"` and `data-has-audio="true"` (no `muted`) on the `<video>`. The workspace `CLAUDE.md` says the opposite: no `clip` on `<video>`, `muted`, and audio in a sibling `<audio>`. The project-level `CLAUDE.md` written by this CLI version (v0.8.186) documents the scaffold's form as current ("A video with sound keeps it on the `<video>`… Give timed visual elements `class=\"clip\"`"), so the workspace doc looks outdated. I'll confirm with `npm run check` + a smoke render before relying on either. This CLI also offers `npm run check` (lint + runtime + layout + contrast) and `hyperframes snapshot --at <s>` for frame checks, which I'll add to the verification loop.
- **T3 — Two aspect ratios from one project:** plan is two root entry files (`index.html` 1920×1080 + `index-vertical.html` 1080×1920) rendered with `render -c`, both loading the same component library, plus `--variables-file` for the beat script. Not tested yet; if `-c` doesn't accept a second root, the fallback is two sibling projects that share `compositions/components/`.
- **T4 — Head-box tracking:** no face-detection model is installed. The footage map will use hand-keyed head-box positions (every 0.5 s from frame analysis), verified on frames. Good enough for locked-off talking heads; moving-camera clips would need a tracker.
- **T5 — Project-level `CLAUDE.md`/`AGENTS.md`:** `init` wrote these into `video-projects/motion-system/`. They carry useful, current CLI facts (T2), but they also point to skills that aren't installed here (`/media-use`, `/figma`, `/slideshow`). They tell agents to load `/media-use` before changing how footage looks; that skill isn't available, and the PREFERENCES rule (don't alter footage) covers it. Recommendation: keep them, and add one line at the top saying the workspace `CLAUDE.md` + `PREFERENCES.md` take precedence. Separately, update the workspace render contract once T2 is verified. Untouched pending your OK.
- **T6 — Sample video not committed:** the 47.8 MB clip is git-ignored in this project (it's your footage and the repo may be public). The container is temporary — to restore it in a new session, re-download from the same Drive link into `assets/sample-home-buying.mp4`.
- **T7 — Skill defaults overridden** (per PREFERENCES, recorded here so they don't creep back): `short-form-video`'s mandatory face grade + Ken Burns, ambient particle/grain backgrounds, navy gradient seam, Montserrat karaoke captions, "one jaw-dropper per 5 s"; `MOTION_PHILOSOPHY.md`'s grid/crosshair/vignette/grain/chrome-text/whip defaults, ~1.5 s scene average, and 4–6 s outro hold. Its technical laws (timeline padding, 1/fps snapping, duration diagnostic) remain in force.

---

## 9. Proposed Phase 2 (after approval)

1. Fix T1/T2; verify T3 (two roots + variables) with a 2-second smoke render per aspect.
2. Write `footage-map.json` for this clip and `beats.json` for the sample.
3. Build components C1–C8 as isolated sub-compositions, each with its own preview URL, in both aspect ratios.
4. Lint → Studio preview gate (you scrub each component) → only then a draft render → every-frame review → MP4 preview gate.
