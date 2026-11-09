# AURAVEDIC HAIR GROWTH SERUM: "IT STARTS AT THE ROOT"
### 30s · 9:16 · AI-generated in Google Flow (Veo) · edited in HyperFrames

---

## 1. The vision

**One idea:** hair fall is a root problem, and Auravedic goes to the root.

Every visual moves *downward into the scalp* and then *back up as fuller hair*. The drop falls, the serum sinks, the roots glow, the hair rises. That vertical motion is the spine of the film.

**Why this gets leads, not just views:**

| Lead lever | How the film uses it |
|---|---|
| **Scroll-stop in 1s** | Open on the most relatable, slightly uncomfortable image there is: a palm full of fallen hair. Every woman watching has seen this in her own hand. No logo, no product, just recognition. |
| **Name the fear** | The mirror shot with the widening parting. Specific beats generic. |
| **Reveal fast** | The product lands by 5.5s. Ads that hide the product past 6s bleed viewers before the brand registers. |
| **Make it believable** | Real ingredient names on screen (Rosemary, Bhringraj, Anagain, Procapil) plus a mechanism shot. Viewers buy what they understand. |
| **Callback payoff** | The result shot returns to **the same mirror, same parting**, now full. Before/after without saying "before/after". |
| **Clear ask** | The last 3s are a still packshot, URL and CTA. Held long enough to read, screenshot or tap. |

**Look and feel:** "warm amber luxury". Dark espresso/amber shadows, honey-gold liquid light, soft cream type. Premium Ayurveda, not clinical, not cartoon. It sits between their cinematic Onion ad (polish) and the Serum mascot ad (same product, same ingredient story), so it reads as *their brand, upgraded*.

**Palette:** espresso `#1a0f08` · amber `#7a4a1e` · liquid gold `#e8b54a` · cream `#f3e6cf` · rosemary green `#5c7a4a` (ingredient beat only)

---

## 2. Before you generate: Flow settings

1. **Model:** Veo 3.1, **Quality** mode for anything with a face or the product. Fast mode is fine for macros and test passes.
2. **Aspect ratio:** **9:16 portrait** on every clip.
3. **Generate 2–4 variations per prompt** and pick the best. I only need **2–4 seconds** from each 8s clip, so the best moment wins, not the best whole clip.
4. **Audio:** Flow will generate sound. Ignore it, because I'm building the whole sound design in the edit. Still keep "no music, no dialogue" in the prompts so the visuals don't drift into people talking.
5. **Product shots (P1, P2, P8):** use **Ingredients to Video** and upload `serum-product-ref.png` (in this folder) as the product ingredient. If the label still comes out warped or garbled, **don't keep re-rolling**. Send me the clip anyway: I'll composite the real label/bottle over it in the edit. A *clean, well-lit* clip matters more than a perfect label.
6. **Our model (the woman):** generate her once as an image (prompt **C0** below), then upload that image as an ingredient for **every shot she appears in** (S2, S6, S9a, S9b). That's how we keep the same face across the film.
7. **No text in clips.** Veo sometimes invents captions or signs. If a variant has random text, discard it. All typography is added by me.
8. **Naming:** export as `S1_v1.mp4`, `S1_v2.mp4`… so I can match them to the timeline.

---

## 3. The edit timeline (what you're generating for)

| # | Time | Duration | Visual | On-screen type (added by me) | Source |
|---|---|---|---|---|---|
| S1 | 0.0–2.0 | 2.0s | Palm full of fallen hair | **"STILL FINDING THIS EVERY MORNING?"** | AI |
| S2 | 2.0–4.0 | 2.0s | Woman in mirror, worried, parting | **THIN. → WEAK. → FALLING.** (staggered) | AI |
| T1 | 4.0–5.5 | 1.5s | Gold particle type on espresso | **"IT STARTS AT THE ROOT."** | Motion graphics |
| P1 | 5.5–8.5 | 3.0s | Serum bottle hero reveal | *auravedic* (small) | AI + real label |
| S5 | 8.5–11.0 | 2.5s | Dropper, golden drop, slow-mo | — | AI |
| S6 | 11.0–13.5 | 2.5s | Drop lands on parting, massage | — | AI |
| S7 | 13.5–17.5 | 4 × 1.0s | Rosemary · Bhringraj · Anagain · Procapil | Ingredient name per beat, gold ring | AI (4 clips) |
| S8 | 17.5–20.5 | 3.0s | Scalp cross-section, roots glow | **"FEEDS THE ROOT"** | AI |
| S9 | 20.5–24.5 | 4.0s | Result: same mirror (callback) + hair flip | — | AI (2 clips) |
| T2 | 24.5–27.0 | 2.5s | Gold kinetic type | **STRONGER ROOTS. / FULLER HAIR.** | Motion graphics |
| P2 | 27.0–30.0 | 3.0s | Packshot + gold ribbon | **auravedic.com · SHOP NOW** + offer | AI + real label |

**Transitions** (all done in the edit, following the client's own references): vertical whip-blur down into P1, zoom-blur into each ingredient, a gold flash into the result, and a particle dissolve into the packshot. No plain hard cuts.

---

## 4. The prompts (copy-paste into Flow)

> Every prompt already includes the camera, light, lens and "no text" instructions. Paste as-is.

---

### C0. Character image (generate as an IMAGE first)
```
Photorealistic portrait of a 26-year-old Indian woman, warm medium-brown skin, natural soft makeup, long dark brown hair worn loose with a centre parting, wearing a simple cream silk camisole. Soft warm window light from the left, neutral warm beige background. Shot on 85mm lens, shallow depth of field, editorial beauty photography, natural skin texture with visible pores, no retouching look. Front-facing, calm neutral expression. Vertical 9:16 framing, head and shoulders. No text, no logos, no jewellery except tiny gold stud earrings.
```
→ Pick the best one and save it as **`model-ref.png`**. Use it as an ingredient in S2, S6, S9a and S9b.

---

### S1. The hook: palm of fallen hair *(Text to Video)*
```
Extreme close-up macro shot of a woman's open palm, slowly uncurling her fingers to reveal a tangled clump of long dark brown fallen hair strands resting in her hand. Tiny water droplets on the skin, as if just out of the shower. Soft, slightly cool bathroom light from above with a warm rim light. Shallow depth of field, background is a blurred white-tiled bathroom. Slow, deliberate movement. The camera slowly pushes in. Photorealistic, cinematic, 100mm macro lens, high detail on individual hair strands. Vertical 9:16. No text, no subtitles, no music, no dialogue.
```
*Use the moment the fingers finish opening.*

---

### S2. The fear: mirror and parting *(Ingredients to Video, with `model-ref.png`)*
```
The woman from the reference image stands close to a bathroom mirror, seen over her shoulder and reflected in the mirror. She uses both hands to part her hair at the centre and leans in to examine her scalp, which shows a slightly widened, thin centre parting. Her expression is quietly worried, with a small frown. Soft warm morning light from a side window, slightly desaturated mood. Slow handheld push-in toward the mirror reflection. Photorealistic, cinematic, 50mm lens, shallow depth of field. Vertical 9:16. No text, no subtitles, no music, no dialogue.
```

---

### P1. Product hero reveal *(Ingredients to Video, with `serum-product-ref.png`)*
```
The exact amber glass dropper bottle from the reference image, label unchanged, stands on a dark polished stone pedestal in a dark espresso-brown studio. A thin layer of golden liquid ripples outward across the stone surface around the base of the bottle. A warm golden rim light slowly sweeps from left to right across the glass, making the amber bottle glow from within. Tiny golden dust particles float in the air. Slow cinematic push-in, starting slightly low and rising to eye level. Luxury cosmetics commercial, photorealistic, 85mm lens, high contrast, deep shadows, honey-gold highlights. Vertical 9:16. No added text, no extra logos, no music, no dialogue.
```
*If the label warps: re-roll once, then send me the best-lit version anyway.*

---

### S5. The golden drop *(Ingredients to Video, with `serum-product-ref.png`, or Text to Video)*
```
Extreme macro slow-motion shot of a glass dropper pipette being lifted out of an amber glass bottle. A single thick drop of golden-amber serum forms at the tip, stretches, and falls in ultra slow motion, catching a warm backlight that makes it glow like liquid gold. Pure dark espresso-brown background with soft golden bokeh. Shot at 240fps, 100mm macro lens, shallow depth of field, photorealistic, luxury beauty commercial lighting. Vertical 9:16. No text, no music, no dialogue.
```

---

### S6. Drop meets scalp *(Ingredients to Video, with `model-ref.png`)*
```
Top-down macro close-up of a woman's centre hair parting on long dark brown hair. A single glowing golden drop of serum falls from above in slow motion and lands precisely on the scalp at the parting, spreading slightly. Her fingertips, with natural nude nails, then enter the frame and gently massage the serum into the scalp in small circles. Warm golden side light, soft bokeh background, natural skin and hair texture, photorealistic, 100mm macro lens. Vertical 9:16. No text, no music, no dialogue.
```

---

### S7. Ingredient beat: 4 short clips *(Text to Video)*
Generate all four with the **same lighting phrase** so they cut together seamlessly. I'll use about 1 second of each and add the ingredient name in gold type with a ring.

**S7a. Rosemary**
```
Macro shot of a fresh sprig of rosemary with tiny pale-blue flowers, slowly rotating in mid-air against a dark espresso-brown background. Tiny droplets of golden oil cling to the needles and glint in a warm golden rim light. Soft golden bokeh particles float around it. Slow cinematic orbit. Photorealistic, 100mm macro lens, shallow depth of field, luxury commercial lighting. Vertical 9:16. No text, no music, no dialogue.
```
**S7b. Bhringraj**
```
Macro shot of fresh green bhringraj (false daisy, Eclipta alba) leaves with a small white daisy-like flower, slowly rotating in mid-air against a dark espresso-brown background. Tiny droplets of golden oil glint on the leaves in a warm golden rim light. Soft golden bokeh particles float around it. Slow cinematic orbit. Photorealistic, 100mm macro lens, shallow depth of field, luxury commercial lighting. Vertical 9:16. No text, no music, no dialogue.
```
**S7c. Anagain (pea sprout extract)**
```
Macro shot of tender fresh green pea sprouts with curling tendrils, slowly rotating in mid-air against a dark espresso-brown background, glowing softly as if lit from within. Tiny droplets of golden oil glint in a warm golden rim light. Soft golden bokeh particles float around it. Slow cinematic orbit. Photorealistic, 100mm macro lens, shallow depth of field, luxury commercial lighting. Vertical 9:16. No text, no music, no dialogue.
```
**S7d. Procapil (the active complex)**
```
A glowing translucent golden molecular structure, spheres connected by thin light bonds, slowly rotating in mid-air against a dark espresso-brown background, inside a single floating drop of golden serum. Warm golden rim light, soft golden bokeh particles. Slow cinematic orbit. Photorealistic 3D scientific beauty-commercial render, shallow depth of field. Vertical 9:16. No text, no music, no dialogue.
```

---

### S8. The mechanism: roots wake up *(Text to Video)*
```
Photorealistic 3D cross-section of human scalp skin, cutaway side view showing layers of skin and hair follicles with dark hair strands growing up out of the surface. Golden glowing serum flows across the scalp surface and seeps down into the follicles. As it reaches each root, the hair bulb lights up with a warm golden glow and the hair strands above visibly thicken and grow upward. Slow camera dolly from left to right. Warm amber and gold colour palette on a dark background, high-end beauty commercial medical visualisation style, cinematic lighting. Vertical 9:16. No text, no labels, no music, no dialogue.
```

---

### S9a. The callback: same mirror, full parting *(Ingredients to Video, with `model-ref.png`)*
```
The woman from the reference image stands at the same bathroom mirror, seen over her shoulder and reflected in the mirror. She parts her hair at the centre with her fingers and looks closely. Her hair is now thick, dense and glossy with a full, healthy-looking parting. Her expression slowly changes into a soft, confident, genuine smile. Warm golden morning sunlight now fills the bathroom. Slow handheld push-in toward the mirror reflection. Photorealistic, cinematic, 50mm lens, shallow depth of field. Vertical 9:16. No text, no subtitles, no music, no dialogue.
```
*This is the emotional payoff. Generate 4 variations and pick the best smile.*

**S9b. Hair flip *(Ingredients to Video, with `model-ref.png`)***
```
The woman from the reference image, in a cream silk camisole, turns toward the camera with a slow-motion hair flip. Her long, thick, glossy dark brown hair swings and catches warm golden-hour backlight, with individual strands shining. She ends looking over her shoulder into the lens with a confident smile. Warm beige background with soft window-light shadows. Shot at 120fps slow motion, 85mm lens, shallow depth of field, luxury haircare commercial, photorealistic. Vertical 9:16. No text, no music, no dialogue.
```

---

### P2. Final packshot *(Ingredients to Video, with `serum-product-ref.png`)*
```
The exact amber glass dropper bottle from the reference image, label unchanged, stands centred on a dark polished stone pedestal. A smooth ribbon of liquid golden serum spirals gracefully around the bottle from bottom to top and then dissolves into tiny floating golden droplets. A fresh rosemary sprig and a few green bhringraj leaves rest at the base of the pedestal. Dark espresso-brown background with a soft warm golden glow behind the bottle. The camera is locked off and still. Luxury cosmetics commercial, photorealistic, 85mm lens, high contrast, honey-gold highlights. Leave empty space in the lower third of the frame. Vertical 9:16. No added text, no extra logos, no music, no dialogue.
```
*"Empty lower third" is deliberate. That's where the URL and CTA go.*

---

## 5. Checklist: what to send me

- [ ] `model-ref.png` (C0)
- [ ] S1, S2, P1, S5, S6
- [ ] S7a, S7b, S7c, S7d
- [ ] S8, S9a, S9b, P2
- [ ] Best 1–2 variations of each (14 clips minimum)

Upload them to one Google Drive folder and send me the link. I'll pull them straight in.

**Need from the client before the final render** (doesn't block the edit):
- Current **offer** for the end card (e.g. "Flat 20% off · Code ROOTS20"), or I'll use a neutral "Shop now at auravedic.com"
- Confirmation we can say **"Rosemary · Bhringraj · Anagain · Procapil"** on screen (it's on their label, so this should be fine)
- Watermark text (parked for now)

**Claims guardrail:** no "100% regrowth", "clinically proven" or "results in X days" unless Auravedic gives us that claim in writing. "Stronger roots. Fuller hair." is a safe, Meta-compliant tagline.

---

## 6. Voiceover: yes, short and intimate

**Voice:** female, late 20s to early 30s, warm and close to the mic, like a friend, not an announcer. Hushed and empathetic on the hook, confident by the CTA. About 55 words in 30s, leaving room to breathe.

| Time | English | Hinglish |
|---|---|---|
| 0.0–2.0 | Still finding this… every morning? | Roz subah… yehi dekhti ho? |
| 2.0–4.0 | Thin. Weak. Falling. | Patle. Kamzor. Jhadte baal. |
| 4.0–5.5 | The truth? It starts at the root. | Asli problem? Jadon mein hai. |
| 5.5–8.5 | Auravedic Hair Growth Serum. | Auravedic Hair Growth Serum. |
| 8.5–13.5 | Just a few drops, massaged into your scalp. | Bas kuch drops, scalp pe halke haathon se massage. |
| 13.5–17.5 | Rosemary. Bhringraj. Anagain. Procapil. | Rosemary. Bhringraj. Anagain. Procapil. |
| 17.5–20.5 | Going deep, to feed every root. | Seedha jadon tak, har root ko nourish kare. |
| 20.5–24.5 | *(no VO: music swells, let the smile land)* | *(no VO)* |
| 24.5–27.0 | Stronger roots. Fuller hair. | Strong roots. Fuller hair. |
| 27.0–30.0 | Shop now at auravedic.com. | Abhi order karein, auravedic.com pe. |

**How to record:** ElevenLabs (best Hindi/Hinglish voices; export WAV), or record on your phone in a quiet room with soft furnishings, 15cm from the mouth, 3 takes. I'll clean it, time it to the cuts and mix it over the music.

## 7. What I build in the edit (so you know what *not* to generate)

- All kinetic typography: the hook line, THIN/WEAK/FALLING, IT STARTS AT THE ROOT, ingredient names, STRONGER ROOTS/FULLER HAIR, URL/CTA
- Real-label composite on P1/P2 if Veo warps it
- Transitions: whip-blur, zoom-blur, gold flash, particle dissolve
- Grade: unify every clip to the amber/espresso palette, plus subtle grain
- Sound: low cinematic pulse, a whoosh on each transition, a liquid "drip" on the drop, a riser into the result, and a soft impact on the packshot
- Watermark at 12% opacity (when you give me the text)
