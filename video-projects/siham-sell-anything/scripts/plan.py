"""Build timeline.json: cut list + every word mapped to output time.

On-screen spelling = Siham's real delivery (confirmed by two Whisper models and
her own burned-in captions), with Whisper's mishearings corrected.
Word starts are snapped to the first audio-energy onset so no caption is early.
"""
import json, os, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FPS = 30

# (id, source in, source out)
CUTS = [
    ("A", 0.00, 1.98), ("B", 2.35, 5.00), ("C", 6.25, 7.62), ("D", 8.45, 9.92),
    ("E", 10.60, 11.58), ("F", 11.76, 12.90), ("G", 13.10, 14.45), ("H", 14.55, 16.85),
    ("I", 17.15, 20.30), ("J", 20.42, 21.66), ("K", 21.75, 26.02), ("L", 26.33, 28.42),
    ("M", 28.45, 29.80), ("N", 29.95, 31.60), ("O", 32.04, 33.62), ("P", 33.74, 34.80),
    ("Q", 34.98, 35.62), ("R", 35.76, 37.50),
]
HOLD = 0.5

# whisper token -> on-screen word (None = drop, merged into previous)
FIX = {
    "Must": "Most", "sells": "sales", "representative": "representatives", "hear?": "hear,",
    "know.": "know,", "It's": "it's", "learned.": "learned:", "fail.": "fail:",
    "futures": "features", "is": "isn't", "in@74": None, "series.": "series,",
    "Take": "take", "notes.": "notes,", "Let's": "let's", "cosmetics": "cosmetics,",
}


def snap_frames(t):
    return round(t * FPS) / FPS


def main():
    words = json.load(open(os.path.join(HERE, "words.json")))
    wav = os.path.join(ROOT, "raw-media/raw/take.wav")
    a = np.frombuffer(open(wav, "rb").read()[44:], dtype="<i2").astype("float32") / 32768
    hop = 160
    rms = np.array([np.sqrt(np.mean(a[i:i + 320] ** 2) + 1e-12) for i in range(0, len(a) - 320, hop)])
    db = 20 * np.log10(rms)
    thr = np.percentile(db, 20) + 8

    # cuts -> output offsets (frame-aligned)
    segs, t = [], 0.0
    for cid, i, o in CUTS:
        d = round((o - i) * FPS) / FPS
        segs.append({"id": cid, "src_in": i, "src_out": round(i + d, 4), "out_in": round(t, 4), "out_out": round(t + d, 4)})
        t += d
    total = round(t + HOLD, 4)

    def to_out(src):
        for s in segs:
            if s["src_in"] - 1e-6 <= src <= s["src_out"] + 1e-6:
                return s["out_in"] + (src - s["src_in"]), s["id"]
        return None, None

    out = []
    for idx, w in enumerate(words):
        tok = w["w"]
        key = f"{tok}@{idx}"
        disp = FIX.get(key, FIX.get(tok, tok)) if key not in FIX else FIX[key]
        if disp is None:
            continue
        s, e = w["s"], w["e"]
        ov = [(min(e, g["src_out"]) - max(s, g["src_in"]), g) for g in segs]
        best = max(ov, key=lambda x: x[0])
        if best[0] <= 0:
            raise SystemExit(f"word outside cuts: {tok} {s}")
        seg = best[1]
        s = max(s, seg["src_in"])
        # snap to first voiced 10ms frame at/after whisper start
        k = int(s * 100)
        k2 = int(min(e, seg["src_out"]) * 100)
        while k < k2 and db[k] < thr:
            k += 1
        s = k / 100
        os_, sid = to_out(s)
        oe, _ = to_out(min(e, seg["src_out"]))
        out.append({"w": disp, "src": s, "t": round(os_, 3), "e": round(oe, 3), "seg": sid})

    # split "yourselves" -> "your" + "sales"
    for i, w in enumerate(out):
        if w["w"] == "yourselves":
            mid = round(w["t"] + (w["e"] - w["t"]) * 0.42, 3)
            out[i:i + 1] = [dict(w, w="your", e=mid), dict(w, w="sales", t=mid)]
            break

    json.dump({"fps": FPS, "duration": total, "segments": segs, "words": out},
              open(os.path.join(HERE, "timeline.json"), "w"), indent=1)
    for s in segs:
        print(f'{s["id"]} src {s["src_in"]:6.2f}-{s["src_out"]:6.2f}  out {s["out_in"]:6.2f}-{s["out_out"]:6.2f}')
    print("total", total)
    for w in out:
        print(f'{w["t"]:6.2f} {w["seg"]} {w["w"]}')


if __name__ == "__main__":
    main()
