# DfDZPCTNVQ0 (Apple Maps: Paris navigation) — @themilesholden

**Source:** https://www.instagram.com/reel/DfDZPCTNVQ0/ (inferred from the uploaded file name)
**Duration:** 16.14s
**Aspect:** 9:16
**Resolution:** 720x1280 @ 30fps
**Studied:** 2026-11-09
**Engagement (at time of study):** not available (local upload)
**Sample rate:** I read every frame at 2fps (32 frames) on timecoded contact sheets.

## Hook (0–2s)
- **0.0–0.5s:** The Apple Maps app icon sits on light grey. The drawing panel shows a wireframe of a nav screen ("200 m, Pl. Charles de Gaulle").
- **1.0s:** It zooms through the icon into a blank map with a blue location puck. The nav pill starts to drop in.
- **1.5s:** The turn banner reads **"200 m · Place Charles de Gaulle · Then ↰"** over a stylised white 3D city.
- The hook opens on the icon, zooms through it and is already mid-navigation. It's the same opening formula as the Find My video.

## Pacing
- Beats: 10 · Avg about 1.6s · Range about 1.0–2.5s
- Feel: one continuous drone flight. It slows at the Arc de Triomphe roundabout and the "Look Around" street view, then speeds up for the zoom-out to the icon.

## Captions
- No spoken captions. The persistent CTA is on screen the whole time.
- In-content UI text tells the story: turn banners (200 m, 80 m, Rue Balzac), the "Café Lumière" place card (6 min, 94%, 350 m, busy-hours histogram), the "Look Around" pill, the "Home" pin, and the end card **" Maps · Find your way."**

## Scene types
1. 0.0–1.0 App icon push-in
2. 1.5–3.0 3D map flyover with a turn banner (stylised clay-white city, green trees)
3. 3.5–4.5 Route line (blue) drawn along the avenue
4. 4.5–6.5 POI reveal: an orange café pin and a place card that slides up with a live bar chart
5. 6.5–8.0 Landmark orbit around the Arc de Triomphe roundabout, with coloured traffic lanes
6. 8.0–9.5 Turn onto Rue Balzac and fly over a park
7. 10.0–11.0 "Look Around" street-level façade
8. 11.5–12.0 Arrival: a red "Home" pin with a radius ring
9. 12.5–13.5 Pull-out: motion-blurred zoom to a radial city map, which tilts as a card in 3D space on navy
10. 14.0–16.1 Logo outro: the Maps icon on deep navy with **" Maps"** and the "Find your way." tagline

## Transitions
- Flavors: zoom-through icon, continuous dolly/orbit, **motion-blur whip pull-out**, a **3D card tilt** (the map turns into a floating tile), crossfade to the logo
- No hard cuts

## Face treatment
None (faceless). The renders are a clean, low-saturation "clay" 3D look, which reads like Apple's design language.

## Audio reactivity
None visible on the chrome.

## Palette
Canvas #0a0a0a · asterisk #e07e52 · CTA pink #f8b0be · subject: clay white #f2f0ea, route blue #0a84ff, park green #4cd964, outro navy #0b1a3a

## Signature move
He takes the user on a full A-to-B journey inside the app, then zooms out until the whole world becomes the app icon again.

## What to steal
- **World shrinks into a card, then into the logo.** Animate `scale` + `rotateX/Y` on the scene wrapper so the full-bleed content becomes a floating tilted tile, then crossfade to the icon. This is cheap in GSAP.
- **Slide-up info card with a live mini bar chart** (a `data-chart` block-style histogram)
- **Turn-banner pill** as a consistent top-of-frame UI anchor during movement

## What's creator-specific
- The Opus funnel CTA. The Apple Maps icon, the Apple logo and the "Look Around" UI are third-party IP.

## Transcript
Not transcribed: `npx hyperframes transcribe` could not download its Whisper model because this environment blocks the Hugging Face host. Nothing on screen points to a voiceover (no presenter, no spoken captions), so the audio is **probably** a music bed, but that is unverified. Re-run transcription where the model can download.
