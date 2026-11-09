# Portfolio videos

Drop the finished, exported edits here using these exact names. Until a file exists, the site shows a pink and sage placeholder in its place.

| File | Shows |
|---|---|
| `showreel.mp4` | Hero showreel (loops, muted) |
| `rehome-spray.mp4` | Rehome Spray |
| `alpaca-story.mp4` | The Alpaca Story |
| `pacagen-spray.mp4` | Pacagen Spray |

Optional cover images use the same name with `.jpg` (for example `rehome-spray.jpg`).

Shrink each export for the web before adding it (keeps each file around 3–6 MB):

```bash
ffmpeg -i final.mp4 -vf "scale=720:-2" -c:v libx264 -crf 26 -preset slow -c:a aac -b:a 128k -movflags +faststart rehome-spray.mp4
ffmpeg -ss 1 -i rehome-spray.mp4 -frames:v 1 -q:v 3 rehome-spray.jpg
```
