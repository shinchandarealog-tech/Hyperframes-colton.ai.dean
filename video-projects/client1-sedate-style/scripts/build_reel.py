"""Client 1 reel in the Sedate Us style. Section geometry/motion = spec (measured on the reference);
only words and b-roll change. Reel frames at 30 fps; voice = raw with 3 pauses removed (see EDL)."""
import json, subprocess, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
N = 554
EDL = [(0.0, 3.80), (3.855, 7.46), (7.73, 16.37), (16.66, 19.08)]   # source seconds kept
CUT = {"S01": (0, 113), "S02": (114, 161), "S03": (162, 231), "S04": (232, 284), "S05": (285, 342), "S06": (343, 388),
       "S09": (389, 455), "S14": (456, 481), "S07": (482, 527), "S17": (528, 553)}
# b-roll: slot, first, last, kind, area, pan(fn of f relative to shot start r)  -- pans reuse the reference's measured shot moves
BROLL = [("S02a", 114, 137, "still", "full", "199.2+(-33.4-199.2)*circ((r-1)/52.7)"),
         ("S02b", 138, 161, "still", "full", "110.1+(-28.0-110.1)*p4out(r/112.7)"),
         ("S03a", 162, 181, "still", "full", "317.7+(-23.5-317.7)*circ((r+0.7)/29.1)"),
         ("S03b", 182, 206, "still", "full", "82.6*Math.exp(-r/9.6)+2.24*(28-r)-6.3"),
         ("S03c", 207, 231, "video", "full", None),
         ("S04t", 232, 284, "still", "top4", "116.2+(-16.1-116.2)*circ(r/29.0)"),
         ("S05a", 285, 304, "still", "top4", "137.1+(-11.8-137.1)*circ((Math.min(r,18)+1.9)/40.1)"),
         ("S05b", 305, 323, "still", "top4", "138.2+(-6.4-138.2)*circ((Math.min(r,17)-1)/35.8)"),
         ("S05c", 324, 342, "still", "top4", "129.5+(-4.7-129.5)*circ(r/62.6)"),
         ("S09a", 389, 410, "still", "full", "255.5*Math.exp(-r/5.9)+3.14*(20-r)-9.2"),
         ("S09b", 411, 432, "video", "full", None),
         ("S09c", 433, 455, "video", "full", None),
         ("S14", 456, 481, "still", "full", "180.8+(-4.4-180.8)*circ((r-0.8)/68.7)"),
         ("S07a", 482, 504, "still", "full", "244.0+(-22.3-244.0)*p4out((r-1.3)/59.2)"),
         ("S07b", 505, 527, "still", "full", "297.6*Math.exp(-r/15.6)-50")]
PICKS = json.load(open(os.path.join(HERE, "broll_picks.json")))

def lay(items):
    p = os.path.join(HERE, "_lay_in.json"); o = os.path.join(HERE, "_lay_out.json")
    json.dump(items, open(p, "w")); subprocess.run(["node", os.path.join(HERE, "layout.cjs"), p, os.path.join(ROOT, "assets/fonts"), o], check=True, capture_output=True)
    return json.load(open(o))
I, B = "Inter", "Bebas Neue"
def it(id, text, fam, wt, size, ls, anchor, x, base): return dict(id=id, text=text, fam=fam, wt=wt, size=size, ls=ls, anchor=anchor, x=x, base=base)

# ---------- pass 1: lines anchored on the reference ----------
P1 = [
 it("s02-w", "If you", I, 400, 72.9, -0.036, "left", 144, 1198),
 it("s03-l1", "YOU AND I HAVE BEEN", I, 400, 66.5, -0.05, "left", 78, 1207),
 it("s03-l2", "DOING", I, 600, 98.9, -0.06, "left", 100, 1290),
 it("s03-l3", "4 OR 5 YEARS", I, 600, 98.9, -0.066, "left", 114, 1380),
 it("s04-l1", "AND SO FAR THERE’S", I, 400, 76.8, -0.063, "left", 78, 731),
 it("s04-l2", "BEEN NO", I, 600, 101.7, -0.068, "left", 83, 812),
 it("s04-l3", "SPACES", I, 600, 101.7, -0.066, "left", 86, 896),
 it("s05-l", "For us to", I, 700, 85.88, -0.0675, "left", 161, 771),
 it("s05-c1", "Connect", I, 700, 58.53, -0.056, "left", 236, 853),
 it("s06-s", "It’s really", I, 600, 69.0, -0.054, "center", 540, 1094),
 it("s06-b", "FRUSTRATING", B, 400, 142.86, -0.05, "center", 540, 1202),
 it("s06-tn", "Your Name", I, 600, 32.67, -0.025, "left", 136, 1301), it("s06-ts", "Creator", I, 400, 24.78, -0.02, "left", 137, 1325),
 it("s09-l1", "BECAUSE LIKE WHERE", I, 400, 70.4, -0.08, "left", 83, 1138),
 it("s09-l2", "DO YOU GO TO", I, 700, 102.8, -0.068, "left", 87, 1226),
 it("s09-l3", "COLLABORATE", I, 700, 102.8, -0.068, "left", 85, 1313),
 it("s14-p", "WITH OTHER", I, 600, 61.13, -0.042, "left", 79, 1199),
 it("s14-l", "CREATORS", I, 500, 113.36, -0.04, "left", 73, 1303),
 it("s07-h", "And also when you have", I, 400, 61.25, -0.044, "left", 172, 1114),
 it("s07-c", "Questions", I, 500, 47.5, -0.025, "left", 150, 1196),
 it("s17-s", "like, who do you", I, 600, 81.0, -0.06, "center", 539, 1017),
 it("s17-b", "ASK?", B, 400, 168.25, -0.046, "center", 539, 1161),
]
L = lay(P1)
# ---------- pass 2: pieces placed after measured ink ----------
s02_pill_x = L["s02-w"]["ink"][2] + 11 + 36
s03_pill_x = L["s03-l2"]["ink"][2] + 22 + 36
c1_right = L["s05-c1"]["ink"][2] + 49; c2_left = c1_right + 15
L.update(lay([
 it("s02-pt", "THINK ABOUT IT", I, 600, 46.8, -0.03, "left", s02_pill_x, 1187),
 it("s03-pt", "THIS FOR", I, 500, 80.6, -0.023, "left", s03_pill_x, 1282),
 it("s05-c2", "With anyone", I, 700, 58.53, -0.056, "left", c2_left + 8 + 76 + 22, 853),
]))
G = {k: v["ink"] for k, v in L.items()}

def span(id, key, fam, wt, color, inner=None, shadow=None, style=""):
    c = L[key]; f = "inter" if fam == I else "bebas"; sh = f";text-shadow:{shadow}" if shadow else ""
    return (f'<span id="{id}" class="txt {f}" style="left:{c["left"]}px;top:{c["top"]}px;font-size:{c["size"]}px;font-weight:{wt};'
            f'letter-spacing:{c["ls"]}em;color:{color}{sh};{style}">{inner if inner is not None else ""}</span>')
def parts(pfx, words): return " ".join(f'<span id="{pfx}-{i}" class="pt">{w}</span>' for i, w in enumerate(words))
def rect(id, x0, y0, x1, y1, fill, r=0, extra=""):
    return f'<div id="{id}" class="abs" style="left:{x0:.1f}px;top:{y0:.1f}px;width:{x1-x0:.1f}px;height:{y1-y0:.1f}px;border-radius:{r}px;background:{fill};{extra}"></div>'
BADGE = open(os.path.join(HERE, "badge_path.txt")).read().strip()
def glyph(kind, d, col):
    if kind == "bang":
        w = 0.115 * d; h = 0.42 * d; dt = 0.115 * d; gap = 0.07 * d; top = (d - (h + gap + dt)) / 2; x = (d - w) / 2
        return f'<svg width="{d}" height="{d}" style="position:absolute;left:0;top:0"><rect x="{x}" y="{top}" width="{w}" height="{h}" rx="{w/2}" fill="{col}"/><rect x="{x}" y="{top+h+gap}" width="{w}" height="{dt}" rx="{w/2}" fill="{col}"/></svg>'
    if kind == "plus":
        a = 0.25 * d; sw = 0.11 * d; c = d / 2
        return f'<svg width="{d}" height="{d}" style="position:absolute;left:0;top:0"><path d="M{c-a} {c} H{c+a} M{c} {c-a} V{c+a}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/></svg>'
    if kind == "sparkle":
        c = d / 2; R = 0.275 * d; r = 0.06 * d
        pts = " ".join(f"{c+(R if i%2==0 else r)*math.cos(math.pi/4*i-math.pi/2):.2f},{c+(R if i%2==0 else r)*math.sin(math.pi/4*i-math.pi/2):.2f}" for i in range(8))
        return f'<svg width="{d}" height="{d}" style="position:absolute;left:0;top:0"><polygon points="{pts}" fill="{col}" stroke="{col}" stroke-width="{0.03*d:.2f}" stroke-linejoin="round"/></svg>'
def icon(id, x0, y0, d, fill, kind, col="#FFFFFF"):
    return f'<div id="{id}" class="abs" style="left:{x0}px;top:{y0}px;width:{d}px;height:{d}px;border-radius:50%;background:{fill}">{glyph(kind, d, col)}</div>'
def tag(pfx, name_key, sub_key, y0):
    n = L[name_key]; bx = n["ink"][2] + 4; w = bx + 34 + 20 - 117; by = y0 + 17
    return (f'<div id="{pfx}" class="abs layer">' + rect(pfx + "-box", 117, y0, 117 + w, y0 + 88, "rgba(0,0,0,.68)", 10)
            + span(pfx + "-n", name_key, I, 600, "#F7F3EF", "Your Name")
            + f'<svg class="abs" style="left:{bx:.1f}px;top:{by}px;width:34px;height:32px" viewBox="-1 -1 36 34" preserveAspectRatio="none"><path fill="#10B3E2" d="{BADGE}"/><path d="M10.5 16.4 L15 20.6 L23.5 11.8" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            + span(pfx + "-s", sub_key, I, 400, "#F3EAE5", "Creator") + "</div>")

JS = []; H = []
canon = lambda sel, v: JS.append(f'W("{sel}",{{D:29,t0:{v-4.6},dur:33.7,vis:{v}}});')
fade = lambda sel, v, op0=0.45, d=10: JS.append(f'FADE("{sel}",{v},{op0},{d});')
grp = lambda sel, a, b: JS.append(f'GRP("{sel}",{a},{b});')
GRAD = {"black": ("0,0,0", [(920, 0), (1080, .043), (1200, .118), (1280, .20), (1360, .31), (1440, .44), (1480, .50), (1520, .57), (1600, .71), (1680, .82), (1760, .90), (1840, .96), (1920, .98)]),
        "orange": ("164,77,37", [(1220, 0), (1300, .16), (1380, .31), (1460, .50), (1540, .57), (1620, .59), (1700, .60), (1780, .66), (1860, .73), (1920, .76)]),
        "green": ("23,33,17", [(1220, 0), (1300, .30), (1380, .60), (1460, .72), (1540, .75), (1620, .84), (1700, .88), (1780, .93), (1860, .96), (1920, .97)]),
        "brown": ("35,28,21", [(1220, 0), (1300, .32), (1380, .72), (1460, .81), (1540, .86), (1620, .92), (1700, .95), (1780, .97), (1860, .99), (1920, .99)]),
        "panel": ("166,92,54", [(540, 0), (600, .14), (720, .34), (900, .52), (948, .56)])}
def grad(name): rgb, st = GRAD[name]; return "linear-gradient(to bottom, " + ", ".join(f"rgba({rgb},{a}) {y}px" for y, a in st) + ")"
F = lambda f: round(f / 30, 6)

# ---------- media ----------
def broll(sh, area_rect, z):
    sid, f0, f1, kind, area, pan = sh; x0, y0, w, h = area_rect; pos = PICKS[sid]["pos"]
    L_, R_ = (330, 60) if pan else (0, 0); box = f"left:{x0-L_}px;top:{y0}px;width:{w+L_+R_}px;height:{h}px"
    if pan: JS.append(f'FN("#pan-{sid}","x",{f0},{f1+1},f=>{{const r=f-{f0};return {pan};}});')
    if kind == "still":
        return (f'<div id="clip-{sid}" class="clip abs" data-start="{F(f0)}" data-duration="{F(f1-f0+1)}" data-track-index="2" style="inset:0;z-index:{z}">'
                f'<div id="pan-{sid}" class="abs" style="{box}"><img src="assets/broll/{sid}.jpg" style="width:100%;height:100%;object-fit:cover;object-position:{pos}% 50%;display:block"></div></div>')
    return (f'<div id="pan-{sid}" class="abs" style="{box};z-index:{z}"><video id="v-{sid}" data-start="{F(f0)}" data-duration="{F(f1-f0+1)}" data-track-index="3" src="assets/broll/{sid}.mp4" muted playsinline '
            f'style="width:100%;height:100%;object-fit:cover;object-position:{pos}% 50%;display:block"></video></div>')
H.append(f'<video id="pl-S01" data-start="0" data-duration="{F(114)}" data-track-index="1" src="assets/plate_S01.mp4" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:1"></video>')
H.append(f'<video id="pl-aroll" data-start="{F(343)}" data-duration="{F(N-343)}" data-track-index="1" src="assets/plate_aroll.mp4" data-media-start="{F(343)}" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:1"></video>')
for sh in BROLL:
    if sh[4] == "full": H.append(broll(sh, (0, 0, 1080, 1920), 2))
# split A (S04-S05): white canvas, top panel b-roll + caption, bottom panel speaker A
sp = ['<div id="splitA" class="abs layer" style="z-index:3;background:#FFFFFF">',
      '<div class="abs" style="left:14px;top:14px;width:1052px;height:930px;border-radius:23.5px;overflow:hidden"><div class="abs" style="left:-14px;top:-14px;width:1080px;height:1920px">']
for sh in BROLL:
    if sh[4] == "top4": sp.append(broll(sh, (14, 14, 1052, 930), 2))
sp.append(f'<div class="abs layer" style="z-index:3;background:{grad("panel")}"></div><div id="cap45" class="abs layer" style="z-index:4">%CAP45%</div></div></div>')
sp.append(f'<div class="abs" style="left:14px;top:974px;width:1052px;height:930px;border-radius:21px;overflow:hidden"><div class="abs" style="left:-14px;top:-974px;width:1080px;height:1920px">'
          f'<video id="pl-split" data-start="{F(232)}" data-duration="{F(111)}" data-track-index="1" src="assets/plate_split.mp4" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px"></video></div></div></div>')
H.append("".join(sp)); grp("#splitA", 232, 342)
# gradients
for i, (n, a, b) in enumerate([("black", 0, 113), ("orange", 114, 231), ("black", 343, 388), ("brown", 389, 455), ("orange", 456, 481), ("green", 482, 527), ("black", 528, 553)]):
    H.append(f'<div id="gr{i}" class="abs layer" style="z-index:5;background:{grad(n)}"></div>'); grp(f"#gr{i}", a, b)

# ---------- S01 (hook, built earlier; same markup and timings) ----------
hook = json.load(open(os.path.join(HERE, "hook_fragment.json")))
H.append(hook["html"]); JS.append(hook["js"]); grp("#g-tag", 0, 113)

C = []  # unclipped captions
# ---------- S02: icon ! + words fade in place + pill vertical spring ----------
pi = G["s02-pt"]; px0, px1 = pi[0] - 36, pi[2] + 33
C.append('<div id="g02" class="abs layer">'
         + f'<div id="s02-icon" class="abs layer">{icon("s02-ic", 62, 1133, 74, "#9F4722", "bang", "#FDF8EE")}</div>'
         + span("s02-w", "s02-w", I, 400, "#FCFAF8", parts("s02-w", ["If", "you"]))
         + f'<div id="s02-pill" class="abs layer">{rect("s02-pr", px0, 1130, px1, 1204, "#9F4825", 37)}{span("s02-ptx", "s02-pt", I, 600, "#FEF7EC", "THINK ABOUT IT")}</div></div>')
grp("#g02", 114, 161)
JS.append('FN("#s02-icon","x",114,129,f=>f<116?-44.1:-44.1*(1-backOut((f-116)/12.3,1.5))); OP("#s02-icon",114,120,0.79,1);')
fade("#s02-w-0", 128, 0.5, 45); fade("#s02-w-1", 132, 0.3, 45)
JS.append('ON("#s02-pill",135); FN("#s02-pill","y",135,162,f=>16.9*Math.exp(-0.115*(f-135.5))*Math.cos(0.409*(f-135.5)+0.68));')
# ---------- S03: thin line / bold + pill / bold, word slide ----------
qi = G["s03-pt"]; qx0, qx1 = qi[0] - 36, qi[2] + 39
C.append('<div id="g03" class="abs layer">'
         + span("s03-l1", "s03-l1", I, 400, "#FCF9FB", parts("s03a", ["YOU", "AND", "I", "HAVE", "BEEN"]))
         + span("s03-l2", "s03-l2", I, 600, "#FCFBFA", parts("s03b", ["DOING"]))
         + f'<div id="s03-pill" class="abs layer">{rect("s03-pr", qx0, 1207, qx1, 1295, "#9E4723", 44)}{span("s03-ptx", "s03-pt", I, 500, "#FCFAF4", "THIS FOR")}</div>'
         + span("s03-l3", "s03-l3", I, 600, "#F4EEEB", parts("s03c", ["4", "OR", "5", "YEARS"])) + "</div>")
grp("#g03", 162, 231)
for i, v in enumerate([162, 164, 168, 172, 178]): canon(f"#s03a-{i}", v)
canon("#s03b-0", 185)
JS.append('ON("#s03-pill",194); FN("#s03-pill","x",194,206,f=>f<195.9?54.6:54.6*(1-backOut((f-195.9)/9.3,2.5)));')
for i, v in enumerate([207, 213, 218, 220]): canon(f"#s03c-{i}", v)
# ---------- S04/S05 captions inside the top panel ----------
cap = []
cap.append('<div id="g04" class="abs layer">' + span("s04-l1", "s04-l1", I, 400, "#FCF8F3", parts("s04a", ["AND", "SO", "FAR", "THERE’S"]))
           + span("s04-l2", "s04-l2", I, 600, "#FCF9F5", parts("s04b", ["BEEN", "NO"])) + span("s04-l3", "s04-l3", I, 600, "#FBF3ED", parts("s04c", ["SPACES"])) + "</div>")
grp("#g04", 232, 284)
for i, v in enumerate([232, 234, 237, 246]): canon(f"#s04a-{i}", v)
for i, v in enumerate([255, 262]): canon(f"#s04b-{i}", v)
canon("#s04c-0", 268)
c1 = G["s05-c1"]; c2 = G["s05-c2"]; c2r = c2[2] + 49
sh05 = "0 3px 12px rgba(0,0,0,.45)"
cap.append('<div id="g05" class="abs layer">'
           + f'<div id="s05-icon" class="abs layer" style="transform-origin:99px 744px">{icon("s05-ic", 51, 696, 96, "#A24A24", "bang", "#F0DCC4")}</div>'
           + span("s05-l", "s05-l", I, 700, "#FFFFFF", parts("s05w", ["For", "us", "to"]), shadow=sh05)
           + f'<div id="s05-chip1" class="abs layer" style="transform-origin:{(130+c1[2]+49)/2}px 836px">{rect("s05-c1r", 130, 791, c1[2]+49, 881, "#FFFFFF", 45)}{icon("s05-c1i", 138, 797, 76, "#A44A21", "plus", "#F0D9B8")}{span("s05-c1t", "s05-c1", I, 700, "#A04B28", "Connect")}</div>'
           + f'<div id="s05-chip2" class="abs layer" style="transform-origin:{(c1[2]+64+c2r)/2}px 836px">{rect("s05-c2r", c1[2]+64, 791, c2r, 881, "#FFFFFF", 45)}{icon("s05-c2i", c1[2]+72, 797, 76, "#A44A21", "plus", "#F0D9B8")}{span("s05-c2t", "s05-c2", I, 700, "#A04B28", parts("s05c2", ["With", "anyone"]))}</div>'
           + "</div>")
grp("#g05", 285, 342)
JS.append('FN("#s05-icon","x",285,301,f=>-43.3*(1-backOut((f-285)/12,2.2))); FN("#s05-icon","scale",285,288,f=>0.8+0.2*Math.min(1,(f-285)/3));')
for i, v in enumerate([285, 292, 297]): fade(f"#s05w-{i}", v, 0.2, 11)
wob = lambda s: {s+1: 0, s+2: 11.8, s+3: 0.2, s+4: 0.2, s+5: 0.1, s+6: 3.9, s+7: -0.1, s+8: -1.8, s+9: -3.1, s+10: -2.5, s+11: -1.5, s+12: -0.7, s+13: -0.1, s+14: 0.2, s+18: 0}
JS.append(f'ON("#s05-chip1",299); FN("#s05-chip1","scale",299,300,f=>f<300?0.76:1); TAB("#s05-chip1","y",{json.dumps({str(k): v for k, v in wob(299).items()})}); FADE("#s05-c1t",299,0.44,7);')
JS.append(f'ON("#s05-chip2",317); FN("#s05-chip2","scale",317,318,f=>f<318?0.76:1); TAB("#s05-chip2","y",{json.dumps({str(k): v for k, v in wob(317).items()})}); FADE("#s05c2-0",318,0.44,7); FADE("#s05c2-1",325,0.44,7);')
# ---------- S06: speaker B, "It's really / [bar] FRUSTRATING", name tag for speaker 2 ----------
b6 = G["s06-b"]; bx0, bx1 = b6[0] - 23, b6[2] + 23
C.append('<div id="g06" class="abs layer">' + span("s06-s", "s06-s", I, 600, "#FBF8F4", parts("s06w", ["It’s", "really"]))
         + rect("s06-bar", bx0, 1094, bx1, 1205, "#A14A24", 0, "transform-origin:0% 50%")
         + span("s06-B", "s06-b", B, 400, "#F6E7DF", "FRUSTRATING") + tag("s06-tag", "s06-tn", "s06-ts", 1255) + "</div>")
grp("#g06", 343, 388)
canon("#s06w-0", 345); canon("#s06w-1", 351)
fr = [116, 259, 390, 511, 616, 703, 774, 820, 850, 860]  # spec S06 right-edge table relative to x0, frames 0..9
JS.append(f'TAB("#s06-bar","scaleX",{json.dumps({str(359+i): round(e/(bx1-bx0)*(bx1-bx0)/860, 4) if False else round(min(1, e/860), 4) for i, e in enumerate(fr)})});')
JS.append('ON("#s06-bar",359);')
JS.append('W("#s06-B",{D:58.5,t0:363.3,dur:21.6,vis:363,op0:0.41,opCirc:true,opDur:21.6});')
JS.append('FN("#s06-tag","x",343,384.2,f=>-141.7*(1-circ((f-343)/41.2)));')
# ---------- S09: thin / bold / bold ----------
C.append('<div id="g09" class="abs layer">' + span("s09-l1", "s09-l1", I, 400, "#F8F6F2", parts("s09a", ["BECAUSE", "LIKE", "WHERE"]))
         + span("s09-l2", "s09-l2", I, 700, "#FBF8F5", parts("s09b", ["DO", "YOU", "GO", "TO"])) + span("s09-l3", "s09-l3", I, 700, "#FAF5F0", parts("s09c", ["COLLABORATE"])) + "</div>")
grp("#g09", 389, 455)
for i, v in enumerate([389, 398, 405]): canon(f"#s09a-{i}", v)
for i, v in enumerate([414, 418, 424, 427]): canon(f"#s09b-{i}", v)
canon("#s09c-0", 431)
# ---------- S14: pill from the left + big line ----------
p14 = G["s14-p"]
C.append('<div id="g14" class="abs layer">' + f'<div id="s14-pill" class="abs layer">{rect("s14-pr", 69, 1136, p14[2]+18, 1211, "#9F4924", 37.5)}{span("s14-pt", "s14-p", I, 600, "#FAF6EF", "WITH OTHER")}</div>'
         + span("s14-l", "s14-l", I, 500, "#F8EFE9", "CREATORS") + "</div>")
grp("#g14", 456, 481)
JS.append('ON("#s14-pill",456); TAB("#s14-pill","x",{"456":-38,"458":-38,"459":-10.9,"461":5.0,"463":5.7,"465":2.8,"467":0.4,"469":-0.6,"473":-0.6,"474":-0.2,"476":0});')
canon("#s14-l", 468)
# ---------- S07: sparkle icon + header (emphasis slide) + chip ----------
c7 = G["s07-c"]
C.append('<div id="g07" class="abs layer">' + f'<div id="s07-icon" class="abs layer" style="transform-origin:108.5px 1095px">{icon("s07-ic", 63, 1049, 92, "#C16E33", "sparkle")}</div>'
         + span("s07-h", "s07-h", I, 400, "#FFFFFF", '<span id="s07h-0" class="pt" style="font-weight:600">And</span> <span id="s07h-1" class="pt" style="font-weight:600">also</span> ' + parts("s07h2", ["when", "you", "have"]))
         + f'<div id="s07-chip" class="abs layer">{rect("s07-cr", 70, 1145, c7[2]+24, 1220, "#FCFCFB", 37.5)}{icon("s07-ci", 74, 1150.5, 64, "#C46E32", "plus")}{span("s07-ct", "s07-c", I, 500, "#B87040", "Questions")}</div></div>')
grp("#g07", 482, 527)
JS.append('FN("#s07-icon","x",482,496,f=>-33*(1-backOut((f-482)/12,1.5))); FN("#s07-icon","scale",482,496,f=>0.675+0.325*backOut((f-482)/12,1.5)); OP("#s07-icon",482,490,0.83,1);')
for sel, v in [("#s07h-0", 482), ("#s07h-1", 484), ("#s07h2-0", 490), ("#s07h2-1", 497), ("#s07h2-2", 502)]:
    JS.append(f'W("{sel}",{{D:53,t0:{v},dur:40,vis:{v},op0:0.38,opCirc:true,opDur:30}});')
JS.append('ON("#s07-chip",508,0.72); FN("#s07-chip","x",508,520,f=>-31.7*(1-backOut((f-508)/9,1.7))); OP("#s07-chip",508,525,0.72,1);')
# ---------- S17 end: small line + bar wipe + Bebas ----------
b17 = G["s17-b"]; ex0, ex1 = b17[0] - 44, b17[2] + 43
C.append('<div id="g17" class="abs layer">' + span("s17-s", "s17-s", I, 600, "#FBF8F3", parts("s17w", ["like,", "who", "do", "you"]))
         + rect("s17-bar", ex0, 1028, ex1, 1168, "#A24A24", 0, "transform-origin:0% 50%") + span("s17-B", "s17-b", B, 400, "#FAF5F0", "ASK?") + "</div>")
grp("#g17", 528, 553)
for i, v in enumerate([528, 530, 535, 540]): JS.append(f'W("#s17w-{i}",{{D:29,t0:{v-4.6},dur:33.7,vis:{v}}});')
# bar: the reference's measured S17 wipe (expo-like, 25 frames 1483->1507) mapped onto 528->552
s17 = [243, 248, 255, 263, 274, 288, 304, 328, 360, 406, 499, 592, 672, 720, 752, 773, 792, 805, 812, 824, 832, 838, 840, 844, 846]
JS.append(f'TAB("#s17-bar","scaleX",{json.dumps({str(528+i): round((e-232)/614, 4) for i, e in enumerate(s17)})});')
JS.append('W("#s17-B",{D:24.5,t0:539.4,dur:33.7,vis:543,op0:1});')

H.append('<div id="gfx" class="abs layer" style="z-index:10">' + "".join(C) + "</div>")
body = "\n".join(H).replace("%CAP45%", "".join(cap))
SFX = json.load(open(os.path.join(HERE, "sfx.json")))
aud = [f'<audio id="voice" data-start="0" data-duration="{F(N)}" data-track-index="20" src="assets/voice.wav" data-volume="1"></audio>',
       f'<audio id="bed" data-start="0" data-duration="{F(N)}" data-track-index="21" src="assets/bed.mp3" data-volume="0.124"></audio>']
for i, (src, t, d, v) in enumerate(SFX):
    aud.append(f'<audio id="sfx{i}" data-start="{t}" data-duration="{d}" data-track-index="{22+i%6}" src="{src}" data-volume="{v}"></audio>')
tpl = open(os.path.join(HERE, "template.html")).read().replace('data-duration="51.0333"', f'data-duration="{F(N)}"')
open(os.path.join(ROOT, "index.html"), "w").write(tpl.replace("%%BODY%%", body).replace("%%AUDIO%%", "\n".join(aud)).replace("%%JS%%", "\n    ".join(JS)))
print("written", len(JS), "js lines")
