# dfss0xtscme — @simar-visuals

**Source:** https://www.instagram.com/reel/DfSS0XtScMe/
**Duration:** 40.51s
**Aspect:** 9:16
**Resolution:** 1080x1920 @ 30fps
**Studied:** 2026-11-05
**Engagement (at time of study):** 386 likes · 21 comments (views not exposed)
**Sample rate:** extracted 81 frames at 2fps; reviewed at 1fps (every 2nd frame, 41 frames) via labeled contact sheets.

> Format note: this is an editor's **portfolio "Before / After"** reel — a small raw "Before" card (left) plays in sync with a larger edited "After" card (right) on a near-black canvas. The analysis below describes the **After** edit (the style being sold). Speaker is a podcast-style guest (on-screen lower-third "Brandon — I help founders build a brand"). Description CTA: DM "Free Edit".

## Hook (0–2s)
- 0.0s: Both cards already on screen. After card: speaker mid-frame over a **collage of b-roll photo tiles** behind him (background replaced/augmented). Centered caption **"Post a 100 videos"** — white bold sans with "100 videos" sitting on a **solid blue-violet highlight block**.
- 0.5–2.0s: tiny dim sub-line types in beneath — "[as quickly as possible]" — in small light sans. Name lower-third ("Brandon / I help founders build a brand") small, left-aligned, under the caption.
- First words: "Post 100 videos as quickly as possible" — the claim IS the hook; no question, no intro.

## Pacing
- Total scenes: ~16 distinct visual beats in 40s
- Average scene length: ~2.5s
- Shortest / longest: ~1.0s (white-flash transition beats) / ~4s (dot-grid calendar 35–38s)
- Distribution feel: medium; talking-head beats alternate with full graphic takeovers every ~3–5s
- Pace accelerates through the "podcast / phone / meta glasses" list (17–21s, a new card per item every ~1.5s) and settles back on the face for the 350-videos payoff.

## Captions
- Style: **phrase chunks, revealed word-by-word**, centered on the chest/lower-middle of the frame.
- Font feel: **two-voice typography** — small, light, tight-tracked sans for filler words ("then you can get", "you wanna keep on"), and a **huge italic condensed serif (Instrument-Serif-like)** or heavy sans for the 1 key word ("*data*", "*testing*", "*your satisfaction*", "*350 videos*", "*Volume*").
- Active-word treatment: key word gets **electric blue-violet color (#4b3cf0-ish)** or a **solid blue-violet highlight rectangle behind it** that wipes in left→right.
- Position: center of frame (mid-chest), never bottom-third.
- Size: filler = small (~3% frame height); key word = large (~8–10%).

## Scene types
1. 0–2.5s talking-head over b-roll photo-collage background + highlight caption + name lower-third.
2. 3s full graphic takeover: black + fire footage, "Your *number* *intention*" editorial serif title, tiny paragraph body copy, social icons — magazine-cover feel.
3. 4–5s b-roll (woman on phone, desaturated) with curved arrow + "*your satisfaction*" in italic serif on blue block.
4. 6–7s talking-head + **animated social-stat counter row** (💬 7k → 13k, ❤ 11k → 45k, 👤 2k → 5k) under "isn't the outcome" — data-feel.
5. 8s talking-head, caption top-right "it's in *posting the video*" on blue block (caption moves to negative space).
6. 9–10s talking-head, background darkened/faded to black, ghosted large word "get there".
7. 11–12s **UI showcase** — Instagram Insights screens (retention curve, skip-rate, top sources bars in magenta) layered over/behind speaker → "then you can get *data*".
8. 13–15s face shrinks into a card; **floating thumbnail collage** of other creators' formats ("talking head" label in yellow) arrives around it.
9. 16s talking-head, small centered caption.
10. 17–21s **editorial cream cards** (#d9d6cc paper) numbered "#001 Podcast", "#002 Phone", "#003 Meta Glasses" — big white-stroke sans title + example clip inset, vertical push between them.
11. 22–23s talking-head + "*testing*" italic serif in blue.
12. 24–27s **data viz**: exponential "Breakout stage" curve (Performance vs Number of videos), dotted line, blue progress bar sweeping, "*Volume*" serif; dim grid of video thumbnails behind.
13. 28–33s talking-head, "350 videos" big blue sans then re-set in italic serif.
14. 34–35s "But many people / just delay the process".
15. 36–38s **dot-grid calendar** (Mon–Sun, blue = video posted, grey = none) under "Most people".
16. 39–40s push-in close-up talking-head (scale ~1.3).

## Transitions
- Flavors observed: hard cuts on the word, **quick white flash frames**, card **scale-down into frame** (face shrinks to reveal graphics), vertical push between numbered cards, background fade-to-black behind the speaker.
- Rotation cadence: rotates; no transition repeats twice in a row.
- Signature: background behind the speaker dims to black so a ghosted word can sit behind/around him.

## Face treatment
- Mode mix: fullscreen talking-head ~60%, face as a shrunken card inside graphics ~15%, full graphic takeovers ~25%.
- Grading: neutral-cool, slightly lifted blacks, soft contrast; background sometimes desaturated.
- Camera motion: subtle punch-ins on emphasis (≈1.1–1.3×), one final push-in.
- Framing: centered medium shot.

## Audio reactivity
- Text pulses on beat: no (word-synced reveals instead)
- Background reactivity: no
- Synced to stress words: yes — every key-word swap lands on the stressed syllable.

## Palette
- `#0c0c0c` near-black canvas (dominant)
- `#4b3cf0` electric blue-violet (accent / highlight block)
- `#ffffff` white text
- `#d9d6cc` warm cream paper (editorial cards)
- `#e0399b` magenta (UI-chart accent, sparing)

## Signature move
**Two-voice captions**: tiny light sans filler + one giant italic-serif or blue-highlighted key word per phrase, placed center-frame.

## What to steal (actionable for Hyperframes builds)
- **Two-voice kinetic captions** — filler words small/light, key word swapped into italic serif (`Instrument Serif` italic) or put on a blue highlight block that wipes in (GSAP `scaleX` from 0, `transformOrigin: left`). Map to a "key-word" flag per caption chunk.
- **Animated stat counters** under a caption (comments / likes / followers ticking up) — easy GSAP `textContent` snap tween; fits any growth/number claim.
- **Numbered editorial cards** (`#001 / #002 / #003`) on cream paper for any list of 3 — rule-of-threes, push transition between them.
- **Background dim-to-black** behind the speaker for a key line (overlay opacity tween), with a ghost word behind.
- **Data-viz beats** (curve, progress bar, dot-grid calendar) for abstract claims — `data-chart` block or hand-built SVG.

## What's creator-specific (don't copy literally)
- The Before/After split-card portfolio framing (it's an editor's ad, not the edit itself).
- The guest's name lower-third, the Instagram Insights screenshots, other creators' thumbnails.
- The "DM Free Edit" CTA.

## Transcript
See `transcript.json` in this folder.
