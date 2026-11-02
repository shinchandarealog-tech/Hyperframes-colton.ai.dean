# Style spec: Hinglish local-agency offer reel (presenter + keyword kinetic type)

Built from: `brandbuddiestudio/videos/DWIu4iwk81P` (ref A) + `visionxvortex/videos/DdZYImyuDeF` (ref B)
Confidence: structure/pacing/captions **high** · color/graphics **high** · fonts **medium** (closest matches) · music/SFX **low** (no stems)

## Core rules (true in both references)
- **Format**: 9:16, 1080×1920 (refs are 720×1280), 30fps, **25–31s**, VO edge to edge with no pauses. Loudness **−14 LUFS**, LRA ≤3.5 (compressed and loud).
- **Talent**: on-camera presenter(s) speaking straight to lens, mostly medium shots (head to mid-thigh), often **walking toward camera**, outdoors in recognizable local streets. Face on screen ≥95% of runtime.
- **Script formula** (both identical):
  1. **Local call-out + pain/objection question** (0–3s): "<City> mein business chala rahe ho? / <City> ke business owners…"
  2. **Answer/insight** (3–9s)
  3. **Brand reveal** ("Yahi par <Brand> aapki help karta hai")
  4. **Service stack**: one item per beat
  5. **Price/offer with a number** (count-up)
  6. **CTA: "DM us / message now"**, plus scarcity optional
- **Pace**: a new **on-screen element every 0.5–1.0s**. Shot length 0.5–5.8s (avg 2.2–4.1s); a long shot is allowed only if overlays keep changing. Max unchanged hold 3.2s.
- **Captions = keyword lockups, not subtitles**: every phrase appears, but as **KEYWORD (huge, colored) + connector words (small, white)**. Keyword cap height **6–9% of frame height**; connectors **2.2–3%**. Words appear on their spoken word (±2 frames).
- **Keyword placement**: upper third (y≈20–35%) **behind or around the head**, or across the chest (y≈50–62%). Never in the bottom 20% (platform UI zone).
- **Every noun becomes an object**: platform → 3D app icons; deliverable → mockup/photo cards; place → 3D pin; people → avatars; price/stat → count-up; service → glass UI card or pill tag. Objects **pop in around the head** (top/sides), never covering the face.
- **Transitions**: a **light-leak flash** (6–10 frames, cut hidden at peak brightness) **only at section boundaries** (3–4 per video); hard cuts everywhere else.
- **Grade**: natural to bright, no grain, no vignette, soft drop shadows on type. Presenters wear solid neutral or tonal wardrobe so the colored type pops.
- **Ending**: CTA on screen + spoken. No outro card. Either a hard stop or cut to black (≤1s).

## Script → visual rules
| Trigger | Show |
|---|---|
| City / audience name | Huge keyword slides in from the side, upper third, behind the head |
| Doubt / objection question | Frame desaturates to B&W on the last word, then flash into the answer (ref B) |
| One-word answer ("Haan!") | One giant word, full width, new shot |
| Platform name (Instagram, YouTube…) | Row of 3D glossy app icons above the head, staggered pop 0.1s |
| Deliverable (post, reel, ad, video) | Mockup cards / tilted photo cards with white border, around the head |
| A specific example | Screenshot card + thin curved callout line to the presenter's hand |
| Brand name | Logo badge rises from behind the head + brand word huge behind the presenter |
| List of categories | Dark pill tags popping one per spoken word |
| Each included service | New location/shot (ref B) **or** new card on the same shot (ref A) + gradient keyword |
| Location | 3D map pin drops & spins |
| People/team | Avatar circles (memoji style) |
| Number / price | Count-up numerals (+ optional progress ring), "Rs"/"₹" small |
| Scarcity | Tight close-up (selfie/car), silver "limited" type |
| CTA | ALL-CAPS white "DM US NOW" with letter stagger, or a DM-bubble UI (avatar + black pill) |
| Section change | Light-leak flash + location change |

## Variants (where the two refs differ: pick one per video)
| | **Variant A: "Calm premium"** (BrandBuddies) | **Variant B: "Hype montage"** (VisionXVortex) |
|---|---|---|
| Talent | 1 presenter, 6 locations | 2–3 presenters, 14 shots |
| Shot length | avg 4.1s; overlays carry pace | avg 2.2s; one benefit = one shot |
| Typography | **one family** (Poppins 800 keyword / 500 connectors), title case | **font switching**: condensed white setup (Oswald) + heavy gradient keyword (Montserrat Black) + italic tail |
| Keyword color | mostly **one brand accent** (cyan `#0CB4FC`) + one special gradient for the brand word | **new gradient every beat** (magenta, blue, red, purple, green, yellow, navy) |
| Type motion | slide-in from side (≈7 frames, expo-out), word-by-word type-on | letter-by-letter drop with vertical motion-blur, blur-smear in/out |
| Flash color | cyan-blue, then warm pink-white for the final section | lime green `#B4FC54` |
| Grade | warm-natural, shallow DOF bokeh | bright high-key, airy |
| B-roll | none | 0.6s BTS + photo cards |
| Hook gimmick | text already moving on frame 1 | white-silhouette strobe reveal, then B&W doubt beat |
| End | 0.9s black | hard stop mid-energy |

**Core vs variant**: build either variant on the core rules. A hybrid that works well is **A's one-accent palette + B's one-benefit-per-shot cutting + B's hook gimmicks**.

## Signature moves
1. **Keyword-behind-presenter**: a giant colored word in the upper third with the presenter's head occluding it (needs a person matte).
2. **Light-leak flash only at section boundaries**, combined with a location change.
3. **Every noun becomes an object popping around the head** (3D icons, cards, pins, avatars, counters).

## HyperFrames implementation notes (this workspace)
- **Person matte for text-behind-head**: pre-render an alpha matte of the presenter (e.g. RobustVideoMatting/rembg → ProRes 4444 or WebM with alpha), then layer: `video` (track 0) → keyword type (track 1) → matte cut-out video (track 2) → connectors/cards (track 3).
- **Light-leak flash**: registry `light-leak` or `flash-through-white` blocks. Tint cyan/lime per variant. 6–10 frames, cut at the peak.
- **Count-up / ring**: GSAP tween on a proxy object with `onUpdate` writing `textContent` and an SVG `stroke-dashoffset` ring. Use a deterministic timeline only.
- **Letter-drop with motion-blur**: split text into spans; stagger `y` from −40px with `filter: blur()` only on Y via `scaleY` 1.6→1 (shader-safe). 1 frame per letter.
- **App icons / pins / avatars**: use the user's own licensed assets or simple SVG. Don't reuse the reference creators' assets.
- Precedence still applies: `CREATOR.md` > `PREFERENCES.md` > this spec > `MOTION_PHILOSOPHY.md`. Note that this spec **overrides** MOTION_PHILOSOPHY's black-canvas/grid/chrome-text defaults for this format: these are live-action presenter reels, not abstract motion spots.

## Mapping notes for this client's footage
- *Pending*: `CREATOR.md` is still un-configured (setup marker present), and no client footage has been provided yet. Fill this in once known (talent count, locations available, brand accent, city/audience).

## Don't copy
- Either agency's logo, name, presenters, prices ("₹6000", "₹30,000"), city lines ("Dehradun", "Bhopal"), client screenshots (mamaearth etc.), third-party brand marks visible in backgrounds (Mercedes, McDonald's, One Walk), and their music tracks.
