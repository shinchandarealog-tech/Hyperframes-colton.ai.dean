# Paints out the baked-in "INSIDE THE VIDEO" line from the dream clip (s04).
import cv2, numpy as np, subprocess, sys, json
src, dst = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src); fps = cap.get(5)
W, H = int(cap.get(3)), int(cap.get(4))
ff = subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(fps),'-i','-',
     '-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',dst], stdin=subprocess.PIPE)
Y0, Y1 = 200, 1100
last = None; i = 0; log = []
while True:
    ok, fr = cap.read()
    if not ok: break
    t = i / fps; i += 1
    band = fr[Y0:Y1].astype(int)
    mn, mx = band.min(2), band.max(2)
    white = (mn > 222) & ((mx - mn) < 40)
    rows = white.sum(1) > 12
    clusters = []; r = 0
    while r < len(rows):
        if rows[r]:
            s = r
            while r < len(rows) and rows[min(r+1, len(rows)-1)] | rows[min(r+2, len(rows)-1)] | rows[min(r+3, len(rows)-1)] and r < len(rows)-1: r += 1
            clusters.append((s, r)); 
        r += 1
    box = None
    if len(clusters) >= 2:
        s, e = clusters[0]
        if 30 <= e - s <= 110 and clusters[1][0] - e < 90 and t < 3.1:
            cols = np.where(white[s:e+1].sum(0) > 0)[0]
            if cols.max() - cols.min() > 300: box = (int(cols.min()), Y0 + s, int(cols.max()), Y0 + e, clusters[1][0] + Y0)
    if box: last = box
    use = box or (last if t < 3.2 else None)
    if use:
        x0, y0, x1, y1, nexttop = use
        xa, xb = max(0, x0 - 24), min(W, x1 + 24)
        ya, yb = max(8, y0 - 16), nexttop - 1
        # colour of the scene just above the text, per column, softened sideways
        top = fr[ya-8:ya-1, xa:xb].astype(np.float32).mean(0, keepdims=True)
        top = cv2.GaussianBlur(top, (0, 0), sigmaX=5, sigmaY=0.1)
        fill = np.repeat(top, yb - ya, 0)
        # tiny vertical drift toward a wider average so it doesn't look like stretched pixels
        wide = cv2.GaussianBlur(top, (0, 0), sigmaX=25, sigmaY=0.1)
        a = np.linspace(0, 0.6, yb - ya)[:, None, None]
        fill = fill * (1 - a) + np.repeat(wide, yb - ya, 0) * a
        # feather horizontally at the box ends
        ramp = np.ones(xb - xa, np.float32); k = min(20, (xb - xa)//4)
        ramp[:k] = np.linspace(0, 1, k); ramp[-k:] = np.linspace(1, 0, k)
        reg = fr[ya:yb, xa:xb].astype(np.float32)
        fr[ya:yb, xa:xb] = (reg * (1 - ramp[None, :, None]) + fill * ramp[None, :, None]).clip(0, 255).astype(np.uint8)
        # navy extrusion pixels hugging the Hindi line top: same column colour
        below = fr[yb:yb+14, xa:xb]; dark = cv2.dilate((below.max(2) < 165).astype(np.uint8), np.ones((3,3),np.uint8)).astype(bool) & (below.min(2) < 200)
        below[dark] = np.repeat(wide, 14, 0)[:below.shape[0]][dark].astype(np.uint8)
    log.append((round(t, 2), use))
    ff.stdin.write(fr.tobytes())
ff.stdin.close(); ff.wait()
print('\n'.join(f'{t} {b}' for t, b in log[::6]))
