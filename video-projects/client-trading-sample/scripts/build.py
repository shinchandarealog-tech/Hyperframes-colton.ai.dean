"""Generates index.html for the client sample.

All timings are OUTPUT seconds on the edited A-roll (assets/aroll.mp4, 80.7s).
Word anchors come from raw-media/final-tx/transcript.json (English parts) and the
large-v3 Hindi pass mapped through raw-media/edl.json (Hinglish parts).
usage: python3 scripts/build.py  (run from the project folder)
"""
import json

AROLL = 80.70
END = 86.0                       # end card holds ~5.3s
CUTS = [7.60, 8.53, 15.80, 18.16, 27.77, 35.39, 43.65, 52.08, 57.72, 70.93]

# Beat anchors (output seconds)
T = dict(
    daily=2.30, payout=3.60, butno=4.62, how=6.05,
    hello=7.62, first=11.78, shark=14.30,
    give=15.95,
    industry=19.15, normal=22.65, fully=26.00, dubai=26.55,
    proof=27.95, flights=32.72, hotels=33.12, food=33.74, covered=34.40,
    same=36.70, highest=39.60, combined=41.45, days30=43.05,
    till=45.12, nov=46.15, most=47.40, trip2=49.00,
    support=52.40, discord=55.55, link=56.50,
    code=59.40, bolt=60.60, strike=63.40, ticket=67.25, claim=68.65, usd111=69.55,
    maxdo=71.65, ball=73.40, court=74.35, letme=77.85,
)

# Captions: (start, end, text, highlight-word, colour-class)
CAPS = [
    (0.10, 1.25, "Everyone shows you", "", ""),
    (1.25, 3.55, "“I hit a reward daily”", "reward", "mint"),
    (3.55, 4.60, "“my payout goes out daily”", "payout", "mint"),
    (4.60, 6.00, "but no one shows you", "", ""),
    (6.00, 7.55, "how you’ll actually withdraw it", "withdraw", "mint"),
    (7.62, 8.50, "What’s up everyone", "", ""),
    (8.55, 10.20, "in this video", "", ""),
    (10.20, 11.75, "how you can hit", "", ""),
    (11.75, 14.25, "your first reward", "reward", "mint"),
    (14.25, 15.78, "from Shark Funded accounts", "Shark", "ink"),
    (15.82, 18.12, "+ a giveaway for you", "giveaway", "gold"),
    (18.18, 20.40, "You know the whole industry", "", ""),
    (20.40, 22.60, "made Shark Funded videos", "", ""),
    (22.60, 24.40, "this isn’t a normal giveaway", "normal", "ink"),
    (24.40, 25.95, "where I just give you an account", "", ""),
    (25.95, 27.72, "a fully sponsored Dubai trip", "Dubai", "gold"),
    (27.80, 29.90, "When I did the Dubai giveaway", "", ""),
    (29.90, 31.40, "3 people came with me", "3", "gold"),
    (31.40, 32.70, "to Forex Expo", "Expo", "gold"),
    (32.70, 34.35, "flights, hotels, food", "", ""),
    (34.35, 35.75, "all covered", "covered", "mint"),
    (35.80, 37.80, "I’m doing the same thing", "", ""),
    (37.80, 39.55, "one trader with the", "", ""),
    (39.55, 42.40, "highest total combined payout", "highest", "gold"),
    (42.40, 43.62, "in the next 30 days", "30", "mint"),
    (43.80, 45.10, "You have time", "", ""),
    (45.10, 46.85, "till 12th November", "November", "gold"),
    (46.85, 49.00, "most payout in 30 days", "payout", "mint"),
    (49.00, 52.02, "wins a fully sponsored Dubai trip", "Dubai", "gold"),
    (52.35, 54.80, "Plus — you get full support", "", ""),
    (54.80, 56.40, "join the Discord", "Discord", "violet"),
    (56.40, 57.68, "link in the description", "", ""),
    (57.85, 59.40, "And if you use", "", ""),
    (59.40, 60.55, "code MSR", "MSR", "violet"),
    (60.55, 63.35, "and buy 5× Bolt 9K+", "Bolt", "ink"),
    (63.35, 66.35, "or 5× Strike 25K+", "Strike", "ink"),
    (66.35, 68.60, "open a ticket in Discord", "ticket", "violet"),
    (68.60, 70.88, "claim your $111 USD", "$111", "mint"),
    (70.95, 72.85, "This is the max I can do", "max", "ink"),
    (72.85, 75.80, "the ball is in your court", "court", "gold"),
    (75.80, 77.80, "so let’s start the video", "", ""),
    (77.80, 80.60, "let me show you how to hit your first reward", "first", "mint"),
]

SFX = [  # (file, start, volume)
    ("pop.mp3", 1.30, 0.32), ("pop.mp3", 2.35, 0.32), ("pop.mp3", 3.60, 0.32),
    ("slam.mp3", 4.62, 0.38),
    ("whoosh.mp3", 7.55, 0.30), ("click.wav", 7.75, 0.35),
    ("whoosh.mp3", 11.70, 0.30),
    ("sparkle.mp3", 15.90, 0.32),
    ("swipe.mp3", 19.10, 0.26), ("click.wav", 22.70, 0.35),
    ("riser.mp3", 24.00, 0.22), ("slam.mp3", 26.00, 0.40),
    ("whoosh.mp3", 27.85, 0.28),
    ("click.wav", 32.72, 0.30), ("click.wav", 33.12, 0.30), ("click.wav", 33.74, 0.30),
    ("pop.mp3", 34.40, 0.34),
    ("swipe.mp3", 36.65, 0.26), ("zap.mp3", 39.60, 0.26),
    ("whoosh.mp3", 43.75, 0.28), ("click.wav", 46.15, 0.32),
    ("sparkle.mp3", 49.00, 0.30),
    ("notification.mp3", 55.55, 0.38),
    ("whoosh.mp3", 57.80, 0.28), ("click.wav", 59.40, 0.34), ("click.wav", 60.60, 0.30),
    ("click.wav", 63.40, 0.30), ("click.wav", 67.25, 0.30), ("sparkle.mp3", 69.55, 0.34),
    ("slam.mp3", 73.40, 0.34),
    ("whoosh.mp3", 77.85, 0.26),
    ("bass-drop.mp3", 80.75, 0.40),
]

sfx_dur = {"pop.mp3": 0.72, "slam.mp3": 1.224, "whoosh.mp3": 0.574, "click.wav": 0.455,
           "sparkle.mp3": 2.037, "swipe.mp3": 1.056, "riser.mp3": 4.032, "zap.mp3": 0.966,
           "notification.mp3": 0.504, "bass-drop.mp3": 1.149}

audio_tags = []
for i, (f, s, v) in enumerate(SFX):
    audio_tags.append(
        f'<audio id="sfx-{i}" src="assets/sfx/{f}" data-start="{s:.2f}" '
        f'data-duration="{sfx_dur[f]:.3f}" data-track-index="{40 + i}" data-volume="{v}"></audio>')

tpl = open("scripts/index.template.html", encoding="utf-8").read()
html = (tpl.replace("/*__T__*/", "const T = " + json.dumps(T) + ";")
           .replace("/*__CAPS__*/", "const CAPS = " + json.dumps(CAPS, ensure_ascii=False) + ";")
           .replace("/*__CUTS__*/", "const CUTS = " + json.dumps(CUTS) + ";")
           .replace("<!--__SFX__-->", "\n    ".join(audio_tags))
           .replace("__AROLL__", f"{AROLL:.2f}")
           .replace("__END__", f"{END:.2f}")
           .replace("__ENDCARD_DUR__", f"{END - AROLL:.2f}"))
for k, v in T.items():
    html = html.replace("{{" + k + "}}", f"{v:.2f}")
open("index.html", "w", encoding="utf-8").write(html)
print("index.html written")
