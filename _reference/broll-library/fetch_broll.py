"""Download only the B-roll clips you need from Google Drive.

Usage (from the repo root):
  python3 -I _reference/broll-library/fetch_broll.py <out_dir> <clip> [<clip> ...]
  python3 -I _reference/broll-library/fetch_broll.py <out_dir> --sheet <clip> ...   # also write a contact sheet
  python3 -I _reference/broll-library/fetch_broll.py --find <words>                    # search the library

<clip> is a Drive file id or a path/name from LIBRARY.md (e.g. "IMG_0114",
"spraying sunlight", "whisker block powder"). Each file is saved as
<out_dir>/<safe name>.<ext> and skipped if already there. Prints duration and
whether the clip is HDR (HDR clips must be tone-mapped when cut).
Needs: pip install gdown; ffmpeg/ffprobe.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = json.load(open(os.path.join(HERE, "library.json")))["clips"]


def find(q):
    q = q.lower().strip()
    exact = [c for c in LIB if c["id"] == q or c["path"].lower() == q
             or os.path.splitext(c["path"].lower())[0].strip() == q]
    if exact:
        return [e for e in exact if not e["duplicate_name"]] or exact
    return [c for c in LIB if q in c["path"].lower()]


def probe(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=color_transfer:format=duration", "-of", "json", f], capture_output=True, text=True)
    try:
        j = json.loads(r.stdout)
        tr = j["streams"][0].get("color_transfer", "")
        return float(j["format"]["duration"]), tr in ("arib-std-b67", "smpte2084")
    except Exception:
        return None, None


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "--find":
        q = " ".join(a[1:]).lower()
        words = q.split()
        for c in LIB:
            hay = " ".join([c["path"], c["description"], c["tags"], c["notes"]]).lower()
            if all(w in hay for w in words):
                print(f"[{c['people']:>4}] {c['folder']}/{c['path']}  {c['id']}\n        {c['description']}  | {c['notes']}")
        return
    out, items, sheet = a[0], a[1:], False
    if "--sheet" in items:
        items.remove("--sheet")
        sheet = True
    os.makedirs(out, exist_ok=True)
    import gdown
    got = []
    for q in items:
        hits = find(q)
        if len(hits) != 1:
            print(f"! '{q}': {len(hits)} matches {[h['path'] for h in hits[:6]]} - use the id")
            continue
        c = hits[0]
        base = re.sub(r"[^A-Za-z0-9._-]+", "_", c["path"].split("/")[-1]).strip("_")
        if "." not in base[-5:]:
            base += ".mov"
        if c["duplicate_name"]:
            base = base.replace(".", f"_{c['id'][:5]}.", 1)
        dst = os.path.join(out, base)
        if not os.path.exists(dst):
            gdown.download(id=c["id"], output=dst, quiet=True)
        dur, hdr = probe(dst)
        print(f"{dst}  {dur and round(dur, 1)}s  {'HDR -> tone-map' if hdr else 'SDR'}  people={c['people']}  {c['notes']}")
        got.append(dst)
    if sheet and got:
        from PIL import Image, ImageDraw
        W, H = 113, 200
        im = Image.new("RGB", (6 * W, len(got) * (H + 18)))
        d = ImageDraw.Draw(im)
        for r, f in enumerate(got):
            dur, _ = probe(f)
            d.text((2, r * (H + 18) + 2), os.path.basename(f), fill="yellow")
            for k in range(6):
                t = (dur or 6) * (k + 0.5) / 6
                tmp = os.path.join(out, f".thumb{k}.jpg")
                subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(t), "-i", f, "-frames:v", "1",
                                "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", tmp])
                if os.path.exists(tmp):
                    im.paste(Image.open(tmp), (k * W, r * (H + 18) + 18))
                    os.remove(tmp)
        p = os.path.join(out, "contact-sheet.jpg")
        im.save(p, quality=85)
        print("contact sheet:", p)


main()
