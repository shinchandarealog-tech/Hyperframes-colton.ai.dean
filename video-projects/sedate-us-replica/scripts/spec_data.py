"""All measured numbers from 'SEDATE US - STYLE SPEC.md' (+ our own pixel measurements where noted).
Frames are reference frames at 30 fps (0-based). Boxes are frame px (x0,y0,x1,y1) of the INK unless noted."""

N_FRAMES = 1531

# ---------- palette ----------
RUST = "#A24A24"; TERRA = "#C77136"; WARM = "#FBF8F3"

# ---------- shots / layers ----------
# speaker plates: (name, first, last, region)  region: full | s04top | s04bot | s05bot | s10bot
SPEAKER = [
    ("S01", 0, 69, "full"), ("S04top", 207, 301, "s04top"), ("S04bot", 207, 301, "s04bot"), ("S05bot", 302, 415, "s04bot"),
    ("S06", 416, 537, "full"), ("S08", 718, 739, "full"), ("S10bot", 826, 948, "s10bot"), ("S11", 949, 1000, "full"),
    ("S12", 1001, 1107, "full"), ("S13", 1108, 1132, "full"), ("S15", 1189, 1304, "full"), ("S17", 1430, 1507, "full"),
    ("S18", 1508, 1530, "full"),
]
# speaker-gradient frame ranges (black). S04/S05 have none; S10 has it over the whole frame; S18 none.
GRAD_SPEAKER = [(0, 69), (416, 537), (718, 739), (826, 1132), (1189, 1304), (1430, 1507)]
GRAD_BROLL = [("orange", 70, 206), ("green", 538, 717), ("brown", 740, 825), ("orange", 1133, 1188), ("orange", 1305, 1429)]
GRADS = {
    "black": ("0,0,0", [(920, 0), (1080, .043), (1200, .118), (1280, .20), (1360, .31), (1440, .44), (1480, .50), (1520, .57), (1600, .71), (1680, .82), (1760, .90), (1840, .96), (1920, .98)]),
    "orange": ("164,77,37", [(1220, 0), (1300, .16), (1380, .31), (1460, .50), (1540, .57), (1620, .59), (1700, .60), (1780, .66), (1860, .73), (1920, .76)]),
    "green": ("23,33,17", [(1220, 0), (1300, .30), (1380, .60), (1460, .72), (1540, .75), (1620, .84), (1700, .88), (1780, .93), (1860, .96), (1920, .97)]),
    "brown": ("35,28,21", [(1220, 0), (1300, .32), (1380, .72), (1460, .81), (1540, .86), (1620, .92), (1700, .95), (1780, .97), (1860, .99), (1920, .99)]),
    "panel": ("166,92,54", [(540, 0), (600, .14), (720, .34), (900, .52), (948, .56)]),
}

# b-roll shots. kind: still|video. area: full | top4 (S05 top panel) | top10 (S10 top panel)
# pan: ("ease", from, to, t0, dur, freeze_from) | ("fn", python-expression-in-f) ; dx relative to the shot's last frame
BROLL = [
    ("S02a", 70, 97, "still", "full", ("circ.out", 199.2, -33.4, 71.0, 52.7, None), "hims&hers-style supplement store shelf"),
    ("S02b", 98, 128, "still", "full", ("power4.out", 110.1, -28.0, 97.9, 112.7, None), "woman drinking from a glass"),
    ("S03a", 129, 148, "still", "full", ("circ.out", 317.7, -23.5, 128.3, 29.1, None), "pharmacy shelves"),
    ("S03b", 149, 178, "still", "full", ("fn", "82.6*Math.exp(-(f-149)/9.6)+2.24*(177-f)-6.3"), "supplement shelf"),
    ("S03c", 179, 206, "video", "full", ("fn", "-15+15*(f-179)/27"), "gloved hands with red softgels"),
    ("S05a", 302, 317, "still", "top4", ("circ.out", 116.2, -16.1, 302.0, 29.0, None), "hand holding 2 pills"),
    ("S05b", 318, 341, "still", "top4", ("circ.out", 137.1, -11.8, 316.1, 40.1, 334), "hand holding a supplement bottle"),
    ("S05c", 342, 368, "still", "top4", ("circ.out", 138.2, -6.4, 343.0, 35.8, 362), "pills poured into a hand"),
    ("S05d", 369, 415, "still", "top4", ("circ.out", 129.5, -4.7, 369.0, 62.6, 397), "handful of capsules"),
    ("S07a", 538, 563, "still", "full", ("power4.out", 244.0, -22.3, 539.3, 59.2, None), "lavender field"),
    ("S07b", 564, 593, "still", "full", ("fn", "297.6*Math.exp(-(f-564)/15.6)-50"), "lavender close-up"),
    ("S07c", 594, 617, "still", "full", ("sine.out", 180.0, None, 592.2, 24.7, None), "chamomile flowers"),
    ("S07d", 618, 647, "still", "full", ("expo.out", 179.7, -16.8, 618.2, 75.8, None), "valerian flowers"),
    ("S07e", 648, 675, "still", "full", ("expo.out", 85.8, None, 647.5, 63.6, None), "kava leaves"),
    ("S07f", 676, 692, "still", "full", ("sine.out", 309.0, None, 665.6, 27.8, None), "rose bush"),
    ("S07g", 693, 717, "still", "full", ("expo.out", 31.4, None, 693.1, 56.4, None), "passionflower"),
    ("S09a", 740, 761, "still", "full", ("fn", "255.5*Math.exp(-(f-740)/5.9)+3.14*(760-f)-9.2"), "open bags of dried herbs"),
    ("S09b", 762, 784, "video", "full", None, "woman at an herb counter"),
    ("S09c", 785, 825, "video", "full", ("zoom", 1.12, 1.0), "two women in an herb shop"),
    ("S10a", 826, 854, "still", "top10", ("circ.out", 124.5, -22.7, 826.0, 60.0, None), "glass jars of chamomile / lavender"),
    ("S10b", 855, 882, "still", "top10", ("circ.out", 124.2, -35.9, 855.0, 72.7, None), "herb-jar shelf"),
    ("S10c", 883, 904, "video", "top10", None, "tea cup with herbs"),
    ("S10d", 905, 948, "video", "top10", None, "woman drinking tea"),
    ("S14", 1133, 1188, "still", "full", ("circ.out", 180.8, -4.4, 1133.8, 68.7, None), "bowls of dried herbs and petals, hand"),
    ("S16a", 1305, 1330, "video", "full", None, "hands with dried rose petals in a bowl"),
    ("S16b", 1331, 1364, "video", "full", None, "hand grinding in a stone mortar"),
    ("S16c", 1365, 1401, "still", "full", ("expo.out", 179.2, None, 1365.1, 112.2, None), "woman with a basket in a field"),
    ("S16d", 1402, 1429, "still", "full", ("circ.out", 138.0, -8.0, 1394.1, 49.3, None), "woman in a hat in a field"),
]

# split layouts
SPLIT_A = dict(frames=(207, 415), top=(14, 14, 1066, 944, 23.5), bot=(14, 974, 1066, 1904, 21))
SPLIT_B = dict(frames=(826, 948), top=(21, 14, 1059, 948, 19), bot=(21, 962, 1059, 2062, 17.5))
# S10 entrance, measured column profiles (ref frames 826..849): top panel bottom edge, bottom panel top edge, bottom content scale
S10_TOP_BOTTOM_EDGE = [444, 497, 546, 588, 626, 662, 694, 725, 752, 778, 802, 824, 842, 860, 876, 892, 904, 914, 924, 932, 937, 944, 946, 950]
S10_BOT_TOP_EDGE = [575, 615, 652, 685, 715, 743, 768, 791, 813, 832, 850, 866, 881, 895, 907, 918, 926, 936, 943, 949, 954, 957, 960, 962]
S10_BOT_SCALE = {826: 1.367, 829: 1.270, 832: 1.207, 835: 1.138, 838: 1.090, 841: 1.065, 844: 1.060, 847: 1.038, 850: 1.0}

# bar wipes: right edge per frame (S01 + S12/S15/S17 measured on ref pixels by us; S06 from spec, first frames confirmed)
BARS = {
    "S01": dict(rect=(232, 1028, 846, 1168), fill="#A24B26", table={45: 232, 46: 242, 47: 248, 48: 254, 49: 263, 50: 274, 51: 285, 52: 304, 53: 326, 54: 360, 55: 408, 56: 482, 57: 592, 58: 672, 59: 720, 60: 752, 61: 772, 62: 792, 63: 804, 64: 816, 65: 824, 66: 830, 67: 836, 68: 840, 69: 844, 70: 846}),
    "S06": dict(rect=(110, 1094, 970, 1205), fill="#A14A24", table={425: 110, 426: 226, 427: 369, 428: 500, 429: 621, 430: 726, 431: 813, 432: 884, 433: 930, 434: 960, 435: 970}),
    "S12": dict(rect=(164, 1025, 922, 1200), fill="#C77136", table={1077: 164, 1078: 168, 1079: 172, 1080: 175, 1081: 179, 1082: 187, 1083: 196, 1084: 208, 1085: 222, 1086: 240, 1087: 264, 1088: 296, 1089: 342, 1090: 418, 1091: 540, 1092: 664, 1093: 736, 1094: 784, 1095: 816, 1096: 840, 1097: 859, 1098: 874, 1099: 885, 1100: 894, 1101: 901, 1102: 906, 1103: 910, 1104: 914, 1105: 916, 1106: 917, 1107: 918}),
    "S15": dict(rect=(350, 1142, 705, 1294), fill="#C77136", table={1236: 350, 1237: 366, 1238: 372, 1239: 380, 1240: 392, 1241: 408, 1242: 430, 1243: 464, 1244: 528, 1245: 600, 1246: 634, 1247: 656, 1248: 672, 1249: 682, 1250: 692, 1251: 700, 1252: 704}),
    "S17": dict(rect=(232, 1028, 846, 1168), fill="#A24A24", table={1482: 232, 1483: 243, 1484: 248, 1485: 255, 1486: 263, 1487: 274, 1488: 288, 1489: 304, 1490: 328, 1491: 360, 1492: 406, 1493: 499, 1494: 592, 1495: 672, 1496: 720, 1497: 752, 1498: 773, 1499: 792, 1500: 805, 1501: 812, 1502: 824, 1503: 832, 1504: 838, 1505: 840, 1506: 844, 1507: 846}),
}
