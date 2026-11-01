"""Render reel.html frame by frame in headless Chromium.

Each output frame n (24 fps) shows source frame(s) mapped 1:1 by srcMap().
Motion blur = 180 deg shutter: when any animation is active inside the
exposure window [n/24, n/24 + 0.5/24] we average K sub-frame screenshots
spread across that window; static frames are a single screenshot.

usage: python render_video.py out.mp4 [start end] (full render or a chunk)
       python render_video.py --stills dir n1 n2 ...   (PNG stills only)
"""
import subprocess, sys, pathlib, time
import numpy as np, cv2
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
FPS, N, K = 24, 888, 8
SHUTTER = 0.5 / FPS


def shoot(page):
    buf = page.screenshot(type="png")
    return cv2.imdecode(np.frombuffer(buf, np.uint8), cv2.IMREAD_COLOR)


def frame(page, n):
    page.evaluate("n => window.setFrame(n)", n)
    t0 = n / FPS
    if page.evaluate("([a,b]) => window.moving(a,b)", [t0, t0 + SHUTTER]):
        acc = None
        for k in range(K):
            page.evaluate("t => window.draw(t)", t0 + (k + 0.5) / K * SHUTTER)
            img = shoot(page).astype(np.float32)
            acc = img if acc is None else acc + img
        return np.clip(acc / K + 0.5, 0, 255).astype(np.uint8), True
    page.evaluate("t => window.draw(t)", t0 + SHUTTER / 2)
    return shoot(page), False


def main():
    args = sys.argv[1:]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--allow-file-access-from-files", "--disable-gpu-vsync"])
        page = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        page.goto((ROOT / "reel.html").as_uri())
        page.evaluate("document.fonts.ready")
        page.evaluate("window.primeAll()")  # register every animation window
        if args[0] == "--stills":
            out = pathlib.Path(args[1]); out.mkdir(parents=True, exist_ok=True)
            for n in map(int, args[2:]):
                img, _ = frame(page, n)
                cv2.imwrite(str(out / f"still_{n:04d}.png"), img)
            return
        ff = subprocess.Popen([
            "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920",
            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "15",
            "-pix_fmt", "yuv420p", "-r", str(FPS), args[0]], stdin=subprocess.PIPE)
        a, z = (int(args[1]), int(args[2])) if len(args) > 2 else (0, N)
        st = time.time(); blurred = 0
        for n in range(a, z):
            img, mv = frame(page, n); blurred += mv
            ff.stdin.write(img.tobytes())
            if n % 48 == 0:
                print(f"frame {n}/{N}  {time.time()-st:.0f}s", flush=True)
        ff.stdin.close(); ff.wait()
        print(f"done: {z-a} frames, {blurred} with shutter blur, {time.time()-st:.0f}s")
        b.close()


if __name__ == "__main__":
    main()
