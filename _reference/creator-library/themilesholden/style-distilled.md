# @themilesholden — Style Fingerprint

Rolled up across 8 videos. See `videos/*/analysis.md` for per-video detail. Last distilled: 2026-11-09.

**The format in one line:** a fixed **"Drawing" vs "✳ Opus 5.5"** split screen. A rough pen storyboard on the left plays in sync with a polished, cinematic, AI-generated brand film of a well-known app or product on the right, over a dark vignette, with a permanent **Comment "OPUS" for guide** lead-magnet CTA. Every video is about 14–17s. They're faceless, with no visible voiceover or spoken captions, and the narrative is told only through UI, kinetic type and camera motion.

## Signature moves (consistent across videos)

### Layout chrome (identical in all 8, never animates)
Measured on a 720×1280 frame (scale ×1.5 for 1080×1920):

| Element | Position / size (720×1280) | Style |
|---|---|---|
| Canvas | full frame | Radial vignette: centre about #2a2a2a, edges #050505 |
| "Drawing" panel | x≈50, y≈490, 216×384 (9:16) | Off-white paper #f7f6f2, black pen sketch, small sharp-cornered card |
| "Drawing" label | centred above the panel, y≈460 | White, about 34px, semibold geometric sans |
| "Opus 5.5" panel | x≈287, y≈297, 380×675 (9:16) | Full-bleed render, square corners, overlaps the drawing panel's right edge by about 20px |
| "✳ Opus 5.5" label | centred above the panel, y≈255 | Orange #e07e52 asterisk glyph plus white "Opus 5.5", same size as "Drawing" |
| CTA | centred, y≈1025 (about 80%) | White **Comment "OPUS" for guide**, keyword in **pink #f8b0be** (switched to red #e31837 in the Domino's video) |

- The big panel is about 1.75× the small one and sits higher, so the eye reads small sketch → big result, left to right.
- The sketch panel always shows the **same shot as a storyboard frame** at the same moment, sometimes with handwritten direction notes ("zoom out", "spin", "shatters", "click", "lights on", "start close, pull back"). This sells the claim "I drew this, the AI made it".

### Hook pattern (0–2s)
- The layout is fully present on frame 1. There's no intro, title card or face.
- 6 of 8 open on an **app icon or app UI**, and in 3 of those a cursor taps the icon in a dock (Duolingo, Spotify, Domino's chat). The others open on a brand sting (Netflix N), a hero object (Apple Card) or a prompt box (SJÄLV).
- By about 1.5s the icon has **zoomed through or scaled up** into the first full-bleed world.
- The hook works because of the left-vs-right contrast. A doodle becoming a cinematic render is the curiosity gap.

### Story structure (the repeatable 6-act template)
1. **Entry (0–1.5s):** tap or zoom into the app icon
2. **Transform (1.5–3s):** the icon hero, often followed by a destructive transition (shatter or particles)
3. **Human use case (3–7s):** something specific typed in (a search query, "I need pizza.") or a real-world task (finding keys)
4. **Payoff (7–10s):** content wall, counter tick (364 → 365, \$0 → \$19.99, 12m → 1m) or data viz
5. **Word stack (10–12s):** a vertical column of words or times scrolls through a **selection box with corner handles** and lands on the key word (Keep / 3:22 AM / Play)
6. **Slogan slam, then the logo resolves (12–16s):** a heavy white or black sans tagline on the brand colour, then the logo or wordmark with a tagline, held for about 2–3s

### Pacing
- 7–10 beats per video, **about 1.5–2.0s per beat**, with no hard cuts. Scene detection at a 0.25 threshold found **zero cuts in all 8 videos**.
- Everything is one continuous camera move or a morph between states.
- Speeds up through counters and montages, slows for the hero object, and holds the logo for 2–3s.
- **The energy follows the brand:** fast, shatter-heavy for playful apps (Duolingo, Spotify, Netflix) and slow, dissolve-only for premium or finance (Apple Card).

### Captions / type
- **No spoken captions in any video.** The only persistent text is the chrome above.
- On-screen words come from either (a) authentic-looking **in-app UI text** or (b) **kinetic slogan type**.
- Slogan type mixes weights: a boxed word, then a small italic or script connector ("the"), then a huge heavy slam word with a "!" ("Keep the **Streak!**", "Just One **More!**", "Play the **Mood!**"). Stickers (stars, vinyl, popcorn) are added for playful brands.
- The **selection box with 4 corner handles** (like a design-tool bounding box) is a recurring device in 4 of 8 videos.
- Typing with a caret appears in 5 of 8: search bars, a chat bubble, the prompt box, URL and product-name outros.

### Transition rotation
- **Zoom through the icon** (open, and often close) is in nearly every video
- **Continuous camera:** dolly, orbit, tilt, drone flight
- **Shape morph:** bubble → card → blob (Domino's), map → floating tilted card (Maps)
- **Destructive:** icon shatter or particle burst (Duolingo, Spotify, Domino's text)
- **Particle reassembly** into the logo (Spotify)
- **Motion-blur whip** (Netflix tiles, Maps pull-out)
- **Soft dissolve** (Apple Card only)
- He rotates 4–6 types per video and never uses the same transition twice in a row.

### Face treatment
- None. The account is fully faceless and the "talent" is the product.

### Palette
- **Fixed chrome (identical every video):** #0a0a0a–#2a2a2a vignette · #ffffff labels · **#e07e52 orange asterisk** · **#f8b0be pink CTA keyword** · #f7f6f2 sketch paper
- **Variable:** the right panel takes the subject brand's full palette (Duolingo green, Netflix red, Spotify green, Apple pastels). The chrome stays neutral so any brand colour works on top.

### Energy profile
- Front-loaded hook, steady escalation, slogan crescendo, then a calm logo hold.

## What to steal (ranked by Hyperframes copy-ability)
1. **The fixed "before / after" split-screen shell.** Two 9:16 video panels (small left, big right, staggered vertically), labels above, a permanent CTA at 80%. It's a pure HTML/CSS layout with two muted `<video>` elements inside wrapper `div`s. Reusable for any "X vs Y" or "sketch → result" or "prompt → output" idea, such as *"My script → the HyperFrames render"* or *"Storyboard → final"*.
2. **Persistent comment-keyword CTA:** `Comment "<KEYWORD>" for guide`, keyword in an accent colour, on screen 100% of the time. Brings in DMs and comments.
3. **Word-stack selection box.** A GSAP list scroll with blur and dim on the inactive items, plus a corner-handle box that snaps to the active word, which then expands into the slogan. Portable to any composition.
4. **Mixed-weight slogan slam** (boxed word + italic connector + heavy slam word + "!") on a flat brand colour.
5. **Counter ticks as micro-payoffs** (364 → 365, prices, distances). A GSAP counter with a scale pop.
6. **No-cut continuity.** Every beat changes through zoom, morph or particles. Maps to `cinematic-zoom`, `transitions-scale`, `transitions-destruction` and `grid-pixelate-wipe` in the registry.
7. **Typed query as the human setup line**, then an ironic or emotional payoff (Netflix: "something to fall asleep to" → 3:22 AM).
8. **Pick transitions from the brand's energy.** Calm brand: blur and dissolve. Playful brand: shatter and slam.
9. **Logo or wordmark resolve with a typed tagline or URL**, held 2–3s.

## Don't copy
- **"✳ Opus 5.5" / the Claude asterisk / "Comment OPUS"** are his specific funnel and model branding. Swap in your own label and keyword.
- **The third-party brand IP** (Netflix, Spotify, Duolingo, Apple, Domino's, an IKEA parody) is his content hook. Making fake ads for real brands carries trademark risk. Use your own products or clearly fictional brands, as he does with SJÄLV.
- The rendered right-panel footage is AI-generated video. HyperFrames can recreate the **chrome, type and UI motion** natively, but photoreal 3D worlds (Find My city, Maps flyover, the SJÄLV lamp) need generated or sourced video clips placed in the right panel.

## Videos studied
- [DfRgEzoN7v-](videos/DfRgEzoN7v-/analysis.md): Find My. Icon → photoreal city → AR wayfinding countdown → keys → icon.
- [DfQToZjNNah](videos/DfQToZjNNah/analysis.md): Duolingo. Streak notification → lesson → 364 → 365 → "Keep the Streak!"
- [DfDZPCTNVQ0](videos/DfDZPCTNVQ0/analysis.md): Apple Maps. Clay-3D Paris drive → Arc de Triomphe → Home → world folds into a card → icon.
- [De_RO_sNvwN](videos/De_RO_sNvwN/analysis.md): "SJÄLV" self-building lamp. Prompt → flat-pack box → self-assembly → extra-screw gag.
- [DezdsQxtJEJ](videos/DezdsQxtJEJ/analysis.md): Netflix. "Something to fall asleep to" → clock stack to 3:22 AM → "Just One More!"
- [DewW90jRVhS](videos/DewW90jRVhS/analysis.md): Domino's. "I need pizza." → one morphing order card → tracker → "Get the door".
- [DeuaPActbwg](videos/DeuaPActbwg/analysis.md): Apple Card. Pastel-sky card → savings data viz → typed " Card". The calmest one.
- [DepiFUht9M3](videos/DepiFUht9M3/analysis.md): Spotify. Dock tap → shatter → rainy-evening search → playlist wall → "Play the Mood!" → particle logo.

**Note on audio:** none of the 8 were transcribed, because the Whisper model download is blocked in this environment. There are no visual signs of a voiceover, so the audio is probably a music bed, but that is unverified.
