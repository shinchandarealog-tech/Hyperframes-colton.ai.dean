"""Render an extracted AE template spec with headless Chromium.

usage:
  python render.py SPEC.json OUT_BASENAME [--texts texts.json] [--media "Media 01=clip.mp4"]
                   [--fps 30] [--shutter 180] [--bg video_or_color] [--stills 0.5,1.0,2.0]

Outputs OUT_BASENAME.mov (ProRes 4444 with alpha, drop it over any footage) and
OUT_BASENAME_preview.mp4 (composited over --bg, default a dark gradient).
--texts maps "Comp name/Layer name" -> new text, e.g. {"Text 02/Text": "Let's"}.
--shutter 180 averages sub-frames across half a frame (motion blur); 0 = off (AE default).
"""
import argparse, base64, json, pathlib, subprocess, tempfile, time
import numpy as np, cv2
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent


def decode(data_url):
    raw = base64.b64decode(data_url.split(",", 1)[1])
    return cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_UNCHANGED)  # BGRA


def avg_premult(frames):
    acc = None
    for f in frames:
        f = f.astype(np.float32); a = f[..., 3:4] / 255.0
        pm = np.concatenate([f[..., :3] * a, a * 255.0], axis=2)
        acc = pm if acc is None else acc + pm
    acc /= len(frames)
    a = acc[..., 3:4] / 255.0
    rgb = np.where(a > 1e-4, acc[..., :3] / np.maximum(a, 1e-4), 0)
    return np.clip(np.concatenate([rgb, acc[..., 3:4]], axis=2) + 0.5, 0, 255).astype(np.uint8)


def prep_media(specs, tmp, fps, size):
    media = {}
    for s in specs or []:
        name, path = s.split("=", 1)
        d = pathlib.Path(tmp) / ("media_" + str(abs(hash(name))))
        d.mkdir(parents=True, exist_ok=True)
        w, h = size.get(name, (1080, 1080))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf",
                        f"fps={fps},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}",
                        "-q:v", "3", str(d / "f%05d.jpg")], check=True)
        n = len(list(d.glob("f*.jpg")))
        media[name] = {"pattern": (d / "f%05d.jpg").as_uri().replace("%2505d", "%05d"), "fps": fps, "frames": n,
                       "_first": 1}
        # ffmpeg numbers from 1; shift to 0-based by renaming
        for i in range(1, n + 1):
            (d / f"f{i:05d}.jpg").rename(d / f"g{i-1:05d}.jpg")
        media[name]["pattern"] = (d / "g%05d.jpg").as_uri().replace("%2505d", "%05d")
    return media


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("out")
    ap.add_argument("--texts"); ap.add_argument("--media", action="append")
    ap.add_argument("--fps", type=float, default=0); ap.add_argument("--shutter", type=float, default=0)
    ap.add_argument("--samples", type=int, default=8)
    ap.add_argument("--bg", default="gradient"); ap.add_argument("--stills")
    ap.add_argument("--duration", type=float, default=0)
    a = ap.parse_args()
    spec = json.loads(pathlib.Path(a.spec).read_text())
    texts = json.loads(pathlib.Path(a.texts).read_text()) if a.texts else {}
    out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    sizes = {c["name"]: (c["w"], c["h"]) for c in spec["comps"].values() if not c["layers"]}
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as p:
        root = spec["comps"][str(spec["root"])]
        fps = a.fps or root["fps"]
        media = prep_media(a.media, tmp, fps, sizes)
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                              args=["--allow-file-access-from-files", "--disable-web-security"])
        page = b.new_page(viewport={"width": root["w"], "height": root["h"]})
        page.on("console", lambda m: print("[page]", m.text) if m.type in ("warning", "error") else None)
        page.goto((HERE / "player.html").as_uri())
        info = page.evaluate("([s,o]) => setup(s,o)", [spec, {"texts": texts, "media": media}])
        dur = a.duration or info["duration"]
        if a.stills:
            for t in [float(x) for x in a.stills.split(",")]:
                cv2.imwrite(f"{a.out}_t{t:05.2f}.png", decode(page.evaluate("t => frame(t)", t)))
            print("stills written"); return
        n = int(round(dur * fps))
        fdir = pathlib.Path(tmp) / "frames"; fdir.mkdir()
        st = time.time()
        for i in range(n):
            t0 = i / fps
            if a.shutter > 0:
                span = a.shutter / 360 / fps
                img = avg_premult([decode(page.evaluate("t => frame(t)", t0 + (k + 0.5) / a.samples * span))
                                   for k in range(a.samples)])
            else:
                img = decode(page.evaluate("t => frame(t)", t0))
            cv2.imwrite(str(fdir / f"f{i:05d}.png"), img)
            if i % 25 == 0: print(f"frame {i}/{n} {time.time()-st:.0f}s", flush=True)
        b.close()
        seq = str(fdir / "f%05d.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(fps), "-i", seq, "-c:v", "prores_ks",
                        "-profile:v", "4444", "-pix_fmt", "yuva444p10le", str(out) + ".mov"], check=True)
        W, Hh = root["w"], root["h"]
        if a.bg == "gradient":
            bg = ["-f", "lavfi", "-i", f"gradients=s={W}x{Hh}:c0=0x1b1d24:c1=0x3a3f4b:x0=0:y0=0:x1={W}:y1={Hh}:d={dur}:r={fps}"]
        elif a.bg.startswith("#") or a.bg.startswith("0x"):
            bg = ["-f", "lavfi", "-i", f"color=c={a.bg.replace('#','0x')}:s={W}x{Hh}:d={dur}:r={fps}"]
        else:
            bg = ["-stream_loop", "-1", "-i", a.bg]
        subprocess.run(["ffmpeg", "-v", "error", "-y", *bg, "-framerate", str(fps), "-i", seq, "-filter_complex",
                        f"[0:v]fps={fps},scale={W}:{Hh}:force_original_aspect_ratio=increase,crop={W}:{Hh},format=rgb24[b];"
                        f"[b][1:v]overlay=format=auto,format=yuv420p[v]", "-map", "[v]", "-t", str(dur),
                        "-c:v", "libx264", "-crf", "16", "-preset", "medium", str(out) + "_preview.mp4"], check=True)
        print(f"done {n} frames in {time.time()-st:.0f}s -> {out}.mov, {out}_preview.mp4")


if __name__ == "__main__":
    main()
