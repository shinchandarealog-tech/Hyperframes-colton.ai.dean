"""Generate index.html for the full replica from spec_data + graphics + calibration.
usage: python3 build.py items   -> writes scripts/items.json (texts to calibrate)
       python3 build.py html    -> writes index.html (needs scripts/calib.json)"""
import json, os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from spec_data import *
from graphics import GROUPS

def walk(children):
    for c in children:
        yield c
        if c["k"] == "unit": yield from walk(c["children"])

def all_texts():
    for g in GROUPS:
        for c in walk(g["children"]):
            if c["k"] == "text": yield c

if sys.argv[1] == "items":
    items = []
    for t in all_texts():
        it = dict(id=t["id"], text=t["text"], fam=t["fam"], wt=t["wt"], ls=t["ls"])
        if t["ink"]: it["ink"] = t["ink"]; it["size0"] = max(20, (t["ink"][3] - t["ink"][1]) * 1.3)
        else: it["fix"] = t["fix"]
        items.append(it)
    json.dump(items, open(os.path.join(HERE, "items.json"), "w"), indent=0); print(len(items), "items"); sys.exit()

CAL = json.load(open(os.path.join(HERE, "calib.json")))
CORR = json.load(open(os.path.join(HERE, "corrections.json"))) if os.path.exists(os.path.join(HERE, "corrections.json")) else {}
F = lambda f: round(f / 30, 6)
H = []; JS = []

PANELS = {"top4": SPLIT_A["top"], "bot4": SPLIT_A["bot"], "top10": SPLIT_B["top"], "bot10": SPLIT_B["bot"]}

def css_grad(name):
    rgb, stops = GRADS[name]
    return "linear-gradient(to bottom, " + ", ".join(f"rgba({rgb},{a}) {y}px" for y, a in stops) + ")"

# ---------- glyph svgs ----------
BADGE = open(os.path.join(HERE, "badge_path.txt")).read().strip()
def glyph_svg(kind, d, col):
    s = d
    if kind == "bang":
        w = 0.115 * s; h = 0.42 * s; dt = 0.115 * s; gap = 0.07 * s; top = (s - (h + gap + dt)) / 2; x = (s - w) / 2
        return f'<svg width="{s}" height="{s}" style="position:absolute;left:0;top:0"><rect x="{x}" y="{top}" width="{w}" height="{h}" rx="{w/2}" fill="{col}"/><rect x="{x}" y="{top+h+gap}" width="{w}" height="{dt}" rx="{w/2}" fill="{col}"/></svg>'
    if kind == "plus":
        a = 0.25 * s; sw = 0.11 * s; c = s / 2
        return f'<svg width="{s}" height="{s}" style="position:absolute;left:0;top:0"><path d="M{c-a} {c} H{c+a} M{c} {c-a} V{c+a}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/></svg>'
    if kind == "check":
        sw = 9 * s / 104
        return f'<svg width="{s}" height="{s}" viewBox="0 0 104 104" style="position:absolute;left:0;top:0"><path class="draw" pathLength="1" d="M32 54 L46 67 L73 38" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray:1;stroke-dashoffset:0"/></svg>'
    if kind == "x":
        return f'<svg width="{s}" height="{s}" viewBox="0 0 106 106" style="position:absolute;left:0;top:0"><path class="draw" pathLength="1" d="M53 53 L33 31 M53 53 L74 77 M53 53 L74 31 M53 53 L33 77" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round" style="stroke-dasharray:0.25 0.75;stroke-dashoffset:0"/></svg>'
    if kind == "sparkle":
        c = s / 2; R = 0.275 * s; r = 0.06 * s
        pts = []
        for i in range(8):
            ang = math.pi / 4 * i - math.pi / 2; rr = R if i % 2 == 0 else r
            pts.append(f"{c+rr*math.cos(ang):.2f},{c+rr*math.sin(ang):.2f}")
        return f'<svg width="{s}" height="{s}" style="position:absolute;left:0;top:0"><polygon points="{" ".join(pts)}" fill="{col}" stroke="{col}" stroke-width="{0.03*s:.2f}" stroke-linejoin="round"/></svg>'
    if kind == "star":
        c = s / 2; R = 0.27 * s; r = 0.12 * s; pts = []
        for i in range(10):
            ang = math.pi / 5 * i - math.pi / 2; rr = R if i % 2 == 0 else r
            pts.append(f"{c+rr*math.cos(ang):.2f},{c+rr*math.sin(ang)+0.02*s:.2f}")
        return f'<svg width="{s}" height="{s}" style="position:absolute;left:0;top:0"><polygon points="{" ".join(pts)}" fill="{col}" stroke="{col}" stroke-width="{0.05*s:.2f}" stroke-linejoin="round"/></svg>'
    raise ValueError(kind)

POP_ICONS = {"s15-c1": 1200, "s15-c2": 1253, "s17-x": 1440.5}

def emit_anim_text(t):
    a = t["anim"]; sel = "#" + t["id"]
    if a is None: return
    k = a[0]
    if k == "canon": JS.append(f'W("{sel}",{{D:29,t0:{a[1]-4.6},dur:33.7,vis:{a[1]}}});')
    elif k == "slide": JS.append(f'W("{sel}",{{D:{a[1]},t0:{a[2]},dur:{a[3]},vis:{a[4]}' + (f',op0:{a[5]}' if len(a) > 5 else '') + '});')
    elif k == "emph": JS.append(f'W("{sel}",{{D:{a[1]},t0:{a[2]},dur:{a[3]},vis:{a[4]},op0:{a[5]},opCirc:true,opDur:{a[6] if len(a)>6 else a[3]}}});')
    elif k == "fade": JS.append(f'FADE("{sel}",{a[1]},{a[2] if len(a)>2 else 0.45},{a[3] if len(a)>3 else 10});')
    elif k == "on": JS.append(f'ON("{sel}",{a[1]});')

def emit_unit_anims(u):
    sel = "#" + u["id"]
    for a in u["anim"]:
        k = a[0]
        if k == "on": JS.append(f'ON("{sel}",{a[1]},{a[2] if len(a)>2 else 1});')
        elif k == "fn": JS.append(f'FN("{sel}","{a[1]}",{a[2]},{a[3]},f=>{a[4]});')
        elif k == "op": JS.append(f'OP("{sel}",{a[1]},{a[2]},{a[3]},{a[4]});')
        elif k == "tab": JS.append(f'TAB("{sel}","{a[1]}",{json.dumps({str(k2): v for k2, v in a[2].items()})});')

def text_html(t):
    c = CAL[t["id"]]; dx, dy = CORR.get(t["id"], (0, 0))
    fam = "bebas" if t["fam"] == "Bebas Neue" else "inter"
    sh = f";text-shadow:{t['shadow']}" if t["shadow"] else ""
    inner = t["text"]
    if t.get("parts"):
        inner = " ".join(f'<span id="{pid}" class="pt">{w}</span>' for pid, w, _ in t["parts"])
        for pid, w, an in t["parts"]: emit_anim_text(dict(id=pid, anim=an))
    return (f'<span id="{t["id"]}" class="txt {fam}" style="left:{c["left"]+dx:.2f}px;top:{c["top"]+dy:.2f}px;font-size:{c["size"]}px;'
            f'font-weight:{t["wt"]};letter-spacing:{c["lsEm"]}em;color:{t["color"]}{sh}">{inner}</span>')

def child_html(c):
    k = c["k"]
    if k == "text": emit_anim_text(c); return text_html(c)
    if k == "rect":
        x0, y0, x1, y1 = c["r"]; dx, dy = CORR.get(c["id"], (0, 0))
        return f'<div id="{c["id"]}" class="abs" style="left:{x0+dx}px;top:{y0+dy}px;width:{x1-x0}px;height:{y1-y0}px;border-radius:{c["radius"]}px;background:{c["fill"]};{c["extra"]}"></div>'
    if k == "badge":
        x0, y0, x1, y1 = c["r"]
        return (f'<svg id="{c["id"]}" class="abs" style="left:{x0}px;top:{y0}px;width:{x1-x0}px;height:{y1-y0}px" viewBox="-1 -1 36 34" preserveAspectRatio="none">'
                f'<path fill="#10B3E2" d="{BADGE}"/><path d="M10.5 16.4 L15 20.6 L23.5 11.8" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    if k == "icon":
        x0, y0, x1, y1 = c["r"]; d = (x1 - x0 + y1 - y0) / 2; dx, dy = CORR.get(c["id"], (0, 0))
        if c["id"] in POP_ICONS:
            f0 = POP_ICONS[c["id"]]; JS.append(f'POPICON("#{c["id"]}",{f0});')
        return (f'<div id="{c["id"]}" class="abs" style="left:{x0+dx}px;top:{y0+dy}px;width:{d}px;height:{d}px;border-radius:50%;background:{c["fill"]};transform-origin:50% 50%">'
                + glyph_svg(c["glyph"], d, c["gcol"]) + '</div>')
    if k == "bar":
        b = BARS[c["key"]]; x0, y0, x1, y1 = b["rect"]; tab = {f: (e - x0) / (x1 - x0) for f, e in b["table"].items()}
        JS.append(f'TAB("#{c["id"]}","scaleX",{json.dumps({str(k2): round(v, 4) for k2, v in tab.items()})});')
        return f'<div id="{c["id"]}" class="abs" style="left:{x0}px;top:{y0}px;width:{x1-x0}px;height:{y1-y0}px;background:{b["fill"]};transform-origin:0% 50%"></div>'
    if k == "tile":
        s = 125; x0 = c["cx"] - s / 2; y0 = c["cy"] - s / 2
        vis = 459 if c["id"].endswith("L") else 464
        JS.append(f'TILE("#{c["id"]}",{vis},{c["rot"]});')
        return (f'<div id="{c["id"]}" class="abs tile" style="left:{x0}px;top:{y0}px;width:{s}px;height:{s}px;transform:rotate({c["rot"]}deg)">'
                f'<svg width="125" height="125" style="position:absolute;left:0;top:0"><rect x="55" y="28" width="15" height="50" rx="7.5" fill="#DD3C37"/><rect x="55" y="86" width="15" height="13" rx="6.5" fill="#DD3C37"/></svg></div>')
    if k == "dot":
        x0, y0, x1, y1 = c["r"]; JS.append(f'ON("#{c["id"]}",{c["anim"][1]});')
        return f'<div id="{c["id"]}" class="abs" style="left:{x0}px;top:{y0}px;width:{x1-x0}px;height:{y1-y0}px;border-radius:50%;background:{c["fill"]}"></div>'
    if k == "unit":
        inner = "".join(child_html(cc) for cc in c["children"])
        emit_unit_anims(c)
        o = c["origin"]; org = f";transform-origin:{o[0]}px {o[1]}px" if o else ""
        return f'<div id="{c["id"]}" class="abs layer"{" style=%r" % org[1:] if org else ""}>{inner}</div>'.replace("'", '"')
    raise ValueError(k)

def group_html(g):
    JS.append(f'GRP("#{g["id"]}",{g["show"]},{g["hide"]});')
    return f'<div id="{g["id"]}" class="abs layer">' + "".join(child_html(c) for c in g["children"]) + "</div>"

# ---------- media ----------
def pan_js(sel, shot):
    sid, f0, f1, kind, area, pan, _ = shot
    if pan is None: return
    if pan[0] == "fn": JS.append(f'FN("{sel}","x",{f0},{f1+1},f=>{pan[1]});'); return
    if pan[0] == "zoom": JS.append(f'FN("{sel}","scale",{f0},{f1+1},f=>{pan[1]}+({pan[2]}-{pan[1]})*(f-{f0})/{f1-f0});'); return
    ease, a, b, t0, dur, frz = pan
    en = {"circ.out": "circ", "power4.out": "p4out", "sine.out": "sineOut", "expo.out": "expoOut"}[ease]
    if b is None:  # solve target so dx(last frame) = 0
        e = {"circ": lambda u: math.sqrt(1 - (min(max(u, 0), 1) - 1) ** 2), "sineOut": lambda u: math.sin(min(max(u, 0), 1) * math.pi / 2),
             "expoOut": lambda u: 1 if u >= 1 else 1 - 2 ** (-10 * max(u, 0)), "p4out": lambda u: 1 - (1 - min(max(u, 0), 1)) ** 4}[en]((f1 - t0) / dur)
        b = a * (1 - 1 / e)
    fz = f"Math.min(f,{frz})" if frz else "f"
    JS.append(f'FN("{sel}","x",{f0},{f1+1},f=>{{const g={fz};return {a}+({b}-{a})*{en}((g-{t0})/{dur});}});')

def pan_extent(shot):
    sid, f0, f1, kind, area, pan, _ = shot
    if pan is None or pan[0] in ("fn", "zoom"):
        if pan and pan[0] == "fn":
            vals = [eval(pan[1].replace("Math.exp", "math.exp"), {"math": math, "f": f}) for f in range(f0, f1 + 1)]
            return max(0, max(vals)) + 4, max(0, -min(vals)) + 4
        return 4, 4
    a, b = pan[1], pan[2] if pan[2] is not None else 0
    return max(a, b, 0) + 4, max(-a, -b, 0) + 40

def broll_html(shot, x0, y0, w, h, z):
    sid, f0, f1, kind, area, pan, desc = shot
    PICKS = json.load(open(os.path.join(HERE, "broll_picks.json"))); op = f"object-position:{PICKS[sid]['pos']}% 50%"
    L, R = pan_extent(shot); sel = f"#pan-{sid}"
    ext = "mp4" if kind == "video" else "jpg"
    src = f"assets/broll/{sid}.{ext}"
    box = f'left:{x0-L}px;top:{y0}px;width:{w+L+R}px;height:{h}px'
    pan_js(sel, shot)
    if kind == "still":
        return (f'<div id="clip-{sid}" class="clip abs" data-start="{F(f0)}" data-duration="{F(f1-f0+1)}" data-track-index="2" style="inset:0;z-index:{z}">'
                f'<div id="pan-{sid}" class="abs" style="{box}"><img src="{src}" style="width:100%;height:100%;object-fit:cover;{op};display:block"></div></div>')
    return (f'<div id="pan-{sid}" class="abs" style="{box};z-index:{z};transform-origin:50% 50%"><video id="v-{sid}" data-start="{F(f0)}" data-duration="{F(f1-f0+1)}" data-track-index="3" '
            f'src="{src}" muted playsinline style="width:100%;height:100%;object-fit:cover;{op};display:block"></video></div>')

def plate_html(name, f0, f1, z):
    return (f'<video id="pl-{name}" data-start="{F(f0)}" data-duration="{F(f1-f0+1)}" data-track-index="1" src="assets/plate_{name}.mp4" muted playsinline '
            f'style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:{z}"></video>')

def panel_open(pid, key, extra_style=""):
    x0, y0, x1, y1, r = PANELS[key]
    return (f'<div id="{pid}" class="abs" style="left:{x0}px;top:{y0}px;width:{x1-x0}px;height:{y1-y0}px;border-radius:{r}px;overflow:hidden;{extra_style}">'
            f'<div class="abs" style="left:{-x0}px;top:{-y0}px;width:1080px;height:1920px">')
PANEL_CLOSE = "</div></div>"

grp_by_clip = {}
for g in GROUPS: grp_by_clip.setdefault(g["clip"], []).append(g)

body = []
# full-frame speaker plates
for name, f0, f1, region in SPEAKER:
    if region == "full": body.append(plate_html(name, f0, f1, 1))
# full-frame b-roll
for shot in BROLL:
    if shot[4] == "full": body.append(broll_html(shot, 0, 0, 1080, 1920, 2))
# split A (S04-S05)
sa = ['<div id="splitA" class="abs layer" style="z-index:3;background:#FFFFFF">']
sa.append(panel_open("s4top", "top4"))
sa.append(plate_html("S04top", 207, 301, 1))
for shot in BROLL:
    if shot[4] == "top4": sa.append(broll_html(shot, 14, 14, 1052, 930, 2))
sa.append(f'<div id="ov4" class="abs layer" style="z-index:3;background:{css_grad("panel")}"></div>')
for g in grp_by_clip.get("top4", []): sa.append(group_html(g).replace('class="abs layer"', 'class="abs layer" style="z-index:4"', 1))
sa.append(PANEL_CLOSE)
sa.append(panel_open("s4bot", "bot4"))
sa.append(plate_html("S04bot", 207, 301, 1)); sa.append(plate_html("S05bot", 302, 415, 1))
for g in grp_by_clip.get("bot4", []): sa.append(group_html(g).replace('class="abs layer"', 'class="abs layer" style="z-index:4"', 1))
sa.append(PANEL_CLOSE); sa.append("</div>")
JS.append('GRP("#splitA",207,415);'); JS.append('GRP("#ov4",207,415);')
body.append("".join(sa))
# split B (S10)
sb = ['<div id="splitB" class="abs layer" style="z-index:3;background:#FFFFFF">']
sb.append(panel_open("s10top", "top10", "z-index:2"))
for shot in BROLL:
    if shot[4] == "top10": sb.append(broll_html(shot, 21, 14, 1038, 935, 2))
sb.append(f'<div class="abs layer" style="z-index:3;background:{css_grad("panel")}"></div>')
for g in grp_by_clip.get("top10", []): sb.append(group_html(g).replace('class="abs layer"', 'class="abs layer" style="z-index:4"', 1))
sb.append(PANEL_CLOSE)
sb.append(panel_open("s10bot", "bot10", "z-index:1;transform-origin:519px 998px"))
sb.append(plate_html("S10bot", 826, 948, 1)); sb.append(PANEL_CLOSE); sb.append("</div>")
JS.append('GRP("#splitB",826,948);')
top_y = {826 + i: e - 948 for i, e in enumerate(S10_TOP_BOTTOM_EDGE)}; top_y[850] = 0
JS.append(f'TAB("#s10top","y",{json.dumps({str(k): v for k, v in top_y.items()})});')
sc = {}; ks = sorted(S10_BOT_SCALE)
for f in range(826, 851):
    for i in range(len(ks) - 1):
        if ks[i] <= f <= ks[i + 1]:
            sc[f] = S10_BOT_SCALE[ks[i]] + (S10_BOT_SCALE[ks[i + 1]] - S10_BOT_SCALE[ks[i]]) * (f - ks[i]) / (ks[i + 1] - ks[i])
bot_ty = {826 + i: round(e - 1960 + sc[826 + i] * 998, 2) for i, e in enumerate(S10_BOT_TOP_EDGE)}; bot_ty[850] = 0
JS.append(f'TAB("#s10bot","scale",{json.dumps({str(k): round(v, 4) for k, v in sc.items()})});')
JS.append(f'TAB("#s10bot","y",{json.dumps({str(k): v for k, v in bot_ty.items()})});')
body.append("".join(sb))
# gradients
for i, (a, b) in enumerate(GRAD_SPEAKER):
    body.append(f'<div id="gs{i}" class="abs layer" style="z-index:5;background:{css_grad("black")}"></div>'); JS.append(f'GRP("#gs{i}",{a},{b});')
for i, (n, a, b) in enumerate(GRAD_BROLL):
    body.append(f'<div id="gb{i}" class="abs layer" style="z-index:5;background:{css_grad(n)}"></div>'); JS.append(f'GRP("#gb{i}",{a},{b});')
# unclipped graphics
for g in grp_by_clip.get(None, []): body.append(group_html(g).replace('class="abs layer"', 'class="abs layer" style="z-index:10"', 1))

AUDIO = json.load(open(os.path.join(HERE, "audio.json"))) if os.path.exists(os.path.join(HERE, "audio.json")) else []
aud = ['<audio id="voice" data-start="0" data-duration="51.0333" data-track-index="20" src="assets/raw.mp4" data-volume="0.88"></audio>',
       '<audio id="bed" data-start="0" data-duration="51.0333" data-track-index="21" src="assets/bed.mp3" data-volume="0.124"></audio>']
for i, (src, t, dur, vol) in enumerate(AUDIO):
    aud.append(f'<audio id="sfx{i}" data-start="{t}" data-duration="{dur}" data-track-index="{22 + i % 6}" src="{src}" data-volume="{vol}"></audio>')

tpl = open(os.path.join(HERE, "template.html")).read()
html = tpl.replace("%%BODY%%", "\n".join(body)).replace("%%AUDIO%%", "\n".join(aud)).replace("%%JS%%", "\n    ".join(JS))
open(os.path.join(ROOT, "index.html"), "w").write(html); print("index.html written", len(html), "bytes,", len(JS), "js lines")
