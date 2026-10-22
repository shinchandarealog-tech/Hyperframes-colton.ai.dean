"""Frame-by-frame compositor for the Bike Masters Dussehra reel.

Layers, bottom to top: blue gradient bg -> source video (whip roll / card shrink) -> water strip
-> HTML/CSS graphics (headless Chrome, glass uses backdrop-filter over the composited base).
Motion blur is a 180-degree shutter: samples spread over half a frame interval and averaged.
Every output frame uses exactly one source frame (see SRC_INDEX), never resampled in time.

usage: render.py video OUT.mp4            full render (video only, no audio)
       render.py stills OUTDIR f1 f2 ...  single frames as PNG
"""
import base64, json, math, subprocess, sys, time
from pathlib import Path
import cv2
import numpy as np
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "source.mp4"
W, H, FPS = 1080, 1920, 30
SEG_A = (0, 558)          # source frames 0..557   -> reel 0.00-18.60
SEG_C = (1215, 1347)      # source frames 1215..1346 -> reel 18.60-23.00
N_FRAMES = (SEG_A[1] - SEG_A[0]) + (SEG_C[1] - SEG_C[0])
SHUTTER = 0.5 / FPS       # 180 degrees

def src_index(f):
    return f if f < SEG_A[1] else SEG_C[0] + (f - SEG_A[1])

# ---------------- easing ----------------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def spring(t, d, z=0.7):
    """Damped spring from rest (zero start velocity, ~4-5% overshoot), settled within d seconds."""
    if t <= 0: return 0.0
    wn = 5.2 / (z * d); wd = wn * math.sqrt(1 - z * z)
    return 1 - math.exp(-z * wn * t) * (math.cos(wd * t) + z * wn / wd * math.sin(wd * t))
def in_out_back(p, c1=0.6):
    c2 = c1 * 1.525
    if p < 0.5: return (2 * p) ** 2 * ((c2 + 1) * 2 * p - c2) / 2
    return ((2 * p - 2) ** 2 * ((c2 + 1) * (p * 2 - 2) + c2) + 2) / 2

# ---------------- video transform ----------------
WHIPS = [3.10, 6.60, 12.40, 18.60]   # whip centers (reel s); 18.60 is the cut
WHIP_D = 0.32
SHRINK_T, SHRINK_D, SHRINK_S, CARD_CY = 18.85, 0.75, 0.58, 770.0

def video_pose(t):
    """-> (roll_px, scale, center_y, corner_radius)"""
    roll = 0.0
    for c in WHIPS:
        p = (t - (c - WHIP_D / 2)) / WHIP_D
        if 0 < p < 1: roll = W * in_out_back(p)
    e = spring(t - SHRINK_T, SHRINK_D)
    s = 1 + (SHRINK_S - 1) * e
    cy = H / 2 + (CARD_CY - H / 2) * e
    return roll, s, cy, 52.0 * clamp(e * 1.6)

def video_motion(t0, t1):
    a, b = video_pose(t0), video_pose(t1)
    dr = abs(b[0] - a[0]); dr = min(dr, W - dr)
    return dr + abs(b[1] - a[1]) * H / 2 + abs(b[2] - a[2])

# ---------------- static layers ----------------
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

def hex_rgb(h): return np.array([int(h[i:i + 2], 16) for i in (5, 3, 1)], np.float32)  # BGR order (OpenCV)

def make_bg():
    stops = [(0, "#0A3F86"), (760, "#1C82D6"), (1350, "#0A3F86"), (1920, "#041633")]  # navy at the bottom so sky-blue captions read
    col = np.zeros((H, 3), np.float32)
    ys = np.arange(H)
    for c in range(3):
        col[:, c] = np.interp(ys, [s[0] for s in stops], [hex_rgb(s[1])[c] for s in stops])
    bg = np.repeat(col[:, None, :], W, axis=1)
    glow = np.exp(-(((XX - 540) / 520) ** 2 + ((YY - 760) / 760) ** 2))[..., None]
    return bg + glow * np.array([90, 70, 40], np.float32)
BG = make_bg()

WY0 = 1640  # water strip region top
WX, WYY = XX[WY0:], YY[WY0:]
DEEP, SKY, FOAM = hex_rgb("#0A4F96"), hex_rgb("#2EA6F2"), hex_rgb("#CFEFFF")

def water(t):
    """-> (rgb, alpha) for rows WY0..H. Slow, continuous motion only."""
    edge = 1712 + 12 * np.sin(2 * np.pi * WX / 620 + 1.3 * t) + 6 * np.sin(2 * np.pi * WX / 250 - 2.1 * t + 1.0)
    u, v = WX / W, (WYY - WY0) / (H - WY0)
    w1 = np.sin(u * 14 + np.sin(v * 9 + t * 1.1) * 1.4 + t * 0.7)
    w2 = np.sin(u * 23 - v * 7 + t * 1.3 + np.sin(u * 6 - t * 0.5))
    lines = np.exp(-((w1 + w2) / 0.35) ** 2)
    depth = np.clip((WYY - edge) / 200, 0, 1)[..., None]
    rgb = SKY * (1 - depth) + DEEP * depth
    rgb = rgb + lines[..., None] * (FOAM - rgb) * 0.45
    d = WYY - edge                                # >0 inside water
    alpha = np.clip(d + 0.5, 0, 1) * 0.94
    rim = np.exp(-(d / 2.2) ** 2)                 # bright rim on the wave crest
    rgb = rgb * (1 - rim[..., None]) + np.array([255, 247, 230], np.float32) * rim[..., None]
    alpha = np.maximum(alpha, rim)
    halo = np.exp(-(np.clip(-d, 0, None) / 16) ** 2) * (d < 0) * 0.45   # sky-blue glow above the crest
    return rgb, alpha, halo

def rrect_sdf(cx, cy, hw, hh, r):
    qx = np.abs(XX - cx) - (hw - r); qy = np.abs(YY - cy) - (hh - r)
    return np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - r

def base_frame(frame, t):
    roll, s, cy, rad = video_pose(t)
    if s >= 0.9999 and rad == 0:
        M = np.float32([[1, 0, -roll], [0, 1, 0]])
        out = cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP) if roll else frame.astype(np.float32)
        out = out.astype(np.float32)
    else:
        M = np.float32([[s, 0, W / 2 * (1 - s)], [0, s, cy - H / 2 * s]])
        vid = cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT).astype(np.float32)
        hw, hh = W * s / 2, H * s / 2
        sdf = rrect_sdf(W / 2, cy, hw, hh, rad)
        a = np.clip(0.5 - sdf, 0, 1)[..., None]
        k = clamp((1 - s) / (1 - SHRINK_S) * 3)   # card ring/glow/shadow fade in with the shrink
        sh = rrect_sdf(W / 2, cy + 26, hw, hh, rad)
        shadow = (k * 0.5 * np.exp(-(np.clip(sh, 0, None) / 38) ** 2) * (sh > -60))[..., None]
        glow = (k * 0.55 * np.exp(-(np.clip(sdf, 0, None) / 22) ** 2) * (sdf > 0))[..., None]
        out = BG * (1 - shadow) + BG * shadow * 0.25
        out = out + glow * (np.array([255, 205, 120], np.float32) - out)
        out = out * (1 - a) + vid * a
        ring = (np.clip(1 - np.abs(sdf + 3) / 2.5, 0, 1) * 0.6 * k)[..., None]
        out = out + ring * (255 - out)
    rgb, alpha, halo = water(t)
    seg = out[WY0:]
    seg += halo[..., None] * (np.array([255, 205, 120], np.float32) - seg)
    out[WY0:] = seg * (1 - alpha[..., None]) + rgb * alpha[..., None]
    return out

# ---------------- source reader ----------------
def read_source():
    sel = f"lt(n\\,{SEG_A[1]})+between(n\\,{SEG_C[0]}\\,{SEG_C[1] - 1})"
    cmd = ["ffmpeg", "-v", "error", "-i", str(SRC), "-vf",
           f"select='{sel}',scale={W}:{H}:flags=lanczos,unsharp=5:5:0.35,format=bgr24",
           "-fps_mode", "passthrough", "-f", "rawvideo", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n = 0
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        yield n, np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        n += 1
    p.wait()
    assert n == N_FRAMES, f"expected {N_FRAMES} source frames, got {n}"

# ---------------- page ----------------
class Page:
    def __init__(self, pw):
        self.b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        self.p = self.b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        self.p.goto((ROOT / "graphics" / "overlay.html").as_uri())
        self.p.evaluate("window.ready")
        self.cdp = self.p.context.new_cdp_session(self.p)

    def render(self, base_bgr, t):
        ok, jpg = cv2.imencode(".jpg", base_bgr, [cv2.IMWRITE_JPEG_QUALITY, 97])
        src = "data:image/jpeg;base64," + base64.b64encode(jpg).decode()
        self.p.evaluate("([s,t]) => setBase(s).then(() => apply(t))", [src, t])
        png = base64.b64decode(self.cdp.send("Page.captureScreenshot", {"format": "png", "optimizeForSpeed": True})["data"])
        return cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR).astype(np.float32)

    def motion(self, t0, t1): return self.p.evaluate("([a,b]) => motion(a,b)", [t0, t1])

def render_frame(page, frame, f, log):
    t = f / FPS
    t0, t1 = t - SHUTTER / 2, t + SHUTTER / 2
    disp = max(video_motion(t0, t1), page.motion(t0, t1))
    n = int(clamp(math.ceil(disp / 5.0), 1, 12))
    times = [t] if n == 1 else [t0 + (i + 0.5) * SHUTTER / n for i in range(n)]
    acc = None
    for ts in times:
        img = page.render(np.clip(base_frame(frame, ts), 0, 255).astype(np.uint8), ts)
        acc = img if acc is None else acc + img
    log.append({"f": f, "src": src_index(f), "samples": n, "disp": round(disp, 2)})
    return np.clip(acc / n + 0.5, 0, 255).astype(np.uint8)

def main():
    mode = sys.argv[1]
    log = []
    with sync_playwright() as pw:
        page = Page(pw)
        if mode == "stills":
            out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
            want = sorted(int(x) for x in sys.argv[3:])
            for n, fr in read_source():
                if n in want:
                    cv2.imwrite(str(out / f"f{n:04d}.png"), render_frame(page, fr, n, log))
                if n >= want[-1]: break
        else:
            enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                                    "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
            t_start = time.time()
            for n, fr in read_source():
                enc.stdin.write(render_frame(page, fr, n, log).tobytes())
                if n % 30 == 0: print(f"frame {n}/{N_FRAMES}  {time.time() - t_start:.0f}s", flush=True)
            enc.stdin.close(); enc.wait()
            assert [e["src"] for e in log] == [src_index(f) for f in range(N_FRAMES)]
        page.b.close()
    (ROOT / "renders").mkdir(exist_ok=True)
    json.dump(log, open(ROOT / "renders" / f"render-log-{mode}.json", "w"), indent=0)
    print("samples total", sum(e["samples"] for e in log), "frames", len(log))

if __name__ == "__main__":
    main()
