"""Generate index.html for the Licious momo story edit in the @fraym-fx style.

Source of truth for the words + timings: assets/captions.json (lifted from the original
burned-in captions, which were already synced to the speech).
Run from the project folder:  python3 scripts/build.py
"""
import json, html, math

W, H = 1080, 1920
DUR = 159.68
CAPS = json.load(open("assets/captions.json"))
C = {c["i"]: c for c in CAPS}

RED = "#A3161C"
CREAM = "#F3E6B5"
YELLOW = "#E2F040"
PINK = "#E8B8C4"

def t0(i): return C[i]["start"]
def t1(i): return C[i]["end"]
def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- beat spec
# Emphasis lockup (small bold sans word + big overlapping script word), upper third.
EMPH = {
    0: ("Me and my", "bestfriend"),
    15: ("nahi hai", "bhaiya"),
    19: ("ho rahi thi", "bhai"),
    33: ("pagalon ki", "tarah"),
    36: ("poori sadak", "khaali padi hai"),
    52: ("maa behen ki", "gaaliyan"),
    59: ("sorry ma'am,", "sorry ma'am"),
    63: ("not stop", "talking at him"),
    77: ("aap thode", "jobless ho kya?"),
    84: ("full body", "reaction"),
    97: ("scary looking", "man okay"),
    107: ("koi fattu", "hai hi nahi"),
    110: ("this", "outfit"),
    115: ("has rahi hu ki", "hehehehe"),
    124: ("the calmest", "person i know"),
    149: ("bhara hua hai", "yaar"),
    158: ("how a good momo", "should be"),
}
# Acid-yellow inner-thought callouts (replace the subtitle for that phrase).
YEL = {
    6: ("guys a story!", "l"),
    22: ("please bhaiya!!", "r"),
    34: ("horn baja rahi hai!!", "l"),
    54: ("tu andha hai kya??", "r"),
    55: ("tuje dikhta nahi hai??", "l"),
    75: ("kya boli kya boli??", "r"),
    101: ("tuje kharid lunga", "l"),
    137: ("goli se uda dega?!", "r"),
    148: ("juicy chicken!!", "l"),
    153: ("laal chutney", "r"),
    156: ("mirchi lag jaati hai", "l"),
}
# Typewriter search bar: (first idx, last idx, text)
TYPE = [(7, 7, "LAST SATURDAY"), (18, 18, "ANDHI BAARISH"), (42, 42, "5 MIN TAK"),
        (96, 96, "6 FEET TALL"), (129, 130, "CRETA MEIN KYU GHUM RAHE HO?")]
ARC = {40: "uske ander hai hi nahi", 121: "itna ameer hu"}
LABEL = {151: "very thin coating", 147: "yeh kya mast"}

# Cream kinetic title cards (face hidden). Lines: (time, kind, text) kind in script|bold|small
CARDS = [
    dict(id="card1", start=t0(2), end=t1(4), lines=[
        (t0(2), "script", "no bullshit"), (t0(2) + 0.55, "bold", "people I know"),
        (t0(3), "small", "even when our life"), (t0(4), "script", "is in"), (t0(4) + 0.3, "bold", "danger")]),
    dict(id="card2", start=t0(66), end=t1(67), lines=[
        (t0(66), "script", "mai toh yu turant"), (t0(67), "bold", "ragebait"),
        (t0(67) + 0.35, "small", "ho jaati hu")]),
    # 90.6-96.2s: she leans into the lens and fills the old caption band, so the clean-up
    # can't be invisible there -- cover it with two back-to-back quote cards.
    dict(id="card3", start=t0(98), end=t1(100), lines=[
        (t0(98), "small", "woh literally"), (t0(99), "script", "humare auto"),
        (t0(99) + 0.4, "bold", "ke ander"), (t0(100), "small", "ghus ke muje bol raha hai ki")]),
    dict(id="card4", start=t0(101), end=t1(103), lines=[
        (t0(101), "script", "tuje"), (t0(101) + 0.3, "bold", "kharid lunga"),
        (t0(102), "small", "tuj jaisi 100"), (t0(102) + 0.45, "script", "kharid lunga"),
        (t0(103), "small", "tu jaanti nahi hai muje")]),
]
YEL.pop(101)  # covered by card4

# Scrapbook collages: three tilted clips of her own momo footage + red line build.
COLLAGES = [
    dict(id="col1", start=t0(8), end=t1(12), media=[0.4, 143.7, 148.4], lines=[
        (t0(8), "small", "hum dono"), (t0(8) + 0.35, "script", "bandra mein"),
        (t0(9), "small", "ache momo"), (t0(9) + 0.3, "script", "dhundhne"),
        (t0(10), "small", "nikle the"), (t0(11), "small", "jo ki humari hi"),
        (t0(12), "script", "galti hai")]),
    dict(id="col2", start=t0(141), end=t1(144), media=[141.3, 145.6, 152.3], lines=[
        (t0(141), "small", "a nice plate of"), (t0(141) + 0.4, "script", "momo"),
        (t0(142), "small", "when we could have"), (t0(143), "small", "ordered the"),
        (t0(143) + 0.35, "script", "best,"), (t0(144), "small", "no BS"),
        (t0(144) + 0.35, "script", "momos online!")]),
]
# Live face framed in a window: polaroid / digicam / pink hearts. Top text per phrase.
FRAMES = [
    dict(id="pol1", kind="polaroid", start=t0(26), end=t1(30), text={
        26: ("yeh bichara", "autowala"), 27: ("apna auto", "start nahi"), 28: ("kar pa raha hai", "kyu ki"),
        29: ("baarish ke", "wajhese"), 30: ("iska auto", "kharab hogaya hai")}),
    dict(id="cam1", kind="digicam", start=t0(69), end=t1(73), text={
        69: ("I look at", "this woman"), 70: ("with a", "straight face"), 71: ("and I", "say"),
        72: ("ma'am", "aap thode"), 73: ("jobless", "ho kya?")}),
    dict(id="pink1", kind="pink", start=t0(88), end=t1(90), text={
        88: ("and I'm", "just like"), 89: ("itna toh maine", "kuch nahi"), 90: ("bola tha", "girliepop")}),
    dict(id="pink2", kind="pink", start=t0(131), end=t1(133), text={
        131: ("and we", "both have"), 132: ("died", "laughing"), 133: ("humse ho hi", "nahi paa raha")}),
    dict(id="pol2", kind="polaroid", start=t0(150), end=t1(152), text={
        150: ("and it", "has a"), 151: ("very thin", "coating"), 152: ("I love to", "eat it")}),
    dict(id="pink3", kind="pink", start=t0(159), end=DUR, text={
        159: ("", "umm"), 160: ("umm", "umm umm..."), 161: ("umm umm", "umm umm...")}),
]
LABEL.pop(151)  # inside pol2
PRODUCT = (145, "The Licious", "Mother of all Momos")
PUNCH = {1, 5, 13, 20, 24, 38, 46, 57, 62, 65, 68, 74, 78, 82, 86, 93, 99, 105, 112, 117, 119, 127, 135, 139, 146, 154}

covered = set()
def cover(a, b):
    for c in CAPS:
        if c["start"] >= a - 1e-3 and c["end"] <= b + 1e-3:
            covered.add(c["i"])
for c in CARDS + COLLAGES + FRAMES:
    cover(c["start"], c["end"])
special = set(EMPH) | set(YEL) | set(ARC) | set(LABEL) | {PRODUCT[0]}
for a, b, _ in TYPE:
    special |= set(range(a, b + 1))

# ---------------------------------------------------------------- emit
els, js = [], []
def clip(id_, start, end, track, cls, inner, style=""):
    els.append(f'<div id="{id_}" class="clip {cls}" data-start="{start:.3f}" data-duration="{end - start:.3f}" '
               f'data-track-index="{track}" style="{style}">{inner}</div>')

def lockup(small, script, cls="lk"):
    s = f'<span class="lk-s">{esc(small)}</span>' if small else ""
    return f'<div class="{cls}">{s}<span class="lk-c">{esc(script)}</span></div>'

def anim_lockup(sel, t):
    js.append(f'tl.fromTo("{sel} .lk-s",{{y:24,opacity:0}},{{y:0,opacity:1,duration:0.28,ease:"power3.out",immediateRender:false}},{t + 0.02:.3f});')
    js.append(f'tl.fromTo("{sel} .lk-c",{{clipPath:"inset(0 100% 0 0)",x:-10}},{{clipPath:"inset(0 0% 0 0)",x:0,duration:0.5,ease:"power2.out",immediateRender:false}},{t + 0.1:.3f});')

# base subtitles
for c in CAPS:
    i = c["i"]
    if i in covered or i in special:
        continue
    clip(f"sub{i}", c["start"], c["end"], 2, "sub", f'<span>{esc(c["text"])}</span>')
    js.append(f'tl.fromTo("#sub{i} span",{{opacity:0,scale:0.94}},{{opacity:1,scale:1,duration:0.16,ease:"power2.out",immediateRender:false}},{c["start"] + 0.01:.3f});')

for i, (s, sc) in EMPH.items():
    clip(f"em{i}", t0(i), t1(i), 3, "emph", lockup(s, sc))
    anim_lockup(f"#em{i}", t0(i))

for i, (txt, side) in YEL.items():
    clip(f"y{i}", t0(i), t1(i), 4, f"yel yel-{side}", f'<span>{esc(txt)}</span>')
    js.append(f'tl.fromTo("#y{i} span",{{x:{-30 if side == "l" else 30},opacity:0,rotation:-3}},{{x:0,opacity:1,rotation:-3,duration:0.3,ease:"back.out(2)",immediateRender:false}},{t0(i) + 0.02:.3f});')

for i, txt in LABEL.items():
    clip(f"lb{i}", t0(i), t1(i), 4, "label", f'<span>{esc(txt)}</span>')
    js.append(f'tl.fromTo("#lb{i} span",{{y:16,opacity:0}},{{y:0,opacity:1,duration:0.25,ease:"power2.out",immediateRender:false}},{t0(i) + 0.02:.3f});')

for k, (a, b, txt) in enumerate(TYPE):
    st, en = t0(a), t1(b)
    chars = "".join(f'<i class="ch">{esc(ch) if ch != " " else "&nbsp;"}</i>' for ch in txt)
    clip(f"tw{k}", st, en, 5, "type", f'<div class="bar"><span class="tw-t">{chars}</span><b class="cur">|</b></div>')
    js.append(f'tl.set("#tw{k} .ch",{{opacity:0,maxWidth:"0em"}},{st:.3f});')
    js.append(f'tl.fromTo("#tw{k} .bar",{{opacity:0,y:-12}},{{opacity:1,y:0,duration:0.18,ease:"power2.out",immediateRender:false}},{st:.3f});')
    span = min(0.065 * len(txt), (en - st) * 0.7)
    for j in range(len(txt)):
        js.append(f'tl.set("#tw{k} .ch:nth-child({j + 1})",{{opacity:1,maxWidth:"2em"}},{st + 0.12 + span * j / len(txt):.3f});')
    blinks = max(1, int((en - st) / 0.5))
    js.append(f'tl.fromTo("#tw{k} .cur",{{opacity:1}},{{opacity:0,duration:0.25,ease:"steps(1)",repeat:{blinks},yoyo:true,immediateRender:false}},{st:.3f});')

for i, txt in ARC.items():
    svg = (f'<svg viewBox="0 0 1080 520" width="1080" height="520"><defs><path id="arcp{i}" d="M150,470 Q540,40 930,470"/></defs>'
           f'<text><textPath href="#arcp{i}" startOffset="50%" text-anchor="middle">{esc(txt)}</textPath></text></svg>')
    clip(f"arc{i}", t0(i), t1(i), 6, "arc", svg)
    js.append(f'tl.fromTo("#arc{i} svg",{{opacity:0,rotation:-6,transformOrigin:"50% 90%"}},{{opacity:1,rotation:0,duration:0.4,ease:"power3.out",immediateRender:false}},{t0(i) + 0.02:.3f});')

# product write-on
pi, ps, pc = PRODUCT
letters = "".join(f'<i class="pl">{esc(ch) if ch != " " else "&nbsp;"}</i>' for ch in pc)
clip("prod", t0(pi), t1(pi), 3, "emph prod", f'<div class="lk"><span class="lk-s">{esc(ps)}</span><span class="pc">{letters}</span></div>')
js.append(f'tl.fromTo("#prod .lk-s",{{y:20,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"power3.out",immediateRender:false}},{t0(pi) + 0.02:.3f});')
js.append(f'tl.fromTo("#prod .pl",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.22,stagger:0.045,ease:"power2.out",immediateRender:false}},{t0(pi) + 0.25:.3f});')

# cream cards
def line_html(kind, text):
    return f'<div class="ln ln-{kind}">{esc(text)}</div>'
for cd in CARDS:
    inner = '<div class="card-in">' + "".join(line_html(k, t) for _, k, t in cd["lines"]) + "</div>"
    clip(cd["id"], cd["start"], cd["end"], 7, "card", inner)
    js.append(f'tl.set("#{cd["id"]} .ln",{{opacity:0}},{cd["start"]:.3f});')
    for j, (t, k, _) in enumerate(cd["lines"]):
        ease = ["power3.out", "back.out(1.6)", "expo.out"][j % 3]
        js.append(f'tl.fromTo("#{cd["id"]} .ln:nth-child({j + 1})",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.32,ease:"{ease}",immediateRender:false}},{t + 0.02:.3f});')

# collages
SLOTS = [dict(x=70, y=250, w=430, h=640, r=-5), dict(x=585, y=840, w=420, h=640, r=5), dict(x=85, y=1150, w=400, h=600, r=-3)]
for cd in COLLAGES:
    st, en = cd["start"], cd["end"]
    txt = '<div class="col-text">' + "".join(line_html(k, t) for _, k, t in cd["lines"]) + "</div>"
    deco = ('<svg class="plane" viewBox="0 0 120 80"><path d="M5 40 L110 8 L70 75 L55 48 Z M55 48 L110 8" fill="none" stroke="#5a3b2e" stroke-width="3" stroke-linejoin="round"/>'
            '<path d="M5 40 C-30 60 -60 20 -90 50" fill="none" stroke="#5a3b2e" stroke-width="2.5" stroke-dasharray="6 7"/></svg>'
            '<div class="star">&#10022;</div>')
    clip(cd["id"], st, en, 8, "collage", txt + deco)
    js.append(f'tl.set("#{cd["id"]} .ln",{{opacity:0}},{st:.3f});')
    for j, (t, k, _) in enumerate(cd["lines"]):
        js.append(f'tl.fromTo("#{cd["id"]} .ln:nth-child({j + 1})",{{opacity:0,y:22}},{{opacity:1,y:0,duration:0.3,ease:"power3.out",immediateRender:false}},{t + 0.02:.3f});')
    for s, (sl, m) in enumerate(zip(SLOTS, cd["media"])):
        appear = st + 0.12 * s
        pos = f"left:{sl['x']}px;top:{sl['y']}px;width:{sl['w']}px;height:{sl['h']}px;transform:rotate({sl['r']}deg);"
        clip(f"{cd['id']}-f{s}", st, en, 20 + s, "slot", '<div class="pin"></div>', pos)
        els.append(f'<div class="slotv" id="{cd["id"]}-w{s}" style="{pos}"><video id="{cd["id"]}-v{s}" data-start="{st:.3f}" data-duration="{en - st:.3f}" '
                   f'data-track-index="{30 + s}" data-media-start="{m}" src="assets/clean.mp4" muted playsinline></video></div>')
        js.append(f'tl.set(["#{cd["id"]}-f{s}","#{cd["id"]}-w{s}"],{{opacity:0}},{st:.3f});')
        js.append(f'tl.fromTo(["#{cd["id"]}-f{s}","#{cd["id"]}-w{s}"],{{scale:0.86,opacity:0}},{{scale:1,opacity:1,duration:0.32,ease:"back.out(1.8)",immediateRender:false}},{appear:.3f});')
        js.append(f'tl.set("#{cd["id"]}-w{s}",{{opacity:0}},{en:.3f});')
        js.append(f'tl.set("#{cd["id"]}-w{s}",{{opacity:0}},0);')

# framed face windows
def window_set(t, s, ty, win, rad):
    x0, y0, x1, y1 = win
    inv = lambda v, c, o=0: c + (v - c - o) / s
    L, R = inv(x0, 540), inv(x1, 540)
    T, B = inv(y0, 960, ty), inv(y1, 960, ty)
    clipv = f"inset({T:.1f}px {W - R:.1f}px {H - B:.1f}px {L:.1f}px round {rad / s:.1f}px)"
    js.append(f'tl.set("#face-wrap",{{scale:{s},y:{ty},clipPath:"{clipv}"}},{t:.3f});')
    js.append(f'tl.fromTo("#face-wrap",{{scale:{s * 1.03:.4f}}},{{scale:{s},duration:0.12,ease:"power2.out",immediateRender:false}},{t:.3f});')

def flower(x, y, r, col):
    pet = "".join(f'<circle cx="{x + r * math.cos(a * math.pi / 2.5):.1f}" cy="{y + r * math.sin(a * math.pi / 2.5):.1f}" r="{r * 0.8:.1f}" fill="{col}"/>' for a in range(5))
    return pet + f'<circle cx="{x}" cy="{y}" r="{r * 0.55:.1f}" fill="#E9C46A"/>'

def prng(seed):
    s = seed
    while True:
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        yield s / 0x7FFFFFFF

HEART = "M50 88 C20 66 4 48 4 30 C4 14 16 4 30 4 C40 4 47 10 50 18 C53 10 60 4 70 4 C84 4 96 14 96 30 C96 48 80 66 50 88 Z"
for fr in FRAMES:
    st, en, kind = fr["start"], fr["end"], fr["kind"]
    if kind == "polaroid":
        win, s, ty, rad = (150, 430, 930, 1450), 0.76, 40, 6
        bg = ('<div class="pol-card"></div>'
              f'<svg class="pol-heart" viewBox="0 0 100 92"><path d="{HEART}" fill="#B5121B" opacity="0.92"/>'
              '<path d="M30 20 C22 26 20 36 26 46" stroke="#fff" stroke-width="4" fill="none" opacity=".5" stroke-linecap="round"/></svg>')
        clip(fr["id"] + "-bg", st, en, 9, "fbg fbg-pol", bg)
    elif kind == "digicam":
        win, s, ty, rad = (175, 560, 905, 1230), 0.76, 70, 14
        rnd = prng(7)
        fl = "".join(flower(int(next(rnd) * 1080), int(next(rnd) * 1920), 9 + int(next(rnd) * 10), "#E7A9B4") for _ in range(26))
        bg = (f'<svg class="paper" viewBox="0 0 1080 1920" width="1080" height="1920">{fl}'
              '<path d="M90 120 C60 60 150 20 200 80 C240 20 340 60 300 140 C270 200 200 240 200 260 C190 230 110 190 90 120 Z" fill="#CDBBA2" opacity=".85"/></svg>'
              '<div class="cam-body"><div class="cam-screen"></div><div class="cam-dial"><span>M</span></div>'
              '<div class="cam-btn b1"></div><div class="cam-btn b2"></div><div class="cam-grill"></div></div>'
              f'<svg class="lily" viewBox="0 0 200 200">{flower(100, 100, 38, "#E6A1B5")}{flower(150, 160, 22, "#F0BFCB")}</svg>')
        clip(fr["id"] + "-bg", st, en, 9, "fbg fbg-cam", bg)
        clip(fr["id"] + "-bz", st, en, 10, "cam-bezel", "")
    else:
        win, s, ty, rad = (70, 150, 1010, 1770), 0.89, 0, 22
        rnd = prng(3)
        hearts = "".join(f'<path d="{HEART}" transform="translate({next(rnd) * 1040:.0f},{next(rnd) * 1880:.0f}) scale({0.25 + next(rnd) * 0.5:.2f})" fill="#fff" opacity="{0.25 + next(rnd) * 0.4:.2f}"/>' for _ in range(34))
        bg = f'<div class="bokeh"></div><svg class="hearts" viewBox="0 0 1080 1920" width="1080" height="1920">{hearts}</svg>'
        clip(fr["id"] + "-bg", st, en, 9, "fbg fbg-pink", bg)
    window_set(st, s, ty, win, rad)
    js.append(f'tl.set("#face-wrap",{{scale:1,y:0,clipPath:"inset(0px 0px 0px 0px round 0px)"}},{en:.3f});')
    for i, (sm, sc) in fr["text"].items():
        e = min(t1(i), en)
        cls = "ftext ftext-red" if kind in ("polaroid", "digicam") else "ftext ftext-white"
        clip(f"{fr['id']}-t{i}", t0(i), e, 11, cls, lockup(sm, sc))
        anim_lockup(f"#{fr['id']}-t{i}", t0(i))

# punch-in zooms on plain face segments (hard-cut reframes, like the reference)
framed = [(f["start"], f["end"]) for f in FRAMES]
for i in sorted(PUNCH):
    a, b = t0(i), t1(i)
    if any(a < e + 0.05 and b > s0 - 0.05 for s0, e in framed):
        continue
    js.append(f'tl.set("#face-wrap",{{scale:1.09}},{a:.3f});')
    js.append(f'tl.set("#face-wrap",{{scale:1}},{b:.3f});')

CSS = open("scripts/fonts.css").read() + open("scripts/style.css").read()
out = f'''<!doctype html>
<html><head><meta charset="utf-8"><title>Licious momo story</title>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
<div id="face-wrap"><video id="face" data-start="0" data-duration="{DUR}" data-track-index="0" src="assets/clean.mp4" muted playsinline></video></div>
<audio id="vo" data-start="0" data-duration="{DUR}" data-track-index="1" src="assets/clean.mp4" data-volume="1"></audio>
{chr(10).join(els)}
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
tl.set({{}}, {{}}, {DUR});
window.__timelines["main"] = tl;
</script>
</div>
</body></html>
'''
open("index.html", "w").write(out)
print("elements", len(els), "tweens", len(js))
