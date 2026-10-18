"""Generates index.html for the client sample (v3: client-style, B-roll on words, hidden cuts).

Everything is scheduled in SOURCE seconds of raw-media/client-raw.mp4 as (segment, src_time)
pairs and mapped to output time through raw-media/edl.json, so re-cutting never breaks sync.
usage: python3 scripts/build.py  (run from the project folder)
"""
import json

EDL = json.load(open("raw-media/edl.json"))
SEGS = {s["label"]: s for s in EDL["segments"]}
AROLL = round(EDL["total"], 2)
END = round(AROLL + 5.3, 2)


def at(seg, src):
    """Output seconds for a source time inside a named segment (clamped to the segment)."""
    s = SEGS[seg]
    src = min(max(src, s["src_in"]), s["src_out"])
    return round(s["out_start"] + (src - s["src_in"]), 3)


CUTS = [round(s["out_start"], 3) for s in EDL["segments"][1:]]
TEASER_END = SEGS["hello"]["out_start"]

# ---- B-roll: (clip, (seg, src_start), (seg, src_end), clip_in_seconds) -------------------
BROLL = [
    ("man-celebrate", ("teaser1", 39.85), ("teaser1", 41.90), 1.2),   # "main daily ek reward hit kar raha hoon"
    ("cash-flip",     ("teaser1", 41.90), ("teaser1", 43.50), 0.6),   # "daily mera payout ja raha hai"
    ("dubai-tower",   ("teaser1", 45.98), ("teaser2", 61.20), 0.5),   # covers teaser cut -> "fully sponsored Dubai"
    ("stock-tablet",  ("hello", 3.55),    ("hello", 6.25),    1.0),   # "how you can hit your first reward"
    ("phone-scroll",  ("dubai", 53.86),   ("dubai", 56.60),   0.8),   # "puri industry ne videos bana rakhi hai"
    ("dubai-night",   ("dubai", 60.30),   ("proof", 73.50),   0.4),   # "fully sponsored Dubai trip" -> covers cut
    ("conference",    ("proof", 74.50),   ("proof", 76.85),   2.0),   # "3 log mere saath Forex Expo gaye"
    ("plane",         ("proof", 76.85),   ("proof", 77.42),   2.6),   # flights
    ("hotel",         ("proof", 77.42),   ("proof", 77.95),   3.0),   # hotels
    ("breakfast",     ("proof", 77.95),   ("proof", 78.65),   1.0),   # food
    ("trophy",        ("rule", 82.00),    ("rule", 85.75),    1.0),   # "one guy who will hit the highest payout"
    ("dubai-skyline", ("deadline", 96.60), ("deadline", 99.09), 0.5), # "usko fully sponsored Dubai trip milegi"
    ("pay-online",    ("offer", 107.40),  ("offer", 110.00),  0.5),   # "purchase 5x 9K+ Bolt accounts"
    ("pay-laptop",    ("offer", 110.00),  ("offer", 113.90),  0.5),   # "or 5x 25K+ Strike account"
    ("typing",        ("offer", 113.90),  ("offer", 116.05),  1.0),   # "open a ticket in Discord"
    ("stock-ui",      ("close", 173.00),  ("close", 175.60),  2.0),   # "let me show you how to hit your first reward"
]

# ---- full-screen graphic beats (cover cuts): (id, (seg,src), (seg,src)) -------------------
CARDS = {
    "fs-shark":  (("hello", 7.70),     ("giveaway", 52.60)),   # Shark Funded title -> GIVEAWAY (covers cut)
    "fs-30":     (("rule", 85.40),     ("deadline", 94.30)),   # 30 DAYS -> 12 OCT..12 NOV (covers cut)
    "fs-dc":     (("discord", 102.30), ("discord", 104.70)),   # JOIN DISCORD
    "fs-code":   (("offer", 106.30),   ("offer", 107.70)),     # USE CODE MSR
    "fs-111":    (("offer", 115.70),   ("close", 167.40)),     # $111 counter (covers cut)
}

# ---- word anchors for overlays on face / B-roll -----------------------------------------
A = dict(
    t_no=at("teaser1", 43.52), t_how=at("teaser1", 44.44),
    t_dubai=at("teaser2", 61.14),
    hello=at("hello", 0.10), first=at("hello", 6.26), shark=at("hello", 7.77),
    give=at("giveaway", 50.98),
    industry=at("dubai", 53.86), normal=at("dubai", 56.99), fully=at("dubai", 60.36), dubai=at("dubai", 61.14),
    lasttime=at("proof", 72.12), expo=at("proof", 75.53),
    flights=at("proof", 76.86), hotels=at("proof", 77.45), food=at("proof", 77.96), covered=at("proof", 78.67),
    highest=at("rule", 83.40), combined=at("rule", 85.49), days30=at("rule", 86.91),
    till=at("deadline", 91.97), nov=at("deadline", 92.61), dtrip=at("deadline", 97.83),
    discord=at("discord", 102.41), link=at("discord", 103.37),
    code=at("offer", 106.85), bolt=at("offer", 107.79), strike=at("offer", 109.93),
    ticket=at("offer", 114.15), usd111=at("offer", 116.43),
    maxdo=at("close", 166.84), ball=at("close", 168.69), court=at("close", 170.15), letme=at("close", 173.0),
)

# ---- captions in source time: (seg, src_start, src_end, text, highlight, colour) ---------
CAPS_SRC = [
    ("teaser1", 38.53, 39.85, "Everyone shows you", "", ""),
    ("teaser1", 39.85, 41.90, "“I hit a reward daily”", "reward", "hl"),
    ("teaser1", 41.90, 43.50, "“my payout goes out daily”", "payout", "hl"),
    ("teaser1", 43.50, 44.44, "but no one shows you", "", ""),
    ("teaser1", 44.44, 46.10, "how you’ll actually withdraw it", "withdraw", "hl"),
    ("teaser2", 59.40, 60.36, "Here I’m giving you", "", ""),
    ("teaser2", 60.36, 62.40, "a fully sponsored Dubai trip", "Dubai", "hl"),
    ("hello", 0.10, 0.90, "What’s up everyone", "", ""),
    ("hello", 0.90, 2.40, "hope you’re all doing good", "", ""),
    ("hello", 2.40, 4.20, "in this video", "", ""),
    ("hello", 4.20, 5.70, "how you can hit", "", ""),
    ("hello", 5.70, 7.70, "your first reward", "reward", "hl"),
    ("hello", 7.70, 9.75, "from Shark Funded accounts", "Shark", "hl"),
    ("giveaway", 50.50, 52.80, "+ a giveaway for you", "giveaway", "hl"),
    ("dubai", 52.86, 55.10, "You know the whole industry", "", ""),
    ("dubai", 55.10, 56.70, "made Shark Funded videos", "", ""),
    ("dubai", 56.70, 58.50, "this isn’t a normal giveaway", "normal", "hl"),
    ("dubai", 58.50, 60.30, "where I just give you an account", "", ""),
    ("dubai", 60.30, 62.40, "a fully sponsored Dubai trip", "Dubai", "hl"),
    ("proof", 72.00, 74.30, "When I did the Dubai giveaway", "", ""),
    ("proof", 74.30, 75.60, "3 people came with me", "3", "hl"),
    ("proof", 75.60, 76.86, "to Forex Expo", "Expo", "hl"),
    ("proof", 76.86, 78.50, "flights, hotels, food", "", ""),
    ("proof", 78.50, 79.54, "all covered", "covered", "hl"),
    ("rule", 79.60, 81.60, "I’m doing the same thing", "", ""),
    ("rule", 81.60, 83.35, "one trader with the", "", ""),
    ("rule", 83.35, 86.20, "highest total combined payout", "highest", "hl"),
    ("rule", 86.20, 87.80, "in the next 30 days", "30", "hl"),
    ("deadline", 90.80, 91.95, "You have time", "", ""),
    ("deadline", 91.95, 93.70, "till 12th November", "November", "hl"),
    ("deadline", 93.70, 96.60, "most payout in 30 days", "payout", "hl"),
    ("deadline", 96.60, 99.05, "wins a fully sponsored Dubai trip", "Dubai", "hl"),
    ("discord", 99.15, 101.60, "Plus — you get full support", "", ""),
    ("discord", 101.60, 103.20, "join the Discord", "Discord", "hl"),
    ("discord", 103.20, 104.70, "link in the description", "", ""),
    ("offer", 104.75, 106.30, "And if you use", "", ""),
    ("offer", 106.30, 107.60, "code MSR", "MSR", "hl"),
    ("offer", 107.60, 109.90, "and buy 5× Bolt 9K+", "Bolt", "hl"),
    ("offer", 109.90, 113.00, "or 5× Strike 25K+", "Strike", "hl"),
    ("offer", 113.00, 115.50, "open a ticket in Discord", "ticket", "hl"),
    ("offer", 115.50, 117.90, "claim your $111 USD", "$111", "hl"),
    ("close", 166.70, 168.60, "This is the max I can do", "max", "hl"),
    ("close", 168.60, 171.00, "the ball is in your court", "court", "hl"),
    ("close", 171.00, 173.00, "so let’s start the video", "", ""),
    ("close", 173.00, 176.40, "let me show you how to hit your first reward", "first", "hl"),
]
CAPS = [(at(g, a), at(g, b), t, h, c) for g, a, b, t, h, c in CAPS_SRC]

SFX = [  # (file, (seg, src) | output float, volume)
    ("pop.mp3", ("teaser1", 39.85), 0.30), ("pop.mp3", ("teaser1", 41.90), 0.30),
    ("slam.mp3", ("teaser1", 43.52), 0.36),
    ("whoosh.mp3", ("teaser1", 45.90), 0.26),
    ("riser.mp3", TEASER_END - 2.6, 0.18),
    ("boom.mp3", TEASER_END - 0.05, 0.30),
    ("whoosh.mp3", ("hello", 3.50), 0.24),
    ("whoosh.mp3", ("hello", 7.65), 0.28), ("click.wav", ("hello", 7.85), 0.32),
    ("sparkle.mp3", ("giveaway", 50.98), 0.30),
    ("swipe.mp3", ("dubai", 53.80), 0.24), ("click.wav", ("dubai", 56.99), 0.32),
    ("whoosh.mp3", ("dubai", 60.25), 0.28), ("slam.mp3", ("dubai", 61.14), 0.30),
    ("whoosh.mp3", ("proof", 74.45), 0.24),
    ("swipe.mp3", ("proof", 76.80), 0.20), ("swipe.mp3", ("proof", 77.40), 0.20), ("swipe.mp3", ("proof", 77.92), 0.20),
    ("pop.mp3", ("proof", 78.67), 0.32),
    ("whoosh.mp3", ("rule", 81.95), 0.24), ("zap.mp3", ("rule", 83.40), 0.24),
    ("whoosh.mp3", ("rule", 85.35), 0.26), ("click.wav", ("deadline", 92.61), 0.30),
    ("whoosh.mp3", ("deadline", 96.55), 0.24),
    ("notification.mp3", ("discord", 102.41), 0.36),
    ("whoosh.mp3", ("offer", 106.25), 0.26), ("click.wav", ("offer", 106.41), 0.32),
    ("swipe.mp3", ("offer", 107.65), 0.20), ("click.wav", ("offer", 109.93), 0.28),
    ("click.wav", ("offer", 114.15), 0.28), ("sparkle.mp3", ("offer", 116.43), 0.32),
    ("slam.mp3", ("close", 169.77), 0.30),
    ("bass-drop.mp3", AROLL + 0.05, 0.38),
]
SFX_DUR = {"pop.mp3": 0.72, "slam.mp3": 1.224, "whoosh.mp3": 0.574, "click.wav": 0.455,
           "sparkle.mp3": 2.037, "swipe.mp3": 1.056, "riser.mp3": 4.032, "zap.mp3": 0.966,
           "notification.mp3": 0.504, "bass-drop.mp3": 1.149, "boom.mp3": 2.784}

tags = []
broll_js = []
for i, (clip, a, b, cin) in enumerate(BROLL):
    s, e = at(*a), at(*b)
    gray = " gray" if e <= TEASER_END + 0.01 else ""
    tags.append(
        f'<div class="br{gray}" id="brw-{i}"><video id="br-{i}" src="assets/broll/{clip}.mp4" '
        f'data-start="{s:.3f}" data-duration="{e - s:.3f}" data-media-start="{cin:.2f}" '
        f'data-track-index="{20 + i}" muted playsinline></video></div>')
    broll_js.append([i, s, e])

for i, (f, t, v) in enumerate(SFX):
    t = at(*t) if isinstance(t, tuple) else t
    tags.append(f'<audio id="sfx-{i}" src="assets/sfx/{f}" data-start="{t:.3f}" '
                f'data-duration="{SFX_DUR[f]:.3f}" data-track-index="{60 + i}" data-volume="{v}"></audio>')

cards = {k: (at(*a), at(*b)) for k, (a, b) in CARDS.items()}

tpl = open("scripts/index.template.html", encoding="utf-8").read()
html = (tpl.replace("/*__DATA__*/",
                    "const A = " + json.dumps(A) + ";\n        const CAPS = " + json.dumps(CAPS, ensure_ascii=False)
                    + ";\n        const CUTS = " + json.dumps(CUTS) + ";\n        const BROLL = " + json.dumps(broll_js)
                    + ";\n        const CARDS = " + json.dumps(cards) + ";\n        const TEASER_END = " + str(TEASER_END) + ";")
        .replace("<!--__MEDIA__-->", "\n      ".join(tags))
        .replace("__AROLL__", f"{AROLL:.2f}")
        .replace("__END__", f"{END:.2f}")
        .replace("__ENDCARD_DUR__", f"{END - AROLL:.2f}")
        .replace("__TEASER_END__", f"{TEASER_END:.2f}")
        .replace("__MONEY_S__", f"{A['give'] - 0.1:.3f}")
        .replace("__MONEY_D__", f"{cards['fs-shark'][1] - (A['give'] - 0.1):.3f}"))
for k, (s, e) in cards.items():
    html = html.replace("{{" + k + ".s}}", f"{s:.3f}").replace("{{" + k + ".d}}", f"{e - s:.3f}")
open("index.html", "w", encoding="utf-8").write(html)
print("index.html written · aroll", AROLL, "· end", END, "· teaser ends", TEASER_END)
print("cards", cards)
