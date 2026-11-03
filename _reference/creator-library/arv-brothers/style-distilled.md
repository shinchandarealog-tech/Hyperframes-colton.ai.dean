# @arv-brothers — Style Fingerprint

Rolled up across 4 videos (2 showroom bike reviews, 1 sponsored oil explainer, 1 workshop service explainer). See `videos/*/analysis.md` for per-video detail. Last distilled: 2026-11-03.

These are the client's chosen reference videos for an automotive/bike content account.

## Storytelling formula (consistent across all 4)

```
HOOK (0–5s)       Big keyword/number BEHIND the host's head, new word every ~1s
                  → number (1222cc) | scarcity (LIMITED 100) | topic (E20 PETROL) | season (WINTER SERVICE 4)
                  Optional: fear/relatable AI skit cutaway (red smoke, regret guy)
BODY              One spoken fact = one shot = one text card, 1.5–3s each
                  Chapters: Engine → Safety → Suspension → Tech → Wheels → Practical (tank/seat/weight/top speed)
                  Each chapter opens on the host with a header word behind his head,
                  then runs macro/AI/ride shots with spec cards
RE-HOOK           Every ~15–20s cut away to an AI cinematic ride or CGI explainer
RECAP (~80%)      Fast 1s-per-feature montage OR split-strip collage (callback)
PAYOFF            Price/brand reveal in a colour used nowhere else (lime 8.23 / white-gold 9.73 / lime CASTROL ACTIV)
CLOSE             10–20s uncut sincere talk to camera, no text → "DESCRIPTION" / "COMMENT" / "FOLLOW" card
```

## Signature moves
- **Hook pattern:** text-behind-subject keyword slam at 0.0s, then a second keyword at ~1.0s, then a breath or a third word. No intro, no logo, no greeting.
- **Caption treatment:** **keyword cards, never subtitles.** Ultra-condensed bold sans, ~10–15° italic slant, chrome gradient fill, dark drop shadow, colored outer glow. Two-line stacks with a smaller subline (white sans or handwritten script).
- **Text animations (ranked by frequency):**
  1. Letter-scatter assemble (letters drift in from random 3D positions, then lock and glow), ~0.45s
  2. Blur-to-sharp scale pop, ~0.3s
  3. Horizontal whip-slide with motion blur; consecutive words push each other
  4. Letter-by-letter typewriter build (acronym → full name)
  5. Underline swipe, marker arrow/circle draw-on, callout box with leader line
- **Colour logic:** 2 workhorse colors + 1 payoff color.
  - Showroom reviews: gold chrome (benefits) + ice cyan (specs) + lime (price)
  - Workshop explainers: red (parts/warnings) + white (explanations) + ice cyan (winter)
  - Sponsored: re-skinned to the brand (lime + cyan for Castrol)
  - Chapter headers can each get their own accent (cyan / red / violet / orange)
- **Transition rotation:** hard cuts on the spec beat (90%+). Light-leak / glitch / ink-splash / flash only at chapter changes.
- **Face treatment:** full-screen talking head, 30–55% of runtime. Extreme low angles, wide lens, host leaning into camera and always touching the bike. Sunglasses, expressive hands and faces.
- **B-roll stack:** (a) handheld macro of the exact part being named, (b) action/360 cam ride footage (low swingarm mount, invisible-selfie-stick fisheye), (c) **AI-generated cinematic riding** (golden hour coastal roads) and **CGI explainers** (cutaways, exploded views, part renders in a navy starfield), (d) key-turn → TFT boot POV.
- **Energy profile:** front-loaded and sustained. High from 0 to ~85%, then a deliberate slow, sincere close.
- **Average shot length:** ~2.0–2.3s (all four videos).

## Palette (observed across most videos)
| Role | Hex | Notes |
|---|---|---|
| Gold chrome headline | `#F5C800` (gradient `#FFF6D0 → #F5B400 → #B86A00`) | reviews |
| Ice cyan spec | `#39D5F5` + glow | all |
| Red warning/part | `#E0162B` | workshop |
| Lime payoff | `#B8FF1A` / `#C8FF00` | price / brand |
| Navy CGI bg | `#0B1A33` | AI part cards |

## What to steal (ranked by Hyperframes copy-ability)
1. **Keyword card system with 2+1 colours.** Pure CSS/GSAP; build it as a reusable `spec-card` sub-composition with props `{word, sub, voice: gold|cyan|red|lime, anim: scatter|pop|whip|type}`.
2. **Letter-scatter assemble.** Per-letter spans, seeded PRNG offsets (determinism rule), `power3.out`, then a glow tween.
3. **Spec + subline lockup** (big value + small white/script descriptor).
4. **Text-behind-subject.** Needs a pre-rendered person alpha matte (rembg/RVM/SAM2 → VP9-alpha webm or PNG seq) layered above the text track. This is the biggest look-maker, so budget time for the matte.
5. **Part card in starfield** (navy radial gradient + seeded stars + part PNG rotate/zoom + red acronym + typed full name).
6. **HUD stat plates** (racing-game number plate with red slash; red LED digits in a chrome pill).
7. **Marker annotations and callout boxes** (SVG draw-on).
8. **Recap montage / split-strip collage** before the payoff.
9. **Chapter transitions** from the registry: `light-leak`, `glitch`, `flash-through-white`, re-tinted.
10. **Lead-gen outro** for local businesses (phone strip, location shot, appointment, closed day, "Part 2?").

## Don't copy
- ARV Brothers' host persona, shop, phone number, showroom names, meme stickers ("bhai sahabbb")
- Their typos on cards (BOSCHE, DISCRIPTION, SPOKE WHEELE, 17INCH FRONT): proofread every card
- Leaving AI-generator sparkle watermarks visible on AI shots
- Sponsor (Castrol) claims and branding unless it's actually the client's sponsor

## Production notes for the editor
- Most of the "look" is **text design + timing**, not camera work. The client's footage only needs: (1) host talking-head takes at low angles, (2) a macro of every part he names, (3) some ride footage. AI cinematic rides and CGI explainers can be generated separately.
- Write the edit as a **spec list first**: every line of the VO maps to exactly one card and one shot.
- On-screen text is English even when the VO is Hindi. Keep that bilingual split if the client's audience is Indian.

## Videos studied
- [Dd6LYV2hYpr](videos/Dd6LYV2hYpr/analysis.md): Brixton Cromwell 1200 (grey) spec walkaround; gold/cyan cards, letter-scatter, real 360-cam rides + AI rides, lime price
- [Dds-z4GhTAe](videos/Dds-z4GhTAe/analysis.md): Brixton Cromwell 1200X limited edition; per-chapter header colors, spec + script sublines, callout boxes, split-strip collage
- [DfIDBcttx84](videos/DfIDBcttx84/analysis.md): E20 petrol → Castrol Activ sponsored explainer; heavy CGI engine cutaways, palette re-skinned to sponsor
- [wa-20261103-0008](videos/wa-20261103-0008/analysis.md): winter service: 5 sensors workshop explainer; starfield part cards, red acronyms, lead-gen outro with phone number
