"""Edit decision list for the client sample: snaps each cut to the quietest 10ms
frame near the transcript boundary, then writes edl.json (source in/out + output times)."""
import array, json, math, subprocess, sys

SRC = sys.argv[1]          # raw talking-head file
OUT = sys.argv[2]          # edl.json path

# (label, in, out) in SOURCE seconds — approximate word boundaries from the transcripts.
# A string value is pinned (verified by windowed transcription) and is not snapped.
SEGMENTS = [
    # --- B&W "COMING UP" teaser ---
    ("teaser1",   38.45, "46.13"),  # "...daily reward, daily payout... but no one shows you how you'll withdraw"
    ("teaser2",  "59.37", "62.44"),  # "yahan par tumko main fully sponsored Dubai trip dene wala hoon"
    # --- main (colour) ---
    ("hello",      0.05,   9.78),   # "What's up everyone, hope you're doing good... first reward from Shark Funded accounts"
    ("giveaway", "50.47",  52.83),   # "and there's gonna be a giveaway for you guys as well"
    ("dubai",     52.83, "62.44"),  # "whole industry made videos... not a normal giveaway... fully sponsored Dubai trip"
    ("proof",     71.94,  79.56),   # "when I did the Dubai giveaway, 3 people went to Forex Expo... all covered"
    ("rule",      79.56, "87.82"),  # "I'm going to do the same thing... highest total combined payout in next 30 days"
    ("deadline",  90.66,  99.09),   # "you have till 12th of November... fully sponsored Dubai trip"
    ("discord",   99.09, 104.73),   # "all the support... join discord... link in the description"
    ("offer",    104.73, "117.94"), # "code MSR... 5x 9K+ Bolt or 5x 25K+ Strike... claim your 111 USD"
    ("close",    166.69, 176.48),   # "this is the max I can do... ball is in your court... let me show you how"
]
SEARCH = 0.18  # seconds either side of each boundary

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
pcm = array.array("h"); pcm.frombytes(raw)
SR, HOP = 16000, 160
energy = []
for i in range(0, len(pcm) - HOP, HOP):
    chunk = pcm[i:i + HOP]
    energy.append(math.sqrt(sum(v * v for v in chunk) / HOP))
dur = len(pcm) / SR

def snap(t):
    if isinstance(t, str):
        return float(t)
    lo, hi = max(0, int((t - SEARCH) * 100)), min(len(energy) - 1, int((t + SEARCH) * 100))
    best = min(range(lo, hi + 1), key=lambda k: energy[k])
    return round(min(best / 100, dur), 2)

edl, cursor = [], 0.0
for label, a, b in SEGMENTS:
    sa, sb = snap(a), snap(b)
    edl.append({"label": label, "src_in": sa, "src_out": sb,
                "out_start": round(cursor, 3), "dur": round(sb - sa, 3)})
    cursor += sb - sa
json.dump({"segments": edl, "total": round(cursor, 3)}, open(OUT, "w"), indent=1)
for s in edl:
    print(f"{s['label']:9s} src {s['src_in']:7.2f}-{s['src_out']:7.2f}  out {s['out_start']:6.2f}  ({s['dur']:.2f}s)")
print("total", round(cursor, 2))
