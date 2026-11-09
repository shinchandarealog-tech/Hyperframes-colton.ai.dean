#!/usr/bin/env python3
"""Generates index.html for the NS Brothers DAV winter-uniform reel (Apple-UI styling).

All timings are seconds on the voiceover (assets/voiceover.mp3, 68.52s).
Edit the tables below and re-run: python3 scripts/build.py
"""
from pathlib import Path

DURATION = 69.2
VO_DURATION = 68.6
X = 0.45  # transition overlap: incoming scene starts this much before its cut
X_QUICK = 0.3  # shorter overlap into the quick item shots so each item stays readable
QUICK = ("tracksuit", "caps", "shoes")


def ov(sid):
    return X_QUICK if sid in QUICK else X

# (id, start, end, kind, source, media_start, transition, tag)
#   kind: video | tour (store-tour clip, cropped to hide burned-in badge/watermark)
#         photo | poster | textcard | maps | call | outro
#   poster tag = (big label, small label); textcard tag = (kicker, headline, subline)
SCENES = [
    ("storefront", 0.0, 5.0, "video", "storefront", 0.0, None, None),
    ("seniors", 5.0, 8.15, "poster", "poster-912-kids", 0, "zoom", ("Class IX – XII", "SMART & WARM")),
    ("jacket", 8.15, 12.1, "video", "jacket", 3.55, "slideL", "DAV Winter Jacket"),
    ("juniors", 12.1, 14.55, "poster", "poster-35-kids", 0, "slideUp", ("Class III – V", "DAV SCHOOL UNIFORM")),
    ("uniformset", 14.55, 18.2, "poster", "poster-68-kids", 0, "zoom", ("Class VI – VIII", "")),
    ("blazer", 18.2, 20.9, "video", "blazer", 0.6, "slideL", "DAV Blazer"),
    ("jacketfront", 20.9, 25.1, "photo", "jacket-front", 0, "zoom", "Winter Essentials"),
    ("sweaters", 25.1, 27.3, "poster", "poster-sweaters", 0, "slideUp", ("Half & Full Sleeve", "NAVY BLUE · WOOL")),
    ("tracksuit", 27.3, 28.8, "video", "tracksuit", 1.2, "slideL", None),
    ("caps", 28.8, 30.3, "textcard", "shot-everything", 0, "slideL", ("STYLISH", "Winter Caps.", "Warm. Comfortable. School-ready.")),
    ("nurkids", 30.3, 34.6, "poster", "poster-nur-kids", 0, "zoom", ("Class Nur – II", "WARM & SMART")),
    ("oneroof", 34.6, 36.6, "tour", "shot-oneroof", 0, "slideR", None),
    ("shoes", 36.6, 38.4, "tour", "shot-shoes", 0, "slideL", None),
    ("counter", 38.4, 42.7, "tour", "shot-counter", 0, "zoom", None),
    ("recap", 42.7, 46.45, "tour", "shot-everything", 0, "slideUp", None),
    ("shopping", 46.45, 49.4, "tour", "shot-shopping", 0, "zoom", None),
    ("visit", 49.4, 51.45, "video", "storefront", 3.65, "slideUp", None),
    ("address", 51.45, 54.45, "maps", None, 0, "zoom", None),
    ("phone", 54.45, 64.75, "call", None, 0, "slideUp", None),
    ("brand", 64.75, DURATION, "outro", None, 0, "zoom", None),
]

# Phrase captions — text from the script, timed to the voiceover.
# Words wrapped in *asterisks* are highlighted.
CAPTIONS = [
    (0.05, 2.0, "*D.A.V. Public School* ke students ke liye"),
    (2.0, 4.85, "aa gaya hai *winter shopping* ka perfect time!"),
    (5.1, 8.05, "Apne bachchon ko dijiye *smart look* aur *thand se bachav*"),
    (8.3, 12.05, "*NS Brothers* ki D.A.V. school uniform aur *winter collection* ke saath"),
    (12.27, 14.5, "Yahan milegi *D.A.V. school ki uniform*"),
    (18.2, 20.75, "ke saath *winter wear* ki bhi poori taiyari hai"),
    (21.03, 24.95, "Thand badhne se pehle, bachchon ke *winter essentials* zaroor taiyar kar lein!"),
    (30.4, 32.25, "jo bachchon ko *thand se bachane* ke saath"),
    (32.3, 34.55, "unke school look ko bhi banayein *smart*"),
    (34.74, 36.5, "Aur baat sirf *uniform* tak hi nahi!"),
    (38.4, 42.6, "jo daily school wear ko banayein *comfortable* aur *complete*"),
    (46.5, 49.3, "bachchon ki school shopping karein *ek hi jagah!*"),
    (49.55, 51.4, "Aaj hi visit karein *NS Brothers!*"),
]

# Item widgets — land exactly on the spoken word, over the matching shot.
ITEMS = [
    ("sweaters", 25.9, "Winter Sweaters", "Half & full sleeve · Wool"),
    ("tracksuit", 27.35, "Fleece Tracksuits", "Warm · Sky blue & navy"),
    ("shoes", 37.4, "Shoes & Socks", "Comfortable · Everyday"),
]

# Reminders-style checklists that tick word by word: (scene id, heading, [(time, label), ...])
CHIPS = [
    ("uniformset", "Complete D.A.V. Uniform",
     [(15.0, "Shirt"), (15.88, "Tie"), (16.35, "Trousers"), (16.96, "Blazer"), (17.68, "Skirt")]),
    ("recap", "This Winter",
     [(43.45, "Uniform"), (44.4, "Sweater"), (45.0, "Shoes"), (45.8, "Cap")]),
]

ADDRESS_LINES = [
    (51.54, "Near Punjab National Bank"),
    (53.0, "Chandauthi More"),
    (53.92, "Gaya, Bihar"),
]

BRAND_WORDS = [(66.13, "Quality."), (66.85, "Style."), (67.6, "Trust.")]

# (src, start, duration, volume)
SFX = (
    [("whoosh.mp3", s[1] - ov(s[0]), 0.6, 0.16) for s in SCENES[1:] if s[0] not in QUICK]
    + [("pop.mp3", t - 0.05, 0.7, 0.25) for _, t, _, _ in ITEMS]
    + [("pop.mp3", 28.85, 0.7, 0.25)]
    + [("pop.mp3", t - 0.03, 0.7, 0.16) for _, _, chips in CHIPS for t, _ in chips]
    + [("sparkle.mp3", 51.5, 2.0, 0.3), ("slam.mp3", 64.85, 1.2, 0.2), ("pop.mp3", 0.3, 0.7, 0.35)]
)

CHECK_SVG = '<svg width="30" height="30" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SNOW_SVG = ('<svg width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round">'
            '<path d="M12 2v20M3.3 7l17.4 10M3.3 17L20.7 7M9 4l3 2 3-2M9 20l3-2 3 2"/></svg>')
PHONE_SVG = ('<svg width="80" height="80" viewBox="0 0 24 24"><path fill="#fff" d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2a1 1 0 011-.25 '
             '11.4 11.4 0 003.6.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1z"/></svg>')
MSG_SVG = ('<svg width="76" height="76" viewBox="0 0 24 24"><path fill="#fff" d="M12 3C6.5 3 2 6.6 2 11c0 2.4 1.3 4.6 3.4 6L4.5 21l4.2-2.3c1 .2 2.1.3 3.3.3 '
           '5.5 0 10-3.6 10-8s-4.5-8-10-8z"/></svg>')


def streets_svg():
    # Hand-placed street grid in Apple Maps dark style; deterministic.
    minor = [(0, 260, 1080, 300), (0, 980, 1080, 940), (120, 0, 180, 1920), (860, 0, 820, 1920), (0, 1240, 1080, 1290),
             (360, 0, 330, 1100), (700, 300, 740, 1300), (0, 420, 1080, 470)]
    major = [(0, 640, 1080, 640), (540, 0, 540, 1300), (0, 120, 1080, 820)]
    blocks = "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="#2a3149" stroke-width="22"/>' for a, b, c, d in minor)
    roads = "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="#3b4566" stroke-width="44"/>' for a, b, c, d in major)
    park = '<rect x="600" y="700" width="230" height="200" rx="30" fill="#1f3a2c"/><rect x="190" y="320" width="130" height="90" rx="20" fill="#26304a"/>'
    labels = ('<text x="80" y="620" fill="#8b95b3" font-family="Inter" font-weight="600" font-size="30">Chandauthi More</text>'
              '<text x="575" y="200" fill="#8b95b3" font-family="Inter" font-weight="600" font-size="28" transform="rotate(90 575 200)">Gaya Road</text>'
              '<text x="620" y="810" fill="#6fae8a" font-family="Inter" font-weight="600" font-size="26">Park</text>')
    return f'<svg class="streets" width="1080" height="1920" viewBox="0 0 1080 1920">{park}{blocks}{roads}{labels}</svg>'


def fmt(t):
    return f"{t:.2f}".rstrip("0").rstrip(".") if t else "0"


def caption_html(text):
    out, hi = [], False
    for part in text.split("*"):
        if part:
            out.append(f'<span class="hl">{part}</span>' if hi else part)
        hi = not hi
    return "".join(out)


def scene_html(i, sc):
    sid, start, end, kind, src, mstart, trans, tag = sc
    cs = start if i == 0 else start - ov(sid)
    dur = end - cs
    track = 1 + (i % 2)
    z = 10 + i
    timed = f'data-start="{fmt(cs)}" data-duration="{fmt(dur)}" data-track-index="{track}"'
    clip_attrs = f'data-start="{fmt(cs)}" data-duration="{fmt(dur)}" data-track-index="{track + 2}"'
    tag_html = (f'<span class="tdot"></span>{tag}') if isinstance(tag, str) else ""
    body = ""
    if kind in ("video", "tour"):
        crop = " tour" if kind == "tour" else ""
        body = (
            f'<div class="kb" id="kb-{sid}"><div class="crop{crop}">'
            f'<video id="v-{sid}" src="assets/{src}-hd.mp4" {timed} data-media-start="{fmt(mstart)}" muted playsinline></video>'
            f"</div></div>"
            f'<div class="shade clip" id="sh-{sid}" {clip_attrs}></div>'
        )
        if tag:
            body += f'<div class="tag glass-lite clip" id="tag-{sid}" data-start="{fmt(cs)}" data-duration="{fmt(dur)}" data-track-index="{track + 4}">{tag_html}</div>'
    elif kind == "textcard":
        kicker, head, sub = tag
        body = (
            f'<div class="kb" id="kb-{sid}"><div class="crop tour blurred">'
            f'<video id="v-{sid}" src="assets/{src}-hd.mp4" {timed} data-media-start="{fmt(mstart)}" muted playsinline></video>'
            f"</div></div>"
            f'<div class="clip textcard" id="tc-{sid}" {clip_attrs}>'
            f'<div class="tc-kicker" id="tck-{sid}">{kicker}</div>'
            f'<div class="tc-head" id="tch-{sid}">{head}</div>'
            f'<div class="tc-sub" id="tcs-{sid}">{sub}</div></div>'
        )
    elif kind == "photo":
        body = (
            f'<div class="clip photo" id="p-{sid}" {timed}>'
            f'<div class="kb" id="kb-{sid}"><img src="assets/{src}.jpg" alt=""></div>'
            f'<div class="shade"></div>'
            f'<div class="tag glass-lite" id="tag-{sid}">{tag_html}</div></div>'
        )
    elif kind == "poster":
        cls, sub = tag
        sub_html = f'<span class="sub">{sub}</span>' if sub else ""
        body = (
            f'<div class="clip poster" id="p-{sid}" {timed}>'
            f'<img class="poster-bg" src="assets/{src}.jpg" alt="">'
            f'<div class="poster-content">'
            f'<div class="pill glass-lite" id="ps-{sid}">DAV PUBLIC SCHOOL · GAYA JI</div>'
            f'<div class="card" id="pc-{sid}"><img src="assets/{src}.jpg" alt=""></div>'
            f'<div class="poster-label" id="pl-{sid}"><span class="cls">{cls}</span>{sub_html}</div>'
            f"</div></div>"
        )
    elif kind == "maps":
        lines = "".join(
            f'<div class="addr-line" id="al{j}"><span class="dot"></span>{t}</div>' for j, (_, t) in enumerate(ADDRESS_LINES)
        )
        body = (
            f'<div class="clip maps" id="g-{sid}" {timed}>'
            f'<div class="kb" id="kb-{sid}">{streets_svg()}'
            f'<div class="pin-wrap"><div class="pulse" id="pulse"></div>'
            f'<svg id="pin" width="140" height="190" viewBox="0 0 140 190"><path d="M70 186L52 128h36z" fill="#ff453a"/>'
            f'<circle cx="70" cy="70" r="64" fill="#ff453a" stroke="#fff" stroke-width="6"/>'
            f'<text x="70" y="88" text-anchor="middle" fill="#fff" font-family="Inter" font-weight="800" font-size="50">NS</text></svg></div>'
            f'<div class="map-label" id="map-label">NS Brothers</div></div>'
            f'<div class="sheet" id="sheet"><div class="grabber"></div>'
            f'<div class="sh-title">NS Brothers</div><div class="sh-sub">School Uniform Store · Open today</div>'
            f'<div class="addr-lines">{lines}</div>'
            f'<div class="directions" id="directions">Directions</div></div>'
            f"</div>"
        )
    elif kind == "call":
        body = (
            f'<div class="clip graphic" id="g-{sid}" {timed}>'
            f'<div class="call" id="call">'
            f'<div class="call-info" id="ph-info">Zyada jaankari ke liye</div>'
            f'<div class="avatar" id="ph-avatar"><img src="assets/logo.png" alt=""></div>'
            f'<div class="call-name" id="ph-name">NS Brothers</div>'
            f'<div class="call-sub" id="ph-sub">School Dress · Gaya</div>'
            f'<div class="num-list glass" id="ph-list">'
            f'<div class="num-row" id="ph-n1"><span class="num-k">mobile</span><span class="num-v">+91 94708 54055</span></div>'
            f'<div class="num-row" id="ph-n2"><span class="num-k">mobile</span><span class="num-v">+91 75418 54737</span></div></div>'
            f'<div class="call-btns" id="ph-btns">'
            f'<div><div class="cbtn msg"><div class="face">{MSG_SVG}</div></div><div class="cbtn-label">Message</div></div>'
            f'<div><div class="cbtn dial"><div class="ring" id="ring"></div><div class="face">{PHONE_SVG}</div></div><div class="cbtn-label">Call</div></div>'
            f"</div></div></div>"
        )
    elif kind == "outro":
        words = "".join(f'<span class="bw" id="bw{j}">{w}</span>' for j, (_, w) in enumerate(BRAND_WORDS))
        body = (
            f'<div class="clip graphic" id="g-{sid}" {timed}>'
            f'<div class="outro" id="outro">'
            f'<div class="keynote" id="br-ns">NS Brothers.</div>'
            f'<div class="br-words">{words}</div>'
            f'<div class="br-meta" id="br-meta">School Dress · Chandauthi More, Gaya</div>'
            f"</div></div>"
        )
    return f'<div class="scene" id="w-{sid}" style="z-index:{z}">{body}</div>'


def blur_in(sel, t, y=24, dur=0.6):
    return f"tl.from('{sel}', {{y:{y}, opacity:0, filter:'blur(14px)', duration:{dur}, ease:'power3.out'}}, {t:.2f});"


def build():
    by_id = {s[0]: s for s in SCENES}
    scenes = "\n      ".join(scene_html(i, s) for i, s in enumerate(SCENES))

    title = (
        '<div class="clip notif glass" id="notif" data-start="0" data-duration="5" data-track-index="9">'
        '<div class="app-icon"><img src="assets/logo.png" alt=""></div><div class="nf-text">'
        '<div class="nf-top"><span class="nf-app">NS Brothers</span><span class="nf-time">now</span></div>'
        '<div class="nf-body">D.A.V. Winter Uniform 2026-27 is now in store</div></div></div>'
    )
    caps = "\n      ".join(
        f'<div class="caption clip" id="cap{i}" data-start="{fmt(s)}" data-duration="{fmt(e - s)}" data-track-index="20">'
        f'<span class="cap-box glass-lite">{caption_html(t)}</span></div>'
        for i, (s, e, t) in enumerate(CAPTIONS)
    )
    items = "\n      ".join(
        f'<div class="item clip" id="item-{sid}" data-start="{fmt(t)}" '
        f'data-duration="{fmt(by_id[sid][2] - t)}" data-track-index="{21 + n % 2}">'
        f'<div class="item-box glass"><div class="item-icon">{SNOW_SVG}</div>'
        f'<div class="item-txt"><span class="item-title">{label}</span><span class="item-sub">{sub}</span></div></div></div>'
        for n, (sid, t, label, sub) in enumerate(ITEMS)
    )
    lists = []
    for n, (sid, head, row) in enumerate(CHIPS):
        dim = '<div class="dim"></div>' if sid == "recap" else ""
        rows = "".join(
            f'<div class="cl-row" id="clr-{sid}-{j}"><div class="cl-circle"><div class="cl-fill" id="clf-{sid}-{j}">{CHECK_SVG}</div></div>'
            f'<span class="cl-label">{label}</span></div>'
            for j, (_, label) in enumerate(row)
        )
        lists.append(
            f'<div class="clip" id="list-{sid}" data-start="{fmt(by_id[sid][1])}" data-duration="{fmt(by_id[sid][2] - by_id[sid][1])}" '
            f'data-track-index="{23 + n}" style="position:absolute;inset:0;z-index:205">{dim}'
            f'<div class="checklist glass" id="chips-{sid}"><div class="cl-head" id="chh-{sid}">{head}</div>{rows}</div></div>'
        )
    chips = "\n      ".join(lists)
    audio = "\n      ".join(
        f'<audio id="sfx{i}" src="assets/{s}" data-start="{fmt(max(st, 0))}" data-duration="{fmt(d)}" '
        f'data-track-index="{40 + i % 4}" data-volume="{v}"></audio>'
        for i, (s, st, d, v) in enumerate(sorted(SFX, key=lambda x: x[1]))
    )

    # Timeline JS
    js = []
    trans = {
        "slideL": ("{x:1080, filter:'blur(8px)'}", "{x:0, filter:'blur(0px)'}", "power3.inOut"),
        "slideR": ("{x:-1080, filter:'blur(8px)'}", "{x:0, filter:'blur(0px)'}", "power3.inOut"),
        "slideUp": ("{y:1920, filter:'blur(8px)'}", "{y:0, filter:'blur(0px)'}", "power3.inOut"),
        "zoom": ("{scale:0.88, opacity:0, filter:'blur(16px)'}", "{scale:1, opacity:1, filter:'blur(0px)'}", "power3.out"),
    }
    for i, (sid, start, end, kind, src, ms, tr, tag) in enumerate(SCENES):
        cs = start if i == 0 else start - ov(sid)
        if tr:
            frm, to, ease = trans[tr]
            js.append(f"tl.fromTo('#w-{sid}', {frm}, {{...{to}, duration:{ov(sid) + 0.1:.2f}, ease:'{ease}'}}, {cs:.2f});")
        if kind in ("video", "tour", "photo", "textcard", "maps"):
            js.append(f"tl.fromTo('#kb-{sid}', {{scale:1}}, {{scale:1.07, duration:{end - cs:.2f}, ease:'none'}}, {cs:.2f});")
        if isinstance(tag, str):
            js.append(f"tl.from('#tag-{sid}', {{x:-30, opacity:0, filter:'blur(10px)', duration:0.6, ease:'back.out(1.4)'}}, {start + 0.15:.2f});")
        if kind == "textcard":
            js.append(blur_in(f"#tck-{sid}", start - 0.05, 16, 0.5))
            js.append(f"tl.from('#tch-{sid}', {{scale:0.86, opacity:0, filter:'blur(20px)', duration:0.6, ease:'power3.out'}}, {start + 0.05:.2f});")
            js.append(blur_in(f"#tcs-{sid}", start + 0.35, 16, 0.5))
        if kind == "poster":
            js.append(blur_in(f"#ps-{sid}", start + 0.05, -20, 0.5))
            js.append(f"tl.fromTo('#pc-{sid}', {{scale:0.94}}, {{scale:1.03, duration:{end - cs:.2f}, ease:'power1.out'}}, {cs:.2f});")
            js.append(blur_in(f"#pl-{sid}", start + 0.15, 30, 0.6))

    js += [
        # opener: iOS notification
        "tl.from('#logo', {scale:0.6, opacity:0, filter:'blur(10px)', duration:0.7, ease:'back.out(1.6)'}, 0.15);",
        "tl.from('#notif', {y:-300, scale:0.92, opacity:0, duration:0.8, ease:'back.out(1.3)'}, 0.3);",
        # maps
        "tl.from('#pin', {y:-500, duration:0.7, ease:'bounce.out'}, 51.2);",
        "tl.fromTo('#pulse', {scale:0.3, opacity:0.9}, {scale:1.5, opacity:0, duration:0.9, repeat:2, ease:'power1.out'}, 51.85);",
        "tl.from('#map-label', {opacity:0, y:14, duration:0.4, ease:'power2.out'}, 51.8);",
        "tl.from('#sheet', {y:900, duration:0.7, ease:'power3.out'}, 51.4);",
        "tl.from('#directions', {scale:0.9, opacity:0, duration:0.5, ease:'back.out(1.8)'}, 52.4);",
    ]
    for j, (t, _) in enumerate(ADDRESS_LINES):
        js.append(blur_in(f"#al{j}", t, 16, 0.5))
    js += [
        # call screen
        blur_in("#ph-info", 54.55, 16, 0.5),
        "tl.from('#ph-avatar', {scale:0.6, opacity:0, duration:0.7, ease:'back.out(1.7)'}, 54.8);",
        blur_in("#ph-name", 55.05, 20, 0.6),
        blur_in("#ph-sub", 55.3, 14, 0.5),
        "tl.from('#ph-list', {y:60, opacity:0, scale:0.96, duration:0.6, ease:'power3.out'}, 56.6);",
        blur_in("#ph-n1 .num-v", 56.95, 16, 0.5),
        blur_in("#ph-n2 .num-v", 61.0, 16, 0.5),
        "tl.from('#ph-btns', {y:80, opacity:0, duration:0.7, ease:'back.out(1.5)'}, 61.9);",
        "tl.fromTo('#ring', {scale:1, opacity:0.8}, {scale:1.7, opacity:0, duration:1.1, repeat:2, ease:'power1.out'}, 62.4);",
        "tl.fromTo('#call', {scale:1}, {scale:1.03, duration:10.3, ease:'none'}, 54.45);",
        # keynote outro
        "tl.from('#br-ns', {scale:0.88, opacity:0, filter:'blur(24px)', duration:0.9, ease:'power3.out'}, 64.75);",
        blur_in("#br-meta", 68.0, 14, 0.5),
        "tl.fromTo('#outro', {scale:1}, {scale:1.04, duration:4.45, ease:'none'}, 64.75);",
        f"tl.to('#fade', {{opacity:1, duration:0.45, ease:'power1.in'}}, {DURATION - 0.5:.2f});",
    ]
    for j, (t, _) in enumerate(BRAND_WORDS):
        js.append(blur_in(f"#bw{j}", t, 20, 0.55))
    for i, (s, e, t) in enumerate(CAPTIONS):
        js.append(blur_in(f"#cap{i} .cap-box", s, 20, 0.5))
    for sid, t, _, _ in ITEMS:
        js.append(f"tl.from('#item-{sid} .item-box', {{y:80, scale:0.9, opacity:0, filter:'blur(12px)', duration:0.55, ease:'back.out(1.5)'}}, {t:.2f});")
    for sid, _, row in CHIPS:
        s0 = by_id[sid][1]
        js.append(f"tl.from('#chips-{sid}', {{y:120, opacity:0, scale:0.95, duration:0.6, ease:'back.out(1.3)'}}, {s0 - 0.2:.2f});")
        for j, (t, _) in enumerate(row):
            js.append(f"tl.from('#clr-{sid}-{j}', {{x:-30, opacity:0, duration:0.35, ease:'power2.out'}}, {s0 + 0.05 * j:.2f});")
            js.append(f"tl.from('#clf-{sid}-{j}', {{scale:0, duration:0.4, ease:'back.out(2.4)'}}, {t - 0.05:.2f});")
    js.append(f"tl.set({{}}, {{}}, {DURATION});")

    template = Path(__file__).with_name("template.html").read_text()
    html = (
        template.replace("{{DURATION}}", fmt(DURATION))
        .replace("{{VO_DURATION}}", fmt(VO_DURATION))
        .replace("{{SCENES}}", scenes)
        .replace("{{TITLE}}", title)
        .replace("{{CAPTIONS}}", caps)
        .replace("{{ITEMS}}", items + "\n      " + chips)
        .replace("{{AUDIO}}", audio)
        .replace("{{TIMELINE}}", "\n      ".join(js))
    )
    Path(__file__).parent.parent.joinpath("index.html").write_text(html)


if __name__ == "__main__":
    build()
