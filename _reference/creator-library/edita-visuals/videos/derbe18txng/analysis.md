# derbe18txng — @edita.visuals ("The most powerful business tool: social media")

**Source:** https://www.instagram.com/reel/DerbE18txNg/ (uploaded file, not downloaded)
**Duration:** 36.55s
**Aspect:** 9:16
**Resolution:** 720x1280 showcase; inner edit card ≈ 360x642
**Studied:** 2026-10-29
**Engagement (at time of study):** n/a (local upload)
**Sample rate:** every frame at 2fps (73 frames) via contact sheets, storyboard at 1fps (first 20s), a 10fps strip across 5.7–6.7s, and a spectrogram.

## Wrapper
The standard @edita.visuals before/after showcase (see `../det-wsmtgue/analysis.md`).

## Hook (0–2s)
- 0.0: Creator at a Shure mic, light grey wall, natural daylight. Caption "I THINK THE MOST" in small **thin all-caps sans**.
- 0.5: "**POWERFUL**" in **lime-yellow (#D7F542) bold italic serif** with a soft glow.
- 1.0–1.5: "**BUSINESS TOOL**" in lime italic serif with a **lime underline swoosh**.
- 2.0: A white **light-sweep flash** crosses the frame. "THAT YOU HAVE TODAY" fades in, then cuts to…
- 2.5: A **lime 4-point sparkle star** on a pale gradient, a lime rounded square drops in, a **3D iPhone with social app icons** rotates up into it, and the big bold sans title "**Social media.**" lands top-left with small right-aligned body copy ("Connect. Share. Grow.") — a **product-ad / landing-page layout**.

## Pacing
- Total scenes: ~14
- Average scene length: ~2.5s
- Shortest / longest: 1s / ~5s
- Distribution: medium, breathing. Fewer cuts than the others. The motion lives in the captions and the graphic scenes are long, polished compositions.

## Captions
- Style: **thin caps lead-in + lime italic serif keyword** with glow; the keyword sometimes gets a lime underline swoosh.
- Active-word treatment: the keyword pops in with a slight scale + glow bloom. The lead-in words build one at a time.
- List captions: **lime ✦ sparkle bullets** ("✦ A MAGAZINE / ✦ A BILLBOARD").
- Position: centre-low, overlapping the mic.
- Size: small lead-in, large keyword.

## Scene types
1. Face-cam fullscreen + lime-keyword captions
2. **Product-ad layout**: sparkle star, lime card, 3D phone with app icons, big "Social media." title + small body copy
3. **3D perspective card swing**: the face-cam video **rotates in 3D (Y-axis) into a floating card**, then **social-app icon coins** (YouTube, Pinterest, Snapchat, Telegram, Instagram, WhatsApp, X…) **burst out and orbit** around the card with a lime glow underneath (10fps strip 5.9–6.6s). Caption "YOU NEED **TO BE ON IT**".
4. White canvas "JUST TO MARKET YOUR BUSINESS." with the sparkle star, the icon-orbit card **shrinking to the lower-left**
5. Face-cam inside a **rounded card sliding up over white** with a **live view counter** ("704K" → "999K" counting up) — "BUT ALSO THE POTENTIAL **TO GO VIRAL**"
6. **Stacked split-screen**: B-roll on top (calculator + cash, $100 bill stack, crowd, Times Square billboards), face-cam bottom, each with a lime gradient wash at the bottom edge of the B-roll card, captions on the B-roll
7. Face-cam with ✦ list captions
8. **TikTok upload UI mock**: the face-cam inside a phone-UI frame with the TikTok bottom nav, a "Drafts" pill, a pink "**Post**" button, and a **mouse cursor that clicks Post**. The like/comment rail appears on the right. Then the card shifts left while the caption builds on the right: "AND IT CAN GO **VIRAL**" → "TENS OF MILLIONS OF VIEWS". View counts tick up on the rail.
9. Face-cam closer: "YOU ARE **WASTING** THAT FREE TOOL", "JUST IN THE PALM **OF YOUR HAND**"

## Transitions
- Flavors: **light-sweep flash**, **3D card swing**, **card slide-up**, **phone-UI zoom out**, hard cuts.
- Rotation: each graphic scene has its own entrance. They don't repeat.
- Signature: the **face-cam becoming a 3D object** (a perspective swing into a card) with orbiting icons.

## Face treatment
- Modes: fullscreen, card on white, stacked top/bottom split, inside the phone-UI mock.
- Grade: bright, airy, neutral-cool daylight with soft contrast.
- Card radius ~16px, soft shadow, matching the wrapper aesthetic.

## Audio reactivity / SFX
- ~47 high-band transients in 36.5s. Strong swooshes on the 3D swing (5.1–6.9s), coin pops on the icon burst, **mouse clicks** on the Post button (≈25–29s: a dense transient cluster), and a tick-up sound under the view counter.
- Low hits at 4.9s, 8.4s, 10.2s and 12.2s on the scene entrances.
- Subtle music bed.

## Palette
- #D7F542 lime/neon yellow-green — accent (keywords, glow, sparkle, card)
- #FFFFFF / #EEF1F5 white & cool pale grey
- #FE2C55 TikTok pink (Post button only, borrowed UI colour)
- #111111 near-black titles
- Natural skin + grey wall

## Signature move
**Landing-page-grade graphic scenes**: a 3D phone with an app-icon orbit, a TikTok post UI with a cursor click and a view counter. The talking head becomes part of the product UI.

## What to steal
- **Cursor-click UI mock**: rebuild the platform UI in HTML (TikTok/IG/YouTube chrome), put the face video inside it, animate a cursor arrow to the button, scale-press the button and fire `click.wav`. Very Hyperframes-friendly.
- **Ticking view counter** (704K → 999K → 10.7M) with a GSAP `onUpdate` number tween and a short tick SFX.
- **3D card swing**: a wrapper div with `perspective` + `rotateY(-35deg)`→0 and translateZ, plus icons bursting in on a staggered arc (back.out ease) with `pop.mp3`.
- **✦ sparkle bullet lists** in the accent colour.
- **Product-ad layout scene**: a big bold title top-left, small body copy right-aligned, a hero object centred on an accent card.

## What's creator-specific
- The speaker; the TikTok UI is borrowed (fine as a parody mock, but don't misrepresent real stats).

## Transcript
See `transcript.json`.
