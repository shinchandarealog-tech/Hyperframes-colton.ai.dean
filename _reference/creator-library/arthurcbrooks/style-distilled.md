# @arthurcbrooks — Style Fingerprint

Rolled up across 4 videos (17.8s, 37.9s, 72.6s, 150s). See `videos/*/analysis.md` for per-video detail. Last distilled: 2026-11-02.
Studied with the method from the `premium-minimal-edit` tutorial: transcript plus frame-by-frame breakdown, looking at **placement** (where in the script), **composition** (what it's made of) and **animation logic**.

> Use together with `.claude/skills/premium-minimal-edit/SKILL.md`. The skill explains how to build the style; this file shows what the real channel does.

## Signature moves (consistent across all 4)

- **Hook pattern:** a visual in the first 1s. Either open straight on a painting or b-roll with the thesis word (bored., masters, "If you're a natural grinder"), or meet the face for 0.5s and cut to art on the first loaded noun. Never a title card, never a logo.
- **Caption system (the core):**
  - White on footage. Center or lower-middle, over the chest, **never at the bottom edge**.
  - **1 hero word per phrase at 2–3x size**, satellites very small (≈20–30% of hero size), tucked tight above/below/beside it.
  - **Font by meaning:** concrete nouns/facts → **bold sans** (Inter/Helvetica 700–800); emotion/abstract/name words → ***serif italic*** (Playfair Display italic 700). One reel (DXcF) runs sans-only, so the serif is optional per client.
  - Words build **one at a time in fixed positions** (no re-flow, no karaoke color swap).
  - No stroke, no pill, no box. Legibility comes from placement + a soft shadow.
- **Color rule:** text is **white on footage, blue on white**. Blue = one saturated royal/electric blue (#1F4FD8–#0A47FF). It appears only on white/paper cards, flat blue cards, graph lines, timeline markers, circle callouts and name boxes. One-off accents (orange "working", yellow highlighter, deep red) are used **once per video** at most.
- **Cut rhythm:** hard cuts **on the stressed word**. A cutaway every 1.5–3s; A-roll never runs more than ~6s without one. Destinations rotate: A-roll → painting → b-roll → card → graphic.
- **Face treatment:** fullscreen 9:16 only, 2–3 crops (wide/medium/tight) rotated like multi-cam. Never bottom-half or PiP. Grade follows the source shoot (black studio / moody atrium / warm interview).
- **Energy profile:** breathing. Fast around lists and claims, slow on emotional lines, a clean ending (summary card or "Thank you") with no CTA graphics.
- **Endings:** either a **blue-on-white summary card** ("That's how to *think* about it."), a **painting** bookend, or A-roll with a serif "Thank you".

## Scene-choice logic observed (script → scene)

| Script moment | What the edit shows |
|---|---|
| Thesis / loaded abstract noun ("masters", "bored", "waste", "balance") | **Painting** (classical or AI-classical) that literally depicts it + giant hero word |
| Concrete example / scenario ("woman with a mug", "running", "gym") | Cinematic b-roll / film still, often B&W with grain |
| List of 3 ("wonderful, beautiful, generative" / "physical, skills, spiritual") | One cutaway per item, 0.5–1s each; or the **kaleidoscope shard** list |
| A number, growth, "progress" | **White paper graph**, blue line climbing out of frame |
| "Studies show / experiment" | **Flat blue claim card** → **research paper with yellow highlighter sweep** |
| A named person | **Name callout**: photo + curved line + name on a blue box |
| Speaker's own history | **Polaroid collage on white** + **life timeline** with a blue marker |
| A question the audience asks | Recreated **phone UI** (DM bubble typing) |
| A quote / turning point | **Blue radial card with big quotation marks** |
| Emphasis pause after a big claim | **Breath card**: pure black or white, ONE serif word, 0.5–1s |
| Lesson / "this is your teacher" | **Rounded inset b-roll on black** (intimate) |
| Speaker addresses "you" | Reverse shot of the interviewer / the audience |

## Animation library (reusable; timestamps point into the source videos)

| # | Animation | Where seen | Duration | Build notes (HyperFrames) |
|---|---|---|---|---|
| A01 | Painting + giant hero word | DQpr 1.0, DP7e 4.0, DXcF 0.0, 69.0 | 0.8–3s | full-bleed img, slow scale 1.00→1.04, hero word fades in + 6px blur→0 |
| A02 | Breath card (one serif word on black/white) | DQpr 8.5, 11.0 | 0.5–1s | solid bg, Playfair italic, fade 0.15s |
| A03 | Blue serif on white paper card | DQpr 5.5, DP7e 22.0, 37.0 | 1–1.5s | paper grain, words appear in fixed slots |
| A04 | Paper graph, blue line climbs out of frame | DP7e 11.0 | 2s | SVG polyline dash draw, `power2.inOut`, keyword in blue serif |
| A05 | Ghost/echo word ("backwards") | DP7e 5.0 | 1s | 3–4 text copies, x-offset, opacity 0.6→0.1 |
| A06 | Grainy B&W halftone b-roll + play/pause icon | DP7e 14.0–16.9 | 3s | `grayscale(1) contrast(1.4)` + noise overlay + SVG icon pop |
| A07 | Kaleidoscope triangle shards w/ paintings + chrome star | DP7e 24.5–28.4 | 4s | triangle `clip-path` masks rotate between states; star SVG with metallic gradient |
| A08 | Split-screen stacked paintings | DP7e 21.5 | 0.5s | two 1080x960 halves |
| A09 | Fixed-slot word reveal (sans) | DXcF throughout | per phrase | pre-laid phrase, per-word opacity at transcript time |
| A10 | Flat electric-blue claim card | DXcF 5.5, 48.0 | 1–2s | #0A47FF, white sans, hero bold |
| A11 | Pink light-leak flash card | DXcF 6.5 | 0.5s | gradient + blur, vertical type fragment |
| A12 | Red anatomical silhouette with glowing nerve lines | DXcF 22.0 | 3s | dark silhouette on #8B0E0A, SVG paths draw with glow |
| A13 | Name callout (curved line + blue name box) | DXcF 32.5 | 1s | SVG path draw → box `scaleX` grows with the text |
| A14 | Research paper + yellow highlighter sweep | DXcF 50.5 | 4.5s | highlight bars `scaleX` 0→1 line by line, origin left |
| A15 | Polaroid drop-in collage on white | Dc1F 2.5, 6.0–9.4, 23.0, 27.0 | 1–3s | `from({y:-60, rotation:-10})`, `back.out(1.4)`; inactive cards dim |
| A16 | Role carousel ("I'm a professor / author / podcaster") | Dc1F 6.0–9.4 | 3s | active label blue + bold, others grey |
| A17 | Recreated Instagram profile + Follow click | Dc1F 12.0 | 2.5s | HTML UI, cursor, button state change, DOF blur |
| A18 | DM bubble typing out a question | Dc1F 19.0 | 3.5s | typewriter in a blue bubble, blurred UI |
| A19 | Hand-drawn glowing circle around a person in a photo | Dc1F 24.0, 109.5 | 1.5s | SVG ellipse dash draw, slight wobble |
| A20 | Life timeline with sliding blue marker (canvas + A-roll overlay) | Dc1F 35.5–38, 51.5–56, 77, 127–130 | recurring | `.track` pans by tick spacing; small-caps labels |
| A21 | Form-field label stamp ("OCCUPATION: MUSICIAN") | Dc1F 62.0 | 1s | blue highlight on small caps |
| A22 | Postage-stamp-edged photo | Dc1F 70.5 | 1.5s | perforated `mask-image` border |
| A23 | Blue radial quote card with big quotation marks | Dc1F 84.5 | 1.5s | radial gradient #1F4FD8→#05070F, quotes scale in |
| A24 | Rounded-corner inset b-roll on black | Dc1F 95–97.5 | 2.5s | `border-radius:48px`, 88% frame |
| A25 | Book-cover flick montage | Dc1F 138–140 | 2s | perspective tilt, DOF blur, quick cuts |
| A26 | Hold one hero word across a 3–4 clip montage | Dc1F 144–148, DXcF 69–72 | 3s | caption layer persists while clips cut under it |
| A27 | Punch-in zoom inside a b-roll on the thesis word | DQpr 12.0 | 0.5s | scale 1→1.6 on the wrapper |

## What to steal (ranked by HyperFrames copy-ability)
1. The **caption system** (hero word + satellites, font-by-meaning, fixed-slot reveal). Pure HTML/GSAP, works on every client clip.
2. **Breath cards** and **blue-on-white summary cards**. Trivial to build, instantly "premium".
3. **Painting + hero word** cutaways (public-domain art from Wikimedia Commons).
4. **Paper graph** and **life timeline**. SVG line draws, very reusable.
5. **Evidence beat** (blue claim card → highlighted research paper).
6. **Polaroid collage + role carousel** for "who is this person" intros.
7. Name callout, circle callout, quote card, rounded inset b-roll.
8. Kaleidoscope shards and red anatomical illustration. Higher effort; save for hero moments.

## Don't copy
- Copyrighted film clips (*Pursuit of Happyness*, *The Social Network*, *Spider-Man*, Chalamet films). For client work use licensed stock or public-domain footage.
- Arthur's personal photos, books, institutions, Instagram UI, his "Hi friends" opener.
- His shoot look (black studio, atrium) comes from the client's footage, not something we add.

## Videos studied
- [DQprSK3DQd7](videos/DQprSK3DQd7/analysis.md): "Real masters practice true gratitude", 18s, paintings + breath cards, fastest cut
- [DP7eSmPADaD](videos/DP7eSmPADaD/analysis.md): "Natural grinders / progress is everything", 38s, paper graph, kaleidoscope list, blue end card
- [DXcF2jhDCFP](videos/DXcF2jhDCFP/analysis.md): "You need to be bored", 73s, sans-only fixed-slot captions, research-paper evidence beat
- [Dc1F2ouMU8w](videos/Dc1F2ouMU8w/analysis.md): "Hi friends, my name is Arthur Brooks", 150s, origin story, Polaroid collage + life timeline
