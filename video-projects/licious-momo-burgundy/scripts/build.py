"""Generate index.html: burgundy v2 of the first 45s of the Licious momo story.

v2 (see V2_STORYBOARD.png): cold open, shoulder-to-shoulder zoom hook, torn-paper frames,
road diagram, 5-minute timer, car-pulls-up mini diagram, bleeped gaaliyan + Part 2 hold.
Words + timings: assets/captions.json (lifted from the original burned-in captions).
Run from the project folder:  python3 scripts/build.py
"""
import json, html

W, H = 1080, 1920
CAPS = json.load(open("assets/captions.json"))
C = {c["i"]: c for c in CAPS}
LAST = 52                       # "maa behen ki gaaliyan" -> ends at 45.33s of her speech
O = 2.4                         # story starts after the cold open + rewind band
MAIN = C[LAST]["end"]
HOLD = 1.6
DUR = O + MAIN + HOLD
CAPS = [c for c in CAPS if c["i"] <= LAST]
COLD_MEDIA = C[128]["start"]    # "agar aap itne ameer ho toh / creta mein kyu ghum rahe ho?"

def t0(i): return O + C[i]["start"]
def t1(i): return O + C[i]["end"]
def m(t): return O + t
def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- beat spec
EMPH = {0: ("me and my", "bestfriend"), 15: ("nahi hai", "bhaiya"), 19: ("ho rahi thi", "bhai"),
        33: ("pagalon ki", "tarah"), 52: ("maa behen ki", "gaaliyan")}
PILL = {6: ("guys a story!", "l"), 22: ("please bhaiya!!", "r"), 34: ("horn baja rahi hai!!", "l")}
TYPE = [(18, "ANDHI BAARISH")]
ARC = {40: "uske ander hai hi nahi"}
PUNCH = {1, 13, 20, 24, 46}

HOOK_A = (t0(2), t0(3))         # "no bullshit people I know"
HOOK_B = (t0(3), t1(4))         # "even when our life is in danger"
TORN = [  # torn-paper window: b-roll (other moments) or live (same moment as the voice)
    dict(id="tp1", start=t0(8), end=t1(12), rot=-2, clips=[(0.4, t0(10)), (148.4, t1(12))], text={
        8: ("hum dono", "bandra mein"), 9: ("ache momo", "dhundhne"), 10: ("", "nikle the"),
        11: ("jo ki", "humari hi"), 12: ("", "galti hai")}),
    dict(id="tp2", start=t0(26), end=t1(30), rot=2, live=True, text={
        26: ("yeh bichara", "autowala"), 27: ("apna auto", "start nahi"), 28: ("kar pa raha hai", "kyu ki"),
        29: ("baarish ke", "wajhese"), 30: ("iska auto", "kharab hogaya hai")}),
]
ROAD = dict(start=t0(35), end=t1(38), text={35: ("jabki side mein", "poori sadak"), 36: ("", "khaali padi hai"),
            37: ("like yeh", "banda na"), 38: ("side se gaadi", "nikal sakta hai")})
TIMER = (t0(42), t1(43))
PULLUP = (t0(44), t1(46))

# shoulder zoom: (scale, x, y) for the face wrapper (transform-origin is the frame centre)
ZOOM_S = 1.6
ZOOM_A = (ZOOM_S, -218, 4)      # face pushed left, empty wall on the right for text
ZOOM_B = (ZOOM_S, 122, 4)       # face pushed right, text on the left

covered = set()
for a, b in [(HOOK_A[0], HOOK_B[1]), (ROAD["start"], ROAD["end"])] + [(t["start"], t["end"]) for t in TORN]:
    for c in CAPS:
        if t0(c["i"]) >= a - 1e-3 and t1(c["i"]) <= b + 1e-3:
            covered.add(c["i"])
special = set(EMPH) | set(PILL) | set(ARC) | {i for i, _ in TYPE}

els, js, aud = [], [], []
def clip(id_, start, end, track, cls, inner="", style=""):
    els.append(f'<div id="{id_}" class="clip {cls}" data-start="{start:.3f}" data-duration="{end - start:.3f}" '
               f'data-track-index="{track}" style="{style}">{inner}</div>')
_sx = [0]
def sfx(name, t, dur, vol=0.35):
    _sx[0] += 1
    aud.append(f'<audio id="sx{_sx[0]}" data-start="{t:.3f}" data-duration="{dur:.3f}" data-track-index="{60 + _sx[0] % 4}" '
               f'src="assets/sfx/{name}" data-volume="{vol}"></audio>')
def T(s): js.append(s)

def lockup(small, big):
    s = f'<span class="lk-s">{esc(small)}</span>' if small else ""
    return f'<div class="lk">{s}<span class="lk-c f-acc">{esc(big)}</span></div>'
def anim_lockup(sel, t):
    T(f'tl.fromTo("{sel} .lk-s",{{y:24,opacity:0}},{{y:0,opacity:1,duration:0.26,ease:"power3.out",immediateRender:false}},{t + 0.02:.3f});')
    T(f'tl.fromTo("{sel} .lk-c",{{opacity:0,scale:1.18,y:10}},{{opacity:1,scale:1,y:0,duration:0.34,ease:"back.out(2)",immediateRender:false}},{t + 0.1:.3f});')
def heads(prefix, text, en_limit, cls="head"):
    for i, (sm, big) in text.items():
        clip(f"{prefix}-t{i}", t0(i), min(t1(i), en_limit), 40, cls, lockup(sm, big))
        anim_lockup(f"#{prefix}-t{i}", t0(i))

GRAIN = '<svg class="grain" width="1080" height="1920"><rect width="1080" height="1920" filter="url(#noise)"/></svg><div class="vig"></div>'

# ---------------------------------------------------------------- cold open + rewind band
els.append(f'<div class="vwrap"><video id="cold" data-start="0" data-duration="2.000" data-track-index="2" '
           f'data-media-start="{COLD_MEDIA}" src="assets/clean.mp4" muted playsinline></video></div>')
aud.append(f'<audio id="vo-cold" data-start="0" data-duration="2.000" data-track-index="3" data-media-start="{COLD_MEDIA}" src="assets/clean.mp4" data-volume="1"></audio>')
clip("cold-lk", 0, 2.0, 21, "emph", lockup("agar aap itne ameer ho toh", "Creta mein kyu?"))
T('tl.fromTo("#cold-lk .lk-s",{y:20,opacity:0},{y:0,opacity:1,duration:0.25,ease:"power3.out"},0.05);')
T(f'tl.fromTo("#cold-lk .lk-c",{{opacity:0,scale:1.2}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{C[129]["start"] - COLD_MEDIA:.3f});')
clip("rewind", 2.0, O, 22, "card rewind", f'<div class="f-disp rw">◀◀ last saturday</div>{GRAIN}')
T('tl.fromTo("#rewind .rw",{x:120,opacity:0},{x:0,opacity:1,duration:0.22,ease:"expo.out"},2.0);')
sfx("whoosh.mp3", 1.96, 0.55, 0.3)

# ---------------------------------------------------------------- main face + voice
els.append(f'<div id="face-wrap"><video id="face" data-start="{O:.3f}" data-duration="{MAIN:.3f}" data-track-index="0" src="assets/clean.mp4" muted playsinline></video></div>')
aud.append(f'<audio id="vo" data-start="{O:.3f}" data-duration="{MAIN:.3f}" data-track-index="1" src="assets/clean.mp4" data-volume="1"></audio>')
clip("warm", O, O + MAIN, 3, "warm")

for c in CAPS:
    i = c["i"]
    if i in covered or i in special:
        continue
    clip(f"sub{i}", t0(i), t1(i), 4, "sub", f'<span>{esc(c["text"])}</span>')
    T(f'tl.fromTo("#sub{i} span",{{opacity:0,y:8}},{{opacity:1,y:0,duration:0.14,ease:"power2.out",immediateRender:false}},{t0(i) + 0.01:.3f});')
for i, (s, b) in EMPH.items():
    clip(f"em{i}", t0(i), DUR if i == LAST else t1(i), 5, "emph", lockup(s, b))
    anim_lockup(f"#em{i}", t0(i))
for i, (txt, side) in PILL.items():
    clip(f"pl{i}", t0(i), t1(i), 6, f"pill pill-{side}", f'<span class="f-acc">{esc(txt)}</span>')
    T(f'tl.fromTo("#pl{i} span",{{opacity:0,scale:0.55,rotation:{-12 if side == "l" else 8}}},{{opacity:1,scale:1,rotation:-3,duration:0.32,ease:"back.out(2.6)",immediateRender:false}},{t0(i) + 0.02:.3f});')
for k, (i, txt) in enumerate(TYPE):
    st, en = t0(i), t1(i)
    chars = "".join(f'<i class="ch">{esc(ch) if ch != " " else "&nbsp;"}</i>' for ch in txt)
    clip(f"tw{k}", st, en, 7, "type", f'<div class="bar"><span class="tw-t">{chars}</span><b class="cur">|</b></div>')
    T(f'tl.set("#tw{k} .ch",{{opacity:0,maxWidth:"0em"}},{st:.3f});')
    T(f'tl.fromTo("#tw{k} .bar",{{opacity:0,y:-12}},{{opacity:1,y:0,duration:0.18,ease:"power2.out",immediateRender:false}},{st:.3f});')
    span = min(0.06 * len(txt), (en - st) * 0.65)
    for j in range(len(txt)):
        T(f'tl.set("#tw{k} .ch:nth-child({j + 1})",{{opacity:1,maxWidth:"2em"}},{st + 0.12 + span * j / len(txt):.3f});')
    T(f'tl.fromTo("#tw{k} .cur",{{opacity:1}},{{opacity:0,duration:0.25,ease:"steps(1)",repeat:{max(1, int((en - st) / 0.5))},yoyo:true,immediateRender:false}},{st:.3f});')
for i, txt in ARC.items():
    svg = (f'<svg viewBox="0 0 1080 520" width="1080" height="520"><defs><path id="arcp{i}" d="M150,470 Q540,40 930,470"/></defs>'
           f'<text class="f-acc"><textPath href="#arcp{i}" startOffset="50%" text-anchor="middle">{esc(txt)}</textPath></text></svg>')
    clip(f"arc{i}", t0(i), t1(i), 8, "arc", svg)
    T(f'tl.fromTo("#arc{i} svg",{{opacity:0,rotation:-6,transformOrigin:"50% 90%"}},{{opacity:1,rotation:0,duration:0.4,ease:"power3.out",immediateRender:false}},{t0(i) + 0.02:.3f});')

# ---------------------------------------------------------------- hook: shoulder-to-shoulder zoom
sa, sb = ZOOM_A, ZOOM_B
T(f'tl.fromTo("#face-wrap",{{scale:1,x:0,y:0}},{{scale:{sa[0]},x:{sa[1]},y:{sa[2]},duration:0.38,ease:"power3.out",immediateRender:false}},{HOOK_A[0]:.3f});')
T(f'tl.to("#face-wrap",{{x:{sb[1]},y:{sb[2]},duration:0.45,ease:"power2.inOut"}},{HOOK_B[0]:.3f});')
T(f'tl.to("#face-wrap",{{scale:1,x:0,y:0,duration:0.35,ease:"power3.inOut"}},{HOOK_B[1]:.3f});')
sfx("whoosh.mp3", HOOK_B[0] - 0.05, 0.55, 0.22)
clip("hookA", HOOK_A[0], HOOK_A[1], 9, "hook hook-r",
     '<div class="kick">no bullshit</div><div class="f-disp hb">people</div><div class="f-disp hb">I know</div>')
T(f'tl.set("#hookA > *",{{opacity:0}},{HOOK_A[0]:.3f});')
T(f'tl.fromTo("#hookA .kick",{{opacity:0,x:30}},{{opacity:1,x:0,duration:0.25,ease:"power3.out"}},{HOOK_A[0] + 0.15:.3f});')
T(f'tl.fromTo("#hookA .hb:nth-child(2)",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"expo.out"}},{m(2.55):.3f});')
T(f'tl.fromTo("#hookA .hb:nth-child(3)",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"expo.out"}},{m(3.0):.3f});')
clip("hookB", HOOK_B[0], HOOK_B[1], 10, "hook hook-l",
     '<div class="hs">even when our life is in</div><div class="f-acc hd">danger.</div>')
T(f'tl.set("#hookB > *",{{opacity:0}},{HOOK_B[0]:.3f});')
T(f'tl.fromTo("#hookB .hs",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.28,ease:"power3.out"}},{HOOK_B[0] + 0.3:.3f});')
T(f'tl.fromTo("#hookB .hd",{{opacity:0,scale:1.25,transformOrigin:"0% 60%"}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{t0(4) + 0.02:.3f});')

# ---------------------------------------------------------------- torn-paper windows
TORN_POLY = ("polygon(0% 2%,5% 0%,11% 1.6%,18% 0%,26% 2%,33% .4%,41% 2.2%,49% 0%,57% 1.8%,64% .2%,72% 2.2%,80% .4%,87% 2%,94% 0%,100% 1.4%,"
             "98.6% 9%,100% 18%,98% 27%,100% 36%,98.4% 45%,100% 54%,98% 63%,100% 72%,98.6% 81%,100% 90%,98.4% 98.4%,"
             "93% 100%,86% 98.2%,78% 100%,70% 98%,62% 100%,54% 98.4%,46% 100%,38% 98%,30% 100%,22% 98.2%,14% 100%,6% 98.4%,0% 100%,"
             "1.6% 91%,0% 82%,2% 73%,0% 64%,1.6% 55%,0% 46%,2% 37%,0% 28%,1.6% 19%,0% 10%)")
TBOX = dict(left=130, top=560, width=820, height=1120)
for tp in TORN:
    st, en = tp["start"], tp["end"]
    box = f"left:{TBOX['left']}px;top:{TBOX['top']}px;width:{TBOX['width']}px;height:{TBOX['height']}px;transform:rotate({tp['rot']}deg);clip-path:{TORN_POLY};"
    clip(tp["id"], st, en, 11, "page", GRAIN)
    clip(tp["id"] + "-paper", st, en, 12, "paper", "", box)
    inner = f"left:{TBOX['left'] + 26}px;top:{TBOX['top'] + 26}px;width:{TBOX['width'] - 52}px;height:{TBOX['height'] - 52}px;transform:rotate({tp['rot']}deg);"
    clips = [(C[min(tp['text'])]['start'], en)] if tp.get("live") else tp["clips"]
    cs = st
    for k, (med, ce) in enumerate(clips):
        els.append(f'<div class="tv" id="{tp["id"]}-w{k}" style="{inner}"><video id="{tp["id"]}-v{k}" data-start="{cs:.3f}" '
                   f'data-duration="{ce - cs:.3f}" data-track-index="{20 + k}" data-media-start="{med:.3f}" src="assets/clean.mp4" muted playsinline></video></div>')
        T(f'tl.set("#{tp["id"]}-w{k}",{{opacity:0}},0);')
        T(f'tl.set("#{tp["id"]}-w{k}",{{opacity:1}},{cs:.3f});')
        T(f'tl.set("#{tp["id"]}-w{k}",{{opacity:0}},{ce:.3f});')
        cs = ce
    clip(tp["id"] + "-tape", st, en, 13, "tape", "", f"left:{TBOX['left'] + TBOX['width'] / 2 - 120}px;top:{TBOX['top'] - 30}px;transform:rotate({-4 if tp['rot'] < 0 else 3}deg);")
    T(f'tl.fromTo(["#{tp["id"]}-paper","#{tp["id"]}-w0"],{{y:-70,opacity:0}},{{y:0,opacity:1,duration:0.32,ease:"back.out(1.4)",immediateRender:false}},{st + 0.01:.3f});')
    T(f'tl.fromTo("#{tp["id"]}-tape",{{opacity:0,scaleX:0.4}},{{opacity:1,scaleX:1,duration:0.2,ease:"power2.out",immediateRender:false}},{st + 0.3:.3f});')
    sfx("paper-flip.mp3", st, 0.9, 0.3)
    heads(tp["id"], tp["text"], en)

# ---------------------------------------------------------------- road diagram
rs, re_ = ROAD["start"], ROAD["end"]
road = ('<div class="road"><div class="lane-l"></div><div class="divider"></div>'
        '<div class="veh auto-v" id="rd-auto"><span>US</span></div><div class="veh car-v" id="rd-car"><span>HIM</span></div>'
        '<div class="empty" id="rd-empty"><span class="f-acc">empty lane</span></div>'
        '<svg class="go" width="620" height="980" viewBox="0 0 620 980"><path d="M155 820 C 155 700, 528 720, 528 560 L 528 200" pathLength="1"/>'
        '<path class="hd" d="M498 236 L528 190 L558 236" pathLength="1"/></svg></div>')
clip("road", rs, re_, 14, "page roadpg", road + GRAIN)
T(f'tl.set(["#rd-auto","#rd-car","#rd-empty","#road .go path"],{{opacity:0}},{rs:.3f});')
T(f'tl.fromTo("#road .road",{{y:60,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"expo.out",immediateRender:false}},{rs + 0.01:.3f});')
T(f'tl.fromTo("#rd-auto",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{rs + 0.25:.3f});')
T(f'tl.fromTo("#rd-car",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{rs + 0.5:.3f});')
T(f'tl.fromTo("#rd-empty",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{t0(36) + 0.05:.3f});')
T(f'tl.fromTo("#road .go path",{{opacity:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.7,ease:"power2.inOut"}},{t0(38) + 0.1:.3f});')
T(f'tl.fromTo("#rd-car",{{x:-6}},{{x:6,duration:0.06,ease:"none",repeat:5,yoyo:true,immediateRender:false}},{t0(37) + 0.05:.3f});')
sfx("honk.wav", t0(37) + 0.05, 0.45, 0.35)
heads("rd", ROAD["text"], re_, "head head-hi")

# ---------------------------------------------------------------- 5-minute timer
ts, te = TIMER
clip("timer", ts, te, 15, "timer", '<div class="tk">lagataar horn</div><div class="f-disp tn">00:00</div>')
T(f'tl.fromTo("#timer",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.25,ease:"power3.out",immediateRender:false}},{ts + 0.02:.3f});')
steps = 30
for k in range(steps + 1):
    sec = round(300 * k / steps)
    T(f'tl.set("#timer .tn",{{textContent:"{sec // 60:02d}:{sec % 60:02d}"}},{ts + 0.2 + k * 0.055:.3f});')
T(f'tl.fromTo("#timer .tn",{{scale:1.15}},{{scale:1,duration:0.35,ease:"back.out(3)",immediateRender:false}},{ts + 0.2 + steps * 0.055:.3f});')
sfx("ticks.wav", ts + 0.2, 1.8, 0.3)

# ---------------------------------------------------------------- car pulls up (mini diagram)
ps, pe = PULLUP
clip("pullup", ps, pe, 16, "mini", '<div class="lane-l"></div><div class="divider"></div><div class="veh auto-v sm"><span>US</span></div><div class="veh car-v sm" id="pu-car"><span>HIM</span></div>')
T(f'tl.fromTo("#pullup",{{opacity:0,x:60}},{{opacity:1,x:0,duration:0.3,ease:"power3.out",immediateRender:false}},{ps + 0.02:.3f});')
T(f'tl.fromTo("#pu-car",{{x:0,y:150}},{{x:120,y:0,duration:1.4,ease:"power2.inOut",immediateRender:false}},{t0(45):.3f});')

# ---------------------------------------------------------------- bleeped gaaliyan + Part 2 hold
clip("bleep", t0(LAST) + 0.6, DUR, 17, "bleepbar", '<span class="f-disp">#@%&amp;!*</span>')
T(f'tl.fromTo("#bleep",{{opacity:0,scale:1.4,rotation:-8}},{{opacity:1,scale:1,rotation:-3,duration:0.2,ease:"back.out(3)",immediateRender:false}},{t0(LAST) + 0.6:.3f});')
sfx("bleep.wav", t0(LAST) + 0.6, 0.6, 0.22)
clip("endhold", O + MAIN, DUR, 24, "freeze", '<img src="assets/stills/end.jpg" alt=""><div class="tint"></div>')
clip("band", O + MAIN - 0.3, DUR, 45, "band", '<span>STORY CONTINUES</span><b></b><span class="f-disp">Part 2 →</span>')
T(f'tl.fromTo("#band",{{yPercent:110}},{{yPercent:0,duration:0.35,ease:"expo.out",immediateRender:false}},{O + MAIN - 0.3:.3f});')

# ---------------------------------------------------------------- punch-ins (plain face only)
blocked = [(HOOK_A[0] - 0.2, HOOK_B[1] + 0.5), (rs, re_)] + [(t["start"], t["end"]) for t in TORN]
for i in sorted(PUNCH):
    a, b = t0(i), t1(i)
    if any(a < e + 0.05 and b > s - 0.05 for s, e in blocked):
        continue
    T(f'tl.set("#face-wrap",{{scale:1.09}},{a:.3f});')
    T(f'tl.set("#face-wrap",{{scale:1}},{b:.3f});')

CSS = open("scripts/style.css").read()
out = f'''<!doctype html>
<html lang="en" data-resolution="portrait"><head><meta charset="utf-8">
<meta name="viewport" content="width=1080, height=1920" />
<title>Licious momo story, burgundy v2</title>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="{W}" data-height="{H}">
<svg width="0" height="0" style="position:absolute"><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter></svg>
{chr(10).join(els)}
{chr(10).join(aud)}
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
print(f"duration {DUR:.3f}  elements {len(els)}  audio {len(aud)}  tweens {len(js)}")
