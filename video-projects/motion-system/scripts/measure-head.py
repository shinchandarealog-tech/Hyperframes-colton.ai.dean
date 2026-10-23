#!/usr/bin/env python3
"""Estimate a talking head's position over time for the footage map.

Samples the clip at --fps, finds skin-toned pixels inside a search box, and
reports the face's horizontal center and vertical extent per sample. The output
is a starting point: verify it with --overlay and hand-edit the footage map.

Usage:
  python3 -I scripts/measure-head.py <video> [--fps 2] [--box x0,y0,x1,y1]
                                     [--overlay out.jpg]
Coordinates are in source pixels. Prints JSON to stdout.
"""
import argparse
import json
import subprocess

import numpy as np


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height:format=duration", "-of", "json", path],
        capture_output=True, check=True, text=True).stdout
    d = json.loads(out)
    s = d["streams"][0]
    return s["width"], s["height"], float(d["format"]["duration"])


def frames(path, fps, w, h, scale):
    sw, sh = w // scale, h // scale
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={sw}:{sh}",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    size = sw * sh * 3
    while True:
        buf = proc.stdout.read(size)
        if len(buf) < size:
            break
        yield np.frombuffer(buf, np.uint8).reshape(sh, sw, 3).astype(np.int16)


def skin_mask(img):
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    return ((r > 95) & (g > 40) & (b > 20) & (mx - mn > 15) &
            (np.abs(r - g) > 15) & (r > g) & (r > b))


def hands(img, w, h, scale, band_top=0.76):
    """Skin-toned blobs in the bottom band (hands entering from the frame edge).
    Returns [[x0, y0, x1, y1], ...] in source px, padded by 24 px."""
    y0 = int(h * band_top) // scale
    m = skin_mask(img[y0:])
    cols = m.sum(axis=0) > 2
    rects, start = [], None
    for x, on in enumerate(list(cols) + [False]):
        if on and start is None:
            start = x
        elif not on and start is not None:
            if x - start >= 8:  # ignore specks narrower than ~32 source px
                ys = np.nonzero(m[:, start:x].sum(axis=1) > 0)[0]
                rects.append([max(0, start * scale - 24), (y0 + int(ys[0])) * scale - 24,
                              min(w, x * scale + 24), h])
            start = None
    return rects


def gesture_windows(samples, w, step):
    """Merge per-sample hand boxes into time windows, one per frame half.
    Blobs present in >60% of samples are static set dressing, not hands."""
    def key(r):
        return (r[0] // 64, r[2] // 64)
    seen = {}
    for s in samples:
        for r in s.get("hands", []):
            seen[key(r)] = seen.get(key(r), 0) + 1
    static = {k for k, n in seen.items() if n > 0.6 * len(samples)}
    # also drop anything overlapping a static blob's span
    spans = [(k[0] * 64, k[1] * 64 + 64) for k in static]
    windows = []
    for side in ("left", "right"):
        cur = None
        for s in samples:
            rs = [r for r in s.get("hands", [])
                  if key(r) not in static
                  and not any(r[0] < b and r[2] > a for a, b in spans)
                  and ((r[0] + r[2]) / 2 < w / 2) == (side == "left")]
            if rs:
                u = [min(r[0] for r in rs), min(r[1] for r in rs), max(r[2] for r in rs), max(r[3] for r in rs)]
                if cur and s["t"] - cur["end"] <= step * 1.5:
                    cur["end"] = s["t"]
                    cur["rect"] = [min(cur["rect"][0], u[0]), min(cur["rect"][1], u[1]),
                                   max(cur["rect"][2], u[2]), max(cur["rect"][3], u[3])]
                else:
                    cur = {"start": s["t"], "end": s["t"], "rect": u}
                    windows.append(cur)
    for g in windows:  # pad by a full sample: fast hands blur and drop out between samples
        g["start"] = round(max(0, g["start"] - step), 3)
        g["end"] = round(g["end"] + step, 3)
    return sorted(windows, key=lambda g: g["start"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--fps", type=float, default=2)
    ap.add_argument("--box", default=None, help="search box x0,y0,x1,y1 (source px)")
    ap.add_argument("--overlay", default=None, help="write a contact sheet with markers")
    ap.add_argument("--hands", action="store_true", help="also report hand boxes in the bottom band")
    a = ap.parse_args()

    w, h, dur = probe(a.video)
    scale = 4
    x0, y0, x1, y1 = ([int(v) for v in a.box.split(",")] if a.box
                      else (int(w * .3), int(h * .05), int(w * .73), int(h * .58)))
    samples = []
    thumbs = []
    for i, img in enumerate(frames(a.video, a.fps, w, h, scale)):
        crop = img[y0 // scale:y1 // scale, x0 // scale:x1 // scale]
        m = skin_mask(crop)
        t = round(i / a.fps, 3)
        cols = m.sum(axis=0)
        if cols.sum() < 50:
            samples.append({"t": t, "cx": None})
            continue
        # weighted median column = robust horizontal center of the face
        c = np.cumsum(cols)
        cx = int(np.searchsorted(c, c[-1] / 2)) * scale + x0
        rows = np.nonzero(m.sum(axis=1) > 3)[0]
        top = int(rows[0]) * scale + y0
        bottom = int(rows[-1]) * scale + y0
        sample = {"t": t, "cx": cx, "faceTop": top, "faceBottom": bottom}
        if a.hands:
            sample["hands"] = hands(img, w, h, scale)
        samples.append(sample)
        if a.overlay:
            thumbs.append((img.copy(), cx, top, bottom))

    out = {"source": {"width": w, "height": h, "duration": round(dur, 3)},
           "fps": a.fps, "box": [x0, y0, x1, y1], "samples": samples}
    if a.hands:
        out["gestures"] = gesture_windows(samples, w, 1 / a.fps)
    print(json.dumps(out, indent=1))

    if a.overlay and thumbs:
        from PIL import Image, ImageDraw
        tw, th = w // scale, h // scale
        cols_n = 6
        rows_n = (len(thumbs) + cols_n - 1) // cols_n
        sheet = Image.new("RGB", (tw * cols_n, th * rows_n))
        for k, (img, cx, top, bottom) in enumerate(thumbs):
            im = Image.fromarray(img.astype(np.uint8))
            d = ImageDraw.Draw(im)
            d.line([(cx // scale, 0), (cx // scale, th)], fill=(0, 255, 0), width=2)
            d.line([(0, top // scale), (tw, top // scale)], fill=(255, 0, 255), width=1)
            d.line([(0, bottom // scale), (tw, bottom // scale)], fill=(255, 0, 255), width=1)
            d.text((6, 6), f"{k / a.fps:.1f}s", fill=(255, 255, 0))
            sheet.paste(im, ((k % cols_n) * tw, (k // cols_n) * th))
        sheet.save(a.overlay, quality=85)


if __name__ == "__main__":
    main()
