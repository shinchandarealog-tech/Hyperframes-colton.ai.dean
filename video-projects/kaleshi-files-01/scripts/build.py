"""Generate index.html for "The Kaleshi Aurat Files - Case #01".

First 45s of the momo story (speech untouched) + a 3.4s cold open / rewind in front and a
1.6s freeze hold at the end. Storyboard: ../licious-momo-burgundy/CASE_FILES_STORYBOARD.png
Run from the project folder:  python3 scripts/build.py
"""
import json, html

W, H = 1080, 1920
CAPS = json.load(open("assets/captions.json"))
C = {c["i"]: c for c in CAPS}
LAST = 52
O = 3.4                         # story starts here (after cold open + case cover)
MAIN = C[LAST]["end"]           # 45.333s of her speech
HOLD = 1.6
DUR = O + MAIN + HOLD
CAPS = [c for c in CAPS if c["i"] <= LAST]

def t0(i): return O + C[i]["start"]
def t1(i): return O + C[i]["end"]
def m(t): return O + t           # media time -> composition time
def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- beat spec
EMPH = {15: ("nahi hai", "bhaiya"), 19: ("ho rahi thi", "bhai"), 33: ("pagalon ki", "tarah"),
        36: ("poori sadak", "khaali padi hai"), 52: ("maa behen ki", "gaaliyan")}
THOUGHT = {6: ("guys a story!", "r"), 22: ("please bhaiya!!", "r")}
NOTES = [(18, "WEATHER: ANDHI BAARISH"), (42, "DURATION: 5 MIN TAK")]
ARC = {40: "uske ander hai hi nahi"}
PEEPS = [34, 41, 43]
PUNCH = {5, 13, 20, 24, 38, 46}
METER = [(m(0.35), 6), (m(11.2), 11), (m(14.9), 18), (m(23.6), 26), (t0(34), 40), (t0(41), 52),
         (t0(43), 62), (m(40.55), 74), (t0(52), 88)]

FREEZES = [  # (start, end, still, suspect no, name, line, accent)
    (m(0.3), m(2.1), "assets/stills/f-0.3.jpg", 1, "The Bestfriend", "calmest person alive · threat level: 0", "#FDC5F4"),
    (m(40.5), m(42.0), "assets/stills/f-40.5.jpg", 2, "Aunty, passenger seat", "volume: 11 · patience: none", "#C0143C"),
]
HOOK = (t0(2), t1(4))
BOARD = (t0(7), t1(14))
RAIN = (t0(18), t0(26))
AUTO = (t0(26), t1(30))

covered = set()
for a, b in [HOOK, BOARD] + [(f[0], f[1]) for f in FREEZES]:
    for c in CAPS:
        if t0(c["i"]) >= a - 1e-3 and t1(c["i"]) <= b + 1e-3:
            covered.add(c["i"])
special = set(EMPH) | set(THOUGHT) | set(ARC) | {i for i, _ in NOTES}

els, js, aud = [], [], []
def clip(id_, start, end, track, cls, inner="", style=""):
    els.append(f'<div id="{id_}" class="clip {cls}" data-start="{start:.3f}" data-duration="{end - start:.3f}" '
               f'data-track-index="{track}" style="{style}">{inner}</div>')
_sfx = [0]
def sfx(name, t, dur, vol=0.4):
    _sfx[0] += 1
    aud.append(f'<audio id="sx{_sfx[0]}" data-start="{t:.3f}" data-duration="{dur:.3f}" data-track-index="{60 + _sfx[0] % 6}" '
               f'src="assets/sfx/{name}" data-volume="{vol}"></audio>')
def T(s): js.append(s)

def lockup(small, big):
    s = f'<span class="lk-s">{esc(small)}</span>' if small else ""
    return f'<div class="lk">{s}<span class="lk-c f-acc">{esc(big)}</span></div>'
def anim_lockup(sel, t):
    T(f'tl.fromTo("{sel} .lk-s",{{y:24,opacity:0}},{{y:0,opacity:1,duration:0.26,ease:"power3.out",immediateRender:false}},{t + 0.02:.3f});')
    T(f'tl.fromTo("{sel} .lk-c",{{opacity:0,scale:1.18,y:10}},{{opacity:1,scale:1,y:0,duration:0.34,ease:"back.out(2)",immediateRender:false}},{t + 0.1:.3f});')

def typed(id_, text):
    return "".join(f'<i class="ch">{esc(ch) if ch != " " else "&nbsp;"}</i>' for ch in text)
def anim_typed(sel, text, st, span):
    T(f'tl.set("{sel} .ch",{{opacity:0,maxWidth:"0em"}},{st:.3f});')
    for j in range(len(text)):
        T(f'tl.set("{sel} .ch:nth-child({j + 1})",{{opacity:1,maxWidth:"2em"}},{st + span * j / len(text):.3f});')
    sfx("keyboard-typing.mp3", st, span + 0.05, 0.28)

# ---------------------------------------------------------------- 1. cold open + rewind + cover
els.append('<div class="vwrap" id="cold-wrap"><video id="cold" data-start="0" data-duration="2.400" data-track-index="2" '
           'data-media-start="120.83" src="assets/clean.mp4" muted playsinline></video></div>')
aud.append('<audio id="vo-cold" data-start="0" data-duration="2.000" data-track-index="3" data-media-start="120.83" src="assets/clean.mp4" data-volume="1"></audio>')
clip("vhs", 0, 2.4, 20, "vhs", '<div class="scan"></div><div class="rec"><b></b>REC</div><div class="tc tw">SAT · 21:47</div>')
T('tl.fromTo("#vhs .rec b",{opacity:1},{opacity:0.15,duration:0.3,ease:"steps(1)",repeat:6,yoyo:true},0);')
clip("cold-lk", 0, 2.0, 21, "emph", lockup("agar aap itne ameer ho toh", "Creta mein kyu?"))
T('tl.fromTo("#cold-lk .lk-s",{y:20,opacity:0},{y:0,opacity:1,duration:0.25,ease:"power3.out"},0.05);')
T('tl.fromTo("#cold-lk .lk-c",{opacity:0,scale:1.25},{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"},0.92);')
clip("rew", 2.0, 2.4, 22, "rew", '<div class="bars"><i></i><i></i><i></i></div><div class="rew-ico f-disp">◀◀</div>')
T('tl.fromTo("#rew .bars i",{yPercent:-120},{yPercent:900,duration:0.2,stagger:0.05,ease:"none",repeat:1},2.0);')
T('tl.fromTo("#cold-wrap",{x:0,scale:1},{x:-22,scale:1.06,duration:0.4,ease:"power2.in"},2.0);')
sfx("rewind.wav", 2.0, 0.95, 0.5)
cover = ('<div class="rw tw">◀◀ REWIND · LAST SATURDAY</div>'
         '<div class="folder"><div class="tw fl-k">CASE FILE #01</div><div class="f-disp fl-t">The Kaleshi Aurat Files</div>'
         '<div class="tw fl-m">LOCATION: BANDRA, MUMBAI<br>WEATHER: ANDHI BAARISH<br>SUSPECTS: 3</div></div>'
         '<div class="stamp tw" id="conf">CONFIDENTIAL</div>')
clip("cover", 2.4, O, 30, "paper cover", cover)
T('tl.fromTo("#cover .folder",{y:60,opacity:0},{y:0,opacity:1,duration:0.3,ease:"expo.out"},2.42);')
T('tl.fromTo("#cover .rw",{opacity:0},{opacity:1,duration:0.15},2.42);')
T('tl.fromTo("#conf",{scale:2.4,opacity:0,rotation:-14},{scale:1,opacity:1,rotation:-8,duration:0.18,ease:"power4.in"},2.85);')
sfx("paper-flip.mp3", 2.4, 1.0, 0.35); sfx("slam.mp3", 3.02, 1.0, 0.4)

# ---------------------------------------------------------------- main face + voice
els.append(f'<div id="face-wrap"><video id="face" data-start="{O:.3f}" data-duration="{MAIN:.3f}" data-track-index="0" src="assets/clean.mp4" muted playsinline></video></div>')
aud.append(f'<audio id="vo" data-start="{O:.3f}" data-duration="{MAIN:.3f}" data-track-index="1" src="assets/clean.mp4" data-volume="1"></audio>')
clip("warm", O, O + MAIN, 4, "warm")

# subtitles
for c in CAPS:
    i = c["i"]
    if i in covered or i in special:
        continue
    clip(f"sub{i}", t0(i), t1(i), 5, "sub", f'<span>{esc(c["text"])}</span>')
    T(f'tl.fromTo("#sub{i} span",{{opacity:0,y:8}},{{opacity:1,y:0,duration:0.14,ease:"power2.out",immediateRender:false}},{t0(i) + 0.01:.3f});')
for i, (s, b) in EMPH.items():
    end = DUR if i == LAST else t1(i)
    clip(f"em{i}", t0(i), end, 6, "emph", lockup(s, b))
    anim_lockup(f"#em{i}", t0(i))
for i, (txt, side) in THOUGHT.items():
    clip(f"th{i}", t0(i), t1(i), 7, f"thought th-{side}", f'<div class="tape"></div><span class="tw">{esc(txt)}</span>')
    T(f'tl.fromTo("#th{i}",{{opacity:0,scale:0.6,rotation:8}},{{opacity:1,scale:1,rotation:3,duration:0.3,ease:"back.out(2.4)",immediateRender:false}},{t0(i) + 0.02:.3f});')
    sfx("pop.mp3", t0(i), 0.5, 0.3)
for k, (i, txt) in enumerate(NOTES):
    clip(f"nt{k}", t0(i), t1(i), 8, "note", f'<b class="tw">CASE NOTE</b><span class="tw">{typed(f"nt{k}", txt)}</span>')
    T(f'tl.fromTo("#nt{k}",{{opacity:0,y:-14}},{{opacity:1,y:0,duration:0.18,ease:"power2.out",immediateRender:false}},{t0(i):.3f});')
    anim_typed(f"#nt{k}", txt, t0(i) + 0.12, min(0.05 * len(txt), (t1(i) - t0(i)) * 0.75))
for i, txt in ARC.items():
    svg = (f'<svg viewBox="0 0 1080 520" width="1080" height="520"><defs><path id="arcp{i}" d="M150,470 Q540,40 930,470"/></defs>'
           f'<text class="f-acc"><textPath href="#arcp{i}" startOffset="50%" text-anchor="middle">{esc(txt)}</textPath></text></svg>')
    clip(f"arc{i}", t0(i), t1(i), 9, "arc", svg)
    T(f'tl.fromTo("#arc{i} svg",{{opacity:0,rotation:-6,transformOrigin:"50% 90%"}},{{opacity:1,rotation:0,duration:0.4,ease:"power3.out",immediateRender:false}},{t0(i) + 0.02:.3f});')

# ---------------------------------------------------------------- freeze-frame suspect cards
for k, (st, en, still, no, name, line, acc) in enumerate(FREEZES):
    inner = (f'<img src="{still}" alt=""><div class="tint"></div>'
             f'<div class="sus" style="border-left-color:{acc}"><div class="tw sus-k" style="color:{acc if no == 2 else "#5E202B"}">SUSPECT #{no}</div>'
             f'<div class="f-disp sus-n">{esc(name)}</div><div class="tw sus-l">{esc(line)}</div></div>')
    clip(f"fz{k}", st, en, 25, "freeze", inner)
    T(f'tl.fromTo("#fz{k} img",{{scale:1}},{{scale:1.04,duration:{en - st:.3f},ease:"none",immediateRender:false}},{st:.3f});')
    T(f'tl.set("#fz{k} .sus",{{x:-700}},{st:.3f});')
    T(f'tl.fromTo("#fz{k} .sus",{{x:-700,rotation:-8}},{{x:0,rotation:{-2 if k == 0 else 2},duration:0.38,ease:"expo.out",immediateRender:false}},{st + 0.08:.3f});')
    sfx("dundun.wav", st, 1.3, 0.55)

# ---------------------------------------------------------------- hook: tabloid front page
hs, he = HOOK
words = ["“No", "bullshit", "people", "I know”"]
wtimes = [m(2.12), m(2.55), m(3.0), m(3.3)]
head = "".join(f'<span class="hw">{esc(w)}</span> ' for w in words)
hook = ('<div class="mast f-disp">THE DAILY KALESH</div><div class="dl tw">SAT · VOL 01 · ₹0 · BANDRA EDITION</div>'
        f'<div class="hl f-disp">{head}</div><div class="rule2"></div>'
        '<div class="photo"><img src="assets/stills/f-1.6.jpg" alt=""><div class="cap2 tw">FIG 1. the reporter</div></div>'
        '<div class="col"><div class="tw col-t">…even when our life is in</div><div class="f-acc dg"><span class="hi"></span><em>danger.</em></div></div>')
clip("hook", hs, he, 30, "paper hook", hook)
for j, t in enumerate(wtimes):
    T(f'tl.fromTo("#hook .hw:nth-child({j + 1})",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.24,ease:"power3.out",immediateRender:false}},{t:.3f});')
T(f'tl.set(["#hook .photo","#hook .col-t","#hook .dg"],{{opacity:0}},{hs:.3f});')
T(f'tl.fromTo("#hook .photo",{{opacity:0,rotation:-6,scale:0.9}},{{opacity:1,rotation:-2,scale:1,duration:0.3,ease:"back.out(1.8)"}},{m(2.3):.3f});')
T(f'tl.fromTo("#hook .col-t",{{opacity:0}},{{opacity:1,duration:0.2}},{m(3.63):.3f});')
T(f'tl.fromTo("#hook .dg",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.25,ease:"power2.out"}},{m(4.43):.3f});')
T(f'tl.fromTo("#hook .hi",{{scaleX:0}},{{scaleX:1,duration:0.3,ease:"power2.inOut",immediateRender:false}},{m(4.6):.3f});')
sfx("paper-flip.mp3", hs, 1.0, 0.35); sfx("whoosh.mp3", m(4.6), 0.55, 0.25)

# ---------------------------------------------------------------- evidence board
bs, be = BOARD
board = ('<div class="cork"></div>'
         '<div class="tag tw"><b>CASE NOTE</b><span>' + typed("bd", "DATE: LAST SATURDAY") + '</span></div>'
         '<div class="map"><div class="map-l"></div><div class="tw map-t">BANDRA, MUMBAI</div><div class="mpin"></div></div>'
         '<svg class="string" width="1080" height="1920"><path d="M300,470 L800,520 L290,900" pathLength="1"/></svg>'
         '<div class="stamp tw" id="nf">ACHE MOMO:<br>NOT FOUND</div>')
clip("board", bs, be, 30, "board", board)
anim_typed("#board .tag", "DATE: LAST SATURDAY", bs + 0.08, 0.6)
T(f'tl.set(["#board .map","#board .mpin","#board .string","#nf"],{{opacity:0}},{bs:.3f});')
T(f'tl.fromTo("#board .map",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.8)"}},{t0(8):.3f});')
T(f'tl.fromTo("#board .mpin",{{opacity:0,y:-90}},{{opacity:1,y:0,duration:0.35,ease:"bounce.out"}},{t0(8) + 0.25:.3f});')
T(f'tl.fromTo("#board .string",{{opacity:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.6,ease:"power2.inOut"}},{t0(9) + 0.6:.3f});')
T(f'tl.fromTo("#nf",{{scale:2.4,opacity:0,rotation:-16}},{{scale:1,opacity:1,rotation:-9,duration:0.18,ease:"power4.in"}},{t0(14):.3f});')
sfx("pop.mp3", t0(8) + 0.25, 0.5, 0.3); sfx("slam.mp3", t0(14) + 0.16, 1.0, 0.45)
POLS = [("pa", 0.4, t0(8) + 0.45, "EXHIBIT A", "left:600px;top:330px;width:400px;height:540px;transform:rotate(5deg);"),
        ("pb", 148.4, t0(9) + 0.15, "EXHIBIT B: momo", "left:90px;top:760px;width:400px;height:540px;transform:rotate(-3deg);")]
for pid, med, ap, lab, pos in POLS:
    els.append(f'<div class="pol" id="{pid}" style="{pos}"><div class="pv"><video id="{pid}-v" data-start="{bs:.3f}" data-duration="{be - bs:.3f}" '
               f'data-track-index="{11 if pid == "pa" else 12}" data-media-start="{med}" src="assets/clean.mp4" muted playsinline></video></div><div class="tw pl">{lab}</div><div class="pin2"></div></div>')
    T(f'tl.set("#{pid}",{{opacity:0}},0);')
    T(f'tl.fromTo("#{pid}",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.8)",immediateRender:false}},{ap:.3f});')
    T(f'tl.set("#{pid}",{{opacity:0}},{be:.3f});')
    sfx("pop.mp3", ap, 0.5, 0.28)
BNOTE = {8: ("hum dono", "bandra mein"), 9: ("ache momo", "dhundhne"), 10: ("", "nikle the"),
         11: ("jo ki", "humari hi"), 12: ("", "galti hai"), 13: ("poore", "bombay mein"), 14: ("ache momo", "milte hi…")}
for i, (s, b) in BNOTE.items():
    s_html = f'<div class="tw bn-s">{esc(s)}</div>' if s else ""
    clip(f"bn{i}", t0(i), t1(i), 31, "bnote", f'{s_html}<div class="f-acc bn-b">{esc(b)}</div>')
    T(f'tl.fromTo("#bn{i} .bn-b",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.25,ease:"power2.out",immediateRender:false}},{t0(i) + 0.04:.3f});')

# ---------------------------------------------------------------- rain
rs, re_ = RAIN
streaks = "".join(f'<line x1="{(k * 137) % 1080}" y1="{(k * 251) % 1920}" x2="{(k * 137) % 1080 - 18}" y2="{(k * 251) % 1920 + 70}"/>' for k in range(46))
clip("rain", rs, re_, 26, "rain", f'<svg class="rl" width="1080" height="3840"><g>{streaks}</g><g transform="translate(0,1920)">{streaks}</g></svg>')
T(f'tl.fromTo("#rain .rl",{{y:-1920}},{{y:0,duration:0.9,ease:"none",repeat:{int((re_ - rs) / 0.9)}}},{rs:.3f});')
T(f'tl.fromTo("#rain",{{opacity:0}},{{opacity:1,duration:0.4}},{rs:.3f});')
sfx("rain.wav", rs, min(6.0, re_ - rs + 0.6), 0.3)

# ---------------------------------------------------------------- auto sticker
as_, ae = AUTO
auto = ('<svg class="auto-svg" viewBox="0 0 300 230" width="300" height="230">'
        '<path d="M40 70 Q60 18 150 14 Q240 18 262 70 L270 170 L30 170 Z" fill="#1E1A18"/>'
        '<path d="M22 100 Q24 76 52 72 L250 72 Q278 76 280 100 L284 178 L18 178 Z" fill="#F2C230" stroke="#1E1A18" stroke-width="7"/>'
        '<rect x="64" y="88" width="80" height="56" rx="8" fill="#9ED3E6" stroke="#1E1A18" stroke-width="5"/>'
        '<rect x="160" y="88" width="80" height="56" rx="8" fill="#9ED3E6" stroke="#1E1A18" stroke-width="5"/>'
        '<rect x="10" y="168" width="282" height="18" rx="9" fill="#2E6B3A" stroke="#1E1A18" stroke-width="5"/>'
        '<circle cx="70" cy="196" r="26" fill="#1E1A18"/><circle cx="70" cy="196" r="10" fill="#C9C2B8"/>'
        '<circle cx="232" cy="196" r="26" fill="#1E1A18"/><circle cx="232" cy="196" r="10" fill="#C9C2B8"/></svg>'
        '<div class="puffs"><i></i><i></i><i></i></div><div class="tw auto-t">EXHIBIT C</div>')
clip("auto", as_, ae, 27, "auto", auto)
T(f'tl.fromTo("#auto",{{opacity:0,scale:0.5,rotation:-10}},{{opacity:1,scale:1,rotation:4,duration:0.35,ease:"back.out(2.2)",immediateRender:false}},{as_ + 0.02:.3f});')
T(f'tl.fromTo("#auto .auto-svg",{{rotation:-3}},{{rotation:3,duration:0.08,ease:"none",repeat:13,yoyo:true,transformOrigin:"50% 90%",immediateRender:false}},{t0(27):.3f});')
T(f'tl.set("#auto .puffs i",{{opacity:0}},{as_:.3f});')
T(f'tl.fromTo("#auto .puffs i",{{opacity:0.9,scale:0.3,y:0,x:0}},{{opacity:0,scale:2.2,y:-150,x:-60,duration:0.9,stagger:0.22,ease:"power1.out",immediateRender:false}},{t0(30):.3f});')
sfx("pop.mp3", as_, 0.5, 0.3); sfx("sputter.wav", t0(27), 1.0, 0.35); sfx("sputter.wav", t0(30), 1.0, 0.4)

# ---------------------------------------------------------------- PEEP slams + camera shake
for k, i in enumerate(PEEPS):
    st, en = t0(i), t1(i)
    T(f'tl.set(["#pp{k} .pw1","#pp{k} .pw2"],{{opacity:0}},{st:.3f});')
    clip(f"pp{k}", st, en, 28, "peep", f'<div class="pw f-disp pw1">PEEP!</div><div class="pw f-disp pw2">PEEP!!</div>')
    T(f'tl.fromTo("#pp{k} .pw1",{{opacity:0,scale:2.2,rotation:-18}},{{opacity:1,scale:1,rotation:-10,duration:0.16,ease:"power4.in",immediateRender:false}},{st + 0.02:.3f});')
    T(f'tl.fromTo("#pp{k} .pw2",{{opacity:0,scale:2.2,rotation:16}},{{opacity:1,scale:1,rotation:8,duration:0.16,ease:"power4.in",immediateRender:false}},{st + 0.2:.3f});')
    T(f'tl.fromTo("#face-wrap",{{x:-14}},{{x:14,duration:0.05,ease:"none",repeat:5,yoyo:true,immediateRender:false}},{st + 0.02:.3f});')
    T(f'tl.set("#face-wrap",{{x:0}},{st + 0.33:.3f});')
    sfx("honk.wav", st + 0.02, 0.45, 0.4); sfx("honk.wav", st + 0.22, 0.45, 0.4)

# ---------------------------------------------------------------- end hold + part 2 band
clip("endhold", O + MAIN, DUR, 24, "freeze", '<img src="assets/stills/f-45.25.jpg" alt=""><div class="tint"></div>')
clip("band", m(44.5), DUR, 45, "band", '<span class="tw">CASE CONTINUES</span><b></b><span class="f-disp">Part 2 →</span>')
T(f'tl.fromTo("#band",{{yPercent:110}},{{yPercent:0,duration:0.35,ease:"expo.out",immediateRender:false}},{m(44.5):.3f});')
sfx("dundun.wav", O + MAIN, 1.3, 0.55)

# ---------------------------------------------------------------- Kalesh meter HUD
clip("meter", m(0.3), DUR, 50, "meter", '<span class="mt tw">KALESH METER</span><div class="mbar"><div class="mf"></div></div><span class="mp tw">6%</span>')
T(f'tl.fromTo("#meter",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.3,ease:"power3.out",immediateRender:false}},{m(0.3):.3f});')
prev = 0
for t, v in METER:
    T(f'tl.fromTo("#meter .mf",{{width:"{prev}%"}},{{width:"{v}%",duration:0.45,ease:"power3.out",immediateRender:false}},{t:.3f});')
    T(f'tl.set("#meter .mp",{{textContent:"{v}%"}},{t + 0.2:.3f});')
    T(f'tl.fromTo("#meter",{{scale:1.12}},{{scale:1,duration:0.3,ease:"back.out(3)",immediateRender:false}},{t:.3f});')
    prev = v
T(f'tl.set("#meter .mt",{{backgroundColor:"#C0143C"}},{m(40.55):.3f});')
T(f'tl.set("#meter",{{opacity:0}},{HOOK[0]:.3f});')
T(f'tl.set("#meter",{{opacity:1}},{HOOK[1]:.3f});')
T(f'tl.set("#meter .mf",{{backgroundImage:"linear-gradient(90deg,#E0609A,#C0143C)"}},{m(40.55):.3f});')

# ---------------------------------------------------------------- punch-ins
blocked = [HOOK, BOARD] + [(f[0], f[1]) for f in FREEZES]
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
<title>Kaleshi Aurat Files 01</title>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="{W}" data-height="{H}">
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
