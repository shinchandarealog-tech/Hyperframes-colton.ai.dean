# Licious momo story — Design

Built in the style of [@fraym-fx](../../_reference/creator-library/fraym-fx/videos/before-after-edit-De7G13nIXPv/analysis.md) (the "After" edit of their before/after UGC reel).

## Style Prompt
Warm cream "scrapbook journal" UGC edit cut into a plain talking-head. Hard cuts only. All the motion lives inside the inserts: line-by-line text builds, collage pieces popping in, write-on script words. There are three caption tiers: a small white phrase subtitle at chest level, a bold-sans + big-script emphasis lockup in the upper third, and acid-yellow italic inner-thought callouts. Mood-shift frames (polaroid, retro digicam, pink hearts) wrap the live face on story beats.

## Colors
| Role | Hex |
|---|---|
| Cream paper (cards, collages) | `#F3E6B5` |
| Cherry red (card / frame text, hearts) | `#A3161C` |
| White (captions on face-cam) | `#FFFFFF` |
| Acid yellow (inner thoughts) | `#E2F040` |
| Dusty pink (emotional frame) | `#E8B8C4` |

## Typography
- **DM Sans** 600–800: subtitles, small lockup words, yellow callouts (italic 800), typewriter bar
- **Great Vibes**: script emphasis words
- **Archivo Narrow** 700: bold headline lines on cream cards
- **Pinyon Script**: product name write-on

## What NOT to Do
- No whip/shader transitions or crossfades. Hard cuts only, like the reference.
- No chrome or neon text, and no dark canvas. This is not the MOTION_PHILOSOPHY default look.
- Don't stack more than one tier of text per phrase (the subtitle is replaced when a lockup or callout shows).
- Don't put text on the Licious pack when she holds it up.
- Don't use emoji glyphs (the renderer has no emoji font).

## Source notes
- `assets/clean.mp4` is the original talking-head with the burned-in captions painted out (`scripts/` in the session scratchpad: per-shot clean plate + inpaint).
- 90.6–96.2s is covered by quote cards because she leans into the lens there and the cleanup can't be invisible.
- `assets/captions.json` holds the words + timings lifted from the original burned-in captions.
