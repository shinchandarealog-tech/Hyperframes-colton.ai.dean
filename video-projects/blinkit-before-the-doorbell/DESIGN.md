# DESIGN — Blinkit "Before the Doorbell" (spec ad)

Source of truth: the approved storyboard (https://claude.ai/artifact/EAhanPWnGwtktG8Nh1xhLs), 9 beats, 17.0s, 1080×1920.

## Style Prompt
A bright, playful Indian quick-commerce spot told only with flat illustrated scenes and lightly dimensional app UI. One relatable moment: guests at 8:00, no milk at 7:50. Clean cream grounds and Blinkit yellow carry the brand, green carries speed and "go", a cold fridge blue carries the problem. No hard cuts: every beat flows into the next through a whip, iris, zoom or morph. Heavy grotesk type slams for the payoff, then a calm, still logo hold.

## Colors (5 hues, each with one meaning)
| Token | Hex | Meaning |
|---|---|---|
| `--yellow` | `#F8CB46` | Blinkit brand, the solution (icon, bag, slogan frame, logo ground) |
| `--green` | `#0C831F` | Speed / go / delivery (ADD buttons, route, Place order, word stack, "it") |
| `--ink` | `#1C1A12` | Type and outlines (warm near-black, never pure #000) |
| `--cream` | `#FFF7E2` | Neutral ground for app and home scenes |
| `--cold` | `#CFE3F5` | The problem: fridge light, empty carton (beat 1 only, echoed on ice) |

White `#FFFFFF` is allowed only for UI card surfaces.

## Typography
- **Display:** Bricolage Grotesque 800 (slogans, timestamps, word stack, wordmark). Tight tracking (-0.03em).
- **UI:** Plus Jakarta Sans 500/700/800 (app header, search, product cards, buttons, ETA pill).
- **Hand:** Caveat 700 for the sticky note only.

## Motion rules
- Every scene enters with motion; scene changes are transitions (whip with blur, iris from the tapped element, zoom-through, rect-to-frame morph). No exit tweens before a transition.
- Camera never fully static: slow push-ins and drift on every scene except the final logo hold.
- UI interactions use the faux-tap sequence (compress 0.07s power4.in → release back.out(3) → ripple).
- Counters tick with a scale pop on the final value.
- Final 1.4s (15.6–17.0) is a deliberate still hold.

## What NOT to Do
- No real Blinkit app screenshots or photography; all UI is our own recreation.
- No gradient text, no neon, no purple/blue gradients.
- No more than the 5 hues above (product art stays inside the palette).
- No hard cuts, no exit fades before a transition.
- No `<br>` line breaks in running text; no random values without the seeded PRNG.
