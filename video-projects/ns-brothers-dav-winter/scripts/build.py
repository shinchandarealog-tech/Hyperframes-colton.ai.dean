#!/usr/bin/env python3
"""Generates index.html for the NS Brothers DAV winter-uniform reel.

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
#         photo | poster | textcard | address | phone | brand
#   poster tag = (big label, small label); textcard tag = (headline, subline)
SCENES = [
    ("storefront", 0.0, 5.0, "video", "storefront", 0.0, None, None),
    ("seniors", 5.0, 8.15, "poster", "poster-912-kids", 0, "fade", ("CLASS IX – XII", "SMART & WARM")),
    ("jacket", 8.15, 12.1, "video", "jacket", 3.55, "slideL", "DAV Winter Jacket"),
    ("juniors", 12.1, 14.55, "poster", "poster-35-kids", 0, "slideUp", ("CLASS III – V", "DAV SCHOOL UNIFORM")),
    ("uniformset", 14.55, 18.2, "poster", "poster-68-kids", 0, "fade", ("CLASS VI – VIII", "")),
    ("blazer", 18.2, 20.9, "video", "blazer", 0.6, "slideL", "DAV Blazer"),
    ("jacketfront", 20.9, 25.1, "photo", "jacket-front", 0, "fade", "Winter Essentials"),
    ("sweaters", 25.1, 27.3, "poster", "poster-sweaters", 0, "slideUp", ("HALF & FULL SLEEVE", "NAVY BLUE · WOOL")),
    ("tracksuit", 27.3, 28.8, "video", "tracksuit", 1.2, "slideL", None),
    ("caps", 28.8, 30.3, "textcard", "shot-everything", 0, "slideL", ("Winter Caps", "Warm · Comfortable · School-ready")),
    ("nurkids", 30.3, 34.6, "poster", "poster-nur-kids", 0, "fade", ("CLASS NUR – II", "WARM & SMART")),
    ("oneroof", 34.6, 36.6, "tour", "shot-oneroof", 0, "slideR", None),
    ("shoes", 36.6, 38.4, "tour", "shot-shoes", 0, "slideL", None),
    ("counter", 38.4, 42.7, "tour", "shot-counter", 0, "fade", None),
    ("recap", 42.7, 46.45, "tour", "shot-everything", 0, "slideUp", None),
    ("shopping", 46.45, 49.4, "tour", "shot-shopping", 0, "fade", None),
    ("visit", 49.4, 51.45, "video", "storefront", 3.65, "slideUp", None),
    ("address", 51.45, 54.45, "address", None, 0, "fade", None),
    ("phone", 54.45, 64.75, "phone", None, 0, "slideUp", None),
    ("brand", 64.75, DURATION, "brand", None, 0, "fade", None),
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

# Big item labels — land exactly on the spoken word, over the matching shot.
ITEMS = [
    ("sweaters", 25.9, "WINTER SWEATERS"),
    ("tracksuit", 27.35, "FLEECE TRACKSUITS"),
    ("shoes", 37.4, "SHOES & SOCKS"),
]

# Chip rows that build word by word: (scene id, heading, [(time, label), ...])
CHIPS = [
    ("uniformset", "Complete D.A.V. Uniform",
     [(15.0, "Shirt"), (15.88, "Tie"), (16.35, "Trousers"), (16.96, "Blazer"), (17.68, "Skirt")]),
    ("recap", "Is Winter",
     [(43.45, "Uniform"), (44.4, "Sweater"), (45.0, "Shoes"), (45.8, "Cap")]),
]

ADDRESS_LINES = [
    (51.54, "Near Punjab National Bank"),
    (53.0, "Chandauthi More"),
    (53.92, "Gaya, Bihar"),
]

BRAND_WORDS = [(66.13, "Quality"), (66.85, "Style"), (67.6, "Trust")]

# (src, start, duration, volume)
SFX = (
    [("whoosh.mp3", s[1] - ov(s[0]), 0.6, 0.18) for s in SCENES[1:] if s[0] not in QUICK]
    + [("pop.mp3", t - 0.05, 0.7, 0.25) for _, t, _ in ITEMS]
    + [("pop.mp3", 28.85, 0.7, 0.25)]
    + [("pop.mp3", t - 0.03, 0.7, 0.16) for _, _, chips in CHIPS for t, _ in chips]
    + [("sparkle.mp3", 51.5, 2.0, 0.3), ("slam.mp3", 64.85, 1.2, 0.22), ("pop.mp3", 0.25, 0.7, 0.35)]
)


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
    body = ""
    if kind in ("video", "tour"):
        crop = " tour" if kind == "tour" else ""
        body = (
            f'<div class="kb" id="kb-{sid}"><div class="crop{crop}">'
            f'<video id="v-{sid}" src="assets/{src}-hd.mp4" {timed} data-media-start="{fmt(mstart)}" muted playsinline></video>'
            f"</div></div>"
            f'<div class="shade clip" id="sh-{sid}" data-start="{fmt(cs)}" data-duration="{fmt(dur)}" data-track-index="{track + 2}"></div>'
        )
        if tag:
            body += (
                f'<div class="tag clip" id="tag-{sid}" data-start="{fmt(cs)}" data-duration="{fmt(dur)}" data-track-index="{track + 4}">'
                f"{tag}</div>"
            )
    elif kind == "textcard":
        head, sub = tag
        body = (
            f'<div class="kb" id="kb-{sid}"><div class="crop tour blurred">'
            f'<video id="v-{sid}" src="assets/{src}-hd.mp4" {timed} data-media-start="{fmt(mstart)}" muted playsinline></video>'
            f"</div></div>"
            f'<div class="clip textcard" id="tc-{sid}" data-start="{fmt(cs)}" data-duration="{fmt(dur)}" data-track-index="{track + 2}">'
            f'<div class="tc-kicker" id="tck-{sid}">STYLISH</div>'
            f'<div class="tc-head" id="tch-{sid}">{head}</div>'
            f'<div class="tc-sub" id="tcs-{sid}">{sub}</div></div>'
        )
    elif kind == "photo":
        body = (
            f'<div class="clip photo" id="p-{sid}" {timed}>'
            f'<div class="kb" id="kb-{sid}"><img src="assets/{src}.jpg" alt=""></div>'
            f'<div class="shade"></div>'
            f'<div class="tag" id="tag-{sid}">{tag}</div></div>'
        )
    elif kind == "poster":
        cls, sub = tag
        sub_html = f'<span class="sub">{sub}</span>' if sub else ""
        body = (
            f'<div class="clip poster" id="p-{sid}" {timed}>'
            f'<img class="poster-bg" src="assets/{src}.jpg" alt="">'
            f'<div class="poster-content">'
            f'<div class="pill school" id="ps-{sid}">DAV PUBLIC SCHOOL · GAYA JI</div>'
            f'<div class="card" id="pc-{sid}"><img src="assets/{src}.jpg" alt=""></div>'
            f'<div class="poster-label" id="pl-{sid}"><span class="cls">{cls}</span>{sub_html}</div>'
            f"</div></div>"
        )
    elif kind == "address":
        lines = "".join(
            f'<div class="addr-line" id="al{j}"><span class="dot"></span>{t}</div>' for j, (_, t) in enumerate(ADDRESS_LINES)
        )
        body = (
            f'<div class="clip graphic address" id="g-{sid}" {timed}>'
            f'<div class="addr-content">'
            f'<svg id="pin" viewBox="0 0 100 130" width="170" height="221"><path d="M50 4C25 4 6 23 6 48c0 33 44 76 44 76s44-43 44-76C94 23 75 4 50 4z" fill="#A9D2F5"/><circle cx="50" cy="48" r="17" fill="#0A1236"/></svg>'
            f'<div class="visit" id="ad-visit">VISIT</div>'
            f'<div class="brand" id="ad-brand">NS BROTHERS</div>'
            f'<div class="city" id="ad-city">GAYA</div>'
            f'<div class="addr-lines">{lines}</div>'
            f"</div></div>"
        )
    elif kind == "phone":
        body = (
            f'<div class="clip graphic phone" id="g-{sid}" {timed}>'
            f'<div class="ph-content">'
            f'<div class="ph-call" id="ph-info">ZYADA JAANKARI KE LIYE</div>'
            f'<div class="ph-brand" id="ph-ns">CALL</div><div class="ph-brand" id="ph-bro">NOW</div>'
            f'<div class="ph-num" id="ph-n1">+91 94708 54055</div>'
            f'<div class="ph-num" id="ph-n2">+91 75418 54737</div>'
            f'<div class="ph-addr" id="ph-addr">NS Brothers · Chandauthi More, Gaya</div>'
            f"</div></div>"
        )
    elif kind == "brand":
        words = "".join(
            f'<span class="bw" id="bw{j}">{w}</span>' + ('<span class="bdot">·</span>' if j < len(BRAND_WORDS) - 1 else "")
            for j, (_, w) in enumerate(BRAND_WORDS)
        )
        body = (
            f'<div class="clip graphic brandcard" id="g-{sid}" {timed}>'
            f'<div class="ph-content">'
            f'<div class="ph-brand" id="br-ns">NS</div><div class="ph-brand" id="br-bro">BROTHERS</div>'
            f'<div class="br-words">{words}</div>'
            f'<div class="ph-sd" id="br-sd">SCHOOL DRESS</div>'
            f'<div class="ph-addr" id="br-addr">Chandauthi More, Gaya</div>'
            f"</div></div>"
        )
    return f'<div class="scene" id="w-{sid}" style="z-index:{z}">{body}</div>'


def build():
    by_id = {s[0]: s for s in SCENES}
    scenes = "\n      ".join(scene_html(i, s) for i, s in enumerate(SCENES))

    title = (
        '<div class="clip title" id="title" data-start="0" data-duration="5" data-track-index="9" style="z-index:12">'
        '<div class="t-ns" id="t-ns">NS BROTHERS</div>'
        '<div class="t-sd" id="t-sd">SCHOOL DRESS · GAYA</div>'
        '<div class="t-dav" id="t-dav">D.A.V. WINTER UNIFORM 2026-27</div></div>'
    )
    caps = "\n      ".join(
        f'<div class="caption clip" id="cap{i}" data-start="{fmt(s)}" data-duration="{fmt(e - s)}" data-track-index="20">'
        f'<span class="cap-box">{caption_html(t)}</span></div>'
        for i, (s, e, t) in enumerate(CAPTIONS)
    )
    items = "\n      ".join(
        f'<div class="item clip" id="item-{sid}" data-start="{fmt(t)}" '
        f'data-duration="{fmt(by_id[sid][2] - t)}" data-track-index="{21 + n % 2}">'
        f'<span class="item-box">{label}</span></div>'
        for n, (sid, t, label) in enumerate(ITEMS)
    )
    chips = "\n      ".join(
        f'<div class="chips clip" id="chips-{sid}" data-start="{fmt(by_id[sid][1])}" '
        f'data-duration="{fmt(by_id[sid][2] - by_id[sid][1])}" data-track-index="{23 + n}">'
        f'<div class="chips-head" id="chh-{sid}">{head}</div><div class="chip-row">'
        + "".join(f'<span class="chip" id="chip-{sid}-{j}">{label}</span>' for j, (_, label) in enumerate(row))
        + "</div></div>"
        for n, (sid, head, row) in enumerate(CHIPS)
    )
    audio = "\n      ".join(
        f'<audio id="sfx{i}" src="assets/{s}" data-start="{fmt(max(st, 0))}" data-duration="{fmt(d)}" '
        f'data-track-index="{40 + i % 4}" data-volume="{v}"></audio>'
        for i, (s, st, d, v) in enumerate(sorted(SFX, key=lambda x: x[1]))
    )

    # Timeline JS
    js = []
    trans = {
        "slideL": ("{x:1080, filter:'blur(10px)'}", "{x:0, filter:'blur(0px)'}", "power2.inOut"),
        "slideR": ("{x:-1080, filter:'blur(10px)'}", "{x:0, filter:'blur(0px)'}", "power2.inOut"),
        "slideUp": ("{y:1920, filter:'blur(10px)'}", "{y:0, filter:'blur(0px)'}", "power2.inOut"),
        "fade": ("{scale:1.08, opacity:0}", "{scale:1, opacity:1}", "sine.inOut"),
    }
    for i, (sid, start, end, kind, src, ms, tr, tag) in enumerate(SCENES):
        cs = start if i == 0 else start - ov(sid)
        if tr:
            frm, to, ease = trans[tr]
            js.append(f"tl.fromTo('#w-{sid}', {frm}, {{...{to}, duration:{ov(sid)}, ease:'{ease}'}}, {cs:.2f});")
            js.append(f"tl.fromTo('#flash', {{opacity:0}}, {{opacity:0.08, duration:0.15, yoyo:true, repeat:1, ease:'sine.inOut'{'' if i == 1 else ', immediateRender:false'}}}, {start - 0.15:.2f});")
        if kind in ("video", "tour", "photo", "textcard"):
            js.append(f"tl.fromTo('#kb-{sid}', {{scale:1}}, {{scale:1.07, duration:{end - cs:.2f}, ease:'none'}}, {cs:.2f});")
            if tag and kind != "textcard":
                js.append(f"tl.from('#tag-{sid}', {{x:-40, opacity:0, duration:0.6, ease:'power2.out'}}, {start + 0.15:.2f});")
        if kind == "textcard":
            js.append(f"tl.from('#tck-{sid}', {{y:20, opacity:0, duration:0.4, ease:'power2.out'}}, {start - 0.05:.2f});")
            js.append(f"tl.from('#tch-{sid}', {{y:30, opacity:0, duration:0.45, ease:'power2.out'}}, {start + 0.05:.2f});")
            js.append(f"tl.from('#tcs-{sid}', {{y:20, opacity:0, duration:0.4, ease:'power2.out'}}, {start + 0.35:.2f});")
        if kind == "poster":
            js.append(f"tl.from('#ps-{sid}', {{y:-60, opacity:0, duration:0.4, ease:'power3.out'}}, {start + 0.05:.2f});")
            js.append(f"tl.fromTo('#pc-{sid}', {{rotation:-1.5}}, {{rotation:1, scale:1.04, duration:{end - cs:.2f}, ease:'none'}}, {cs:.2f});")
            js.append(f"tl.from('#pl-{sid}', {{y:40, opacity:0, duration:0.5, ease:'power2.out'}}, {start + 0.15:.2f});")

    js += [
        # opener title
        "tl.from('#t-ns', {y:30, opacity:0, duration:0.8, ease:'power2.out'}, 0.25);",
        "tl.from('#t-sd', {y:30, opacity:0, duration:0.4, ease:'power2.out'}, 0.7);",
        "tl.from('#t-dav', {y:20, opacity:0, duration:0.6, ease:'power2.out'}, 3.0);",
        # address
        "tl.from('#pin', {y:-400, duration:0.6, ease:'bounce.out'}, 51.3);",
        "tl.from('#ad-visit', {opacity:0, y:20, duration:0.3, ease:'power2.out'}, 51.45);",
        "tl.from('#ad-brand', {opacity:0, y:30, duration:0.4, ease:'power2.out'}, 51.5);",
        "tl.from('#ad-city', {opacity:0, y:30, duration:0.5, ease:'power2.out'}, 51.7);",
        "tl.fromTo('#pin', {rotation:-4}, {rotation:4, duration:1.0, yoyo:true, repeat:2, ease:'sine.inOut'}, 51.9);",
    ]
    for j, (t, _) in enumerate(ADDRESS_LINES):
        js.append(f"tl.from('#al{j}', {{x:-80, opacity:0, duration:0.45, ease:'power2.out'}}, {t:.2f});")
    js += [
        # phone
        "tl.from('#ph-info', {opacity:0, y:24, duration:0.5, ease:'power2.out'}, 54.55);",
        "tl.from('#ph-ns', {y:-120, opacity:0, duration:0.6, ease:'power3.out'}, 55.0);",
        "tl.from('#ph-bro', {y:120, opacity:0, duration:0.6, ease:'power3.out'}, 55.15);",
        "tl.from('#ph-n1', {y:30, opacity:0, duration:0.5, ease:'power2.out'}, 56.95);",
        "tl.from('#ph-n2', {y:30, opacity:0, duration:0.5, ease:'power2.out'}, 61.0);",
        "tl.from('#ph-addr', {opacity:0, y:20, duration:0.4, ease:'power2.out'}, 61.8);",
        "tl.fromTo('#g-phone .ph-content', {scale:1}, {scale:1.04, duration:10.75, ease:'none'}, 54.0);",
        # brand outro
        "tl.from('#br-ns', {y:-120, opacity:0, duration:0.6, ease:'power3.out'}, 64.8);",
        "tl.from('#br-bro', {y:120, opacity:0, duration:0.6, ease:'power3.out'}, 64.95);",
        "tl.from('#br-sd', {y:20, opacity:0, duration:0.5, ease:'power2.out'}, 68.0);",
        "tl.from('#br-addr', {opacity:0, y:20, duration:0.4, ease:'power2.out'}, 68.2);",
        "tl.from('.bdot', {opacity:0, duration:0.3, stagger:0.7}, 66.5);",
        "tl.fromTo('#g-brand .ph-content', {scale:1}, {scale:1.04, duration:4.9, ease:'none'}, 64.3);",
        f"tl.to('#fade', {{opacity:1, duration:0.45, ease:'power1.in'}}, {DURATION - 0.5:.2f});",
    ]
    for j, (t, _) in enumerate(BRAND_WORDS):
        js.append(f"tl.from('#bw{j}', {{y:24, opacity:0, duration:0.45, ease:'power2.out'}}, {t:.2f});")
    for i, (s, e, t) in enumerate(CAPTIONS):
        js.append(f"tl.from('#cap{i} .cap-box', {{y:24, opacity:0, duration:0.45, ease:'power2.out'}}, {s:.2f});")
    for sid, t, _ in ITEMS:
        js.append(f"tl.from('#item-{sid} .item-box', {{y:30, opacity:0, duration:0.35, ease:'power2.out'}}, {t:.2f});")
    for sid, _, row in CHIPS:
        js.append(f"tl.from('#chh-{sid}', {{y:20, opacity:0, duration:0.4, ease:'power2.out'}}, {by_id[sid][1]:.2f});")
        for j, (t, _) in enumerate(row):
            js.append(f"tl.from('#chip-{sid}-{j}', {{y:24, opacity:0, duration:0.35, ease:'power2.out'}}, {t - 0.05:.2f});")
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
