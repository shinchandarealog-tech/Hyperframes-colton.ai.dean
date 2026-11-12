"""All-20 compilation (number badge burned in, compilation only) + overview image (4x5 grid, settled frame of each)."""
import subprocess, os, cv2, numpy as np
R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "renders")
ids = [n for n in range(1, 21) if os.path.exists(f"{R}/t{n:02d}.mp4")]
font = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
parts = []
for n in ids:
    o = f"{R}/_badge{n:02d}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/t{n:02d}.mp4", "-vf", f"drawtext=fontfile={font}:text='#{n:02d}':x=36:y=36:fontsize=72:fontcolor=white:box=1:boxcolor=black@0.65:boxborderw=18",
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", o], check=True)
    parts.append(o)
open(f"{R}/_list.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{R}/_list.txt", "-c", "copy", "-movflags", "+faststart", f"{R}/all-20-templates.mp4"], check=True)
for p in parts: os.remove(p)
os.remove(f"{R}/_list.txt")
tiles = []
for n in ids:
    cap = cv2.VideoCapture(f"{R}/t{n:02d}.mp4"); N = int(cap.get(7)); cap.set(1, max(0, N - 4)); ok, fr = cap.read()
    im = cv2.resize(fr, (360, 640), interpolation=cv2.INTER_AREA)
    cv2.rectangle(im, (0, 0), (118, 92), (0, 0, 0), -1); cv2.putText(im, f"{n:02d}", (10, 72), cv2.FONT_HERSHEY_DUPLEX, 2.3, (255, 255, 255), 3, cv2.LINE_AA)
    tiles.append(cv2.copyMakeBorder(im, 6, 6, 6, 6, cv2.BORDER_CONSTANT, value=(255, 255, 255)))
while len(tiles) % 5: tiles.append(np.full_like(tiles[0], 255))
cv2.imwrite(f"{R}/overview-20-templates.jpg", np.vstack([np.hstack(tiles[i:i + 5]) for i in range(0, len(tiles), 5)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok", ids)
