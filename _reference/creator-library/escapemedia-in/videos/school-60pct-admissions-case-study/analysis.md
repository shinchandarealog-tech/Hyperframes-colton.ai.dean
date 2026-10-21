# school-60pct-admissions-case-study — @escapemedia.in

**Source:** Uploaded file `Video_by_escapemedia.in_Dak-ACwTmxA.mp4` (Instagram Reel, id `Dak-ACwTmxA`)
**Duration:** 16.67s
**Aspect:** 9:16
**Resolution:** 720x1280 @ 30fps
**Studied:** 2026-10-21
**Engagement (at time of study):** n/a (local upload, no info JSON)
**Sample rate:** every extracted frame at 2fps (33 frames). Cut times from ffmpeg scene detection: 2.97s, 5.5s, 9.2s, 11.67s.
**Genre note:** Agency case-study / client-results ad (social-media agency → school client). Not real estate, but the structure carries straight over to property ads: on-location presenter, big result number, proof b-roll, DM CTA.

## Hook (0–2s)
- **0.0s:** Presenter (turban, beige shirt) stands full-body, centred, in front of the client's school building with yellow buses. A huge **red "60" + "%"** is layered *behind* him (depth-composited, so he occludes part of the number) and the digits scale/slide in.
- **0.5s:** Paper **application forms explode outward** from behind him, flying toward camera. "60%" re-centres in solid red (#C8102E-ish) and white word-by-word caption "more admission" types in under him.
- **1.0–1.5s:** The flying forms settle into two "APPLICATION FORM" cards at the top. The **whole frame starts shrinking into a TV screen**, which is the transition into scene 2.
- **First words:** "60% more admission in just 3 months of working." The hook is the result number, said and shown in the first frame.

## Pacing
- Total scenes: 5 (each scene also has several graphic beats inside it)
- Average scene length: ~3.3s
- Shortest / longest: ~2.5s (classroom-montage) / ~5s (CTA)
- Distribution feel: medium scenes, but a new graphic beat lands every ~0.5–0.8s, so it feels fast-chopped
- Pace shift: the white notebook "We created…" scene (5.5–9.2s) is the calmest moment, a breather before the CTA. The CTA itself speeds back up with social-icon pops.

## Captions
- Style: phrase chunks (2–3 words) that **type in letter by letter** ("d m i…" → "admission")
- Font feel: bold rounded geometric sans (Poppins/Montserrat ExtraBold-like), lowercase, white, no stroke, soft drop shadow
- Accent captions: the hero words are **huge red uppercase bold sans** ("SCHOOL", "CLIENT", "60%", "2X") that span the full frame width, placed behind or over the presenter's head
- Mixed sizes: small red lowercase "this is the result" above big white "given to"
- Position: lower-middle (around the waist) for normal captions, upper third for hero words
- Size: medium normal captions; hero words are huge (~90% of frame width)

## Scene types
1. **0–2.97s — Result-number slam over on-location presenter** (kinetic typography slam + depth composite). Red "60%" behind the subject; paper forms burst toward camera; "more admission" caption.
2. **~2–3s — Screen-in-screen transition:** the whole first scene shrinks into a TV on a principal's desk (over-the-shoulder shot of a man in an office watching it). "IN JUST 3 MONTHS" in white + red on the TV. Sells the idea that "the client is watching the result".
3. **2.97–5.5s — Presenter walking toward camera (school wall + buses)**, with a cloud/sky reveal wiping down from the top. Caption "this is the result / given to", then a **letter-by-letter red build of "SCHOOL"** and a hard swap to "CLIENT" (kinetic typography).
4. **5.5–9.2s — Notebook-paper explainer:** off-white grid paper. A red marker **hand-draws an ellipse** around serif text "We created", then three serif columns slide in as a horizontal pan: "Storytelling content / Educational content / Awareness content" (rule of threes). Editorial and calm.
5. **9.2–11.67s — Floating proof-card stack:** presenter (cut out) stands in front of a school bus and grass. Behind and above him, **rounded-corner video cards of the actual delivered content** (student interviews, staff, classroom) cycle in a vertical carousel. Captions "creative way", "right audience". Yellow "WHY WE" label stickers sit inside the cards.
6. **11.67–16.67s — CTA among the buses:** presenter walks between two yellow school buses. A huge red **"2X"** appears behind him, then **3D social icons** (Instagram, Snapchat, X, Threads, Facebook, CapCut) fan out from behind him. Captions "DM us today" and "BOOK your slots". The Instagram card stays parked behind his torso.

## Transitions
- Flavors: screen-shrink into a TV (scene-in-scene), sky/cloud wipe from the top, hard cut to the white paper, a blur/fade into the card stack, a hard cut to the CTA
- Rotation: no transition repeats
- Signature: the **zoom-out-into-a-screen** reveal, where the scene you just watched turns into footage someone in the story is watching

## Face treatment
- Mode mix: full-body presenter, always centred, always on location (the client's premises). No face close-ups.
- Grading: bright, airy, slightly warm, lifted shadows, clean blue skies
- Camera motion: presenter walks toward camera (handheld gimbal push). Subtle punch-ins.
- Presenter is **rotoscoped** so that graphics can sit behind him (depth layering is the main trick)

## Audio reactivity
- Text slams land on the stressed syllable ("SIXTY", "SCHOOL", "CLIENT", "TWO-X")
- Background music bed plus whoosh SFX on the form explosion and icon pops (inferred from the motion; music not isolated)

## Palette
- `#D0121B` brand red: dominant accent, used for all hero words
- `#FFFFFF` white: captions
- `#F2F0F2` off-white grid paper: explainer scene background
- `#F2C21B` school-bus yellow: environment, which they lean into for the CTA
- `#8DB8E0` sky blue: environment

## Signature move
Giant red result-number typography composited **behind** a full-body on-location presenter, so the subject stands "inside" the stat.

## What to steal (actionable for Hyperframes builds)
- **Depth-sandwich hero number:** background plate → giant stat text → rotoscoped presenter (alpha matte / segmented PNG sequence or a `.webm` with alpha) → captions. In Hyperframes: three stacked layers with `data-track-index`; stat text animated with GSAP `scale: 1.4→1, opacity 0→1, ease: "expo.out"` over 0.4s.
- **Burst-toward-camera props:** for real estate, swap application forms for keys, floor-plan sheets or "SOLD" cards flying out of the frame centre. GSAP `z`/`scale` from 0.2→2 with a stagger of 0.03 and a seeded random rotation.
- **Scene-shrinks-into-a-TV transition:** scale the whole prior scene into a screen rect inside the next plate. For real estate: the listing walkthrough shrinks into a phone held by a buyer.
- **Letter-by-letter red word build** ("S-C-H-O-O-L") with each letter popping on a beat. Easy with SplitText-style per-char spans.
- **Notebook explainer card** with a hand-drawn marker ellipse (SVG `stroke-dashoffset` draw) plus three serif columns: perfect for "3 reasons to buy this home" or a "3BHK / 2 parking / pool" amenity list.
- **Floating rounded-card carousel of proof footage** behind the presenter. Use it for room-by-room clips of the property.
- **CTA with 3D social icons fanning out** behind the presenter, plus "DM us today" and "BOOK your slots" (for real estate: "Book a site visit").

## What's creator-specific (don't copy literally)
- The @escapemedia.in agency branding, the specific school (Chandigarh), and their red as a brand colour. Use the user's own brand-tokens.
- The specific client footage inside the cards.

## Transcript
See `transcript.json` in this folder. Clean English and accurate (the "DMS today" token is "DM us today").
