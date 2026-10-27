"""Generate index.html: first 45s of the Licious momo story in the burgundy / Fraunces style.

Words + timings: assets/captions.json (lifted from the original burned-in captions).
Style: see STYLE_SKETCH.png in ../style-sample-burgundy.
Run from the project folder:  python3 scripts/build.py
"""
import json, html

W, H = 1080, 1920
CAPS = json.load(open("assets/captions.json"))
C = {c["i"]: c for c in CAPS}
LAST = 52                       # "maa behen ki gaaliyan" -> ends at 45.33s
DUR = C[LAST]["end"]
CAPS = [c for c in CAPS if c["i"] <= LAST]

def t0(i): return C[i]["start"]
def t1(i): return C[i]["end"]
def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- beat spec
# Key-word lockup: small DM Sans word + big pink Fraunces italic.
EMPH = {
    0: ("me and my", "bestfriend"),
    15: ("nahi hai", "bhaiya"),
    19: ("ho rahi thi", "bhai"),
    33: ("pagalon ki", "tarah"),
    36: ("poori sadak", "khaali padi hai"),
    52: ("maa behen ki", "gaaliyan"),
}
# Pink pill stickers for inner thoughts.
PILL = {6: ("guys a story!", "l"), 22: ("please bhaiya!!", "r"), 34: ("horn baja rahi hai!!", "l")}
# Typewriter bar: (caption idx, text)
TYPE = [(7, "LAST SATURDAY"), (18, "ANDHI BAARISH"), (42, "5 MIN TAK")]
ARC = {40: "uske ander hai hi nahi"}

# Burgundy title card (face hidden). kind: acc = pink italic, big = cream display, small = DM Sans
CARDS = [
    dict(id="card1", start=t0(2), end=t1(4), kick="no bullshit", lines=[
        (t0(2) + 0.45, "big", "people"), (t0(2) + 0.75, "big", "I know"),
        (t0(3), "small", "even when our life is in"), (t0(4), "acc", "danger.")]),
]
# Arched-window b-roll inserts (other moments of her eating), head text per phrase.
ARCH_BROLL = [
    dict(id="ab1", start=t0(8), end=t1(12), clips=[(0.4, t0(10)), (148.4, t1(12))], text={
        8: ("hum dono", "bandra mein"), 9: ("ache momo", "dhundhne"), 10: ("", "nikle the"),
        11: ("jo ki", "humari hi"), 12: ("", "galti hai")}),
]
# Live face inside the arched window.
ARCH_FACE = [
    dict(id="af1", start=t0(26), end=t1(30), text={
        26: ("yeh bichara", "autowala"), 27: ("apna auto", "start nahi"), 28: ("kar pa raha hai", "kyu ki"),
        29: ("baarish ke", "wajhese"), 30: ("iska auto", "kharab hogaya hai")}),
]
PUNCH = {1, 5, 13, 20, 24, 38, 46}

ARCH_WIN = (150, 560, 930, 1680)       # x0, y0, x1, y1
ARCH_R = "390px 390px 26px 26px"

covered = set()
for c0 in CARDS + ARCH_BROLL + ARCH_FACE:
    for c in CAPS:
        if c["start"] >= c0["start"] - 1e-3 and c["end"] <= c0["end"] + 1e-3:
            covered.add(c["i"])
special = set(EMPH) | set(PILL) | set(ARC) | {i for i, _ in TYPE}

# ---------------------------------------------------------------- emit
els, js = [], []
def clip(id_, start, end, track, cls, inner="", style=""):
    els.append(f'<div id="{id_}" class="clip {cls}" data-start="{start:.3f}" data-duration="{end - start:.3f}" '
               f'data-track-index="{track}" style="{style}">{inner}</div>')

def lockup(small, big):
    s = f'<span class="lk-s">{esc(small)}</span>' if small else ""
    return f'<div class="lk">{s}<span class="lk-c f-acc">{esc(big)}</span></div>'

def anim_lockup(sel, t):
    js.append(f'tl.fromTo("{sel} .lk-s",{{y:24,opacity:0}},{{y:0,opacity:1,duration:0.26,ease:"power3.out",immediateRender:false}},{t + 0.02:.3f});')
    js.append(f'tl.fromTo("{sel} .lk-c",{{opacity:0,scale:1.18,y:10}},{{opacity:1,scale:1,y:0,duration:0.34,ease:"back.out(2)",immediateRender:false}},{t + 0.1:.3f});')

GRAIN = '<svg class="grain" width="1080" height="1920"><rect width="1080" height="1920" filter="url(#noise)"/></svg><div class="vig"></div>'
SPARK = '<svg class="spark" style="{}" viewBox="0 0 100 100"><path d="M50 4 L58 42 L96 50 L58 58 L50 96 L42 58 L4 50 L42 42 Z" fill="{}"/></svg>'

# warm tint over the face for the whole edit (hidden while the face is framed)
clip("warm", 0, DUR, 3, "warm")

# base subtitles
for c in CAPS:
    i = c["i"]
    if i in covered or i in special:
        continue
    clip(f"sub{i}", c["start"], c["end"], 4, "sub", f'<span>{esc(c["text"])}</span>')
    js.append(f'tl.fromTo("#sub{i} span",{{opacity:0,y:8}},{{opacity:1,y:0,duration:0.14,ease:"power2.out",immediateRender:false}},{c["start"] + 0.01:.3f});')

for i, (s, b) in EMPH.items():
    clip(f"em{i}", t0(i), t1(i), 5, "emph", lockup(s, b))
    anim_lockup(f"#em{i}", t0(i))

for i, (txt, side) in PILL.items():
    clip(f"pl{i}", t0(i), t1(i), 6, f"pill pill-{side}", f'<span class="f-acc">{esc(txt)}</span>')
    js.append(f'tl.fromTo("#pl{i} span",{{opacity:0,scale:0.55,rotation:{-12 if side == "l" else 8}}},{{opacity:1,scale:1,rotation:-3,duration:0.32,ease:"back.out(2.6)",immediateRender:false}},{t0(i) + 0.02:.3f});')

for k, (i, txt) in enumerate(TYPE):
    st, en = t0(i), t1(i)
    chars = "".join(f'<i class="ch">{esc(ch) if ch != " " else "&nbsp;"}</i>' for ch in txt)
    clip(f"tw{k}", st, en, 7, "type", f'<div class="bar"><span class="tw-t">{chars}</span><b class="cur">|</b></div>')
    js.append(f'tl.set("#tw{k} .ch",{{opacity:0,maxWidth:"0em"}},{st:.3f});')
    js.append(f'tl.fromTo("#tw{k} .bar",{{opacity:0,y:-12}},{{opacity:1,y:0,duration:0.18,ease:"power2.out",immediateRender:false}},{st:.3f});')
    span = min(0.06 * len(txt), (en - st) * 0.65)
    for j in range(len(txt)):
        js.append(f'tl.set("#tw{k} .ch:nth-child({j + 1})",{{opacity:1,maxWidth:"2em"}},{st + 0.12 + span * j / len(txt):.3f});')
    js.append(f'tl.fromTo("#tw{k} .cur",{{opacity:1}},{{opacity:0,duration:0.25,ease:"steps(1)",repeat:{max(1, int((en - st) / 0.5))},yoyo:true,immediateRender:false}},{st:.3f});')

for i, txt in ARC.items():
    svg = (f'<svg viewBox="0 0 1080 520" width="1080" height="520"><defs><path id="arcp{i}" d="M150,470 Q540,40 930,470"/></defs>'
           f'<text class="f-acc"><textPath href="#arcp{i}" startOffset="50%" text-anchor="middle">{esc(txt)}</textPath></text></svg>')
    clip(f"arc{i}", t0(i), t1(i), 8, "arc", svg)
    js.append(f'tl.fromTo("#arc{i} svg",{{opacity:0,rotation:-6,transformOrigin:"50% 90%"}},{{opacity:1,rotation:0,duration:0.4,ease:"power3.out",immediateRender:false}},{t0(i) + 0.02:.3f});')

# burgundy title cards
STAMP = ('<svg class="stamp" viewBox="0 0 200 200"><defs><path id="ring{0}" d="M100,100 m-72,0 a72,72 0 1,1 144,0 a72,72 0 1,1 -144,0"/></defs>'
         '<circle cx="100" cy="100" r="94" fill="none" stroke="#FDC5F4" stroke-width="3"/>'
         '<text font-family="DM Sans" font-weight="700" font-size="22" fill="#FDC5F4"><textPath href="#ring{0}" textLength="438" lengthAdjust="spacing">STORYTIME · STORYTIME · STORYTIME · </textPath></text>'
         '<path d="M100 74 L106 94 L126 100 L106 106 L100 126 L94 106 L74 100 L94 94 Z" fill="#F3EAE3"/></svg>')
for cd in CARDS:
    lines = "".join(f'<div class="ln ln-{k}{" f-disp" if k == "big" else ""}{" f-acc" if k == "acc" else ""}">{esc(t)}</div>' for _, k, t in cd["lines"])
    inner = f'<div class="stack"><div class="kick">{esc(cd["kick"])}</div>{lines}</div>{STAMP.format(cd["id"])}{GRAIN}'
    clip(cd["id"], cd["start"], cd["end"], 10, "card", inner)
    js.append(f'tl.set("#{cd["id"]} .stack > *",{{opacity:0}},{cd["start"]:.3f});')
    js.append(f'tl.fromTo("#{cd["id"]} .kick",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},{cd["start"] + 0.04:.3f});')
    for j, (t, k, _) in enumerate(cd["lines"]):
        if k == "acc":
            js.append(f'tl.fromTo("#{cd["id"]} .ln:nth-child({j + 2})",{{opacity:0,scale:1.25,transformOrigin:"0% 60%"}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{t + 0.02:.3f});')
        else:
            js.append(f'tl.fromTo("#{cd["id"]} .ln:nth-child({j + 2})",{{opacity:0,y:{50 if k == "big" else 16}}},{{opacity:1,y:0,duration:{0.45 if k == "big" else 0.3},ease:"{"expo.out" if k == "big" else "power2.out"}"}},{t + 0.02:.3f});')
    js.append(f'tl.fromTo("#{cd["id"]} .stamp",{{rotation:0}},{{rotation:40,duration:{cd["end"] - cd["start"]:.3f},ease:"none"}},{cd["start"]:.3f});')

def arch_head(prefix, text, en_limit):
    for i, (sm, big) in text.items():
        clip(f"{prefix}-t{i}", t0(i), min(t1(i), en_limit), 40, "head", lockup(sm, big))
        anim_lockup(f"#{prefix}-t{i}", t0(i))

x0, y0, x1, y1 = ARCH_WIN
box = f"left:{x0}px;top:{y0}px;width:{x1 - x0}px;height:{y1 - y0}px;border-radius:{ARCH_R};"
sparks = SPARK.format("left:70px;top:1560px", "#FDC5F4") + SPARK.format("left:930px;top:640px;width:60px;height:60px", "#F3EAE3")

# arched b-roll inserts: burgundy page, separate clips inside the window
for ab in ARCH_BROLL:
    st, en = ab["start"], ab["end"]
    clip(ab["id"], st, en, 11, "page", sparks + GRAIN)
    clip(ab["id"] + "-rim", st, en, 12, "rim", "", box + "z-index:33;")
    cs = st
    for k, (m, ce) in enumerate(ab["clips"]):
        els.append(f'<div class="archv" id="{ab["id"]}-w{k}" style="{box}"><video id="{ab["id"]}-v{k}" data-start="{cs:.3f}" '
                   f'data-duration="{ce - cs:.3f}" data-track-index="{20 + k}" data-media-start="{m}" src="assets/clean.mp4" muted playsinline></video></div>')
        js.append(f'tl.set("#{ab["id"]}-w{k}",{{opacity:0}},0);')
        js.append(f'tl.set("#{ab["id"]}-w{k}",{{opacity:1}},{cs:.3f});')
        js.append(f'tl.set("#{ab["id"]}-w{k}",{{opacity:0}},{ce:.3f});')
        cs = ce
    js.append(f'tl.fromTo(["#{ab["id"]}-rim","#{ab["id"]}-w0"],{{y:80,scale:0.94}},{{y:0,scale:1,duration:0.4,ease:"expo.out",immediateRender:false}},{st + 0.01:.3f});')
    js.append(f'tl.fromTo("#{ab["id"]} .spark",{{rotation:-30,scale:0.4}},{{rotation:15,scale:1,duration:{en - st:.3f},ease:"power1.out",immediateRender:false}},{st:.3f});')
    arch_head(ab["id"], ab["text"], en)

# live face in the arch: scale + clip the face wrapper into the window
def window_set(t, s, ty, win):
    wx0, wy0, wx1, wy1 = win
    inv = lambda v, c, o=0: c + (v - c - o) / s
    L, R = inv(wx0, 540), inv(wx1, 540)
    T, B = inv(wy0, 960, ty), inv(wy1, 960, ty)
    r = " ".join(f"{float(v[:-2]) / s:.1f}px" for v in ARCH_R.split())
    clipv = f"inset({T:.1f}px {W - R:.1f}px {H - B:.1f}px {L:.1f}px round {r})"
    js.append(f'tl.set("#face-wrap",{{scale:{s},y:{ty},clipPath:"{clipv}"}},{t:.3f});')
    js.append(f'tl.fromTo("#face-wrap",{{scale:{s * 1.03:.4f}}},{{scale:{s},duration:0.14,ease:"power2.out",immediateRender:false}},{t:.3f});')

for af in ARCH_FACE:
    st, en = af["start"], af["end"]
    clip(af["id"], st, en, 13, "page page-under", sparks + GRAIN)
    clip(af["id"] + "-rim", st, en, 14, "rim", "", box + "z-index:3;")
    window_set(st, 0.8, 160, ARCH_WIN)
    js.append(f'tl.set("#face-wrap",{{scale:1,y:0,clipPath:"inset(0px 0px 0px 0px round 0px)"}},{en:.3f});')
    js.append(f'tl.set("#warm",{{opacity:0}},{st:.3f});')
    js.append(f'tl.set("#warm",{{opacity:1}},{en:.3f});')
    js.append(f'tl.fromTo("#{af["id"]} .spark",{{rotation:-30,scale:0.4}},{{rotation:15,scale:1,duration:{en - st:.3f},ease:"power1.out",immediateRender:false}},{st:.3f});')
    arch_head(af["id"], af["text"], en)

# punch-in reframes on plain face segments
framed = [(f["start"], f["end"]) for f in ARCH_FACE]
for i in sorted(PUNCH):
    a, b = t0(i), t1(i)
    if any(a < e + 0.05 and b > s0 - 0.05 for s0, e in framed):
        continue
    js.append(f'tl.set("#face-wrap",{{scale:1.09}},{a:.3f});')
    js.append(f'tl.set("#face-wrap",{{scale:1}},{b:.3f});')

CSS = open("scripts/style.css").read()
out = f'''<!doctype html>
<html lang="en" data-resolution="portrait"><head><meta charset="utf-8">
<meta name="viewport" content="width=1080, height=1920" />
<title>Licious momo story, burgundy</title>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="{W}" data-height="{H}">
<svg width="0" height="0" style="position:absolute"><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter></svg>
<div id="face-wrap"><video id="face" data-start="0" data-duration="{DUR:.3f}" data-track-index="0" src="assets/clean.mp4" muted playsinline></video></div>
<audio id="vo" data-start="0" data-duration="{DUR:.3f}" data-track-index="1" src="assets/clean.mp4" data-volume="1"></audio>
{chr(10).join(els)}
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</div>
</body></html>
'''
open("index.html", "w").write(out)
print("duration", DUR, "elements", len(els), "tweens", len(js))
