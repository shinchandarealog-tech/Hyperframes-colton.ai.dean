---
name: ugc-meta-edit
description: Edit a UGC talking-head ad for Meta (Instagram/Facebook Reels, also TikTok) the way this client approves first time - clean cut, B-roll that matches every line and hides every jump cut, white 2-3 word captions just below the speaker's face, an optional "pov:" hook title, all inside Meta's safe area, then render and verify. Use when the user sends a raw or pre-cut talking-head video (usually a Google Drive link) plus B-roll for a UGC / Pacagen-style product ad, says "new video", "edit this UGC", "add brolls and captions", "add the hook title", or asks for a Meta-safe edit.
---

# UGC Meta Ad Edit

The client (Pacagen via Zagged) approves simple, native-looking UGC: a real person talking to camera at home, cut against B-roll that shows each claim, with small plain captions. **It must not look like an ad.** This skill is the exact process that got three videos approved.

**Read first, every time:** `CREATOR.md`, `PREFERENCES.md` (wins over this file if they ever disagree), and the client brief if one is sent. Load `/hyperframes` before writing the composition.

## Fixed rules (from the user's approved edits)

| Area | Rule |
|---|---|
| Editing | Light. Talking head + real B-roll. Plain straight cuts only - no transition effects, zooms, stickers, logos, motion graphics or end cards. |
| Audio | Her voice only. No music or SFX unless the user asks. If asked: soft bed ~22 dB under the voice (see `video-projects/pacagen-supplement-ugc/edit-data/music-bed.py`). |
| Captions | White `#FFFFFF` for the whole video, soft dark shadow, Inter 600 54px, sentence case, **2-3 words per caption** (fast swaps), no pills, strokes, karaoke or emoji. Start at frame 0 (even under a hook title). |
| Caption position | **One fixed spot just below her chin** for the whole video, never on her face, never above her head, never moving per shot. |
| B-roll | Must show what she is saying at that moment. **Must cover every jump cut** in her footage. **Never a different person** in frame (hands-only shots are fine). No speaker flash shorter than 0.5s between two B-roll clips. If nothing fits a line, stay on her. |
| Footage | Level a tilted camera (small rotate inside the crop). Conform to 1080x1920, 30fps CFR. Loudness about -16 LUFS. |
| Brief | Check claims against the brief. Pacagen: say "**up to** 98%", spray lasts "up to 2 months", no medical claims ("treats/cures allergies", "fight allergies"). Rehome angle: end on the cat. Never mix spray and supplement mechanisms. |

## Meta safe area (1080x1920)

- Keep clear: **top 14% (0-270px), bottom 35% (1250-1920px), 6% each side (65px)**. Captions and titles live inside **x 65-1015, y 270-1250**.
- Pacagen's brief is stricter (**bottom 40% clear, y <= 1152**). Get as close as her face allows; if the caption has to sit lower, keep it above 1250 and tell the user how far into the 40% zone it is.
- Verify on rendered frames (the contact sheet draws the 270 and 1250 lines in red), not just in CSS.

## Workflow

Tell the user a time estimate before starting. A typical 30-50s video takes about 20-25 minutes with a direct final render, or about 35-50 minutes with a draft round. If they're in a hurry, skip the plan/approval step, pick sensible defaults, say what you picked, and render the final directly.

### 1. Get the files
Drive links must be "Anyone with the link - Viewer". Download into the scratchpad, not the repo:
```bash
pip install -q gdown
python3 -m gdown <FILE_ID>                       # single file (talking head, reference, brief .docx)
python3 -m gdown --folder <FOLDER_URL> -O broll/  # B-roll folder
```
The Pacagen B-roll folders (SPRAY / SUPPLEMENT / CLEANING_AIR PURIFIERS, plus the pills / 3pm fog / dry mouth set) may already be in the scratchpad from earlier sessions; reuse before re-downloading. Read a brief .docx by unzipping `word/document.xml`.

### 2. Transcribe and analyze her footage
```bash
ffmpeg -i head.mp4 -vn -ac 1 -ar 16000 head.wav
WHISPER=~/.cache/hyperframes/whisper/whisper.cpp/build/bin/whisper-cli
MODEL=~/.cache/hyperframes/whisper/models/ggml-small.en.bin   # run `npx hyperframes transcribe` once if missing
$WHISPER -m $MODEL -f head.wav -ml 1 -sow -t 4 -np --prompt "Pacagen, Fel d 1, allergist" > words.txt
```
Convert to `words.json` ([{text,start,end}]) and run:
```bash
python3 -I .claude/skills/ugc-meta-edit/scripts/analyze_talking_head.py head-1080.mp4 words.json
```
It reports pauses > 0.35s, **jump-cut frames** (each needs B-roll), audio clicks, and the **face range + suggested caption top**. Whisper mishears brand words ("Packagen", "its brain" for "its spray"); fix them in captions.

- **Raw footage:** cut silences, stumbles, false starts and repeated takes (keep the cleanest, usually the last take). Cut each kept range separately with a 15ms fade in / 30ms fade out, frame-exact (`-frames:v round(dur*30)`), concat, then loudnorm the joined audio. Doing all cuts in one filter graph runs out of memory.
- **Already cut by the user:** don't re-edit. Only fix real problems (clicks, a word clipped, a flash frame) and say what you checked.

### 3. Plan the B-roll (look before you pick)
Make contact sheets (6 thumbnails per clip) and look at every candidate. For each line, write the clip and the exact in-point, then check those exact frames for: a different person in frame, the product label, and whether the shot really shows the line. Proven mappings for Pacagen:

| She says | Clip that worked |
|---|---|
| hook about her cat / rehoming | cat asleep on bed (`bottle in front of cat` @10s, bottle out of frame) |
| allergy pills / 6 years of pills | `allergy pills`, `annoyed taking pills` |
| 3pm fog / dry mouth / sprays not working | `3pm fog_confused`, `dry mouth_drinking water`, `allergy sprays` |
| air purifiers / washing bedding | `2 air purifiers`, `laundry` |
| allergens stay behind / on everything | spray held next to sleeping cat (`bottle in front of cat` @0.3s) |
| things they touch | `spraying cat tree 2` @0.3s (before the spray appears) |
| neutralizes up to 98% | `spraying sunlight` @3.2 (mist), `spray on guest bed` @1 |
| targets the environment | `spraying closeup` @0.2, `spraying cat tree` @1.4 (hands only) |
| supplement switch / how it works | `supplement in front of cat`, `putting supplement in food` @16, `eating + supplement`, `supplement in front of bed` |
| ending (rehome angle) | the cat, last ~1s |

Clips that show a **different woman**: spraying sheets / scratcher / pillows / stools / dining chairs / carpet entryway / coffee table / bed / stairs / desk chair, `laundry 3`. Don't use them. The empty sofa read as "plain B-roll" and was rejected.

Place each B-roll start/end on word boundaries, snapped to 1/30s, and make sure each jump-cut frame falls inside a B-roll clip.

### 4. Build the project
```bash
cd video-projects && HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init <slug> --example blank --resolution portrait --non-interactive --skip-transcribe
```
Start from `.claude/skills/ugc-meta-edit/templates/index.html` (the approved rehome video). It has the talking head as a muted `<video>` plus an `<audio>` from the same file, B-roll `<video class="broll">` on track 1, the hook title, and the caption CSS. Change the durations, B-roll list, title text and `.cap { top }` (from the analyzer's suggestion). Cut each B-roll to exact length first (`-ss <in> -frames:v <n> -an -vf scale=1080:1920,fps=30`). Copy `.gitignore` from an existing project (media and renders stay out of git; keep `edit-data/` with the EDL, B-roll plan, words and captions).

**Captions:** write the script as 2-3 word lines (break on punctuation, keep names like "Fel d 1" together), then:
```bash
python3 -I ../../.claude/skills/ugc-meta-edit/scripts/build_captions.py edit-data/words.json phrases.txt <duration> fix.json
```
It checks every phrase against the transcript, starts captions at 0, snaps to frames and injects them into index.html. Captions under 0.35s are flagged; merge them into a neighbour.

**Hook title** (only when the client wants one): cream `#F7F2B8` lowercase "pov: ..." text, **Poppins** 700 (Plus Jakarta Sans isn't auto-embedded), 74px, letter-spacing -0.065em, line-height 0.98, two forced lines (`<span class="ln">` with `white-space: nowrap`), left 65 / width 950 / top ~282, a soft dark text-shadow so it reads on white walls, and five small cream SVG stars around it but off her face. Static, shown for the first spoken line (~4-5s). Take the wording from the brief's hook options when possible.

### 5. Check before rendering
```bash
npx hyperframes lint                         # 0 errors (track-density / nested-div warnings are fine)
npx hyperframes snapshot . --at 0.5,<cut points>,<mid B-roll> --no-end -o .hyperframes/snap
```
Read the contact sheet: the title isn't on her face, captions sit below her chin, nothing is outside the safe lines, and the B-roll is right.

### 6. Render and verify
```bash
npx hyperframes render --quality standard --output renders/<name>-final.mp4   # ~2.5 min for 30s
python3 -I ../../.claude/skills/ugc-meta-edit/scripts/verify_render.py renders/<name>-final.mp4 assets/talking-head.mp4 <jump-cut frames> --sheet <scratchpad>/sheet.jpg
```
You need: 0 black/frozen events, loudness about -16 LUFS, every jump cut "covered", and a shortest shot of at least 15 frames. Then **look at the 4fps contact sheet** for captions, the title, the safe lines and B-roll content. Fix and re-render until clean. Use a draft render (`--quality draft`) first only when the user wants to review before the final.

### 7. Deliver
- Send with `SendUserFile` (`display: attach` for the final). If the user can't download, also make an ~18MB copy (`-crf 22 -maxrate 5M -bufsize 10M`), send it, and commit it to `deliverables/` so they can download it from GitHub (give the blob URL and say to click the download icon).
- Commit the project (not media) and push to the session branch.
- Report in plain words what you did, what you checked, and any trade-off, e.g. a caption slightly inside the brief's 40% zone.
- When the user gives feedback, apply it, re-verify, and save any new lasting rule to `PREFERENCES.md`.

## Mistakes already made (don't repeat)
- Mid-frame captions landed on her mouth when she leaned in; moving them above her head was rejected. Below the chin is correct.
- A 1-frame face flash between two B-roll clips: B-roll boundaries must touch exactly (snap both to the same frame).
- A 0.4s speaker flash between B-roll clips: extend the previous clip instead.
- Title wrapped to 3 lines and sat on her forehead: force 2 lines, move it up, check it on a snapshot.
- Using the B-roll folder without looking: other people appear in many spray clips.
- Yellow hook captions vs white body captions: one caption color only.
