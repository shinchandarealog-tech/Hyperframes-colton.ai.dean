"""20 Sedate-Us-style templates from the client's own a-roll sentences.
Geometry, colours, sizes and motion come from the spec / reference measurements (same values as the replica and the
client-1 reel); only the words, the b-roll and the speaker footage change. Lines wider than the spec's safe area
(x 58..1022) are shrunk to fit. usage: templates.py <rawframes_dir> <matte_model> [ids...]"""
import json, os, sys, math, subprocess
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
RAW, MODEL = sys.argv[1], sys.argv[2]; ONLY = [int(x) for x in sys.argv[3:]]
WORDS = json.load(open(os.path.join(ROOT, "assets/transcript.json")))
WORDS[28]["start"] = 7.76            # "five" sits after the 7.43-7.75 s pause (audio level), whisper put it before
PAUSES = [(7.46, 7.73), (16.37, 16.66)]   # measured silences cut inside phrases
SPK_CUT = 11.745
I, B = "Inter", "Bebas Neue"
BADGE = open(os.path.join(HERE, "badge_path.txt")).read().strip()

# ---------------------------------------------------------------- timing
class Seg:
    def __init__(s, t0, t1):
        s.t0, s.t1 = t0, t1
        s.cuts = [(a, b) for a, b in PAUSES if t0 < a and b < t1]
        s.dur = (t1 - t0) - sum(b - a for a, b in s.cuts); s.N = int(round(s.dur * 30))
    def reel(s, t):  # source -> template seconds
        r = t - s.t0
        for a, b in s.cuts:
            if t >= b: r -= (b - a)
            elif t > a: r -= (t - a)
        return r
    def src(s, r):   # template seconds -> source
        t = s.t0 + r
        for a, b in s.cuts:
            if t >= a: t += (b - a)
        return t
    def f(s, wi, lead=4):  # visible frame of word index wi
        return max(0, int(round(s.reel(WORDS[wi]["start"]) * 30)) - lead)

# ---------------------------------------------------------------- layout (Chromium ink measurement)
def lay(items):
    p = os.path.join(HERE, "_lay_in.json"); o = os.path.join(HERE, "_lay_out.json")
    json.dump(items, open(p, "w"))
    subprocess.run(["node", os.path.join(HERE, "layout.cjs"), p, os.path.join(ROOT, "assets/fonts"), o], check=True, capture_output=True)
    return json.load(open(o))
def it(id, text, fam, wt, size, ls, anchor, x, base): return dict(id=id, text=text, fam=fam, wt=wt, size=size, ls=ls, anchor=anchor, x=x, base=base)
def fit(item, maxw):
    """lay one item; shrink its size until the ink width fits maxw (keeps anchor + baseline)"""
    for _ in range(6):
        r = lay([item])[item["id"]]; w = r["ink"][2] - r["ink"][0]
        if w <= maxw: return r
        item = dict(item, size=round(item["size"] * maxw / w * 0.995, 2))
    return r

# ---------------------------------------------------------------- html helpers
def span(id, L, fam, wt, color, inner, shadow=None):
    f = "inter" if fam == I else "bebas"; sh = f";text-shadow:{shadow}" if shadow else ""
    return (f'<span id="{id}" class="txt {f}" style="left:{L["left"]}px;top:{L["top"]}px;font-size:{L["size"]}px;font-weight:{wt};'
            f'letter-spacing:{L["ls"]}em;color:{color}{sh}">{inner}</span>')
def parts(pfx, words): return " ".join(f'<span id="{pfx}-{i}" class="pt">{w}</span>' for i, w in enumerate(words))
def rect(id, x0, y0, x1, y1, fill, r=0, extra=""):
    return f'<div id="{id}" class="abs" style="left:{x0:.1f}px;top:{y0:.1f}px;width:{x1-x0:.1f}px;height:{y1-y0:.1f}px;border-radius:{r}px;background:{fill};{extra}"></div>'
def glyph(kind, d, col):
    if kind == "bang":
        w = 0.115 * d; h = 0.42 * d; dt = 0.115 * d; gap = 0.07 * d; top = (d - (h + gap + dt)) / 2; x = (d - w) / 2
        return f'<svg width="{d}" height="{d}" style="position:absolute;left:0;top:0"><rect x="{x}" y="{top}" width="{w}" height="{h}" rx="{w/2}" fill="{col}"/><rect x="{x}" y="{top+h+gap}" width="{w}" height="{dt}" rx="{w/2}" fill="{col}"/></svg>'
    if kind == "plus":
        a = 0.25 * d; sw = 0.11 * d; c = d / 2
        return f'<svg width="{d}" height="{d}" style="position:absolute;left:0;top:0"><path d="M{c-a} {c} H{c+a} M{c} {c-a} V{c+a}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/></svg>'
    if kind == "check":
        return f'<svg width="{d}" height="{d}" viewBox="0 0 104 104" style="position:absolute;left:0;top:0"><path class="draw" pathLength="1" d="M32 54 L46 67 L73 38" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray:1;stroke-dashoffset:0"/></svg>'
    if kind == "x":
        return f'<svg width="{d}" height="{d}" viewBox="0 0 106 106" style="position:absolute;left:0;top:0"><path class="draw" pathLength="1" d="M53 53 L33 31 M53 53 L74 77 M53 53 L74 31 M53 53 L33 77" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round" style="stroke-dasharray:0.25 0.75;stroke-dashoffset:0"/></svg>'
    if kind in ("sparkle", "star"):
        n, R, r = (4, 0.275, 0.06) if kind == "sparkle" else (5, 0.27, 0.12); c = d / 2
        pts = " ".join(f"{c+(R if i%2==0 else r)*d*math.cos(math.pi/n*i-math.pi/2):.2f},{c+(R if i%2==0 else r)*d*math.sin(math.pi/n*i-math.pi/2):.2f}" for i in range(2 * n))
        return f'<svg width="{d}" height="{d}" style="position:absolute;left:0;top:0"><polygon points="{pts}" fill="{col}" stroke="{col}" stroke-width="{0.04*d:.2f}" stroke-linejoin="round"/></svg>'
def icon(id, x0, y0, d, fill, kind, col="#FFFFFF"):
    return f'<div id="{id}" class="abs" style="left:{x0}px;top:{y0}px;width:{d}px;height:{d}px;border-radius:50%;background:{fill};transform-origin:50% 50%">{glyph(kind, d, col)}</div>'
GRADS = {"black": ("0,0,0", [(920, 0), (1080, .043), (1200, .118), (1280, .20), (1360, .31), (1440, .44), (1480, .50), (1520, .57), (1600, .71), (1680, .82), (1760, .90), (1840, .96), (1920, .98)]),
         "orange": ("164,77,37", [(1220, 0), (1300, .16), (1380, .31), (1460, .50), (1540, .57), (1620, .59), (1700, .60), (1780, .66), (1860, .73), (1920, .76)]),
         "green": ("23,33,17", [(1220, 0), (1300, .30), (1380, .60), (1460, .72), (1540, .75), (1620, .84), (1700, .88), (1780, .93), (1860, .96), (1920, .97)]),
         "brown": ("35,28,21", [(1220, 0), (1300, .32), (1380, .72), (1460, .81), (1540, .86), (1620, .92), (1700, .95), (1780, .97), (1860, .99), (1920, .99)]),
         "panel": ("166,92,54", [(540, 0), (600, .14), (720, .34), (900, .52), (948, .56)])}
def grad(n): rgb, st = GRADS[n]; return "linear-gradient(to bottom, " + ", ".join(f"rgba({rgb},{a}) {y}px" for y, a in st) + ")"
F = lambda f: round(f / 30, 6)
PANS = ["199.2+(-33.4-199.2)*circ((r-1)/52.7)", "110.1+(-28.0-110.1)*p4out(r/112.7)", "317.7+(-23.5-317.7)*circ((r+0.7)/29.1)",
        "180.8+(-4.4-180.8)*circ((r-0.8)/68.7)", "244.0+(-22.3-244.0)*p4out((r-1.3)/59.2)", "297.6*Math.exp(-r/15.6)-50", "255.5*Math.exp(-r/5.9)+3.14*(20-r)-9.2"]
PANELPANS = ["116.2+(-16.1-116.2)*circ(r/29.0)", "137.1+(-11.8-137.1)*circ((Math.min(r,18)+1.9)/40.1)", "138.2+(-6.4-138.2)*circ((Math.min(r,17)-1)/35.8)"]
MK = {l.split()[0]: int(l.split()[1]) for l in open(os.path.join(HERE, "mixkit_picks.txt"))}

class T:
    def __init__(s, n, t0, t1, kind):
        s.n, s.seg, s.kind = n, Seg(t0, t1), kind; s.H = []; s.JS = []; s.media = []; s.broll_runs = []; s.cuts = []; s.sfx = []; s.N = s.seg.N
        s.speaker = "A" if t1 <= SPK_CUT + 0.05 else "B"
    # timing helpers
    def v(s, wi, lead=4): return s.seg.f(wi, lead)
    def canon(s, sel, v): s.JS.append(f'W("{sel}",{{D:29,t0:{v-4.6},dur:33.7,vis:{v}}});')
    def emph(s, sel, v, D=53, dur=40, op0=0.38, opd=30): s.JS.append(f'W("{sel}",{{D:{D},t0:{v},dur:{dur},vis:{v},op0:{op0},opCirc:true,opDur:{opd}}});')
    def fade(s, sel, v, op0=0.45, d=10): s.JS.append(f'FADE("{sel}",{v},{op0},{d});')
    def grp(s, sel, a, b): s.JS.append(f'GRP("{sel}",{a},{b});')
    # media
    def face(s, z=1):
        s.media.append(("face", 0, s.N - 1)); s.H.append(f'<video id="face" data-start="0" data-duration="{F(s.N)}" data-track-index="1" src="assets/t{s.n:02d}_face.mp4" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:{z}"></video>')
    def gradient(s, name, a=0, b=None):
        b = s.N - 1 if b is None else b; s.H.append(f'<div id="gr-{name}-{a}" class="abs layer" style="z-index:5;background:{grad(name)}"></div>'); s.grp(f"#gr-{name}-{a}", a, b)
    def broll(s, shots, area=(0, 0, 1080, 1920), panel=False, z=2):
        """shots: [(clip, f0, f1, 'still'|'video', pos%)]"""
        out = []
        for k, (clip, f0, f1, kind, pos) in enumerate(shots):
            x0, y0, w, h = area; pan = (PANELPANS if panel else PANS)[k % (3 if panel else 7)] if kind == "still" else None
            Lp, Rp = (330, 60) if pan else (0, 0); box = f"left:{x0-Lp}px;top:{y0}px;width:{w+Lp+Rp}px;height:{h}px"; sid = f"b{k}"
            src = f"assets/t{s.n:02d}_{sid}.{'jpg' if kind=='still' else 'mp4'}"; s.media.append(("broll", clip, f0, f1, kind, src))
            if pan: s.JS.append(f'FN("#pan-{sid}","x",{f0},{f1+1},f=>{{const r=f-{f0};return {pan};}});')
            if kind == "still":
                out.append(f'<div id="clip-{sid}" class="clip abs" data-start="{F(f0)}" data-duration="{F(f1-f0+1)}" data-track-index="2" style="inset:0;z-index:{z}"><div id="pan-{sid}" class="abs" style="{box}">'
                           f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos}% 50%;display:block"></div></div>')
            else:
                out.append(f'<div id="pan-{sid}" class="abs" style="{box};z-index:{z}"><video id="v-{sid}" data-start="{F(f0)}" data-duration="{F(f1-f0+1)}" data-track-index="3" src="{src}" muted playsinline style="width:100%;height:100%;object-fit:cover;object-position:{pos}% 50%;display:block"></video></div>')
            if k > 0: s.cuts.append(f0)
        if not panel: s.broll_runs.append((shots[0][1], shots[-1][2]))
        return out
    def split(s, top_shots, caption_html):
        sp = ['<div id="splitA" class="abs layer" style="z-index:3;background:#FFFFFF">',
              '<div class="abs" style="left:14px;top:14px;width:1052px;height:930px;border-radius:23.5px;overflow:hidden"><div class="abs" style="left:-14px;top:-14px;width:1080px;height:1920px">']
        sp += s.broll(top_shots, (14, 14, 1052, 930), panel=True)
        sp.append(f'<div class="abs layer" style="z-index:3;background:{grad("panel")}"></div><div class="abs layer" style="z-index:4">{caption_html}</div></div></div>')
        sp.append('<div class="abs" style="left:14px;top:974px;width:1052px;height:930px;border-radius:21px;overflow:hidden"><div class="abs" style="left:-14px;top:-974px;width:1080px;height:1920px">'
                  f'<video id="spl" data-start="0" data-duration="{F(s.N)}" data-track-index="1" src="assets/t{s.n:02d}_split.mp4" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px"></video></div></div></div>')
        s.media.append(("split", 0, s.N - 1)); s.H.append("".join(sp))
        for f in [x[1] for x in top_shots[1:]]: s.sfx.append(("dclick", f))
    def tag(s, y0, f0=0):
        n = lay([it("tn", "Your Name", I, 600, 32.67, -0.025, "left", 136, y0 + 46), it("ts", "Creator", I, 400, 24.78, -0.02, "left", 137, y0 + 70)])
        bx = n["tn"]["ink"][2] + 4; w = bx + 54 - 117
        s.H.append(f'<div id="tag" class="abs layer" style="z-index:10">' + rect("tagbox", 117, y0, 117 + w, y0 + 88, "rgba(0,0,0,.68)", 10) + span("tagn", n["tn"], I, 600, "#F7F3EF", "Your Name")
                   + f'<svg class="abs" style="left:{bx:.1f}px;top:{y0+17}px;width:34px;height:32px" viewBox="-1 -1 36 34" preserveAspectRatio="none"><path fill="#10B3E2" d="{BADGE}"/><path d="M10.5 16.4 L15 20.6 L23.5 11.8" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
                   + span("tags", n["ts"], I, 400, "#F3EAE5", "Creator") + "</div>")
        s.JS.append(f'FN("#tag","x",{f0},{f0+41.2},f=>-141.7*(1-circ((f-{f0})/41.2)));')
    def gfx(s, html): s.H.append(f'<div class="abs layer" style="z-index:10">{html}</div>')

# ---------------------------------------------------------------- components (reference geometry)
def bar_page(t, pid, small, small_wis, big, big_wis, geo, a, b, color="#A24A24", wipe=None):
    """small line + highlight bar + Bebas word(s). geo: S01 (small 80.7 @1016, bar 1028-1168, Bebas 168) | S06 | S12 | S15 | S17"""
    G = {"S01": dict(ss=80.7, sw=600, sls=-0.05, sb=1016, bt=1028, bb=1168, bs=168.25, bls=-0.045, bbase=1161.4, padl=27, padr=25),
         "S06": dict(ss=69.0, sw=600, sls=-0.054, sb=1094, bt=1094, bb=1205, bs=142.86, bls=-0.05, bbase=1202, padl=23, padr=23),
         "S12": dict(ss=67.63, sw=400, sls=-0.05, sb=1027, bt=1025, bb=1200, bs=222.8, bls=-0.057, bbase=1189, padl=37, padr=34),
         "S15": dict(ss=62.43, sw=400, sls=-0.05, sb=1138, bt=1142, bb=1294, bs=193.9, bls=-0.053, bbase=1287, padl=15, padr=9),
         "S17": dict(ss=81.0, sw=600, sls=-0.06, sb=1017, bt=1028, bb=1168, bs=168.25, bls=-0.046, bbase=1161, padl=44, padr=43)}[geo]
    caps = geo in ("S12", "S15")
    sm = fit(it(pid + "s", small.upper() if caps else small, I, G["sw"], G["ss"], G["sls"], "center", 540, G["sb"]), 940)
    bg = fit(it(pid + "b", big, B, 400, G["bs"], G["bls"], "center", 540, G["bbase"]), 960 - G["padl"] - G["padr"])
    x0, x1 = bg["ink"][0] - G["padl"], bg["ink"][2] + G["padr"]
    sw = (small.upper() if caps else small).split(" "); bw = big.split(" ")
    html = (f'<div id="{pid}" class="abs layer">' + span(pid + "-s", sm, I, G["sw"], "#FBF8F3", parts(pid + "s", sw))
            + rect(pid + "-bar", x0, G["bt"], x1, G["bb"], color, 0, "transform-origin:0% 50%")
            + span(pid + "-B", bg, B, 400, "#F9F5EF", parts(pid + "b", bw)) + "</div>")
    t.grp("#" + pid, a, b)
    for i, wi in enumerate(small_wis): t.canon(f"#{pid}s-{i}", max(a, t.v(wi)))
    bv = [max(a, t.v(wi)) for wi in big_wis]
    # bar: the reference's measured expo-like right-edge curve (S17, 25 frames), opening so the Bebas lands at ~35 %
    curve = [243, 248, 255, 263, 274, 288, 304, 328, 360, 406, 499, 592, 672, 720, 752, 773, 792, 805, 812, 824, 832, 838, 840, 844, 846]
    st = max(a, bv[0] - 8); t.JS.append(f'ON("#{pid}-bar",{st});')
    t.JS.append(f'TAB("#{pid}-bar","scaleX",{json.dumps({str(st+i): round((e-232)/614, 4) for i, e in enumerate(curve)})});')
    for i, v in enumerate(bv): t.JS.append(f'W("#{pid}b-{i}",{{D:29,t0:{v-4.6},dur:33.7,vis:{v},op0:1}});')
    return html

def build(n):
    S = {}  # template definitions
    def tdef(n, t0, t1, kind, fn): S[n] = (t0, t1, kind, fn)

    # 1 hook speaker A: the approved client hook (plate + fragment reused unchanged)
    def t1(t):
        t.H.append('<video id="face" data-start="0" data-duration="3.8" data-track-index="1" src="assets/plate_S01.mp4" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:1"></video>')
        t.gradient("black"); hk = json.load(open(os.path.join(HERE, "hook_fragment.json"))); t.H.append(hk["html"]); t.JS.append(hk["js"])
    tdef(1, 0.0, 3.80, "hook", t1)

    # 2 hook speaker B (S01 layout: small / peach big / pill, then small / rust bar Bebas)
    def t2(t):
        t.media.append(("face", 0, t.N - 1, "hook")); t.H.append(f'<video id="face" data-start="0" data-duration="{F(t.N)}" data-track-index="1" src="assets/t02_face.mp4" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:1"></video>')
        t.gradient("black"); t.tag(1201, 0)
        L = lay([it("s", "It’s really", I, 400, 83.4, -0.063, "center", 540, 1017), it("p", "frustrating", I, 500, 151, -0.06, "center", 530, 1100),
                 it("q", "because like", I, 600, 54.63, -0.067, "center", 541, 1143.3)])
        q = L["q"]["ink"]; pv = t.v(46)
        p1 = ('<div id="p1" class="abs layer">' + span("p1s", L["s"], I, 400, "#F9F8F8", parts("p1w", ["It’s", "really"])) + span("p1p", L["p"], I, 500, "#ECA572", "frustrating")
              + f'<div id="p1q" class="abs layer">{rect("p1qr", q[0]-42.5, 1091.7, q[2]+41.5, 1156.9, "#A24A26", 32.6)}{span("p1qt", L["q"], I, 600, "#FFF8ED", "because like")}</div></div>')
        end1 = t.v(48) - 1; t.grp("#p1", 2, end1)
        t.canon("#p1w-0", 2); t.canon("#p1w-1", max(4, t.v(44)))
        t.JS.append(f'W("#p1p",{{D:40.4,t0:{t.v(45)-8.15},dur:32.7,vis:{t.v(45)}}});')
        t.JS.append(f'ON("#p1q",{pv},0.86); FN("#p1q","y",{pv},{pv+14.2},f=>f<{pv+0.6}?27.3:27.3*(1-backOut((f-{pv+0.6})/13.6,2.7))); OP("#p1q",{pv},{pv+4},0.86,1);')
        t.gfx(p1 + bar_page(t, "p2", "where do you", [48, 49, 50], "GO?", [51], "S01", end1 + 1, t.N - 1))
    tdef(2, 11.80, 14.67, "hook", t2)

    # 3 b-roll + pill (S02), two pages
    def t3(t):
        t.H += t.broll([("S02a", 0, 33, "still", 50), ("S02b", 34, t.N - 1, "still", 50)]); t.gradient("orange")
        a = lay([it("w", "Because if you", I, 400, 72.9, -0.036, "left", 144, 1198)]); px = a["w"]["ink"][2] + 11 + 36
        a.update(lay([it("pt", "THINK ABOUT IT", I, 600, 46.8, -0.03, "left", px, 1187), it("w2", "Like, you and I", I, 400, 72.9, -0.036, "left", 144, 1198)]))
        if a["pt"]["ink"][2] + 33 > 1022: a["pt"] = fit(it("pt", "THINK ABOUT IT", I, 600, 46.8, -0.03, "left", px, 1187), 1022 - 33 - px)
        p = a["pt"]["ink"]; sw = t.v(17) - 1
        h = (f'<div id="ic" class="abs layer">{icon("ici", 62, 1133, 74, "#9F4722", "bang", "#FDF8EE")}</div>'
             + f'<div id="pg1" class="abs layer">{span("w1", a["w"], I, 400, "#FCFAF8", parts("w1", ["Because", "if", "you"]))}'
             + f'<div id="pill" class="abs layer">{rect("pr", p[0]-36, 1130, p[2]+33, 1204, "#9F4825", 37)}{span("ptx", a["pt"], I, 600, "#FEF7EC", "THINK ABOUT IT")}</div></div>'
             + f'<div id="pg2" class="abs layer">{span("w2", a["w2"], I, 400, "#FCFAF8", parts("w2", ["Like,", "you", "and", "I"]))}</div>')
        t.gfx(h); t.grp("#pg1", 0, sw); t.grp("#pg2", sw + 1, t.N - 1)
        t.JS.append('FN("#ic","x",0,15,f=>f<2?-44.1:-44.1*(1-backOut((f-2)/12.3,1.5))); OP("#ic",0,6,0.79,1);')
        for i, wi in enumerate([11, 12, 13]): t.fade(f"#w1-{i}", max(1, t.v(wi, 0)), 0.5 if i == 0 else 0.3, 40)
        pv = t.v(14, 0); t.JS.append(f'ON("#pill",{pv}); FN("#pill","y",{pv},{sw+1},f=>16.9*Math.exp(-0.115*(f-{pv+0.5}))*Math.cos(0.409*(f-{pv+0.5})+0.68));')
        for i, wi in enumerate([17, 18, 19, 20]): t.fade(f"#w2-{i}", max(sw + 1, t.v(wi, 0)), 0.45, 40)
        t.sfx.append(("whoosh", 0))
    tdef(3, 3.86, 5.92, "broll", t3)

    # 4 b-roll 3 lines + pill (S03)
    def t4(t):
        N = t.N; t.H += t.broll([("S03a", 0, 19, "still", 30), ("S03b", 20, 44, "still", 25), ("S03c", 45, N - 1, "video", 50)]); t.gradient("orange")
        a = lay([it("l1", "YOU AND I HAVE BEEN", I, 400, 66.5, -0.05, "left", 78, 1207), it("l2", "DOING", I, 600, 98.9, -0.06, "left", 100, 1290), it("l3", "4 OR 5 YEARS", I, 600, 98.9, -0.066, "left", 114, 1380)])
        a.update(lay([it("pt", "THIS FOR", I, 500, 80.6, -0.023, "left", a["l2"]["ink"][2] + 22 + 36, 1282)])); p = a["pt"]["ink"]
        t.gfx(span("l1", a["l1"], I, 400, "#FCF9FB", parts("a", ["YOU", "AND", "I", "HAVE", "BEEN"])) + span("l2", a["l2"], I, 600, "#FCFBFA", parts("b", ["DOING"]))
              + f'<div id="pill" class="abs layer">{rect("pr", p[0]-36, 1207, p[2]+39, 1295, "#9E4723", 44)}{span("ptx", a["pt"], I, 500, "#FCFAF4", "THIS FOR")}</div>'
              + span("l3", a["l3"], I, 600, "#F4EEEB", parts("c", ["4", "OR", "5", "YEARS"])))
        for i, wi in enumerate([18, 19, 20, 21, 22]): t.canon(f"#a-{i}", t.v(wi, 4))
        t.canon("#b-0", t.v(23)); pv = t.v(24); t.JS.append(f'ON("#pill",{pv}); FN("#pill","x",{pv},{pv+12},f=>f<{pv+1.9}?54.6:54.6*(1-backOut((f-{pv+1.9})/9.3,2.5)));')
        for i, wi in enumerate([26, 27, 28, 29]): t.canon(f"#c-{i}", t.v(wi))
        t.sfx.append(("whoosh", 0))
    tdef(4, 5.43, 8.06, "broll", t4)

    # 5 b-roll pill + big lines (S14), two pages
    def t5(t):
        N = t.N; sw = t.v(57, 2)
        t.H += t.broll([("S05c", 0, sw - 1, "still", 50), ("S07a", sw, N - 1, "still", 65)]); t.gradient("orange")
        a = lay([it("p1", "WITH OTHER", I, 600, 61.13, -0.042, "left", 79, 1199), it("l1", "CREATORS", I, 500, 113.36, -0.04, "left", 73, 1303),
                 it("p2", "AND ALSO", I, 600, 61.13, -0.042, "left", 79, 1199), it("m1", "WHEN YOU HAVE", I, 500, 113.36, -0.04, "left", 73, 1303), it("m2", "QUESTIONS", I, 500, 114.9, -0.03, "left", 78, 1402)])
        h = ""
        for pg, (pk, lines) in enumerate([("p1", [("l1", ["CREATORS"])]), ("p2", [("m1", ["WHEN", "YOU", "HAVE"]), ("m2", ["QUESTIONS"])])]):
            pr = a[pk]["ink"]; h += (f'<div id="g{pg}" class="abs layer"><div id="pill{pg}" class="abs layer">{rect(f"pr{pg}", 69, 1136, pr[2]+18, 1211, "#9F4924", 37.5)}{span(f"pt{pg}", a[pk], I, 600, "#FAF6EF", " ".join(["WITH OTHER", "AND ALSO"][pg].split()))}</div>'
                                     + "".join(span(f"{lk}", a[lk], I, 500, "#F8EFE9" if lk == "m2" else "#FBF8F5", parts(lk, ws)) for lk, ws in lines) + "</div>")
        t.gfx(h); t.grp("#g0", 0, sw - 1); t.grp("#g1", sw, N - 1)
        for pg, f0 in enumerate([0, sw]):
            t.JS.append(f'ON("#pill{pg}",{f0}); TAB("#pill{pg}","x",{{"{f0}":-38,"{f0+2}":-38,"{f0+3}":-10.9,"{f0+5}":5.0,"{f0+7}":5.7,"{f0+9}":2.8,"{f0+11}":0.4,"{f0+13}":-0.6,"{f0+17}":-0.6,"{f0+18}":-0.2,"{f0+20}":0}});')
        t.canon("#l1-0", t.v(56, 2))
        for i, wi in enumerate([59, 60, 61]): t.canon(f"#m1-{i}", t.v(wi, 2))
        t.canon("#m2-0", t.v(62, 2)); t.sfx.append(("whoosh", 0)); t.sfx.append(("dclick", sw))
    tdef(5, 15.48, 18.20, "broll", t5)

    # 6 b-roll stack (S09)
    def t6(t):
        N = t.N; t.H += t.broll([("S09a", 0, 21, "still", 50), ("S09b", 22, 45, "video", 50), ("S09c", 46, N - 1, "video", 50)]); t.gradient("brown")
        a = lay([it("l1", "WHERE DO YOU GO TO", I, 400, 70.4, -0.07, "left", 83, 1138)])
        a["l2"] = fit(it("l2", "COLLABORATE WITH", I, 700, 102.8, -0.068, "left", 87, 1226), 935); a["l3"] = fit(it("l3", "OTHER CREATORS", I, 700, 102.8, -0.068, "left", 85, 1313), 937)
        t.gfx(span("l1", a["l1"], I, 400, "#F8F6F2", parts("a", ["WHERE", "DO", "YOU", "GO", "TO"])) + span("l2", a["l2"], I, 700, "#FBF8F5", parts("b", ["COLLABORATE", "WITH"]))
              + span("l3", a["l3"], I, 700, "#FAF5F0", parts("c", ["OTHER", "CREATORS"])))
        for pfx, wis in [("a", [48, 49, 50, 51, 52]), ("b", [53, 54]), ("c", [55, 56])]:
            for i, wi in enumerate(wis): t.canon(f"#{pfx}-{i}", t.v(wi, 5))
        t.sfx.append(("whoosh", 0))
    tdef(6, 13.93, 16.37, "broll", t6)

    # 7/8 split + chips (S05)
    def chips_split(t, words_line, wis_line, chip1, chip1_wi, chip2_words, chip2_wis, tops):
        a = lay([it("l", " ".join(words_line), I, 700, 85.88, -0.0675, "left", 161, 771)])
        a["c1"] = fit(it("c1", chip1, I, 700, 58.53, -0.056, "left", 236, 853), 300); c1r = a["c1"]["ink"][2] + 49
        a["c2"] = fit(it("c2", " ".join(chip2_words), I, 700, 58.53, -0.056, "left", c1r + 15 + 106, 853), 1000 - (c1r + 15 + 106) - 49); c2r = a["c2"]["ink"][2] + 49
        sh = "0 3px 12px rgba(0,0,0,.45)"
        cap = (f'<div id="ic" class="abs layer" style="transform-origin:99px 744px">{icon("ici", 51, 696, 96, "#A24A24", "bang", "#F0DCC4")}</div>'
               + span("l", a["l"], I, 700, "#FFFFFF", parts("w", words_line), shadow=sh)
               + f'<div id="ch1" class="abs layer" style="transform-origin:{(130+c1r)/2}px 836px">{rect("c1r", 130, 791, c1r, 881, "#FFFFFF", 45)}{icon("c1i", 138, 797, 76, "#A44A21", "plus", "#F0D9B8")}{span("c1t", a["c1"], I, 700, "#A04B28", chip1)}</div>'
               + f'<div id="ch2" class="abs layer" style="transform-origin:{(c1r+15+c2r)/2}px 836px">{rect("c2r", c1r+15, 791, c2r, 881, "#FFFFFF", 45)}{icon("c2i", c1r+23, 797, 76, "#A44A21", "plus", "#F0D9B8")}{span("c2t", a["c2"], I, 700, "#A04B28", parts("c2w", chip2_words))}</div>')
        t.split(tops, cap)
        t.JS.append('FN("#ic","x",0,16,f=>-43.3*(1-backOut(f/12,2.2))); FN("#ic","scale",0,3,f=>0.8+0.2*Math.min(1,f/3));')
        for i, wi in enumerate(wis_line): t.fade(f"#w-{i}", max(1, t.v(wi, 0)), 0.2, 11)
        def wob(s): return {s+1: 0, s+2: 11.8, s+3: 0.2, s+4: 0.2, s+5: 0.1, s+6: 3.9, s+7: -0.1, s+8: -1.8, s+9: -3.1, s+10: -2.5, s+11: -1.5, s+12: -0.7, s+13: -0.1, s+14: 0.2, s+18: 0}
        for cid, f0 in [("ch1", t.v(chip1_wi, 4)), ("ch2", t.v(chip2_wis[0], 4))]:
            t.JS.append(f'ON("#{cid}",{f0}); FN("#{cid}","scale",{f0},{f0+1},f=>f<{f0+1}?0.76:1); TAB("#{cid}","y",{json.dumps({str(k): v for k, v in wob(f0).items()})});')
        t.fade("#c1t", t.v(chip1_wi, 4), 0.44, 7)
        for i, wi in enumerate(chip2_wis): t.fade(f"#c2w-{i}", t.v(wi, 2), 0.44, 7)
        t.sfx.append(("whoosh", 0))
    def t7(t):
        N = t.N; chips_split(t, ["No", "spaces", "for", "us", "to"], [35, 36, 37, 38, 39], "Connect", 40, ["With", "anyone"], [41, 42],
                             [("S05a", 0, 24, "still", 35), ("S05b", 25, 50, "still", 40), ("S05c", 51, N - 1, "still", 50)])
    tdef(7, 9.17, 11.74, "split", t7)
    def t8(t):
        N = t.N; chips_split(t, ["Where", "do", "you", "go", "to"], [48, 49, 50, 51, 52], "Collaborate", 53, ["With", "other", "creators"], [54, 55, 56],
                             [("S09c", 0, 24, "still", 50), ("S14", 25, 48, "still", 40), ("S05b", 49, N - 1, "still", 40)])
    tdef(8, 13.93, 16.37, "split", t8)

    # 9 split static caption (S04)
    def t9(t):
        a = lay([it("l1", "AND SO FAR THERE’S", I, 400, 76.8, -0.063, "left", 78, 731)])
        a["l2"] = fit(it("l2", "BEEN NO SPACES", I, 600, 101.7, -0.068, "left", 83, 812), 935); a["l3"] = fit(it("l3", "FOR US", I, 600, 101.7, -0.066, "left", 86, 896), 935)
        cap = (span("l1", a["l1"], I, 400, "#FCF8F3", parts("a", ["AND", "SO", "FAR", "THERE’S"])) + span("l2", a["l2"], I, 600, "#FCF9F5", parts("b", ["BEEN", "NO", "SPACES"]))
               + span("l3", a["l3"], I, 600, "#FBF3ED", parts("c", ["FOR", "US"])))
        t.split([("S04t", 0, t.N - 1, "still", 45)], cap)
        for pfx, wis in [("a", [30, 31, 32, 33]), ("b", [34, 35, 36]), ("c", [37, 38])]:
            for i, wi in enumerate(wis): t.canon(f"#{pfx}-{i}", t.v(wi))
    tdef(9, 8.01, 10.37, "split", t9)

    # 10 rust bar (S06 p1) speaker B + tag
    def t10(t):
        t.face(); t.gradient("black"); t.tag(1255, 0); p2 = t.v(46)
        t.gfx(bar_page(t, "p1", "It’s really", [43, 44], "FRUSTRATING", [45], "S06", 0, p2 - 1, "#A14A24")
              + f'<div id="p2" class="abs layer">{span("p2s", lay([it("x", "because like", I, 600, 69.0, -0.054, "center", 540, 1094)])["x"], I, 600, "#FBF8F4", parts("p2w", ["because", "like"]))}</div>')
        t.grp("#p2", p2, t.N - 1); t.canon("#p2w-0", p2); t.canon("#p2w-1", t.v(47))
    tdef(10, 11.80, 13.95, "face", t10)

    # 11 rust bar (S01 page 2) speaker A
    def t11(t):
        t.face(); t.gradient("black"); t.gfx(bar_page(t, "p", "Aussie creators is finding", [6, 7, 8, 9], "COMMUNITY", [10], "S01", 0, t.N - 1))
    tdef(11, 1.20, 3.80, "face", t11)

    # 12 terracotta bar (S12 page 2) speaker A
    def t12(t):
        t.face(); t.gradient("black"); t.gfx(bar_page(t, "p", "and so far there’s been", [30, 31, 32, 33, 34], "NO SPACES FOR US", [35, 36, 37, 38], "S12", 0, t.N - 1, "#C77136"))
    tdef(12, 8.01, 10.37, "face", t12)

    # 13 rust bar ending (S17 page 2) speaker B
    def t13(t):
        t.face(); t.gradient("black"); t.gfx(bar_page(t, "p", "when you have questions, like,", [59, 60, 61, 62, 63], "WHO DO YOU ASK?", [64, 65, 66, 67], "S17", 0, t.N - 1))
    tdef(13, 17.02, 19.08, "face", t13)

    # 14 list with chips (S07)
    def t14(t):
        N = t.N; q = N // 4
        t.H += t.broll([("S09b", 0, q - 1, "still", 50), ("S05b", q, 2 * q - 1, "still", 40), ("S14", 2 * q, 3 * q - 1, "still", 40), ("S07b", 3 * q, N - 1, "still", 50)]); t.gradient("green")
        hd = lay([it("h", "Where do you go to", I, 400, 61.25, -0.044, "left", 172, 1114)])["h"]
        chips = [("Collaborate", 53, (70, 1145)), ("With other creators", 54, None), ("Questions", 62, (70, 1231))]
        h = f'<div id="ic" class="abs layer" style="transform-origin:108.5px 1095px">{icon("ici", 63, 1049, 92, "#C16E33", "sparkle")}</div>' + span("h", hd, I, 400, "#FFFFFF", '<span id="h-0" class="pt" style="font-weight:600">Where</span> ' + parts("h1", ["do", "you", "go", "to"]))
        x = 70
        for k, (txt, wi, pos) in enumerate(chips):
            if pos: x, y = pos
            else: y = 1145
            L = lay([it(f"c{k}", txt, I, 500, 47.5, -0.025, "left", x + 80, y + 51)])[f"c{k}"]; r = L["ink"][2] + 24
            if r > 1010: x, y = 70, 1231; L = lay([it(f"c{k}", txt, I, 500, 47.5, -0.025, "left", x + 80, y + 51)])[f"c{k}"]; r = L["ink"][2] + 24
            h += f'<div id="ch{k}" class="abs layer">{rect(f"cr{k}", x, y, r, y+75, "#FCFCFB", 37.5)}{icon(f"ci{k}", x+4, y+5.5, 64, "#C46E32", "plus")}{span(f"ct{k}", L, I, 500, "#B87040", txt)}</div>'
            f0 = t.v(wi, 2); t.JS.append(f'ON("#ch{k}",{f0},0.72); FN("#ch{k}","x",{f0},{f0+12},f=>-31.7*(1-backOut((f-{f0})/9,1.7))); OP("#ch{k}",{f0},{f0+17},0.72,1);')
            x = r + 18
        t.gfx(h)
        t.JS.append('FN("#ic","x",0,14,f=>-33*(1-backOut(f/12,1.5))); FN("#ic","scale",0,14,f=>0.675+0.325*backOut(f/12,1.5)); OP("#ic",0,8,0.83,1);')
        t.emph("#h-0", 0)
        for i, wi in enumerate([49, 50, 51, 52]): t.emph(f"#h1-{i}", t.v(wi, 2))
        t.sfx.append(("whoosh", 0))
    tdef(14, 13.93, 18.20, "broll", t14)

    # 15 list with chips (S16: star header static, chips pop up)
    def t15(t):
        N = t.N; t.H += t.broll([("S02a", 0, 33, "video", 50), ("S05c", 34, 70, "still", 50), ("S05b", 71, N - 1, "still", 40)]); t.gradient("orange")
        hd = lay([it("h", "The biggest challenge", I, 450, 59.83, -0.053, "left", 155, 1033)])["h"]
        h = icon("star", 65, 971, 83, "#A04823", "star", "#FAF8F3") + span("h", hd, I, 450, "#F9F8F2", "The biggest challenge")
        x, y = 101, 1057
        for k, (txt, wi) in enumerate([("Aussie creators", 6), ("Finding community", 9)]):
            L = lay([it(f"c{k}", txt, I, 600, 59.12, -0.06, "left", x + 40, y + 64)])[f"c{k}"]; r = L["ink"][2] + 40
            if r > 1010: x, y = 96, 1154; L = lay([it(f"c{k}", txt, I, 600, 59.12, -0.06, "left", x + 40, y + 64)])[f"c{k}"]; r = L["ink"][2] + 40
            h += f'<div id="ch{k}" class="abs layer">{rect(f"cr{k}", x, y, r, y+85, "#FCFCF9", 42.5)}{span(f"ct{k}", L, I, 600, "#984B2E", txt)}</div>'
            f0 = t.v(wi, 2); t.JS.append(f'ON("#ch{k}",{f0},0.72); FN("#ch{k}","y",{f0},{f0+30},f=>f<{f0+1.9}?26.2:26.2*(1-backOut((f-{f0+1.9})/11,3))); OP("#ch{k}",{f0},{f0+4},0.72,0.96); OP("#ch{k}",{f0+4},{f0+8},0.96,1);')
            x = r + 13
        t.gfx(h); t.sfx.append(("whoosh", 0))
    tdef(15, 0.22, 3.80, "broll", t15)

    # 16 check + two lines (S15 page 3) speaker A
    def icon_lines(t, kind, l1, l1w, l2, l2w, fill="#C57137"):
        a = lay([it("l1", " ".join(l1), I, 600, 59.92, -0.05, "left", 227, 1116)]); a["l2"] = fit(it("l2", " ".join(l2), I, 500, 78.09, -0.058, "left", 226, 1178), 1012 - 226)
        t.gfx(icon("ic", 105, 1075, 104, fill, kind) + span("l1", a["l1"], I, 600, "#FCF9F1", parts("a", l1)) + span("l2", a["l2"], I, 500, "#FCF7EF", parts("b", l2)))
        t.JS.append('POPICON("#ic",0);')
        for i, wi in enumerate(l1w): t.canon(f"#a-{i}", t.v(wi))
        for i, wi in enumerate(l2w): t.canon(f"#b-{i}", t.v(wi))
    def t16(t):
        t.face(); t.gradient("black"); icon_lines(t, "check", ["You", "and", "I", "have", "been"], [18, 19, 20, 21, 22], ["doing", "this", "for", "4", "or", "5", "years"], [23, 24, 25, 26, 27, 28, 29])
    tdef(16, 5.43, 8.06, "face", t16)

    # 17 X icon + lines (S17 page 1 icon, S15 page 3 stack)
    def t17(t):
        t.face(); t.gradient("black"); icon_lines(t, "x", ["There’s", "been", "no", "spaces"], [33, 34, 35, 36], ["for", "us", "to", "connect"], [37, 38, 39, 40], "#C37139")
    tdef(17, 8.62, 10.96, "face", t17)

    # 18 check + one emphasised line (S15 page 1)
    def t18(t):
        t.face(); t.gradient("black")
        L = fit(it("w", "For us to connect with anyone", I, 400, 81.8, -0.048, "left", 160, 1154), 1012 - 160)
        t.gfx(icon("ic", 50, 1075, 104, "#C57137", "check") + span("w", L, I, 400, "#FAF6F5", parts("w", ["For", "us", "to", "connect", "with", "anyone"])))
        t.JS.append('POPICON("#ic",0);')
        for i, wi in enumerate([37, 38, 39, 40, 41, 42]): t.JS.append(f'W("#w-{i}",{{D:42.9,t0:{t.v(wi)+0.6},dur:22.1,vis:{t.v(wi)},op0:0.56,opCirc:true,opDur:22.1}});')
    tdef(18, 9.78, 11.74, "face", t18)

    # 19 cream big word (S13)
    def t19(t):
        t.face(); t.gradient("black")
        s = fit(it("s", "FOR AUSSIE CREATORS IS FINDING", I, 450, 67.8, -0.06, "center", 540, 964), 940); b = fit(it("b", "COMMUNITY", I, 500, 154.75, -0.03, "center", 541, 1077), 940)
        t.gfx(span("s", s, I, 450, "#FBF6F1", parts("a", ["FOR", "AUSSIE", "CREATORS", "IS", "FINDING"])) + span("b", b, I, 500, "#DCC9B4", "COMMUNITY"))
        for i, wi in enumerate([5, 6, 7, 8, 9]): t.canon(f"#a-{i}", t.v(wi))
        v = t.v(10); t.JS.append(f'W("#b",{{D:21,t0:{v-3.4},dur:33.7,vis:{v},op0:0.85}});')
    tdef(19, 1.10, 3.80, "face", t19)

    # 20 glass "!" tiles + cream word (S06 page 2) speaker B
    def t20(t):
        t.face(); t.gradient("black")
        a = lay([it("w1", "It’s", I, 600, 68.93, -0.045, "left", 420, 1057), it("w2", "really", I, 600, 69.01, -0.06, "left", 571, 1057)])
        b = fit(it("b", "frustrating", I, 500, 148.6, -0.04, "center", 541, 1140), 940)
        tile = lambda id, cx, cy, rot: (f'<div id="{id}" class="abs tile" style="left:{cx-62.5}px;top:{cy-62.5}px;width:125px;height:125px;transform:rotate({rot}deg)">'
                                        '<svg width="125" height="125" style="position:absolute;left:0;top:0"><rect x="55" y="28" width="15" height="50" rx="7.5" fill="#DD3C37"/><rect x="55" y="86" width="15" height="13" rx="6.5" fill="#DD3C37"/></svg></div>')
        bi = b["ink"]
        t.gfx(tile("tL", bi[0] + 32, 1025, -12) + span("w1", a["w1"], I, 600, "#FBF5EE", "It’s") + rect("dot", (a["w1"]["ink"][2]+a["w2"]["ink"][0])/2-8, 1028, (a["w1"]["ink"][2]+a["w2"]["ink"][0])/2+8, 1043, "#E8DCC8", 8)
              + span("w2", a["w2"], I, 600, "#F9F7F9", "really") + span("b", b, I, 500, "#E1D1BB", "frustrating") + tile("tR", bi[2] - 30, 1068, 12))
        v0, v1, v2 = 0, t.v(44), t.v(45)
        t.JS.append(f'TILE("#tL",{v0},-12); TILE("#tR",{v2},12); ON("#dot",{v2});')
        t.JS.append(f'W("#w1",{{D:35,t0:{v0-6.7},dur:34.4,vis:{v0},op0:0.9}}); W("#w2",{{D:35,t0:{v1-6.7},dur:34.4,vis:{v1},op0:0.9}}); W("#b",{{D:29,t0:{v2-4.6},dur:33.7,vis:{v2},op0:0.9}});')
        t.sfx.append(("impact", v2))
    tdef(20, 11.80, 13.95, "face", t20)
    return S

# ---------------------------------------------------------------- media writers
seg_model = None
def raw_frame(t): k = min(572, int(round(t * 30000 / 1001))); return cv2.imread(f"{RAW}/f{k+1:04d}.jpg")
def encode(path, frames):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "medium",
                          "-crf", "14", "-pix_fmt", "yuv420p", "-movflags", "+faststart", path], stdin=subprocess.PIPE)
    for fr in frames: p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
def matte(img):
    global seg_model
    import mediapipe as mp
    from mediapipe.tasks import python as mpp
    from mediapipe.tasks.python import vision
    if seg_model is None: seg_model = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(base_options=mpp.BaseOptions(model_asset_path=MODEL), output_confidence_masks=True))
    r = seg_model.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
    b = ((1 - r.confidence_masks[0].numpy_view()) > 0.5).astype(np.uint8)
    b = cv2.morphologyEx(b, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61)))
    h, w = b.shape; ff = b * 255; m = np.zeros((h + 2, w + 2), np.uint8); cv2.floodFill(ff, m, (0, 0), 128); cv2.floodFill(ff, m, (w - 1, 0), 128)
    return np.clip(cv2.GaussianBlur((ff != 128).astype(np.float32), (0, 0), 40) * 1.6, 0, 1)[..., None]
def write_media(t):
    seg = t.seg; n = t.n
    for m in t.media:
        if m[0] == "face":
            hook = len(m) > 3
            def frames():
                for f in range(t.N):
                    img = raw_frame(seg.src(f / 30))
                    if hook:
                        u = min(f / 31, 1); s = 1 + 0.15 * (1 - math.sqrt(1 - (u - 1) ** 2))
                        img = cv2.warpAffine(img, np.float64([[s, 0, 540 - 540 * s], [0, s, 960 - 960 * s]]), (1080, 1920), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
                        if f in (1, 3, 5): a = matte(img); img = (img * (1 - a) + 255 * a).astype(np.uint8)
                    yield img
            encode(os.path.join(ROOT, f"assets/t{n:02d}_face.mp4"), frames())
        elif m[0] == "split":
            s_ = 930 / 955; M = np.float64([[s_, 0, 14 + (1052 - 1080 * s_) / 2], [0, s_, 974 - 120 * s_]])
            encode(os.path.join(ROOT, f"assets/t{n:02d}_split.mp4"), (cv2.warpAffine(raw_frame(seg.src(f / 30)), M, (1080, 1920), flags=cv2.INTER_LANCZOS4) for f in range(t.N)))
        elif m[0] == "broll":
            _, clip, f0, f1, kind, src = m; inp = os.path.join(ROOT, f"assets/broll/{clip}.mp4")
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", inp], capture_output=True, text=True).stdout)
            tin = round(dur * 0.35, 2)
            if kind == "still": subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(tin), "-i", inp, "-frames:v", "1", "-q:v", "1", os.path.join(ROOT, src)], check=True)
            else: subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(tin), "-i", inp, "-t", f"{(f1-f0+1)/30+0.6:.3f}", "-an", "-vf", "fps=30", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", os.path.join(ROOT, src)], check=True)
    # voice: source segment with the pauses inside it removed, 10 ms fades, level matched to the reference (as in the reel)
    pieces = []; a = seg.t0
    for c0, c1 in seg.cuts + [(seg.t1, None)]:
        pieces.append((a, c0)); a = c1
    fl = ";".join(f"[0:a]atrim={p0}:{p1},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={p1-p0-0.012:.3f}:d=0.012[a{i}]" for i, (p0, p1) in enumerate(pieces))
    fl += ";" + "".join(f"[a{i}]" for i in range(len(pieces))) + f"concat=n={len(pieces)}:v=0:a=1,volume=3.0dB,alimiter=limit=0.84[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(ROOT, "assets/client_raw.mp4"), "-filter_complex", fl, "-map", "[o]", "-ar", "48000", "-ac", "2", os.path.join(ROOT, f"assets/t{n:02d}_voice.wav")], check=True)

SFXF = {"whoosh": ("assets/sfx-whoosh.wav", 0.165, 0.57), "dclick": ("assets/sfx-dclick.wav", 0.006, 0.15), "impact": ("assets/sfx-impact.wav", 0.514, 1.4), "glitch": ("assets/sfx-glitch.wav", 0, 0.32)}
def write_html(t):
    aud = [f'<audio id="voice" data-start="0" data-duration="{F(t.N)}" data-track-index="20" src="assets/t{t.n:02d}_voice.wav" data-volume="1"></audio>',
           f'<audio id="bed" data-start="0" data-duration="{F(t.N)}" data-track-index="21" src="assets/bed.mp3" data-volume="0.124"></audio>']
    sfx = list(t.sfx) + [("dclick", f) for f in t.cuts]
    if t.kind == "hook": sfx.append(("glitch", 1))
    for i, (k, f) in enumerate(sfx):
        src, pk, d = SFXF[k]; aud.append(f'<audio id="sfx{i}" data-start="{max(0, round(f/30-pk, 3))}" data-duration="{d}" data-track-index="{22+i%6}" src="{src}" data-volume="{0.1 if k=="glitch" else 1}"></audio>')
    tpl = open(os.path.join(HERE, "template.html")).read().replace('data-duration="51.0333"', f'data-duration="{F(t.N)}"')
    open(os.path.join(ROOT, "index.html"), "w").write(tpl.replace("%%BODY%%", "\n".join(t.H)).replace("%%AUDIO%%", "\n".join(aud)).replace("%%JS%%", "\n    ".join(t.JS)))
    hold = {}
    for a, b in t.broll_runs:
        pat = [2, 2, 2, 2, 2, 2, 2, 3]; u = a; i = 0; nxt = a + 2; cuts = set(t.cuts) | {a}
        for f in range(a, b + 1):
            if f in cuts: u, i, nxt = f, 0, f + 2
            elif f >= nxt: u = f; i += 1; nxt = f + pat[i % 8]
            hold[f] = u
    json.dump(hold, open(os.path.join(HERE, "holdmap.json"), "w"))
    return bool(hold)

S = build(0); meta = {}
for n in sorted(S):
    if ONLY and n not in ONLY: continue
    t0, t1, kind, fn = S[n]; t = T(n, t0, t1, kind); fn(t)
    if n != 1: write_media(t)
    else: subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(ROOT, "assets/client_raw.mp4"), "-t", "3.80", "-vn", "-af", "volume=3.0dB,alimiter=limit=0.84,afade=t=out:st=3.78:d=0.02", "-ar", "48000", "-ac", "2", os.path.join(ROOT, "assets/t01_voice.wav")], check=True)
    post = write_html(t)
    out = os.path.join(ROOT, f"renders/t{n:02d}.mp4"); raw = out.replace(".mp4", "_raw.mp4")
    r = subprocess.run(["npx", "hyperframes", "render", "--quality", "high", "--output", raw], cwd=ROOT, capture_output=True, text=True)
    if not os.path.exists(raw): print(n, "RENDER FAILED", r.stdout[-800:], r.stderr[-800:]); continue
    if post: subprocess.run(["python3", "-I", os.path.join(HERE, "postpass.py"), raw, out], check=True, capture_output=True)
    else: os.replace(raw, out)
    meta[n] = dict(kind=kind, src=[t0, t1], frames=t.N, seconds=round(t.N / 30, 2), speaker=t.speaker)
    print(f"T{n:02d} {kind:6s} {t.N/30:.2f}s ok", flush=True)
    mp = os.path.join(HERE, "templates_meta.json"); old = json.load(open(mp)) if os.path.exists(mp) else {}; old.update({str(k): v for k, v in meta.items()}); json.dump(old, open(mp, "w"), indent=1)
