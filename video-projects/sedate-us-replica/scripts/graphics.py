"""Graphic groups S01-S18 from the spec. Coordinates = frame px; frames = ref frames.
Text: ink=(x0,y0,x1,y1) -> calibrated (size + tracking + position fitted to the ink box);
      fix=(size, x0_ink, baseline) -> size/tracking from spec, position from ink-left + baseline (spec gave no full box).
Anim mini-language (emitted as JS calls):
  ("canon", vis)                       word preset: x +29 -> 0 circ.out 33.7 f, starts vis-4.6, opacity 0.83 -> 1
  ("slide", D, t0, dur, vis[, op0])    measured per-word slide
  ("emph", D, t0, dur, vis, op0[, opdur])  emphasis slide + circ.out fade op0 -> 1
  ("fade", vis[, op0, dur])            fade in place (no move)
  ("on", vis)                          appears at vis, no motion
"""
I = "Inter"; B = "Bebas Neue"
W = "#FBF8F3"

def T(id, text, fam, wt, ls, color, anim, ink=None, fix=None, shadow=None, parts=None):
    """parts: [(span_id, word, anim)] -> one calibrated line, each word an inline-block with its own anim"""
    if parts: text = " ".join(w for _, w, _ in parts)
    return dict(k="text", id=id, text=text, fam=fam, wt=wt, ls=ls, color=color, anim=anim, ink=ink, fix=fix, shadow=shadow, parts=parts)

def unit(id, children, anim=None, origin=None):
    return dict(k="unit", id=id, children=children, anim=anim or [], origin=origin)

def rect(id, r, fill, radius=0, extra=""):
    return dict(k="rect", id=id, r=r, fill=fill, radius=radius, extra=extra)

def icon(id, r, fill, glyph, gcol="#FFFFFF"):
    return dict(k="icon", id=id, r=r, fill=fill, glyph=glyph, gcol=gcol)

def bar(id, key):
    return dict(k="bar", id=id, key=key)

def tile(id, cx, cy, rot):
    return dict(k="tile", id=id, cx=cx, cy=cy, rot=rot)

def dot(id, r, fill, anim):
    return dict(k="dot", id=id, r=r, fill=fill, anim=anim)

def G(id, show, hide, children, clip=None):
    return dict(id=id, show=show, hide=hide, children=children, clip=clip)

canon = lambda v: ("canon", v)

GROUPS = [
 # ---------------- S01 ----------------
 G("s01-tag", 0, 69, [unit("s01-tagu", [
     rect("s01-tagbox", (117, 1201, 436, 1289), "rgba(0,0,0,.68)", 10),
     T("s01-tagname", "Rachelle Robinett", I, 600, -0.03, "#F7F3EF", None, ink=(136, 1223, 378, 1247)),
     dict(k="badge", id="s01-badge", r=(382, 1218, 416, 1250)),
     T("s01-tagsub", "Herbalist", I, 400, -0.03, "#F3EAE5", None, ink=(137, 1253, 230, 1271)),
   ], anim=[("fn", "x", 0, 41.2, "-141.7*(1-circ(f/41.2))")])]),
 G("s01-p1", 2, 35, [
   T("w-I", "I", I, 400, -0.06, "#FAF9F4", ("slide", 24.4, -2.5, 33.0, 2), ink=(516, 956, 523, 1017)),
   T("w-think", "think", I, 400, -0.06, "#F9F8F8", ("slide", 28.4, -0.2, 33.7, 4), ink=(550, 956, 704, 1017)),
   T("w-right", "right", I, 500, -0.05, "#ECA572", ("slide", 29, 1.4, 33.7, 7), ink=(265, 990, 526, 1131)),
   T("w-now", "now", I, 500, -0.05, "#E8A472", ("slide", 40.4, 3.85, 32.7, 12), ink=(541, 1019, 794, 1102)),
   unit("pill-wellness", [rect("pill-wellness-r", (405.5, 1087.4, 676.5, 1152.6), "#A24A26", 32.6),
        T("pill-wellness-t", "wellness", I, 600, -0.03, "#FFF8ED", None, ink=(448, 1098, 635, 1139))],
        anim=[("on", 22, 0.86), ("fn", "y", 22, 36.2, "f<22.6?27.3:27.3*(1-backOut((f-22.6)/13.6,2.7))"), ("op", 22, 26, 0.86, 1)]),
 ]),
 G("s01-p2", 36, 69, [
   T("w-is", "is", I, 600, -0.05, "#FAF7F1", ("slide", 29, 14.6, 33.7, 19.2), ink=(362, 957, 412, 1017)),
   T("w-in", "in", I, 600, -0.05, "#FCF8F3", ("slide", 22.7, 29.1, 31, 33.7), ink=(426, 957, 478, 1017)),
   T("w-a", "a", I, 600, -0.05, "#FBF6EF", ("slide", 38, 33.8, 35.6, 36), fix=(80.04, 492, 1016)),
   T("w-really", "really", I, 600, -0.053, "#F6F4F5", ("emph", 60.6, 40.4, 31.1, 40, 0.36, 30.8), ink=(547, 958, 716, 1031)),
   bar("bar-s01", "S01"),
   T("w-INTERESTING", "INTERESTING", B, 400, -0.053, "#F9F5EF", ("slide", 60, 41.6, 31, 54, 1), ink=(259, 1038, 821, 1160)),
 ]),
 # ---------------- S02 (b-roll) ----------------
 G("s02", 70, 128, [
   unit("s02-icon", [icon("s02-icon-c", (62, 1133, 135, 1208), "#9F4722", "bang", "#FDF8EE")],
        anim=[("fn", "x", 70, 85, "f<72?-44.1:-44.1*(1-backOut((f-72)/12.3,1.5))"), ("op", 70, 76, 0.79, 1)]),
   T("s02-And", "And", I, 400, -0.05, "#FCFAF8", ("fade", 75, 0.5, 45), ink=(144, 1144, 262, 1198)),
   T("s02-sort", "sort", I, 400, -0.05, "#FCFAFA", ("fade", 79, 0.3, 45), ink=(278, 1149, 384, 1198)),
   T("s02-of", "of", I, 400, -0.05, "#FDF9F7", ("fade", 85, 0.4, 45), ink=(398, 1143, 454, 1198)),
   unit("s02-pill", [rect("s02-pill-r", (465, 1130, 959, 1204), "#9F4825", 37),
        T("s02-pill-t", "PRECARIOUS PLACE", I, 600, -0.02, "#FEF7EC", None, ink=(501, 1151, 926, 1187))],
        anim=[("on", 85), ("fn", "y", 85, 129, "16.9*Math.exp(-0.115*(f-85.5))*Math.cos(0.409*(f-85.5)+0.68)")]),
 ]),
 # ---------------- S03 ----------------
 G("s03", 129, 206, [
   T("s03-WHERE", "WHERE", I, 400, -0.05, "#FCF9FB", canon(129), ink=(78, 1159, 310, 1207)),
   T("s03-WERE", "WE’RE", I, 400, -0.05, "#FCF9FB", canon(136), ink=(325, 1159, 503, 1207)),
   T("s03-ON", "ON", I, 600, -0.06, "#FCFBFA", canon(149), ink=(100, 1216, 232, 1290)),
   T("s03-THE", "THE", I, 600, -0.06, "#FCFAF9", canon(155), ink=(248, 1217, 420, 1289)),
   unit("s03-pill", [rect("s03-pill-r", (442, 1207, 886, 1295), "#9E4723", 44),
        T("s03-pill-t", "VERGE OF", I, 500, -0.03, "#FCFAF4", None, ink=(478, 1221, 847, 1282))],
        anim=[("on", 159), ("fn", "x", 159, 171, "f<160.9?54.6:54.6*(1-backOut((f-160.9)/9.3,2.5))")]),
   T("s03-LOSING", "LOSING", I, 600, -0.06, "#FCF9F6", canon(179), ink=(114, 1306, 429, 1380)),
   T("s03-THE2", "THE", I, 600, -0.06, "#F9F7F3", canon(187), ink=(444, 1307, 613, 1379)),
   T("s03-PLOT", "PLOT", I, 600, -0.06, "#F4EEEB", canon(196), ink=(635, 1306, 850, 1380)),
 ]),
 # ---------------- S04 (split A) ----------------
 G("s04-cap", 207, 301, [
   T("s04-THE", "THE", I, 400, -0.05, "#FCF8F3", canon(213), ink=(78, 675, 208, 731)),
   T("s04-POINT", "POINT", I, 400, -0.05, "#FBF7F1", canon(218), ink=(224, 674, 421, 732)),
   T("s04-IS", "IS", I, 400, -0.05, "#FAF7F1", canon(223), ink=(435, 674, 487, 732)),
   T("s04-TO", "TO", I, 400, -0.05, "#FAF6F1", canon(231), ink=(498, 674, 589, 732)),
   T("s04-BE", "BE", I, 400, -0.05, "#FBF7F1", canon(242), ink=(604, 675, 682, 731)),
   T("s04-HEALTHY", "HEALTHY", I, 600, -0.05, "#FCF9F5", canon(255), ink=(83, 738, 490, 812)),
   T("s04-AND", "AND", I, 600, -0.05, "#FCF8F5", canon(264), ink=(503, 738, 700, 812)),
   T("s04-WELL", "WELL", I, 600, -0.05, "#FBF7F3", canon(271), ink=(715, 738, 960, 812)),
   T("s04-RIGHT", "RIGHT?", I, 600, -0.05, "#FBF3ED", canon(285), ink=(86, 820, 400, 896)),
 ], clip="top4"),
 G("s04-tag", 207, 301, [unit("s04-tagu", [
     rect("s04-tagbox", (87, 1497, 406, 1587), "rgba(0,0,0,.68)", 10),
     T("s04-tagname", "Radhi Devlukia", I, 600, -0.03, "#FCF8F5", None, ink=(106, 1519, 310, 1543)),
     dict(k="badge", id="s04-badge", r=(314, 1514, 346, 1546)),
     T("s04-tagsub", "Author", I, 400, -0.03, "#F3EAE5", None, fix=(25, 106, 1567)),
   ], anim=[("fn", "x", 207, 250, "f<208?-141.7:-141.7*(1-circ((f-208)/41.2))")])], clip="bot4"),
 # ---------------- S05 ----------------
 G("s05-cap", 302, 415, [
   unit("s05-icon", [icon("s05-icon-c", (51, 696, 147, 792), "#A24A24", "bang", "#F0DCC4")], origin=(99, 744),
        anim=[("fn", "x", 302, 318, "-43.3*(1-backOut((f-302)/12,2.2))"), ("fn", "scale", 302, 305, "0.8+0.2*Math.min(1,(f-302)/3)")]),
   T("s05-Not", "Not", I, 700, -0.05, "#FFFFFF", ("fade", 307, 0.2, 11), ink=(161, 707, 286, 771), shadow="0 3px 12px rgba(0,0,0,.45)"),
   T("s05-nec", None, I, 700, -0.0675, "#FFFFFF", None, fix=(85.88, "after:s05-Not", 771), shadow="0 3px 12px rgba(0,0,0,.45)",
     parts=[("s05-necessarily", "necessarily", ("fade", 317, 0.2, 11)), ("s05-to", "to", ("fade", 338, 0.2, 11))]),
   unit("s05-chip1", [rect("s05-chip1-r", (130, 791, 522, 881), "#FFFFFF", 45), icon("s05-chip1-i", (138, 797, 214, 873), "#A44A21", "plus", "#F0D9B8"),
        T("s05-chip1-t", "Consume", I, 700, -0.03, "#A04B28", ("fade", 348, 0.44, 7), ink=(236, 809, 473, 853))], origin=(326, 836),
        anim=[("on", 348), ("fn", "scale", 348, 349, "f<349?0.76:1"), ("tab", "y", {349: 0, 350: 11.8, 351: 0.2, 352: 0.2, 353: 0.1, 354: 3.9, 355: -0.1, 356: -1.8, 357: -3.1, 358: -2.5, 359: -1.5, 360: -0.7, 361: -0.1, 362: 0.2, 366: 0})]),
   unit("s05-chip2", [rect("s05-chip2-r", (537, 791, 1000, 881), "#FFFFFF", 45), icon("s05-chip2-i", (545, 797, 621, 873), "#A44A21", "plus", "#F0D9B8"),
        T("s05-chip2-t", None, I, 700, -0.03, "#A04B28", None, ink=(634, 810, 985, 854),
          parts=[("s05-chip2-t1", "Over", ("fade", 374, 0.44, 7)), ("s05-chip2-t2", "consume", ("fade", 380, 0.44, 7))])], origin=(768, 836),
        anim=[("on", 369), ("fn", "scale", 369, 370, "f<370?0.76:1"), ("tab", "y", {370: 0, 371: 11.8, 372: 0.2, 373: 0.2, 374: 0.1, 375: 3.9, 376: -0.1, 377: -1.8, 378: -3.1, 379: -2.5, 380: -1.5, 381: -0.7, 382: -0.1, 383: 0.2, 387: 0})]),
 ], clip="top4"),
 # ---------------- S06 ----------------
 G("s06-p1", 416, 458, [
   T("s06-There", "There", I, 600, -0.07, "#FBF8F4", canon(416), ink=(391, 1043, 556, 1094)),
   T("s06-is", "is", I, 600, -0.07, "#FBFAFA", canon(418), ink=(569, 1042, 611, 1094)),
   T("s06-an", "an", I, 600, -0.07, "#FBF9FB", canon(422), fix=(75, 622, 1094)),
   bar("bar-s06", "S06"),
   T("s06-HERB", "HERB", B, 400, -0.05, "#FCF9F5", ("emph", 58.5, 430.3, 21.6, 430, 0.41, 21.6), ink=(132, 1102, 328, 1202)),
   T("s06-FOR", "FOR", B, 400, -0.05, "#FBF6F0", ("emph", 54, 439.4, 19.5, 439, 0.41, 19.5), ink=(346, 1102, 484, 1202)),
   T("s06-EVERYTHING", "EVERYTHING", B, 400, -0.05, "#F6E7DF", ("emph", 64.2, 447.3, 11.8, 448, 0.41, 11.8), ink=(512, 1102, 961, 1202)),
 ]),
 G("s06-p2", 459, 484, [
   tile("s06-tileL", 335, 1025, -12),
   T("s06-So", "So", I, 600, -0.06, "#FBF5EE", ("slide", 35, 452.3, 34.4, 459, 0.9), ink=(464, 1005, 540, 1057)),
   T("s06-for", "for", I, 600, -0.06, "#F9F7F9", ("slide", 35, 454.3, 34.4, 461, 0.9), ink=(571, 1006, 648, 1057)),
   dot("s06-dot", (546, 1028, 562, 1043), "#E8DCC8", ("on", 464)),
   T("s06-anxiety", "anxiety", I, 500, -0.06, "#E1D1BB", ("slide", 29, 459.4, 33.7, 464, 0.9), ink=(303, 1040, 780, 1179)),
   tile("s06-tileR", 750, 1068, 12),
 ]),
 G("s06-p3", 488, 537, [
   T("s06-some", "some", I, 600, -0.063, "#FBF8F1", ("fade", 488, 0.5, 9), ink=(244, 1007, 412, 1048)),
   T("s06-of", "of", I, 600, -0.063, "#FAF7F1", ("fade", 492, 0.45, 9), ink=(423, 993, 482, 1048)),
   T("s06-the", "the", I, 600, -0.063, "#FBF8F2", ("fade", 496, 0.45, 9), ink=(493, 994, 591, 1048)),
   T("s06-best", "best", I, 600, -0.063, "#F9F8F9", ("fade", 500, 0.45, 9), ink=(604, 994, 734, 1048)),
   T("s06-are", "are", I, 600, -0.063, "#FCF7F0", ("fade", 505, 0.45, 9), ink=(746, 1007, 839, 1048)),
   T("s06-NERVE", "NERVE", B, 400, -0.053, "#FBF7F2", ("canon", 517), ink=(251, 1056, 562, 1180)),
   T("s06-VINES", "VINES", B, 400, -0.053, "#F4F1F3", ("slide", 21, 519.4, 33.7, 524, 0.92), ink=(581, 1055, 861, 1180)),
 ]),
 # ---------------- S07 ----------------
 G("s07", 538, 717, [
   unit("s07-icon", [icon("s07-icon-c", (63, 1049, 154, 1141), "#C16E33", "sparkle")], origin=(108.5, 1095),
        anim=[("fn", "x", 538, 552, "-33*(1-backOut((f-538)/12,1.5))"), ("fn", "scale", 538, 552, "0.675+0.325*backOut((f-538)/12,1.5)"), ("op", 538, 546, 0.83, 1)]),
   T("s07-Lavenda", "Lavenda", I, 600, -0.03, "#FFFFFF", ("emph", 53, 545, 40, 545, 0.38, 30), ink=(172, 1067, 391, 1114)),
   T("s07-is", "is", I, 400, -0.03, "#FFFFFF", ("emph", 53, 545, 40, 545, 0.38, 30), ink=(405, 1068, 439, 1113)),
   T("s07-a", "a", I, 400, -0.03, "#FFFFFF", ("emph", 45, 554, 40, 556, 0.38, 30), fix=(58, 451, 1113)),
   T("s07-pe", None, I, 400, -0.03, "#FFFFFF", None, ink=(492, 1067, 879, 1124),
     parts=[("s07-perfect", "perfect", ("emph", 35, 572, 40, 577, 0.38, 30)), ("s07-example", "example", ("emph", 52, 583, 40, 583, 0.38, 30))]),
 ] + [unit(f"s07-chip-{n}", [rect(f"s07-chip-{n}-r", r, "#FCFCFB", 37.5), icon(f"s07-chip-{n}-i", (r[0] + 4, r[1] + 5.5, r[0] + 68, r[1] + 69.5), "#C46E32", "plus"),
        T(f"s07-chip-{n}-t", txt, I, 500, -0.025, "#B87040", None, fix=(47.5, r[0] + 80, r[1] + 51))], origin=((r[0] + r[2]) / 2, (r[1] + r[3]) / 2),
        anim=[("on", v, 0.72), ("fn", "x", v, v + 12, "-31.7*(1-backOut((f-%d)/9,1.7))" % v), ("op", v, v + 17, 0.72, 1)])
      for n, txt, r, v in [("cham", "Chamomile", (70, 1145, 400, 1220), 594), ("val", "Valerian", (418, 1145, 690, 1220), 618), ("kava", "Kava", (713, 1145, 920, 1220), 650),
                           ("rose", "Rose", (106, 1231, 300, 1306), 686), ("pass", "Passion flower", (342, 1231, 723, 1306), 697)]]),
 # ---------------- S09 ----------------
 G("s09", 740, 825, [
   T("s09-WE", "WE", I, 400, -0.06, "#F8F6F2", canon(740), ink=(83, 1087, 178, 1138)),
   T("s09-CAN", "CAN", I, 400, -0.06, "#F9F4EF", canon(743), ink=(191, 1086, 318, 1139)),
   T("s09-USE", "USE", I, 400, -0.06, "#FAF7EC", canon(747), ink=(334, 1086, 448, 1139)),
   T("s09-THEM", "THEM", I, 400, -0.06, "#FBF4EC", canon(749), ink=(460, 1087, 629, 1138)),
   T("s09-RIGHT", "RIGHT", I, 700, -0.05, "#FBF8F5", canon(758), ink=(87, 1149, 364, 1226)),
   T("s09-AWAY", "AWAY", I, 700, -0.05, "#FBF8F4", canon(770), ink=(378, 1150, 645, 1225)),
   T("s09-TO", "TO", I, 700, -0.05, "#FBF8F3", canon(777), ink=(659, 1149, 785, 1226)),
   T("s09-FEEL", "FEEL", I, 700, -0.05, "#FCF8F3", canon(794), ink=(805, 1150, 1014, 1225)),
   T("s09-THE", "THE", I, 700, -0.05, "#FBF8F4", canon(798), ink=(85, 1238, 266, 1313)),
   T("s09-BENEFITS", "BENEFITS", I, 700, -0.05, "#FAF5F0", canon(807), ink=(289, 1237, 714, 1314)),
 ]),
 # ---------------- S10 (captions ride the top panel) ----------------
 G("s10-cap", 826, 948, [
   icon("s10-icon", (69, 775, 173, 878), "#C57137", "check"),
   T("s10-l1", None, I, 300, -0.045, "#F7F4F2", None, ink=(196, 753, 898, 785),
     parts=[("s10-BUT", "BUT", ("fade", 827, 0.4, 9)), ("s10-WE", "WE", ("fade", 829, 0.4, 9)), ("s10-CAN", "CAN", ("fade", 831, 0.4, 9)), ("s10-ALSO", "ALSO", ("fade", 834, 0.4, 9)), ("s10-USE", "USE", ("fade", 841, 0.4, 9)), ("s10-THEM", "THEM", ("fade", 848, 0.4, 9)), ("s10-OVER", "OVER", ("fade", 858, 0.4, 9)), ("s10-TIME", "TIME", ("fade", 863, 0.4, 9))]),
   T("s10-TO", "TO", I, 700, -0.05, "#FBFAF7", canon(880), ink=(196, 793, 293, 852)),
   T("s10-HELP", "HELP", I, 700, -0.05, "#FBFAF9", canon(885), ink=(308, 793, 485, 851)),
   T("s10-REHAB", "REHABILITATE", I, 700, -0.05, "#FCFAF8", canon(895), ink=(501, 793, 972, 851)),
   T("s10-THE", "THE", I, 350, -0.045, "#FCEEE3", canon(925), ink=(196, 861, 265, 892)),
   T("s10-NERVOUS", "NERVOUS", I, 350, -0.045, "#F7EAE4", canon(931), ink=(276, 861, 447, 892)),
   T("s10-SYSTEM", "SYSTEM", I, 350, -0.045, "#F5E4DC", ("slide", 21, 932.4, 33.7, 937), ink=(457, 861, 600, 892)),
 ], clip="top10"),
 # ---------------- S11 + S12 page 1 (line carries over the cut) ----------------
 G("s11-line", 949, 1047, [
   T("s11-AND", "AND", I, 400, -0.05, "#FAF7F1", canon(949), ink=(205, 982, 303, 1020)),
   T("s11-IT", "IT", I, 400, -0.05, "#F9F7EF", canon(954), ink=(315, 982, 351, 1020)),
   T("s11-HAS", "HAS", I, 400, -0.05, "#FAF6EF", canon(960), ink=(361, 981, 453, 1020)),
   T("s11-THE", "THE", I, 400, -0.05, "#FAF6EF", canon(966), ink=(462, 982, 560, 1020)),
   unit("s11-pill", [rect("s11-pill-r", (563, 968, 864, 1029), "#C77136", 30.5, extra="border:2px solid #FFF4D5"),
        T("s11-pill-t", "POWER TO", I, 500, -0.03, "#FFFAED", None, ink=(596, 980, 829, 1018))],
        anim=[("on", 975), ("tab", "x", dict(zip(range(975, 1012), [53.6, 36.2, 18.9, 1.6, -5.3, -9.9, -12.0, -11.8, -9.8, -6.7, -3.0, 0.5, 3.4, 5.5, 6.5, 6.8, 6.2, 5.1, 3.8, 2.3, 1.1, 0.2, -0.2, -0.5, -0.3, 0.0, -1.0, -0.5, 0, 0.2, 0.6, 0.7, 0.7, 0.5, 0.5, 0.2, 0])))]),
 ]),
 G("s12-p1", 1001, 1047, [
   T("s12-SEDATE", "SEDATE", B, 400, -0.059, "#FCFBF9", canon(1012), ink=(245, 1038, 668, 1198)),
   T("s12-US", "US", B, 400, -0.059, "#F8F6F8", ("slide", 25.5, 1027.0, 33.7, 1030), ink=(695, 1039, 842, 1198)),
 ]),
 G("s12-p2", 1048, 1107, [
   T("s12-HAS", "HAS", I, 400, -0.05, "#FBF8F2", canon(1050), ink=(256, 976, 377, 1027)),
   T("s12-THE", "THE", I, 400, -0.05, "#FBF7F2", canon(1055), ink=(388, 977, 504, 1026)),
   T("s12-POWER", "POWER", I, 400, -0.05, "#FBF9F8", canon(1063), ink=(519, 976, 732, 1027)),
   T("s12-TO", "TO", I, 400, -0.05, "#FBF7F1", canon(1072), ink=(743, 976, 824, 1027)),
   bar("bar-s12", "S12"),
   T("s12-WAKE", "WAKE", B, 400, -0.057, "#FBF6F1", canon(1085), ink=(201, 1033, 537, 1189)),
   T("s12-US2", "US", B, 400, -0.057, "#F9F2ED", ("slide", 26, 1085.6, 33.7, 1090), ink=(564, 1033, 710, 1191)),
   T("s12-UP", "UP", B, 400, -0.057, "#FAF3ED", ("slide", 20, 1093.2, 33.7, 1097, 0.85), ink=(738, 1032, 888, 1188)),
 ]),
 # ---------------- S13 ----------------
 G("s13", 1108, 1132, [
   T("s13-THAT", "THAT", I, 450, -0.05, "#FBF6F1", canon(1108), ink=(345, 915, 498, 964)),
   T("s13-IS", "IS", I, 450, -0.05, "#FBF5F0", canon(1111), ink=(512, 914, 560, 965)),
   T("s13-THE", "THE", I, 450, -0.05, "#F6EFE7", canon(1114), ink=(571, 915, 688, 965)),
   T("s13-MAGIC", "MAGIC", I, 500, -0.078, "#DCC9B4", ("slide", 21, 1114.6, 33.7, 1118, 0.85), ink=(309, 960, 773, 1077)),
 ]),
 # ---------------- S14 ----------------
 G("s14", 1133, 1188, [
   unit("s14-pill", [rect("s14-pill-r", (69, 1136, 381, 1211), "#9F4924", 37.5),
        T("s14-pill-t", "AND ALSO", I, 600, -0.03, "#FAF6EF", None, ink=(79, 1153, 363, 1199))],
        anim=[("on", 1133), ("tab", "x", {1133: -38.0, 1135: -38.0, 1136: -10.9, 1138: 5.0, 1140: 5.7, 1142: 2.8, 1144: 0.4, 1146: -0.6, 1150: -0.6, 1151: -0.2, 1153: 0})]),
   T("s14-THE", "THE", I, 500, -0.039, "#FBF8F5", canon(1146), ink=(73, 1220, 275, 1303)),
   T("s14-REALITY", "REALITY", I, 500, -0.039, "#FBF8F3", canon(1148), ink=(299, 1220, 712, 1303)),
   T("s14-OF", "OF", I, 500, -0.039, "#FAF5F0", canon(1163), ink=(732, 1218, 869, 1304)),
   T("s14-HERBALISM", "HERBALISM", I, 500, -0.03, "#F8EFE9", ("slide", 14, 1172, 16, 1174, 0.88), ink=(78, 1316, 662, 1402)),
 ]),
 # ---------------- S15 ----------------
 G("s15-p1", 1200, 1222, [
   icon("s15-c1", (339, 1075, 442, 1179), "#C57137", "check"),
   T("s15-Timeless", "Timeless", I, 400, -0.048, "#FAF6F5", ("emph", 42.9, 1200.6, 22.1, 1200, 0.56, 22.1), ink=(444, 1092, 723, 1154)),
 ]),
 G("s15-p2", 1223, 1252, [
   T("s15-ITS", "IT’S", I, 400, -0.05, "#FCF7EF", canon(1224), ink=(398, 1091, 487, 1138)),
   T("s15-NOTA", "NOT A", I, 400, -0.05, "#F9F5F2", ("slide", 28.5, 1223.6, 33.7, 1228), ink=(499, 1091, 663, 1138)),
   bar("bar-s15", "S15"),
   T("s15-TREND", "TREND", B, 400, -0.049, "#FBF7F1", ("slide", 23.5, 1233.4, 33.7, 1237, 1), ink=(365, 1151, 696, 1287)),
 ]),
 G("s15-p3", 1253, 1304, [
   icon("s15-c2", (105, 1075, 209, 1178), "#C57137", "check"),
   T("s15-It", "It", I, 600, -0.05, "#FCF9F1", canon(1253), ink=(227, 1072, 252, 1116)),
   T("s15-exists", "exists", I, 600, -0.05, "#FBF6ED", canon(1260), fix=(60, "after:s15-It", 1116)),
   T("s15-outside", "outside", I, 500, -0.058, "#FCF7EF", canon(1271), fix=(78.09, 226, 1178)),
   T("s15-of", "of", I, 500, -0.058, "#FBF4EE", canon(1281), ink=(467, 1119, 527, 1178)),
   T("s15-wellness", "wellness", I, 500, -0.058, "#F4F1F3", ("slide", 22, 1286.4, 33.7, 1290), ink=(543, 1120, 808, 1178)),
 ]),
 # ---------------- S16 ----------------
 G("s16", 1305, 1429, [
   icon("s16-star", (65, 971, 148, 1053), "#A04823", "star", "#FAF8F3"),
   T("s16-head", "The Natural Choice", I, 450, -0.03, "#F9F8F2", None, ink=(155, 988, 605, 1033)),
 ] + [unit(f"s16-chip-{n}", [rect(f"s16-chip-{n}-r", r, "#FCFCF9", 42.5), T(f"s16-chip-{n}-t", txt, I, 600, -0.03, col, None, ink=ink)],
        anim=[("on", v, 0.72), ("fn", "y", v, v + 30, "f<%g?%g:%g*(1-backOut((f-%g)/%g,3))" % (t0, D, D, t0, d)), ("op", v, v + 4, 0.72, 0.96), ("op", v + 4, v + 8, 0.96, 1)])
      for n, txt, r, ink, col, v, D, t0, d in [
        ("simple", "Simple", (101, 1057, 337, 1142), (144, 1076, 304, 1130), "#984B2E", 1305, 26.2, 1306.9, 11.0),
        ("eff", "Effective", (350, 1057, 646, 1142), (400, 1076, 598, 1121), "#984B30", 1340, 21.8, 1340.9, 10.6),
        ("str", "Straight from nature", (96, 1154, 617, 1238), (130, 1172, 588, 1228), "#954C32", 1395, 16, 1395.9, 9.9)]]),
 # ---------------- S17 ----------------
 G("s17-p0", 1430, 1438, [
   T("s17-Its", "It’s", I, 600, -0.07, "#FBF8F3", ("slide", 29, 1430 - 4.6 - 11.5, 33.7, 1430), ink=(376, 1090, 462, 1150)),
   T("s17-not", "not", I, 600, -0.07, "#FBF8F3", ("slide", 29, 1433 - 4.6 - 14.5, 33.7, 1433), ink=(478, 1096, 582, 1150)),
   T("s17-a", "a", I, 600, -0.0638, "#FBF8F3", ("slide", 29, 1436 - 4.6 - 18, 33.7, 1436), fix=(80.66, 597, 1150)),
 ]),
 G("s17-p1", 1439, 1472, [
   icon("s17-x", (152, 1072, 258, 1178), "#C37139", "x"),
   T("s17-Manufactured", "Manufactured", I, 400, -0.052, "#FBF8F4", ("slide", 28.1, 1437.1, 20.1, 1440), ink=(273, 1090, 718, 1154)),
   T("s17-thing", "thing", I, 400, -0.052, "#FAF7F6", ("emph", 49.7, 1446.5, 22.0, 1446, 0.39, 22.0), ink=(734, 1092, 895, 1169)),
 ]),
 G("s17-p2", 1473, 1507, [
   T("s17-and", "and", I, 600, -0.08, "#FBF8F3", ("slide", 29, 1451.6, 33.7, 1473), ink=(290, 958, 413, 1017)),
   T("s17-it", "it", I, 600, -0.08, "#FAF8F3", ("slide", 29, 1461.0, 33.7, 1473), ink=(429, 957, 464, 1017)),
   T("s17-can", "can", I, 600, -0.08, "#FBF8F4", ("slide", 29, 1468.4, 33.7, 1473), ink=(477, 973, 596, 1017)),
   T("s17-be", "be", I, 600, -0.08, "#F9F8FA", ("emph", 60, 1469.3, 31, 1473, 0.5, 31), ink=(612, 958, 694, 1018)),
   T("s17-so", "so", I, 600, -0.08, "#F8F2EE", ("emph", 63, 1478, 31, 1478, 0.34, 31), ink=(709, 973, 787, 1018)),
   bar("bar-s17", "S17"),
   T("s17-ACCESSIBLE", "ACCESSIBLE", B, 400, -0.048, "#FAF5F0", ("slide", 24.5, 1487.0, 33.7, 1491, 1), ink=(276, 1039, 803, 1161)),
 ]),
]
