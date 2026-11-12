# AUDIO.md — the reference's sound

- **Loudness (ebur128):** mix **−14.2 LUFS integrated**, LRA 4.3 LU.
- **Speech vs gaps:** speech −16.4 dBFS RMS, gaps between words −19.0 dBFS → a **music bed is present and loud (≈ 2.5-6 dB under the voice during speech gaps)**, no audible ducking.
- **Stem separation:** Demucs could NOT be installed in this environment (PyTorch wheel index blocked by the network proxy). SFX were found by spectral-flux onset detection (150 Hz-12 kHz) on the full mix and kept only outside speech (`spec/_tools/sfx_onsets.json`).
- **SFX hits outside speech** (sparse — a few soft whooshes on b-roll changes):
| t (s) | frame | sits on |
|---|---|---|
| 6.63 | 159 | cut photo → speaker |
| 18.96 | 455 | carousel slide |
| 20.76 | 498 | cut carousel → sugars page |
| 21.74 | 521 | before grid page |
| 27.59 | 662 | S17 page fade-out |
  No pops on individual words were detectable; graphics are carried by the music.
- **Text lead vs voice** (whisper word times vs first visible frame): median **5.6 f** ahead; sans words 0-2 f, serif accents 6-15 f.
- For our edit (later phase): voice chain from the skill, warm bed ≈ 3-6 dB below voice in gaps per the measurement (to be confirmed with the user), whooshes only on b-roll changes. **Templates carry the speaker's voice only.**
