# dewlyzsncme — @edita.visuals ("Paid off your home? Keep liability insurance")

**Source:** https://www.instagram.com/reel/DewlyZSNcme/ (uploaded file, not downloaded)
**Duration:** 23.33s
**Aspect:** 9:16
**Resolution:** 720x1280 showcase; inner edit card ≈ 360x642
**Studied:** 2026-10-29
**Engagement (at time of study):** n/a (local upload)
**Sample rate:** every frame at 2fps (46 frames) via contact sheets, storyboard at 1fps, a 10fps strip across 13.1–14.1s, and a spectrogram.

## Wrapper
The standard @edita.visuals before/after showcase (see `../det-wsmtgue/analysis.md`).

## Hook (0–2s)
- 0.0: Insurance agent in a navy suit, shot outdoors against tropical plants and a city building, with a **reflective glossy blue "desk" foreground** at the bottom (a glass/water-like gradient band). The opening frame already has a graphic: "When the house is **PAID OFF**" (bold italic cobalt-blue caps with a white stroke) plus a frosted-blue **progress card** ("Their Homes · $ Paying · 23%").
- 0.5–1.0: The camera **punches in hard** (~2×) onto the progress card. The bar fills **88% → 99%**, and **dollar-bill emojis fly off** the card. A pitch-rising **riser SFX** (a visible upward diagonal in the spectrogram at 0.2–0.6s) sells it.
- 1.5: A heavy **defocus blur** of the speaker with "they" (a reset beat).
- 2.0: "they think, oh **NO INSURANCE**" in the cobalt italic caps.

## Pacing
- Total scenes: ~12 (mostly overlay changes on one continuous face shot)
- Average scene length: ~1.9s
- Shortest / longest: 0.5s / ~3s
- Distribution: fast and dense, with something new on screen every ~1s.

## Captions
- Style: small white italic lead-in + **bold italic cobalt-blue caps keyword** (#2F6BFF → #4FA3FF gradient, white inner stroke). The keyword type-ons left to right.
- Active-word treatment: a slide/type-on with a slight overshoot.
- Position: centre-chest.
- Size: medium-large.

## Scene types
1. Face-cam fullscreen with a glossy blue foreground band (desk reflection overlay)
2. **Frosted-glass UI progress card** (house thumbnail, label, % bar filling, flying money)
3. **Toggle-pill UI**: "✓ I'M FINALLY DONE" (green check) and "✕ PAYING FOR INSURANCE" (red x) pills slide in with a **cursor hand** hovering/clicking. The speaker is **raising both hands** (gesture synced to "I'm done").
4. **Face-cam shrinks to a square app-icon-style card** on a light-blue gradient canvas, with chat-option chips "🤔 Yes or No?" and "😊 I Agree" (the second gets selected with an outline glow). A poll/chatbot UI.
5. Face-cam + "I see a lot of **CLIENTS**"
6. **Polaroid-style photo sticker** of a house blown over by a hurricane drops in, rotated ~-8°, with a red tab "NOT CARRY" and a caption "Hurricane Coverage". A sticker pop.
7. Face-cam + "but at least **HAVE LIABILITY** on the home"
8. Face-cam + "You throw **A PARTY** somebody", with emoji speech-bubble chips **😓 Slips** / **😣 Falls** popping in
9. **Hard cut to a staged "stress" photo** (the same man, hands in hair, in a courtroom with a gavel, AI-generated or composited) framed by a **torn-paper / flying-documents vignette border**, with a slow push-in. Caption "you don't want **A LAWSUIT** coming in the mail".
10. Face-cam + "so definitely **AT LEAST**", with a shield-check list (🛡 LIABILITY, 🛡 FIRE POLICY) stacking
11. Face-cam blur reset, then "Much less **EXPENSIVE**"
12. Face-cam punch-in + a glossy blue **pill "STRONGLY RECOMMEND"** with **🔥 fire emojis** bursting around it
13. Closer: "especially when **PAID OFF**" plus a **house photo in a viewfinder/focus-bracket frame** with sparkles

## Transitions
- Flavors: **punch-in zoom** (scale 1→2 on a graphic), **defocus blur reset** (1.5s, 18.5s), **face → app-card shrink**, **hard cut to a torn-paper-framed photo**, sticker drop.
- Rotation: blur, punch, shrink, cut, blur. A blur reset roughly every 6–8s.
- Signature: **the defocus-blur "breath"**: the whole frame goes soft for 0.3–0.5s between ideas, then snaps back sharp with the new caption.

## Face treatment
- Modes: fullscreen (dominant), square app-card on a gradient, a staged reaction photo (the same person, composited).
- Grade: vivid, saturated, punchy; cool blue foreground versus green plants.
- **Glossy blue foreground band** at the bottom 20% on every face shot. It's a branded "desk".

## Audio reactivity / SFX
- ~32 high-band transients in 23s plus ~27 low-band hits: the **most bass-heavy** of the set (low hits roughly every 0.8s).
- **Riser** (pitch sweep up) at 0.2–0.6s on the money progress bar.
- A **broadband paper/whoosh wash** 12.9–13.8s for the torn-paper lawsuit transition.
- Pops on emoji chips, clicks on the cursor toggles, a whoosh on the sticker drop.

## Palette
- #2F6BFF → #4FA3FF cobalt gradient — dominant accent (keywords, pills, glossy band)
- #E6F2FF light-blue gradient canvas
- #22C55E green check / #EF4444 red x (semantic only)
- #FFFFFF white text, frosted-glass cards (white at ~70% + blur)
- Natural greens from the background plants

## Signature move
**Every sentence becomes a tappable UI element** (progress bar, toggle pills, poll chips, a shield checklist, a recommendation pill), animated in sync with the speaker's gestures and finished with emoji bursts.

## What to steal
- **Frosted-glass UI cards** (`backdrop-filter: blur()`, white 70%, 16px radius) for progress bars, toggles and polls. Animate the % with a GSAP number tween + a riser SFX.
- **Gesture-synced overlays**: pop a UI element exactly when the speaker gestures (hands up = "I'm done" pill).
- **Emoji chips** in speech bubbles to dramatise a mini-story (😓 Slips, 😣 Falls).
- **Defocus-blur reset**: `filter: blur(12px)` on the face wrapper for 0.3s between topics, then snap back. Cheap and effective.
- **Polaroid sticker drop** (rotated photo with a tab label) for an example case.
- **Torn-paper vignette frame** around a dramatic still, with a slow push.

## What's creator-specific
- The agent's footage and the composited courtroom photo (it depicts a real person; only do this with your own likeness/consent).

## Transcript
See `transcript.json`.
