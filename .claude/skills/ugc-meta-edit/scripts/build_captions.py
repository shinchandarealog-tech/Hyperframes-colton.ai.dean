"""Build 2-3 word captions from hand-written phrase lines and inject them into index.html.

Usage (from the project folder):
  python3 -I build_captions.py <words.json> <phrases.txt> <duration_seconds> [fix.json]

- <phrases.txt>: the script split into caption chunks, one per line, 2-3 words each,
  breaking on punctuation. Words must match the transcript in order (punctuation and
  case are ignored), so every word is captioned exactly once.
- [fix.json]: optional {"wrong": "right"} word fixes for whisper mistakes,
  e.g. {"brain": "spray", "Packagen": "Pacagen"}; map a word to null to merge it
  into the previous word (e.g. "a.m." after "2" -> "2am").

Writes edit-data/captions.json and replaces everything between
"<!-- Captions -->" and the closing root </div> in index.html.
"""
import html
import json
import re
import sys

words_path, phrases_path, D = sys.argv[1], sys.argv[2], float(sys.argv[3])
fix = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else {}

ws = []
for w in json.load(open(words_path)):
    t = fix.get(w["text"], w["text"])
    if t is None:
        ws[-1]["end"] = w["end"]
        continue
    ws.append(dict(w, text=t))

P = [l.strip() for l in open(phrases_path) if l.strip()]
norm = lambda t: "".join(c for c in t.lower() if c.isalnum())
i, caps = 0, []
for p in P:
    n = len(p.split())
    got = [norm(w["text"]) for w in ws[i:i + n]]
    if [norm(x) for x in p.split()] != got:
        sys.exit(f"Phrase does not match transcript: {p!r} vs {[w['text'] for w in ws[i:i + n]]}")
    if not 2 <= n <= 3:
        print(f"note: {n}-word chunk: {p!r}")
    caps.append({"text": p, "start": ws[i]["start"]})
    i += n
if i != len(ws):
    sys.exit(f"Unused transcript words: {[w['text'] for w in ws[i:]]}")

fr = lambda t: round(round(t * 30) / 30, 3)  # snap to 30fps frames
for c in caps:
    c["start"] = fr(max(0, c["start"] - 0.05))
caps[0]["start"] = 0.0  # captions run from the very first frame
for j, c in enumerate(caps):
    c["end"] = caps[j + 1]["start"] if j + 1 < len(caps) else D

json.dump(caps, open("edit-data/captions.json", "w"), indent=0)
block = "\n".join(
    f'      <div id="cap-{k + 1:02d}" class="clip cap" data-start="{c["start"]}" '
    f'data-duration="{round(c["end"] - c["start"], 3)}" data-track-index="2">{html.escape(c["text"])}</div>'
    for k, c in enumerate(caps))
h = open("index.html").read()
h, n = re.subn(r"(      <!-- Captions -->\n).*?(\n    </div>\n    <script>)",
               lambda m: m.group(1) + block + m.group(2), h, flags=re.S)
if not n:
    sys.exit("No '<!-- Captions -->' block found in index.html")
open("index.html", "w").write(h)
short = [(c["text"], round(c["end"] - c["start"], 2)) for c in caps if c["end"] - c["start"] < 0.35]
print(f"{len(caps)} captions written; shortest {min(c['end'] - c['start'] for c in caps):.2f}s",
      f"| very short: {short}" if short else "")
