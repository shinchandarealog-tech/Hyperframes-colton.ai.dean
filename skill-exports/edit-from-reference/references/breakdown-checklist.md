# Breakdown checklist: how to study any reference

Work through every section. Write answers with **timestamps** and **numbers**. If something isn't present in the reference (e.g. no captions), write "none". That's information too.

## A. Commands (adapt paths; run each tool's own folder conventions)

```bash
# 0. Get it
yt-dlp -f 'bv*+ba/b' --no-playlist -o 'ref.%(ext)s' '<url>'          # social links
# Google Drive: https://drive.google.com/uc?export=download&id=<ID>  (large files return a
# "virus scan" page — parse its form action + hidden inputs and request that URL)

# 1. Probe
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of compact ref.mp4

# 2. Word-level transcript (any Whisper variant with word timestamps)
whisper ref.mp4 --model small.en --word_timestamps True --output_format json

# 3. Shot list (cut times)
ffmpeg -i ref.mp4 -an -vf "fps=30,scale=320:-1,select='gt(scene,0.15)',showinfo" -f null - 2>&1 | grep -o "pts_time:[0-9.]*"

# 4. Frames: 2 fps for the whole video, every frame around the hook/transitions
ffmpeg -i ref.mp4 -vf "fps=2,scale=270:-1" frames/f-%05d.jpg
ffmpeg -ss 0 -t 3 -i ref.mp4 -vsync 0 hook/h-%04d.jpg

# 5. Contact sheets with timestamps (makes reviewing hundreds of frames practical)
#    tile 24–40 frames per sheet, stamp each with its time, then READ every sheet

# 6. Silences / speech rhythm
ffmpeg -i ref.mp4 -vn -af "silencedetect=noise=-38dB:d=0.18" -f null - 2>&1 | grep silence_

# 7. Loudness
ffmpeg -i ref.mp4 -vn -af ebur128 -f null - 2>&1 | grep -E "I:|LRA:"

# 8. Colors: sample the most common pixel colors of a frame region (PIL/ImageMagick)
```

## B. What to observe

### 1. Format & structure
- Aspect ratio, resolution, fps, total length.
- Section map with timestamps: hook → setup → body beats → payoff → CTA/end.
- The energy curve: where it speeds up, where it breathes.

### 2. Hook (0–3s), frame by frame
- Frame 1: what exactly is on screen? A face, a product, text, motion?
- The first spoken words, and the first on-screen text.
- When the first cut or visual change happens (in seconds).
- The open loop or promise ("…and the 3rd one surprised me").

### 3. Pacing
- Number of shots, average shot length, shortest and longest.
- Where pacing changes and why (speeds up before a reveal, slows on emotion).
- How long the face is held between cutaways, and the maximum hold.

### 4. Cut logic
- What each cut is synced to: a stressed word, a sentence end, a music beat, an action (door opens, hand moves), a sound effect.
- Are cuts hard, or do they have a transition? Roughly what percentage of each?

### 5. Captions & typography
- Present? Full transcript, keywords only, or titles only?
- Words per caption; how many lines; does it build word by word or appear whole?
- Font family and weight (identify the closest Google/system font), case, letter-spacing.
- Size as a **percentage of frame height**; position (y range); alignment.
- Colors: base, emphasis, stroke or shadow, box or pill.
- Emphasis method: size jump, color, font switch, underline, box, animation.
- Entrance and exit animation (fade, pop, slide, typewriter, mask wipe) with durations.
- Timing tightness: does each word appear exactly on its word?

### 6. Graphics & overlays
- Types: lower thirds, name/price/spec tags, callouts with lines, numbers, maps, icons, logos, progress bars, UI recreations, charts.
- For each: design (shape, color, font), placement, entrance, exit, duration, and the script moment that triggers it.

### 7. Footage & camera
- Shot types: talking head (crop sizes), wide/establishing, detail/macro, drone, gimbal walk, POV, screen recording, stock.
- Camera motion: push-in, pull-out, pan, tilt, orbit, parallax, handheld, speed ramps, slow motion (and from what fps).
- Framing rules (face height, headroom, the subject on thirds) and how 16:9 sources are reframed.
- Source mix: the client's own footage vs stock vs AI vs archive.

### 8. Transitions
- List each type with its timestamp (hard cut, whip, zoom, blur, flash, mask wipe, match cut, morph, light leak).
- Rotation: do they repeat or vary? Is there a signature transition?

### 9. Color & texture
- Grade: warm/cool, contrast, saturation, crushed or lifted blacks, skin tone handling.
- Palette: 3–6 hex values (sampled) and their roles (background, text, accent).
- Texture: film grain, paper grain, noise, vignette, halation, overlays.

### 10. Script → visual mapping (most reusable)
- Make a table of "when they say X-type line, the edit shows Y". Examples: price → price card; new room → wide establishing shot; a feature → detail macro plus a spec tag; a number → animated counter; a claim → text slam; emotion → slow motion.

### 11. Sound
- Music: genre, BPM (approx.), energy curve, does it change at sections, does it end on a hit?
- Are cuts on the beat? Does the music duck under the voice, and by how much?
- SFX: types (whoosh, click, pop, riser, impact, ambience) and density (per 10s).
- Voice: processing (bright, compressed), room tone, voiceover vs on-camera.
- Use of silence or a music drop for emphasis.

### 12. Ending
- How it pays off the hook; CTA style (spoken, on screen, both); hold length; does it loop back to the start?

### 13. Signature moves & don't-copy list
- The 1–3 moves that make this style recognizable.
- Things that belong to the creator: logo, handles, faces, personal photos, catchphrases, licensed music, film clips.

## C. Quality bar for a breakdown

- Every claim has a **timestamp**; every size, length or color has a **number**.
- You could hand the style spec to another editor and they'd produce something recognizably similar.
- You've stated what you **couldn't** determine (e.g. "exact font unknown; closest match Montserrat 800").
