"""Measure each text/shape element's offset vs the reference at a settled frame (phase correlation of gradient
magnitude in a box around the element) and accumulate into scripts/corrections.json.
usage: correct.py <refdir> <minedir> [--apply]"""
import cv2, numpy as np, sys, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from graphics import GROUPS
refdir, minedir = sys.argv[1:3]; apply = "--apply" in sys.argv
CAL = json.load(open(os.path.join(HERE, "calib.json")))
cp = os.path.join(HERE, "corrections.json"); CORR = json.load(open(cp)) if os.path.exists(cp) else {}
def g(im):
    im = cv2.GaussianBlur(im, (0, 0), 1.0); return np.hypot(cv2.Sobel(im, cv2.CV_32F, 1, 0), cv2.Sobel(im, cv2.CV_32F, 0, 1))
def boxes():
    for G in GROUPS:
        f = G["hide"] - 1 if G["hide"] - G["show"] > 3 else G["hide"]
        stack = list(G["children"])
        while stack:
            c = stack.pop()
            if c["k"] == "unit": stack += c["children"]; continue
            if c["k"] == "text":
                cal = CAL[c["id"]]
                if c["ink"]: x0, y0, x1, y1 = c["ink"]
                else: x0 = cal["left"]; x1 = x0 + cal["adv"]; y0 = cal["base"] - cal["size"] * 0.78; y1 = cal["base"] + cal["size"] * 0.05
                yield c["id"], f, (int(x0) - 10, int(y0) - 10, int(x1) + 10, int(y1) + 10)
            elif c["k"] in ("rect", "icon"):
                x0, y0, x1, y1 = c["r"]; yield c["id"], f, (int(x0) - 8, int(y0) - 8, int(x1) + 8, int(y1) + 8)
res = {}
for eid, f, (x0, y0, x1, y1) in boxes():
    x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(1080, x1), min(1920, y1)
    a = cv2.imread(f"{refdir}/f{f+1:04d}.png", 0).astype(np.float32)[y0:y1, x0:x1]
    b = cv2.imread(f"{minedir}/f{f+1:04d}.png", 0).astype(np.float32)[y0:y1, x0:x1]
    if a.shape[0] < 16 or a.shape[1] < 16: continue
    win = cv2.createHanningWindow((a.shape[1], a.shape[0]), cv2.CV_32F)
    (dx, dy), r = cv2.phaseCorrelate(g(b), g(a), win)
    res[eid] = (round(dx, 2), round(dy, 2), round(r, 2), f)
    flag = "  !" if (abs(dx) > 1.5 or abs(dy) > 1.5) else ""
    print(f"{eid:22s} f{f:5d} dx {dx:+6.2f} dy {dy:+6.2f} resp {r:.2f}{flag}")
if apply:
    for eid, (dx, dy, r, f) in res.items():
        if r < 0.3 or abs(dx) > 25 or abs(dy) > 25: continue   # unreliable match
        old = CORR.get(eid, [0, 0]); CORR[eid] = [round(old[0] + dx, 2), round(old[1] + dy, 2)]
    json.dump(CORR, open(cp, "w"), indent=0); print("applied", len(CORR))
