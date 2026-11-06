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
| Audio | Her voice (-16 LUFS) plus a **soft, warm music bed by default** at **about -30 LUFS (~14 dB under her voice)**. Generate it with `video-projects/pacagen-bedding-spray-ugc/edit-data/music-bed.py <out.wav> <total_duration>`, then gain it to -30 LUFS. -38 LUFS was too quiet ("very little sound"). It must be audible in her pauses but never compete with her words. No SFX. |
| Captions | White `#FFFFFF` for the whole video, soft dark shadow, Inter 600 54px, sentence case, **2-3 words per caption** (fast swaps), no pills, strokes, karaoke or emoji. Start at frame 0 (even under a hook title). |
| Caption position | **One fixed spot just below her chin** for the whole video, never on her face, never above her head, never moving per shot. |
| B-roll | Must show what she is saying at that moment. **Must cover every jump cut** in her footage. **Never a different person** in frame (hands-only shots are fine). No speaker flash shorter than 0.5s between two B-roll clips. If nothing fits a line, stay on her. |
| Footage | Level a tilted camera (small rotate inside the crop). Conform to 1080x1920, 30fps CFR. Loudness about -16 LUFS. |
| CTA | If her video has no CTA and the client sends a CTA video (several alternative lines), see step 4b. |
| Brief | Check claims against the brief. Pacagen: say "**up to** 98%", spray lasts "up to 2 months", no medical claims ("treats/cures allergies", "fight allergies"). Rehome angle: end on the cat. Never mix spray and supplement mechanisms. |

## Meta safe area (1080x1920)

- Keep clear: **top 14% (0-270px), bottom 35% (1250-1920px), 6% each side (65px)**. Captions and titles live inside **x 65-1015, y 270-1250**.
- Pacagen's brief is stricter (**bottom 40% clear, y <= 1152**). Get as close as her face allows; if the caption has to sit lower, keep it above 1250 and tell the user how far into the 40% zone it is.
- Verify on rendered frames (the contact sheet draws the 270 and 1250 lines in red), not just in CSS.

## Workflow

Tell the user a time estimate before starting. A typical 30-50s video takes about 20-25 minutes with a direct final render, or about 35-50 minutes with a draft round. If they're in a hurry, skip the plan/approval step, pick sensible defaults, say what you picked, and render the final directly.

### 1. Get the files
Drive links must be "Anyone with the link - Viewer". Download into the scratchpad, not the repo, **directly from `drive.usercontent.google.com` with curl. Don't use gdown**: it redirects to `doc-*.googleusercontent.com`, which the session proxy blocks (403). curl uses the proxy and works for files of any size (a 1.2 GB talking head took ~1 min):
```bash
curl -sSL -o head-raw.mp4 -w "%{http_code} %{size_download}\n" \
  "https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=t"
file head-raw.mp4        # must say ISO Media / MP4; "HTML document" means the file isn't shared publicly
```
The Drive connector (`get_file_metadata`) is handy for the file's name and size, but don't download video through it (base64 into context).
**B-roll: start from the library, not a folder download.** `_reference/broll-library/LIBRARY.md` lists every Pacagen B-roll clip on Drive with what it shows, who is in it (`none` / `A` / `B`), good in-points (`@N`) and HDR notes. Plan the B-roll from it, then download **only the clips you picked**:
```bash
python3 -I _reference/broll-library/fetch_broll.py --find cat bed          # search
python3 -I _reference/broll-library/fetch_broll.py <scratch>/broll IMG_0114 "spraying sunlight" --sheet
```
Look at the contact sheet before using a clip. If the user sends a **new** B-roll folder, list it (`gdown.download_folder(url, skip_download=True)`; a folder over 50 files needs listing per subfolder), add it to `FOLDERS` + notes in `build_library.py`, add the listing to `drive-listing.json`, run `build_library.py`, and commit, so later sessions know it. Read a brief .docx by unzipping `word/document.xml`.

### 2. Transcribe and analyze her footage
```bash
ffmpeg -i head.mp4 -vn -ac 1 -ar 16000 head.wav
WHISPER=~/.cache/hyperframes/whisper/whisper.cpp/build/bin/whisper-cli
MODEL=~/.cache/hyperframes/whisper/models/ggml-small.en.bin
# Missing model? Fetch it with curl. `npx hyperframes transcribe` ignores the proxy and fails with ENOTFOUND huggingface.co.
# Needs huggingface.co + us.aws.cdn.hf.co on the environment allowlist (if curl gets a 403, ask to add them).
# If whisper-cli itself is missing, run `npx hyperframes transcribe` once to build it (it builds before failing on the model).
[ -s $MODEL ] || curl -sSL --create-dirs -o $MODEL https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin
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

People in B-roll are marked in the library: `A` (pacagen-main batch: spraying sheets / scratcher / pillows / stools / dining chairs / carpet entryway / coffee table / bed / stairs / desk chair, `laundry 3`) and `B` (the Nov-5 creator: lint rolling, showing each product, IMG_0165 couch, IMG_1108-1110 spraying). Use a person clip only when that person is the speaker. The empty sofa read as "plain B-roll" and was rejected.

Place each B-roll start/end on word boundaries, snapped to 1/30s, and make sure each jump-cut frame falls inside a B-roll clip.

### 4. Build the project
```bash
cd video-projects && HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init <slug> --example blank --resolution portrait --non-interactive --skip-transcribe
```
Start from `.claude/skills/ugc-meta-edit/templates/index.html` (the approved rehome video). It has the talking head as a muted `<video>` plus an `<audio>` from the same file, B-roll `<video class="broll">` on track 1, the hook title, and the caption CSS. Change the durations, B-roll list, title text and `.cap { top }` (from the analyzer's suggestion). Cut each B-roll to exact length first (`-ss <in> -frames:v <n> -an -vf scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30`), tone-mapping any HDR clip (see mistakes list). Copy `.gitignore` from an existing project (media and renders stay out of git; keep `edit-data/` with the EDL, B-roll plan, words and captions).

**GSAP must be local, not from the CDN.** The render browser can't reach `cdn.jsdelivr.net` through the session proxy, so the template loads `assets/gsap.min.js`. Copy it into the project (npm works through the proxy; the file is small, so commit it):
```bash
# from the project folder: copy it from an existing project...
cp ../pacagen-cats-gone-spray-ugc/assets/gsap.min.js assets/
# ...or, if none has it, pull it from npm:
(cd <scratch> && npm pack gsap@3.14.2 --silent && tar xzf gsap-3.14.2.tgz package/dist/gsap.min.js) && cp <scratch>/package/dist/gsap.min.js assets/
```

**Captions:** write the script as 2-3 word lines (break on punctuation, keep names like "Fel d 1" together), then:
```bash
python3 -I ../../.claude/skills/ugc-meta-edit/scripts/build_captions.py edit-data/words.json phrases.txt <duration> fix.json
```
It checks every phrase against the transcript, starts captions at 0, snaps to frames and injects them into index.html. Captions under 0.35s are flagged; merge them into a neighbour.

**Hook title** (only when the client wants one): **a new line for every video, and not always "pov:"** (e.g. "antihistamines vs. this spray: two different jobs"); cream `#F7F2B8` lowercase text, **Poppins** 700 (Plus Jakarta Sans isn't auto-embedded), 74px (drop to ~64px for a long first line), letter-spacing -0.065em, line-height 0.98, two forced lines (`<span class="ln">` with `white-space: nowrap`), left 65 / width 950 / top ~282. **It must not cover her face:** when her head is close to the top of the frame, drop to ~58px and pin it to top 272 so it sits on her hair, above the eyebrows, and check snapshots where she leans in. Use a soft dark text-shadow so it reads on white walls, and five small cream SVG stars around it but off her face. Static, shown for the first spoken line (~4-5s). Take the wording from the brief's hook options when possible.

### 4b. CTA from a separate video (when her script has none)
The client may send a CTA video in which she reads several alternative CTA lines. Transcribe it, find each line's edges with silencedetect / an RMS envelope (whisper word times run ~0.3-0.6s early), and pick the **one** line that fits this script (e.g. after "...at my friend's house." -> "If this sounds like your house, take a look at Pacagen."). Tell the user which one you picked plus 1-2 alternatives.
- **Audio only:** cut the line with ~0.25s of lead silence (`-ss <start> -t <dur> -vn`), gain it to -16 LUFS, add a 15ms fade in and a 30ms fade out, and save it as `assets/cta-01.m4a`. Add it as `<audio id="cta" data-start="<end of her video>">` and extend the root duration and the music bed to cover it.
- **B-roll over all of it**, since there's no face video there: keep the last cat shot running through the first half, then cut to the product (`showing product on counter` @0.4, only the first ~1.5s; a person appears in the background later) on "take a look at Pacagen". No other people in frame.
- Add the CTA words to `words.json` (timed from the envelope) and the lines to `phrases.txt`, then re-run `build_captions.py` with the new duration.

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
- iPhone HDR B-roll (`color_transfer=arib-std-b67`, bt2020) sends the renderer down a very slow HDR path (13+ min, half done) and can wash out colours. Check every cut clip with ffprobe and tone-map HDR ones to SDR bt709 when cutting: `-vf "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,..." -color_primaries bt709 -color_trc bt709 -colorspace bt709`.
- Detecting HDR in a shell loop with `ffprobe ... -of csv=p=0` returns `arib-std-b67,` (trailing comma), so an `= arib-std-b67` test silently fails and the clip isn't tone-mapped. Match with `case "$tr" in arib-std-b67*|smpte2084*)` or use `fetch_broll.py`'s HDR flag.
- Selfie-mode talking heads can be mirrored (the bottle label reads backwards). Check one frame and `hflip` if needed.
- Music bed at -38 LUFS (22 dB under) was "very little sound". Use about -30 LUFS.
- A 0.001s rounding gap between two B-roll clips (start + duration a hair short of the next start) shows one frame of the speaker. Set each duration to exactly `next_start - start`; verify_render.py flags it as a 1-frame shot.
- Stars on a full-width title land on the letters: keep stars in the side margins.
- Mid-frame captions landed on her mouth when she leaned in; moving them above her head was rejected. Below the chin is correct.
- A 1-frame face flash between two B-roll clips: B-roll boundaries must touch exactly (snap both to the same frame).
- A 0.4s speaker flash between B-roll clips: extend the previous clip instead.
- Title wrapped to 3 lines and sat on her forehead: force 2 lines, move it up, check it on a snapshot.
- Using the B-roll folder without looking: other people appear in many spray clips.
- Yellow hook captions vs white body captions: one caption color only.
- GSAP loaded from `cdn.jsdelivr.net`: the render stopped with `sub_timeline_script_failure ... ERR_TUNNEL_CONNECTION_FAILED` (`Cannot read properties of null (reading 'timeline')`). Load `assets/gsap.min.js` instead (step 4).
