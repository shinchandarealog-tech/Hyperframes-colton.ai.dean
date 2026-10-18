# DESIGN — Client sample (MSR · Shark Funded first-reward announcement)

## Style Prompt
"Trading-desk night mode." A dark, warm-tinted canvas that sits naturally next to the client's lantern-lit set. Graphics feel like a premium trading terminal crossed with an event ticket: thin hairline rules, monospaced data labels, big heavy numbers that count up, and a single ticket/pass motif that carries the giveaway. Light, not colour, does the premium work — soft glows, a slow vignette, faint grain. The client's violet appears only as a brand signature (MSR code, Discord), never as a full-screen wash, so this reads as an upgrade of their channel rather than a copy of their old template.

## Colors (≤5, each owns one meaning)
| Role | Hex | Meaning |
|---|---|---|
| Canvas | `#0B0A0F` | background / panels (tinted toward violet, never pure black) |
| Ink | `#F5F2EA` | primary text (warm off-white, matches lantern light) |
| Money / reward | `#36F1A4` | payouts, $111, "reward", ticks |
| Giveaway / trip | `#FFC24B` | trip, expo, deadline, winner |
| Brand signature | `#8E6BFF` | MSR code, Discord, channel identity only |
| Muted ink | `#A7A2B5` | labels, secondary text |

## Typography
- **Display / statements:** `Archivo` 800–900, condensed via `font-stretch` where supported, tracking −0.03em. Headlines 72–160px.
- **Data / labels / numbers:** `JetBrains Mono` 500–700, tabular nums. Labels 20–28px, uppercase, +0.12em tracking.
- **Human voice accent (one word per beat max):** `Instrument Serif` italic — used for the emotional word ("first", "court").
- Captions: Archivo 800, 54px, warm ink with the keyword in its meaning-colour.

## Signature elements (ours, not the reference's)
1. **The Ticket** — giveaway pass with perforated edge, gold foil glint, serial "MSR-001". Returns as the end-card callback.
2. **Terminal ticker strip** — thin mono ticker along the top edge during data beats (`CODE: MSR · BOLT 9K+ ×5 · STRIKE 25K+ ×5 · $111`).
3. **Count-up numbers** with hairline underline sweep.
4. **Side-panel layout** — speaker shifts to the left 58% of frame (wrapper move + slight zoom) and a glass data panel slides in on the right; never a full-screen colour slate.
5. **Keyword captions** — 2–4 word chunks, bottom-centre, active keyword coloured by meaning.

## Motion
- Punch-ins on the A-roll at cut points (1.0 → 1.12) to hide jump cuts; slow 1–2% drift otherwise.
- Entrances: `expo.out` 0.35s for panels, `back.out(1.4)` for tickets/badges, `power3.out` for text.
- Transitions between graphic beats: light-streak whip / blur push, 0.3s.
- Every graphic beat gets ONE SFX (whoosh, pop, click, sparkle, slam) at −14 dB under voice.

## What NOT to Do
- No full-screen indigo/purple gradient slates, no glowing rounded-square stat cards, no orbiting logo carousel, no podium, no B&W "COMING UP" tag — those are the reference's signatures.
- No flat pure #000 / #fff.
- No more than one coloured keyword per caption chunk.
- Never cover the speaker's face; panels live in the right 40%.
- No banned fonts (Inter, Poppins, Roboto, Syne…).
