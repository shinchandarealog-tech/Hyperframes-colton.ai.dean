"""Generate EDIT_PLAN.html (self-contained) for the Iman watch clip.
Run from the project folder:  python3 -I scripts/make_plan.py
"""
import base64, io, json, subprocess, html
from PIL import Image

EDIT = "assets/iman-edit.mp4"
REF = "../../_reference/creator-library/arthurcbrooks/videos"
FRONT_X, SIDE_X = 656, 810           # 9:16 crop left edge per camera angle
ANGLES = [(0, 2.33, FRONT_X), (2.33, 12.43, SIDE_X), (12.43, 21.26, FRONT_X),
          (21.26, 24.69, SIDE_X), (24.69, 99, FRONT_X)]

def b64(im, w):
    im = im.convert("RGB"); h = int(im.height * w / im.width)
    buf = io.BytesIO(); im.resize((w, h)).save(buf, "JPEG", quality=72)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def clip_thumb(t):
    x = next(c for a, b, c in ANGLES if a <= t < b)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", EDIT, "-frames:v", "1",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    im = Image.open(io.BytesIO(raw)).crop((x, 0, x + 608, 1080))
    return b64(im, 180)

def ref_thumb(vid, t):
    try:
        return b64(Image.open(f"{REF}/{vid}/frames/frame-{int(t*2)+1:05d}.jpg"), 120)
    except FileNotFoundError:
        return ""

# beat: (start, end, script, thumb_t, [options]); option: (title, archetype, desc, why, ref_id, (vid, t), suggested)
BEATS = [
 (0.00, 2.40, "I don't go anywhere without a watch.", 1.0, [
   ("Face → macro watch cut", "A-roll + b-roll + text (A01)",
    "0–0.8s on his face (front cam). On “watch.” hard-cut to a cinematic macro of a watch movement ticking. Lockup: small “I don't go / anywhere / without a” + serif italic hero <i>watch.</i>",
    "Arthur's hook rule: a visual inside the first second, landing on the loaded noun.", "A01", ("DXcF2jhDCFP", 0.5), True),
   ("Stay on face, big lockup", "A-roll + captions (A09)",
    "Full A-roll. Bold sans hero <b>anywhere</b> with small satellites, then serif <i>watch.</i> builds under it.",
    "Lets the viewer meet Iman before anything happens. Safest, but a slower hook.", "A09", ("DQprSK3DQd7", 17.0), False),
   ("Open on a painting", "Painting + hero word (A01)",
    "Open straight on a public-domain painting of a pocket-watch portrait, giant <i>watch.</i>, then cut to his face on “Even”.",
    "Most ‘Arthur’, but a painting doesn't fit Iman's modern luxury world as well.", "A01", ("DQprSK3DQd7", 1.5), False)]),
 (2.40, 6.25, "Even if I'm going abroad literally for a few days, I'm bringing a watch roll with me.", 4.0, [
   ("Travel b-roll → back on the roll", "B-roll + text",
    "On “abroad” cut to plane-window / airport b-roll: “going / <i>abroad</i> / for a few days”. Back on side-cam A-roll for “<b>watch roll</b> with me” (he's holding it).",
    "Describing a scenario → show it; return to the face for the object he's holding.", "B", ("DXcF2jhDCFP", 2.5), True),
   ("Rounded inset b-roll", "Inset b-roll on black (A24)",
    "Plane-window b-roll inside a rounded card on black, “literally / <i>a few days</i>”.",
    "More intimate and stylised. Good for rhythm variety.", "A24", ("Dc1F2ouMU8w", 95.5), False),
   ("Punch-in on the watch roll", "A-roll punch-in (A27)",
    "Stay on side cam; on “watch roll” punch in 1.0→1.5 onto his hands + roll. Hero <b>watch roll</b>.",
    "No external assets, keeps it personal.", "A27", ("DQprSK3DQd7", 12.5), False)]),
 (6.25, 10.60, "Watches are something that I've been infatuated with from the time I was eight years old,", 8.0, [
   ("Start the life timeline", "Timeline overlay on A-roll (A20)",
    "Serif hero <i>infatuated</i>. On “eight years old” a thin timeline fades in over the lower third: tick “8 YEARS — FIRST WATCH”, blue marker lands on it.",
    "This clip is a <b>collecting journey (8 → 18 → today)</b>. Arthur's origin-story reel uses a timeline as its spine.", "A20", ("Dc1F2ouMU8w", 52.0), True),
   ("Painting: the fascinated child", "Painting + hero word (A01)",
    "Cut to Chardin's <i>Soap Bubbles</i> (boy mesmerised, public domain). Giant serif <i>infatuated</i>, small “since I was eight”.",
    "Abstract feeling → painting, Arthur's #1 cutaway.", "A01", ("DP7eSmPADaD", 4.5), False),
   ("A-roll + breath card", "Captions + breath card (A02)",
    "A-roll with <i>infatuated</i>, then 0.7s white card, blue serif “<i>eight years old.</i>”",
    "Simple, adds rhythm.", "A02", ("DQprSK3DQd7", 9.0), False)]),
 (10.60, 15.30, "…that I bought my first Timex for 15 pounds. I remember I got it from Argos here in London.", 12.5, [
   ("Polaroid drop-ins on white", "Polaroid collage (A15)",
    "White canvas: a classic Timex photo drops in rotated, then settles. Label “my first / <i>Timex</i>” blue serif + huge sans <b>£15</b>. On “Argos… London” a second polaroid (Argos store / London street) lands beside it.",
    "Personal story with concrete objects → photos, like Arthur's credentials collage.", "A15", ("Dc1F2ouMU8w", 3.5), True),
   ("Form-field stamp", "Photo + label stamp (A21)",
    "Timex photo with a small blue form field: “FIRST WATCH: TIMEX · PRICE: £15 · BOUGHT AT: ARGOS, LONDON”.",
    "Fun, catalogue-like and very fast to read.", "A21", ("Dc1F2ouMU8w", 62.0), False),
   ("Paper card, big price", "Text-centric paper card (A03)",
    "Paper card: blue serif <i>first Timex</i>, huge black sans <b>£15</b>. No photos.",
    "No external images needed.", "A03", ("DP7eSmPADaD", 22.5), False)]),
 (15.30, 16.85, "Saved up for a couple weeks for it,", 16.0, [
   ("Coins b-roll", "B-roll + text",
    "Close-up b-roll of hands counting coins / a coin jar. “<i>Saved</i> up / for a couple weeks”.",
    "Quick concrete visual; keeps the cut rate up (a cutaway every 1.5–3s).", "B", ("DXcF2jhDCFP", 2.5), True),
   ("Breath card", "Breath card (A02)",
    "1.5s black card, white serif “<i>a couple weeks.</i>”",
    "A beat of stillness before the big Rolex jump.", "A02", ("DQprSK3DQd7", 9.0), False),
   ("Stay on A-roll", "A-roll + captions",
    "Front cam, hero <i>Saved</i> up.",
    "Gives face time between two graphic beats.", "A09", ("DQprSK3DQd7", 17.0), False)]),
 (16.85, 21.35, "…and my watch collecting journey really started when I was 18 and I bought my first Rolex,", 19.0, [
   ("Timeline slides to 18 + Rolex polaroid", "Timeline on white canvas (A20)",
    "Hero <i>journey</i> on A-roll, then cut to white canvas: timeline pans from 8 → <b>18 YEARS — FIRST ROLEX</b>; a Rolex photo drops onto the tick. Blue serif <i>first Rolex</i>.",
    "Continues the spine from beat 3. The callback makes the video feel designed.", "A20", ("Dc1F2ouMU8w", 37.0), True),
   ("A-roll + timeline overlay", "Timeline overlay on A-roll (A20)",
    "Stay on face; the overlay timeline slides to 18 under him. Hero <b>Rolex</b>.",
    "Lighter version of A, more face time.", "A20", ("Dc1F2ouMU8w", 52.0), False),
   ("Rolex b-roll", "B-roll + text",
    "Macro stock shot of a Rolex, hero <b>Rolex</b>, small “when I was 18”.",
    "Straightforward luxury shot.", "B", ("DXcF2jhDCFP", 2.5), False)]),
 (21.35, 24.80, "So at this point, I probably owned 50-plus watches.", 23.0, [
   ("Grid of 50 line-drawn watches", "Illustration grid + big number",
    "White paper: 50 thin blue line-art watch faces draw on fast in a grid (stagger), then <b>50+</b> slams in huge black sans with “<i>watches.</i>” blue serif.",
    "A number → make the viewer <i>see</i> the quantity. Built in-house, no stock needed.", "A04", ("DP7eSmPADaD", 12.0), True),
   ("Paper graph to 50+", "Paper graph (A04)",
    "Blue line climbs from 1 → 50+ on paper, exits frame. Hero <b>50+</b>.",
    "Growth over time, matches “progress” graph.", "A04", ("DP7eSmPADaD", 12.0), False),
   ("Flat blue claim card", "Blue card (A10)",
    "Full-bleed electric blue, white “I probably owned / <b>50+</b> / watches.”",
    "Punchy, fastest to build.", "A10", ("DXcF2jhDCFP", 48.5), False)]),
 (24.80, 29.95, "On the wrist at the moment is my favourite piece ever, the Patek Philippe Nautilus 5711R.", 27.5, [
   ("His real wrist + name callout", "Object callout (A13), reuses his own footage",
    "Reuse the side-cam shot where the rose-gold Nautilus is on his wrist (≈4–5s), slow push-in. Thin white curved line to the watch → name box “Patek Philippe / <b>Nautilus</b> 5711R” growing letter by letter. Serif <i>favourite piece ever</i>.",
    "<b>Covers the burned-in title (26.0–30.0s) completely</b>, shows the actual watch, no stock needed.", "A13", ("DXcF2jhDCFP", 33.0), True),
   ("Blue card → product shot", "Blue card (A10) + object card",
    "26.0s electric-blue card “my <i>favourite piece</i> ever”, then black card with a Nautilus product photo + small-caps spec line “PATEK PHILIPPE · NAUTILUS · 5711R”.",
    "Luxury-catalogue feel. Needs a licensed product photo.", "A10", ("DXcF2jhDCFP", 48.5), False),
   ("Polaroid on white", "Polaroid (A15)",
    "White canvas, Nautilus photo drops in, blue serif <i>Nautilus</i> 5711R; hand-drawn blue circle around the dial.",
    "Consistent with the collage beats, but repeats the beat-4 archetype.", "A19", ("Dc1F2ouMU8w", 110.0), False)]),
 (29.95, 32.41, "If I had to have one watch for the rest of my life, it would be this.", 31.5, [
   ("End on his face, holding it", "A-roll + serif ending",
    "Front cam. “If I had to have / <i>one watch</i>”, then “it would be / <b><i>this.</i></b>” held to the end as he shows the watch.",
    "“This” points at the physical watch, so we must <i>see</i> it in his hand. Arthur's A-roll serif ending.", "A09", ("Dc1F2ouMU8w", 149.0), True),
   ("Blue-on-white summary card", "Paper summary card (A03)",
    "Last 1.2s: white card, blue serif “<i>one watch</i> / for the rest of my life.”",
    "Arthur's signature end card, but loses the ‘this’ payoff.", "A03", ("DP7eSmPADaD", 37.5), False),
   ("Quote card", "Blue radial quote card (A23)",
    "Blue radial card with big quotation marks around “it would be <i>this.</i>”",
    "Dramatic close; also loses the watch reveal.", "A23", ("Dc1F2ouMU8w", 85.5), False)]),
]

css = """
:root{--bg:#f6f6f8;--card:#fff;--ink:#0b0b0d;--dim:#6b6b76;--line:#e3e3ea;--blue:#1F4FD8;--pick:#eef2ff}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0e0e11;--card:#17171b;--ink:#f2f2f5;--dim:#9a9aa6;--line:#2a2a31;--pick:#1a2140}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 Inter,system-ui,sans-serif}
.wrap{max-width:1100px;margin:0 auto;padding:24px 16px 120px}
h1{font:italic 800 34px/1.1 'Playfair Display',Georgia,serif;margin:0 0 4px}h1 b{font:800 34px Inter,system-ui,sans-serif;font-style:normal;color:var(--blue)}
.meta{color:var(--dim);font-size:13px}
.bar{display:flex;height:22px;border-radius:6px;overflow:hidden;margin:16px 0 4px;border:1px solid var(--line)}
.bar div{border-right:1px solid var(--bg);background:var(--blue);color:#fff;font-size:11px;display:flex;align-items:center;justify-content:center}
.note{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:16px 0;font-size:14px}
.beat{background:var(--card);border:1px solid var(--line);border-radius:14px;margin:18px 0;display:grid;grid-template-columns:1fr 200px;gap:0}
.left{padding:16px;border-right:1px solid var(--line);min-width:0}.right{padding:12px;text-align:center}
.right img{width:180px;border-radius:8px;display:block;margin:0 auto 8px}.script{font:italic 600 15px 'Playfair Display',Georgia,serif;text-align:left}
.bh{display:flex;justify-content:space-between;align-items:baseline;gap:8px}.bh h2{margin:0;font-size:18px}.ts{color:var(--dim);font-size:13px;font-variant-numeric:tabular-nums}
textarea{width:100%;min-height:44px;margin:10px 0;padding:8px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--ink);font:inherit}
.opts{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
label.opt{display:flex;flex-direction:column;border:1.5px solid var(--line);border-radius:10px;padding:10px;cursor:pointer;font-size:13px;position:relative}
label.opt:has(input:checked){border-color:var(--blue);background:var(--pick)}
label.opt input{position:absolute;top:10px;right:10px;accent-color:var(--blue)}
.ot{font-weight:700;font-size:14px;padding-right:20px}.oa{color:var(--blue);font-size:12px;margin-bottom:6px}
.od{margin-bottom:6px}.ow{color:var(--dim);font-size:12px}.refr{display:flex;gap:8px;align-items:center;margin-top:8px;color:var(--dim);font-size:11px}
.refr img{width:46px;border-radius:4px}.sug{display:inline-block;background:var(--blue);color:#fff;border-radius:99px;font-size:10px;padding:1px 7px;margin-left:6px;vertical-align:middle}
.dock{position:fixed;left:0;right:0;bottom:0;background:var(--card);border-top:1px solid var(--line);padding:12px 16px;display:flex;gap:12px;justify-content:center;align-items:center}
button{background:var(--blue);color:#fff;border:0;border-radius:99px;padding:10px 22px;font:600 15px Inter,system-ui,sans-serif;cursor:pointer}
#out{display:none;width:100%;max-width:1100px;margin:16px auto;min-height:220px}
@media (max-width:760px){.beat{grid-template-columns:1fr}.left{border-right:0;border-bottom:1px solid var(--line)}.opts{grid-template-columns:1fr}}
"""

parts = [f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Iman Watch Edit Plan</title><style>{css}</style></head><body><div class=wrap>
<h1>Iman Gadzhi · watches <b>edit plan</b></h1>
<div class=meta>Clip: iman-edit.mp4 (silences cut, 35.3s → 32.4s) · 9:16 1080×1920 · Style: premium minimal (@arthurcbrooks) · {len(BEATS)} beats</div>
<div class=bar>""" + "".join(f"<div style='flex:{e-s:.2f}'>{i+1}</div>" for i, (s, e, *_ ) in enumerate(BEATS)) + """</div>
<div class=note><b>How to use:</b> pick one design per beat (my suggestion is pre-selected), add notes if you want changes, then hit <b>Copy plan</b> and paste it back to me.<br>
<b>Heads-up:</b> the raw clip has a burned-in “PATEK PHILIPPE NAUTILUS” title at <b>26.0–30.0s</b>. In a vertical crop it gets sliced in half, so beat 8 must be a full-screen scene.<br>
<b>Captions everywhere:</b> white on footage, one hero word per phrase (bold sans for facts, serif italic for feelings), over the chest, never at the bottom.</div>
"""]
for i, (s, e, script, tt, opts) in enumerate(BEATS):
    n = i + 1
    o_html = ""
    for j, (title, arch, desc, why, rid, (rv, rt), sug) in enumerate(opts):
        L = "ABC"[j]; r = ref_thumb(rv, rt)
        o_html += f"""<label class=opt><input type=radio name=b{n} value="{L}" data-t="{html.escape(title)}" {'checked' if sug else ''}>
<div class=ot>{L} · {title}{'<span class=sug>suggested</span>' if sug else ''}</div><div class=oa>{arch}</div><div class=od>{desc}</div><div class=ow>{why}</div>
<div class=refr>{f'<img src="{r}" alt="">' if r else ''}<span>ref {rid} · {rv[:4]} @{rt:.1f}s</span></div></label>"""
    parts.append(f"""<section class=beat><div class=left><div class=bh><h2>Beat {n}</h2><span class=ts>{s:.2f}–{e:.2f}s · {e-s:.1f}s</span></div>
<textarea id=n{n} placeholder="Your notes for this beat (optional)"></textarea><div class=opts>{o_html}</div></div>
<div class=right><img src="{clip_thumb(tt)}" alt=""><div class=script>“{html.escape(script)}”</div></div></section>""")
parts.append(f"""<textarea id=out readonly></textarea></div>
<div class=dock><button onclick="copyPlan()">Copy plan</button><span class=meta id=msg></span></div>
<script>
const B={json.dumps([[s,e,sc] for s,e,sc,*_ in BEATS])};
function copyPlan(){{let t='EDIT PLAN — Iman watches\\n';B.forEach((b,i)=>{{const n=i+1,c=document.querySelector('input[name=b'+n+']:checked'),no=document.getElementById('n'+n).value.trim();
t+='Beat '+n+' ('+b[0].toFixed(2)+'-'+b[1].toFixed(2)+'s): '+(c?c.value+' · '+c.dataset.t:'none')+(no?' | notes: '+no:'')+'\\n';}});
const o=document.getElementById('out');o.value=t;o.style.display='block';
try{{navigator.clipboard.writeText(t).then(()=>msg.textContent='Copied! Paste it to Claude.',()=>{{o.select();msg.textContent='Select the text box and copy it.'}})}}catch(e){{o.select();msg.textContent='Select the text box and copy it.'}}}}
</script></body></html>""")
open("EDIT_PLAN.html", "w").write("".join(parts))
print("ok", sum(len(p) for p in parts) // 1024, "KB")
