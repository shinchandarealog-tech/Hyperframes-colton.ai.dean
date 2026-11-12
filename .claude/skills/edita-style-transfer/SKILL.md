---
name: edita-style-transfer
description: Use when the user wants the style of a reference edit put on DIFFERENT footage (their own or a client's A-roll, not the reference's own raw clip). Covers measuring the reference, preparing the A-roll, the graphics engine, 20-30 templates, the full edit, sound, QC and revisions.
---

# EDITA STYLE TRANSFER: any reference style on new footage

**What this is:** the exact method we use at @edita.visuals to edit our clients' videos in the style of a reel they love.

**The job:** the user gives you two things:
1. **a reference**: a finished reel whose style they want;
2. **an A-roll**: different footage. Usually a different person, saying different things, filmed differently.

Make a video where the A-roll **looks, moves and sounds like the reference**, while the words and the face stay the user's (or their client's).

This is different from copying a reel 1:1 on its own raw clip. Here the footage and the words are new, so you cannot copy cut by cut. You copy the **style system**: fonts, colours, components, motion curves, rhythm, camera, sound. Then you build a new edit from that system.

How we used it on real client work:
- **A car dealership (Hebrew, right-to-left).** Reference: a podcast-style reel with rust/orange pills, highlight bars and split screens. We built 30 templates first. The client deleted 3, then we made the full edit and revisions v1 to v14.
- **A doctor (English, left-to-right).** Same reference style, a different client. We reused the same engine, flipped back to left-to-right, and made a 27.6 s edit.

---

## 0. The whole workflow

```
REFERENCE ──────► 1. MEASURE the reference (spec: CUTS, S01..Sn, STYLE, AUDIO)
                               │
NEW A-ROLL ─────► 2. PREPARE (rough cut, timed words, silences out, face/chin line, b-roll, fonts)
                               │
                               ▼
                  3. ENGINE kit.js = the reference's components with MEASURED numbers
                               │
                               ▼
                  4. 20-30 TEMPLATES on the A-roll's own sentences ──► the user deletes bad ones, you WAIT
                               │
                               ▼
                  5. FULL EDIT (opening = the reference's order 1:1, then the approved templates)
                               │
                  6. SOUND ──► 7. QC ──► v1 ──► revisions v2, v3 … (only what they ask)
```

---

## 1. Golden rules (learned on real client work, do NOT skip)

1. **"Use this style" means COPY the reference 1:1.** Don't interpret it or invent your own structure. The new A-roll changes only WHAT is said, not how the edit looks and moves. Copy everything:
   - the order of sections and how dense the graphics are;
   - fonts, text sizes (as % of the frame width) and colours;
   - motion curves and the rhythm of the cuts;
   - how tight the framing is.

   One of our first tries was rejected with "you didn't copy the reference": the model had invented 22 beats of its own and used text that was far too small.
2. **Measure, never guess.** Every number comes from measuring the reference's frames: position, font size, colour, animation length, ease. Anything "by eye" gets rejected.
3. **Hook first.** Build the hook, compare it with the reference frame by frame, and only then do the rest.
4. **Never put text or a name tag over the face.** We had a template rejected because one big word crossed the face. All captions sit below the chin.
5. **Everything stays in the Instagram safe zone:** x 84-900, y ≤ 1520 on a 1080×1920 canvas. The IG buttons are on the right; the username and caption are at the bottom.
6. **Motion must be smooth and premium.** An element comes in on a spring with one overshoot and stays on screen for at least 1 s. Never a bare fade or a linear slide. The camera on the speaker makes one decisive move per shot (in OR out). Never back and forth in the same shot, never a hard "punch".
7. **Sound: less is more.** Hits go only on meaningful moments, never a fast series of the same pop. Sounds are warm and low-mid; nothing hissy, squeaky or high-pitched.
8. **A revision = EXACTLY what was asked.** Don't add or offer anything "smart" on top.
9. **Never overwrite a version.** Every version (v1, v2, v3 …) is its own file. Deliver MP4 (H.264) only.
10. **No paid service without asking the user first.** B-roll comes from the user (their photos, clips, Canva exports) or free stock (Mixkit, Pexels).
11. **Never build a graphic or thumbnail from a still cut out of the A-roll.** Those stills are soft and blurry and look cheap. For photos of the person, use their professional photos.
12. **Don't say "done" until it's 100%.** First compare with the reference yourself (QC, chapter 10). Give short updates while you work, but don't send half-finished results.
13. **Don't start the next video until the user has reviewed the previous one.**

---

## 2. Tools and setup

| What | Notes |
|---|---|
| Python 3 | opencv-python, numpy, scipy, soundfile, playwright (with Chromium), rembg, faster-whisper |
| ffmpeg | on the PATH. Newer versions dropped `-vsync`; use `-fps_mode` or `-r` |
| Whisper | `faster-whisper` on CPU (int8) is fine. Keep the models in one cache folder (set `HF_HOME`) so they download once |
| Demucs (optional) | separates the voice from music/SFX in the reference, for the sound analysis |
| Rendering | headless Chromium through Playwright, frame by frame. On a normal PC run at most 2 render processes in parallel |
| Project | one folder per client, e.g. `Desktop\<Client>\` |
| Delivery | `<Client>\Templates\` and `<Client>\Video\` |

If something is missing, tell the user what you want to install and install it.

Windows notes:
- In PowerShell, `python -c "..."` with quotes breaks. Write every script to a .py file and run it.
- PowerShell 5.1 has no `&&`; use `;`.
- **Never kill processes by name** (`Stop-Process -Name python`). The user may run other jobs; kill only the PID you started.

---

## 3. Project structure

```
<Client>\
  src\        the original files (raw or rough cut, SRT, logo, info)
  ref\        the reference: frames, _cache, overview sheets, proof images per section (s01\, s02\ …)
  spec\       MEASUREMENTS of the reference: CUTS.md, S01.md … Sn.md, STYLE.md, AUDIO.md
  spec\_tools\  measuring scripts
  aroll\      rough.mov, voice.wav, voice_edit.wav, f\a_%04d.jpg (A-roll frames at 1080x1920)
  broll\      the user's photos/clips, stock clips
  web\        ENGINE: kit.js (components), tpl.js (templates), edit.js (the edit),
              templates.html, video.html, words.js, faces.js, edl.js,
              fonts\, img\ (photos, clips, sil_*.png silhouettes)
  _tools\     helper scripts (transcribe, rough, edit_build, face_track, prep_assets …)
  audio\      stems, sfx, mix.wav
  tpl\        rendered template frames   (Txx\f_%04d.jpg)
  vid\        rendered edit frames       (Txx\f_%04d.jpg = segment xx)
  an\         contact sheets, QC images, json reports
  render_tpl.py   render.py   audio_build.py   encode.py
```

---

## 4. PHASE 1: Measure the reference (the most important part)

The goal is a written spec so precise that someone could rebuild the reference from it without ever watching it.

### 4.1 Basics
- Use `ffprobe` to get the resolution, fps, duration and audio.
- Extract ALL frames (`ffmpeg -i ref.mp4 ref\f\%05d.png`) and build a small cache for fast analysis.
- Make an overview sheet: every 5th frame in a grid, labelled with the frame number. Look at it first, then measure.

### 4.2 CUTS.md: every cut
- For every frame, compute how much it changed (mean absolute difference + histogram correlation). Do it on the whole frame and separately on the top and bottom halves, because of split screens.
- Drop false cuts (the picture doesn't really change) and find cuts that happen in only one panel.
- Check the cadence, i.e. duplicated frames. In our worked example:
  - the speaker was filmed at 25 fps and converted to 30 (every 5th frame repeats);
  - full-screen b-roll updates 8 new frames every 17, which is **14.12 fps**, together with its captions.

  You must find things like this, because the "feel" of the reference depends on them.
- Write a table per shot: `# | first frame | last | time | length | type (speaker / b-roll still / b-roll video / split) | content | transition | text and graphics on screen`.
- For b-roll, decide still or video: align each frame to the shot's last frame (SIFT + RANSAC + ECC). If the residual stays flat it's a still being moved; if it grows, it's video.

### 4.3 S01.md … Sn.md: every section, every element
For every element (word, pill, bar, icon, chip, name tag, panel) measure:
- **Its box at rest** (x0, y0, x1, y1) in px on 1080×1920.
- **The font**: family, weight, size (from the x-height or cap height), tracking in em, and the measured hex colour.
- **The first visible frame** and how it relates to the spoken word. In our example, text appears **2-8 frames BEFORE** the word is spoken, 5 on average.
- **The motion curve:**
  - track the element frame by frame (template matching with shift and scale) to get a dx/dy/scale/opacity series;
  - fit a named GSAP ease to that series (circ.out, back.out(s), expo.inOut, power…) or a damped spring (gives ζ and the period);
  - write down the start offset in px, the ease, the length in frames and t0.

  Examples from our spec:
  > word: `x +29 → 0 px, circ.out, 33.7 f`; visible 4.6 f after the tween starts, opacity 0.83 → 1
  > pill: rises from below, `back.out(2.7)` from +27.3 px, 13.6 f, 22.7% overshoot
  > highlight bar: grows from the left, `expo.inOut` 41 f; the big word flies in when the bar is 20-35% open
  > name tag: comes in from the left at −141.7 px, `circ.out` 41.2 f, no fade
- **The camera on the footage** (similarity transform per frame vs a reference frame). Our example's hook is a zoom-out 1.15 → 1.0, circ.out 31 f.
- **Gradients**: alpha per y row. On the speaker there was a black gradient at the bottom; on b-roll it was orange or brown.
- **Exits.** Our reference had no animated exits at all: everything disappears on a hard cut or a hard page swap. That is data too, and you copy it.
- End every S-file with a JSON block holding all its numbers.

### 4.4 Identify the font
- Render candidate fonts in the same Chromium you'll render the edit with, and compare the letter shapes with the reference (NCC on the ink). Google Fonts is the first place to look.
- In our example: **Bebas Neue** (NCC 0.94-0.98, certain) and **Inter** (0.86-0.97).
- Never settle for the "closest" wrong font.
- For another language, find a font with the same character. For Hebrew we used Heebo for Inter and Karantina for Bebas Neue.
- **For a right-to-left language EVERYTHING is mirrored:** words fly in from the left, bars grow from the right, the name tag moves to the right.

### 4.5 STYLE.md: the style summary
- The palette (role → hex).
- A typography table.
- **The list of components with their canonical motion.** Our example had 13:
  - word slide, emphasis slide, fade in place;
  - highlight bar, pill, ✓ ✕ icons, ! ✦ ★ + icons, chip, name tag;
  - static split, animated split, glass "!" tiles and the intro strobe.
- Backgrounds and the grade.
- Global rules. In our example:
  - text zone y ≈ 950-1410, centred, or left-aligned at x 62-114 with an icon;
  - margins: left ≥ 51 px, right ≥ 58 px;
  - one caption page has 1-3 lines: a small line + ONE accent (bar with a big word, pill, big cream word, chips or icon) and lasts 23-60 f;
  - screen time: speaker 40%, full b-roll 38%, split 22%;
  - b-roll or a split comes every 2-4 s, **never more than ~4 s on the speaker**.

### 4.6 AUDIO.md: the reference's sound
- Measure loudness with ffmpeg `ebur128`: the whole mix, the voice and the rest. Our example: mix −14.9 LUFS, music ≈ 15 dB below the voice, no ducking.
- Run Demucs on the reference (voice / rest), then find the transients in the "rest" stem. The result is a table of SFX hits: time, frame, type (whoosh / click / glitch / riser) and what it sits on (cut, pill, bar …).
- For the reference's words, use whisper + forced alignment, so you know how far the text leads the voice.

### 4.7 Sheets
Put every component at rest on one image (components sheet) and every layout on another (layouts sheet). That's the catalogue you build the templates from.

> Measuring a 50 s reference is a big job (our example needed 18 section files). You can split the sections across several agents, but they MUST all write numbers in the same format.

---

## 5. PHASE 2: Prepare the A-roll

### 5.1 Rough cut
- **If the user sends a finished rough cut**, use it as it is. Our car dealer sent a 4K ProRes rough cut (37.8 s) and an SRT with one word per cue.
- **If the user sends a long raw video** (our doctor's was a YouTube video):
  - transcribe it and pick the strongest sentences for 20-40 s (a hook at the start, a closing line at the end);
  - remove fillers ("In fact,", "oh, well,");
  - cut each piece at the quietest frame boundary within ±70 ms, cut picture and sound on the same frame, and put a 5 ms fade on every join.

### 5.2 Timed words
- Run faster-whisper with `word_timestamps=True` to get `[{w, s, e, p}]`. Model: `medium.en` for English, `large-v3` for other languages.
- If there's an SRT, use it (it's more accurate for that language) and use whisper only to check.
- The result goes into `web\words.js` as `window.WORDS = [{w:'...', s:1.23, e:1.51}, ...]`. Templates and the edit call words by **index** (word 1, 2, 3 …).

### 5.3 Remove silences and mistakes (`edit_build.py`)
- Find silences with `silencedetect=noise=-30dB:d=0.12`.
- Shorten every pause longer than 0.16 s to 0.10 s (half from each side). Cut in the middle of the silence with a 5 ms equal-power crossfade.
- Outputs:
  - `aroll\voice_edit.wav`;
  - `web\edl.js` with `EDL`, `EDIT_DUR`, `e2o()` (edit time → original) and `o2e()` (original → edit time). WORDS are converted to edit time automatically.
- Compare whisper with the script or the SRT, and remove repeated or wrong words.

### 5.4 A-roll frames
- Extract `aroll\f\a_%04d.jpg` at 1080×1920, at the canvas fps (30).
- For a 4K delivery, make a second set at 2160×3840.
- Keep the voice separately in `aroll\voice.wav`.

### 5.5 Face and chin line (`face_track.py`)
- Detect the face on every frame and write `web\faces.js` = `[top, chin, x0, x1]` per frame.
- Chin = bottom of the face box + 5% of its height. Take the maximum over ±3 frames, so captions never touch the chin.
- Make a QC image `an\faces_qc.jpg` (red line = chin) and **LOOK at it**.

The engine then moves every caption page below the LOWEST chin in its own frames (+24 px), see `fitUnder()` and `faceSafe()` below.

### 5.6 Silhouette for a strobe
- Our example's hook flashes a white silhouette of the speaker on frames 1, 3 and 5.
- Make it with rembg `u2net_human_seg` → white mask + a soft 80-120 px halo → `img\sil_k.png`.

### 5.7 B-roll
- **Sources:** the user's own photos and clips, Canva exports (download in 4K, pages as separate files), or free stock (Mixkit, Pexels). Nothing paid without asking.
- Our reference used mostly **MOVING PHOTOS**, not video. Copy whatever your reference does.
- **Preparation:**
  - crop photos wider than the frame (we used 1740×1920) so there is room for the measured pan, and to the split panel size for splits (we used 1452×930);
  - convert clips to 30 fps frames at 1080×1920 or the panel size.
- Make an overview `broll\00 OVERVIEW.jpg` so you see what you have.
- A Canva page with two photos on it is unusable as b-roll.

### 5.8 Grade
- By default the footage stays as in the reference. Ours was untouched, with only a black gradient at the bottom.
- The client may ask for something else. Our car dealer asked for "darker, not so bright": gamma 1.2, saturation 1.42, contrast 1.12, blacks at 0, a light unsharp.
- Bake the grade directly into the A-roll frames.

### 5.9 Who is speaking
- For the name tag you need the name and title (from their website or bio), whether they are verified (blue tick ONLY if they are), the logo, slogan and services.

---

## 6. PHASE 3: The engine (how the graphics are made)

All graphics are an **HTML page at 1080×1920, rendered frame by frame in headless Chromium** (Playwright). No After Effects and no real-time CSS animations: every frame is computed, so nothing can stutter.

How `web\kit.js` works:
1. Every component (Line, Pill, Bar, Icon …) creates a DOM element and registers a function `U(fe => {...})`. That function computes `transform` and `opacity` from the frame number, along the MEASURED curve.
2. `window.initT(i)` builds a template or segment and returns its frame count. `window.renderT(f)` sets frame f, and Playwright saves it as a JPEG.
3. Every visible graphic event is logged: `EV(frame, 'pill'|'marker'|'icon'|'chip'|'word'|'tag'|'glass'|'group')`. The sound goes on those frames later, so the sync is perfect.
4. After each page is built, `faceSafe()` (nothing over the face) and `igSafe()` (everything inside x 84-900, y ≤ 1520; move first, shrink only if needed) run automatically.
5. `c.v(i, lead)` is the frame where word i APPEARS; `lead` = 5 frames before it's spoken, like the reference.
6. B-roll segments go through `stepF()`, i.e. the reference's 14.12 fps cadence.

The components in our example kit (all with measured numbers):

| Component | What it is | Key numbers |
|---|---|---|
| `Line` + `Ws(…,'std')` | a line of words, each flying in on its own | x +28.5→0, circ.out 33.7 f, opacity 0.83→1 |
| `Ws(…,'emph')` | an emphasised word | +60.6 px, opacity 0.31→1, 31 f |
| `Ws(…,'fade')` | a bottom caption on b-roll | no movement, opacity 0.45→1 |
| `Pill` | rust pill (stadium shape) | 'up' = back.out(2.7) 13.6 f; variants 'springY', 'side', 'springX' |
| `Bar` | highlight bar behind a big word | grows from the left, expo.inOut 41 f |
| `Icon` | circle with ! ✓ ✕ ✦ ★ + | 'pop' 0.55→1 back.out(2.5); 'slide' −44 px back.out(1.5) |
| `ChipB` | white chip with a + icon | pops in, words fade in with the voice |
| `NameTag` | black tag at 68% + blue tick | −141.7 px, circ.out 41.2 f |
| `Glass` | glass "!" tiles at ±12° | pop with a small wobble |
| `SplitStatic` | white canvas, 2 panels 1052×930 | radii 23.5 / 21 |
| `Still` / `Clip` | b-roll photo with a pan / b-roll video | pan right to left, circ.out |
| `Strobe`, `Grad`, `Scan` | white silhouette, gradients, scanlines | measured alpha per y |
| `Page(a,b)` | a caption page visible from frame a to b | hard swap, no exit animation |

This is what one segment looks like in code (b-roll with a "!" icon and a pill):
```js
const BROLL_WORSE = c => {
  Still(c.root, 1, { f0: 0, f1: 36, D: 199.2, T: 33.4, t0: 1, dur: 52.7 });      // photo 1, pan measured in S02
  Still(c.root, 2, { f0: 37, f1: 9999, D: 110.1, T: 28, t0: 37, dur: 112.7, ez: EZ.pOut(4) });
  Grad(c.root, 'orangeHi');
  Icon(c.root, { cx: 116, cy: 1170.5, d: 74, fill: '#9F4722', g: '!', V: 0, enter: 'slide' });
  const w = wds(18, 22); w[0] = cap(w[0]);                                         // the speaker's words 18-22
  Ws(Line(c.root, w, { wt: 400, size: 64, base: 1194, xl: 168, ls: -0.04, maxW: 730 }), [3].concat(vs(c, 19, 22, -1)), 'fade');
  Pill(c.root, wds(23, 25).join(' ').toUpperCase(), { xl: 84, top: 1226, h: 76, size: 46, fill: C.rustPill, V: c.v(23, 0), enter: 'springY' });
  Scan(c.root);
};
```

**For a new reference (a different style):** the architecture stays (kit.js + Playwright render). The components are NEW, built from the numbers in YOUR measurements. Keep the base (D, Seq, Page, Line, Ws, Aroll, EV, faceSafe, igSafe, buildT, renderT) and rewrite the components and presets from the new STYLE.md.

**Same reference style, a new client:** copy the previous client's project, swap the inputs (A-roll, words, faces, edl, b-roll, name), and write new `tpl.js` and `edit.js`. Save every script as reusable; the second client is much faster than the first.

---

## 7. PHASE 4: 20-30 templates

### What a template is
One piece of the A-roll (usually 2-4 s, one or two sentences), with the speaker's OWN words and voice, made with one combination of components from the reference. The user watches them and deletes the bad ones. The video is built from the approved ones.

In code (`tpl.js`):
```js
T('Hook - zoom, flash, name tag, pill, bar', 0, 3.38, 'speaker', c => { ... });
//  name (descriptive)                        from to (s)  type: speaker | broll | split
```

### How to choose the 20-30
1. **First, every section of the reference becomes one template** on the speaker's sentences, in the same order. T01 = the hook 1:1. Our reference had 17 sections, which gave 17-23 templates.
2. **Then 4-8 NEW ones**, made ONLY from parts of the reference (same colours, fonts and motion) and fitted to the client's business. Examples from our car dealer:
   - a card with ticks (a list of conditions);
   - a circle drawn around the mileage;
   - a crossed-out question + its replacement;
   - a chip with ✕;
   - a "leave your details" form (CTA);
   - logo + slogan for the end.
3. Mix the types like the reference does: speaker, b-roll, split.
4. Put each template on a DIFFERENT sentence, so the user sees the style across the whole A-roll.

**What gets rejected** (from real verdicts):
- anything over the face;
- a panel that sinks into the black gradient so the speaker disappears;
- clip-art objects (clocks, scales, batteries), stock faces, invented dark worlds;
- decoration without meaning: random lines, a panel behind the speaker, "note to self" tags;
- stills from the A-roll used as graphics.

**What passes:** clean UI cards and widgets, typography, chips, lists, anything that looks like it came out of the reference.

### Rendering the templates
```
python render_tpl.py test            -> an\tpl_test.jpg   (4 frames of each template: a quick check)
python render_tpl.py strip 5 0 60 2  -> an\tpl_strip.jpg  (consecutive frames of T05: motion check)
python render_tpl.py all 1 15        (process 1)
python render_tpl.py all 16 30       (process 2, in parallel)
python render_tpl.py encode 1 30     -> <Client>\Templates\Txx - name.mp4 (+ the speaker's voice for that piece)
python render_tpl.py pack            -> 00 ALL TEMPLATES.mp4 (all in order, a black card with the number before each)
                                        + 00 OVERVIEW.jpg (a grid of all of them)
```
- Templates carry ONLY the speaker's voice, no music and no SFX.
- File names describe the content ("T08 - Line + rust bar + big narrow words.mp4").

When you deliver, write the user a short note:
- how many templates there are, which are 1:1 from the reference and which are new;
- EVERY difference from the reference, with the reason. Examples: "the Hebrew letters are taller, so the lines are 20-35 px further apart"; "I kept the blue tick, remove it if they're not verified".

Then **WAIT for the verdict.**

---

## 8. PHASE 5: The full edit

### 8.1 Segment plan
When the user says which templates to delete:
- **The video opens with a copy of the reference, in the same order** (hook → b-roll with "!" → split → bar + glass → …). **After that come the approved templates, none used twice.**
- The rhythm follows the reference: never more than ~4 s on the speaker, b-roll or a split every 2-4 s, roughly half of the video is not the speaker.
- The name tag appears ONLY in the hook. The same person talks the whole video, so showing it again makes no sense.

In code (`edit.js`) the timeline is a list of segments:
```js
const SEGS = [
  [HOOK, 'speaker', 1, 18, 'Hook'],            // [function, type, first word, first word of the next segment, name]
  [BROLL_WORSE, 'broll', 18, 26, 'B-roll ! + pill'],
  ...
  [SPK_CLOSE, 'speaker', 88, 0, 'End tick + bar'],   // 0 = to the end
];
```
A segment starts 0.04 s before its first word. Frames are rounded at the level of the whole video, so segments join exactly and the picture stays in sync with the voice.

### 8.2 Camera on the speaker
- Hook: copy the reference (ours was a zoom-out 1.15 → 1.0, circ.out 31 f).
- Every following shot (between two jump cuts) = **ONE move across the whole shot**, with a sine ease. The direction alternates (in, then out), and each shot starts where the previous one stopped.
- The range depends on the framing: 1.00-1.12 for an extreme close-up (max 10% per shot), up to 1.00-1.24 for a wider shot (~7.5%/s, max 16% per shot).
- The zoom centre is on the face or chin, so the face stays in place.
- NEVER back and forth in the same shot, never a hard punch.

### 8.3 Render and assemble
```
python render.py all 1 5   (process 1)    +    python render.py all 6 10  (process 2)
python audio_build.py                    -> audio\mix.wav
python encode.py sheet                   -> an\video_sheet.jpg (every 12th frame), LOOK at it
python encode.py deliver " v1"           -> <Client>\Video\<Name> v1.mp4 (never overwrites an existing file)
```
- Encoding: H.264, crf 15, yuv420p, bt709 tags, AAC 320k, `+faststart`.
- **Deliver at the source resolution.** A 4K source gets a 2160×3840 delivery (render at device scale 2 with 4K sources). A 720p selfie gets 1080×1920.

---

## 9. PHASE 6: Sound (`audio_build.py`)

| Layer | How |
|---|---|
| Voice | highpass 70 Hz → afftdn −30 → compressor 3:1 from −22 dB → +2.5 dB at 3 kHz → loudnorm −15 LUFS |
| Music (bed) | 25 LU below the voice, starts at frame 0 (10 ms fade-in), 1 s fade-out at the end. **If the user says "no music", there is NO bed at all.** |
| Hook | flicker/glitch on the strobe frames (quiet, 22 dB below the voice) |
| Marker | a marker sound on every bar that grows (`EV 'marker'`) |
| Pops | on graphics, THINNED by the rule below; pitch ±0.7 semitones so they don't all sound the same |
| Risers | only 3-4 times, when the shot type changes (speaker → b-roll or split); every other cut is DRY |
| Master | −14 LUFS, −1.5 dBTP |

**The pop thinning rule** (after a client said "in the first 5 seconds some effect hits at random, everything repeats"):
- priority: graphic (pill, chip, icon, card, glass, tag) > a new caption group > an emphasised word;
- at least 18 frames between two pops;
- at least 12 frames from a flicker, riser or marker;
- no pop from −25 to +30 frames around a marker.

A sound goes on the frame where its element is ≥ 50% visible, never earlier. Our car dealer edit ended with 28 SFX in 37 s.

**Where the sounds come from:**
- your own SFX library or free sound sites;
- from the reference itself only if the client explicitly asks. Even then, never use raw clips where you can hear the reference's voice or music: clean them (Demucs + spectral subtraction + gate) or synthesise the same sound.

Nothing hissy or squeaky: the sound should be warm, low-mid, "premium".

---

## 10. PHASE 7: QC before sending (checklist)

- [ ] **The reference and ours side by side** for every segment (same type of frame): text size, position, colour, font.
- [ ] **Motion**: a strip of consecutive frames of every element vs the reference. No jitter, no bare fades, every element holds for at least 1 s.
- [ ] Wherever it differs: write the reference number and our number in `DIFF.md`, fix it, measure again.
- [ ] No text over the face on any frame (check the fit report and look close up).
- [ ] Everything inside the IG safe zone.
- [ ] Text appears ~5 f before the spoken word and no word is late.
- [ ] No silences longer than 0.1 s, no repeated or wrong words.
- [ ] Sound: −14 LUFS; no series of the same pop; the first 5 s are not crowded; no voice or music from the reference audible in the SFX.
- [ ] `ffprobe` on the output: resolution, fps, duration, audio present.
- [ ] The contact sheet of the whole video checked from start to end.

---

## 11. Revisions

- When the user or the client sends notes, do **EXACTLY that**, nothing else. The new version gets a new number (v2, v3 …), the old one stays.
- If only the sound changes, don't re-render the picture: mux the new sound onto the last version's picture.
- If they say "too much X", only lower or thin out X. Never change the whole concept.
- When the client and the user disagree, the client wins.

Real notes from our car dealer project, so you know what usually gets asked:

| Version | Note | Fix |
|---|---|---|
| v2 | the name tag also shows in the splits | name tag only in the hook |
| v3 (client) | SFX not clean or in sync, no zoom, lines too long (IG covers them), needs more colour | SFX on graphic events, zoom on jump cuts, igSafe, a grade |
| v4 | take the effects straight from the reel | effects extracted from the reference's Demucs stem |
| v5 | everything must stay inside the margins; music from 0.0 s; first effect too loud | safe zone x 120-910; bed from frame 0; one soft whoosh |
| v6 | I don't want the hiss of the marker | a warm swipe instead |
| v7-v8 | weak zooms; "decisively in or out, not swaying" | one eased move per shot, alternating directions |
| v9 (client) | darker; a premium click on some words; bring back the hook flicker | new grade, clicks added, flicker back |
| v11 | not your click, the one from the reference | pops from the reference |
| v12 | some audio is audible behind the effect | cleaned and synthesised SFX |
| v13 (client) | voice too quiet; clicks random | compressor + presence, bed −25 LU; pops only on new caption groups |
| v14 | in the first 5 s everything hits, it repeats | thinning (the rule in chapter 9) |

**Lesson:** most revision rounds were about SOUND. Apply the chapter 9 rules on the very first version.

---

## 12. Same style, different client: what changes

When we moved the car dealer's engine to the doctor:
- **Direction:** flipped from right-to-left back to the reference's original direction (words come from the right, bars grow from the left, the tag is on the left), and the fonts went back to Inter + Bebas Neue.
- **Extreme close-up:** her chin was at y ≈ 1240-1300, his at ≈ 960. So:
  - every caption page is placed below the chin in ITS OWN frames (`fitUnder`);
  - more text moved to b-roll and split pages, like the reference (~60% of the video is not the speaker).
- **Camera:** zoom centre [540,1180], range 1.00-1.12. The bottom split panel was raised so it fills the space from the eyes to the chin.
- **Name tag:** next to the chin, with a blue tick because she IS verified.
- **Gradient:** raised where the photo or clip is bright under the captions.
- **Sound:** the final v14 rules from the very first version.
- **Rough cut from a long YouTube video:** 4 pieces, a strong hook line first and a closing line last.

---

## 13. Quick start for a new client

1. Make `<Client>\`, put the reference in `ref\` and the client's files in `src\`.
2. If the reference style is one you already built, copy that project and skip step 3.
3. If the reference is new, do all of PHASE 1 (CUTS.md, S01…Sn.md, STYLE.md, AUDIO.md, sheets), then build a new kit.js.
4. Prepare the A-roll:
   - rough cut;
   - timed words (whisper or the SRT) → `words.js`;
   - silences out (`edit_build.py`);
   - A-roll frames;
   - chin line (`face_track.py`, look at the QC image);
   - silhouette, b-roll, fonts in `web\fonts\`.
5. Write 20-30 templates in `tpl.js` (first the reference's sections, then new ones from the reference's parts). Then `render_tpl.py test` → fix → `all` (2 processes) → `encode` → `pack`.
6. Deliver the templates with a short note about the differences. **WAIT for the verdict.**
7. Make the edit:
   - write SEGS in `edit.js` (opening = the reference's order, then the approved templates) and the camera by the rules;
   - render, then `audio_build.py`;
   - QC (chapter 10);
   - `encode.py deliver " v1"`.
8. Tell the user the path to v1. Do revisions only from their notes: v2, v3 …

### What to ask the user (ONLY if it's missing; don't ask what you can find out yourself)
- the name and title for the name tag, and whether the person is verified;
- where the b-roll comes from, if they didn't give any;
- music: yes or no;
- the caption language and the delivery resolution, if it isn't clear from the source.
