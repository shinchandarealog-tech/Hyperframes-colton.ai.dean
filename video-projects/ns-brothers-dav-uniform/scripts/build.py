#!/usr/bin/env python3
"""Generates index.html for the NS Brothers DAV uniform reel.

All timings are seconds on the voiceover (assets/voiceover.mp3, 57.97s).
Edit the tables below and re-run: python3 scripts/build.py
"""
from pathlib import Path

DURATION = 58.6
X = 0.3  # transition overlap: incoming scene starts this much before its cut

# (id, start, end, kind, source, media_start, transition, tag)
#   kind: video | tour (store-tour clip, cropped to hide burned-in badge/watermark)
#         poster | onestop | address | phone
SCENES = [
    ("storefront", 0.0, 6.1, "video", "storefront", 0.0, None, None),
    ("nurkids", 6.1, 9.5, "poster", "poster-nur-kids", 0, "zoom", ("CLASS NUR – II", "DAV WINTER UNIFORM")),
    ("tracksuit", 9.5, 12.3, "video", "tracksuit", 0.4, "whipL", "DAV TRACKSUIT"),
    ("seniors", 12.3, 13.8, "poster", "poster-912-kids", 0, "whipUp", ("CLASS IX – XII", "DAV WINTER UNIFORM")),
    ("smart", 13.8, 15.95, "poster", "poster-35-kids", 0, "whipR", ("CLASS III – V", "SMART LOOK")),
    ("blazer", 15.95, 17.0, "video", "blazer", 1.0, "zoom", "DAV BLAZER"),
    ("jacket", 17.0, 20.45, "video", "jacket", 4.5, "whipL", "DAV WINTER JACKET"),
    ("davjacket", 20.45, 22.3, "poster", "poster-nur-jacket", 0, "whipUp", ("DAV", "WINTER JACKET")),
    ("otherschools", 22.3, 25.4, "tour", "store-tour", 5.5, "whipR", "OTHER SCHOOLS TOO"),
    ("bags", 25.4, 26.15, "tour", "store-tour", 10.9, "zoom", None),
    ("stationery", 26.15, 27.1, "tour", "store-tour", 28.4, "whipL", None),
    ("lunch", 27.1, 28.2, "tour", "store-tour", 22.4, "whipUp", None),
    ("bottles", 28.2, 28.95, "tour", "store-tour", 9.85, "whipR", None),
    ("everything", 28.95, 32.7, "tour", "store-tour", 33.7, "zoom", None),
    ("oneroof", 32.7, 34.1, "tour", "store-tour", 24.2, "whipL", None),
    ("counter", 34.1, 37.95, "tour", "store-tour", 38.95, "whipUp", None),
    ("onestop", 37.95, 39.6, "onestop", None, 0, "zoom", None),
    ("visit", 39.6, 41.8, "video", "storefront", 3.8, "whipR", None),
    ("address", 41.8, 46.75, "address", None, 0, "zoom", None),
    ("phone", 46.75, DURATION, "phone", None, 0, "whipUp", None),
]

# Phrase captions — text from the script, timed to the voiceover.
# Words wrapped in *asterisks* are highlighted.
CAPTIONS = [
    (0.05, 2.95, "Gaya mein *DAV School* ke students ke liye"),
    (2.97, 5.9, "*NS Brothers* lekar aaya hai khaas uniform collection!"),
    (6.12, 9.3, "*DAV School* ke students aur parents, dhyan dijiye!"),
    (9.58, 12.28, "Aapke bachchon ki *DAV School Uniform*"),
    (12.3, 13.6, "ab milegi *NS Brothers* par!"),
    (13.9, 15.9, "School ki *smart look* uniform ho"),
    (15.9, 16.75, "ya *winter uniform*"),
    (17.0, 18.75, "*DAV School* ke uniform collection ke liye"),
    (18.76, 20.35, "aaiye *NS Brothers!*"),
    (20.5, 22.3, "Aur haan! *DAV* ke saath-saath,"),
    (22.3, 25.15, "*doosre schools* ki uniforms bhi yahan available hain"),
    (29.1, 32.6, "School ki zaroorat ka bahut kuchh, *ek hi jagah!*"),
    (32.85, 33.95, "*Ek chhat* ke neeche"),
    (34.19, 36.1, "Toh apne bachchon ki *school uniform* ke liye"),
    (36.1, 37.85, "kahin aur jaane ki *zaroorat nahi!*"),
    (39.68, 41.7, "Aaj hi visit karein *NS Brothers!*"),
]

# Big item labels — land exactly on the spoken word, over the matching shot.
ITEMS = [
    ("bags", 25.45, "SCHOOL BAGS"),
    ("stationery", 26.16, "STATIONERY"),
    ("lunch", 27.36, "LUNCH BOXES"),
    ("bottles", 28.22, "WATER BOTTLES"),
]

ADDRESS_LINES = [
    (41.95, "Near Punjab National Bank"),
    (43.36, "Chandauthi More"),
    (44.6, "Opp. Military Hospital Gate"),
    (45.85, "Gaya, Bihar"),
]

# (src, start, duration, volume)
SFX = (
    [("whoosh.mp3", s[1] - X - 0.05, 0.6, 0.35) for s in SCENES[1:] if s[0] not in {i[0] for i in ITEMS}]
    + [("pop.mp3", t - 0.05, 0.7, 0.45) for _, t, _ in ITEMS]
    + [("slam.mp3", 38.0, 1.2, 0.4), ("sparkle.mp3", 41.9, 2.0, 0.3), ("pop.mp3", 0.25, 0.7, 0.35)]
)


def fmt(t):
    return f"{t:.2f}".rstrip("0").rstrip(".") if t else "0"


def caption_html(text):
    out, hi = [], False
    for i, part in enumerate(text.split("*")):
        if part:
            out.append(f'<span class="hl">{part}</span>' if hi else part)
        hi = not hi
    return "".join(out)


def scene_html(i, sc):
    sid, start, end, kind, src, mstart, trans, tag = sc
    cs = start if i == 0 else start - X
    dur = end - cs
    track = 1 + (i % 2)
    z = 10 + i
    body = ""
    if kind in ("video", "tour"):
        crop = ' tour' if kind == "tour" else ""
        body = (
            f'<div class="kb" id="kb-{sid}"><div class="crop{crop}">'
            f'<video id="v-{sid}" src="assets/{src}.mp4" data-start="{fmt(cs)}" data-duration="{fmt(dur)}" '
            f'data-media-start="{fmt(mstart)}" data-track-index="{track}" muted playsinline></video>'
            f"</div></div>"
            f'<div class="shade clip" id="sh-{sid}" data-start="{fmt(cs)}" data-duration="{fmt(dur)}" data-track-index="{track + 2}"></div>'
        )
        if tag:
            body += (
                f'<div class="tag clip" id="tag-{sid}" data-start="{fmt(cs)}" data-duration="{fmt(dur)}" data-track-index="{track + 4}">'
                f"{tag}</div>"
            )
    elif kind == "poster":
        cls, sub = tag
        body = (
            f'<div class="clip poster" id="p-{sid}" data-start="{fmt(cs)}" data-duration="{fmt(dur)}" data-track-index="{track}">'
            f'<img class="poster-bg" src="assets/{src}.jpg" alt="">'
            f'<div class="poster-content">'
            f'<div class="pill school" id="ps-{sid}">DAV PUBLIC SCHOOL · GAYA JI</div>'
            f'<div class="card" id="pc-{sid}"><img src="assets/{src}.jpg" alt=""></div>'
            f'<div class="poster-label" id="pl-{sid}"><span class="cls">{cls}</span><span class="sub">{sub}</span></div>'
            f"</div></div>"
        )
    elif kind == "onestop":
        body = (
            f'<div class="clip graphic onestop" id="g-{sid}" data-start="{fmt(cs)}" data-duration="{fmt(dur)}" data-track-index="{track}">'
            f'<div class="os-line" id="os1">ONE STOP</div><div class="os-line yellow" id="os2">SOLUTION</div>'
            f'<div class="os-sub" id="os3">Uniforms · Bags · Stationery · Bottles</div></div>'
        )
    elif kind == "address":
        lines = "".join(
            f'<div class="addr-line" id="al{j}"><span class="dot"></span>{t}</div>' for j, (_, t) in enumerate(ADDRESS_LINES)
        )
        body = (
            f'<div class="clip graphic address" id="g-{sid}" data-start="{fmt(cs)}" data-duration="{fmt(dur)}" data-track-index="{track}">'
            f'<div class="addr-content">'
            f'<svg id="pin" viewBox="0 0 100 130" width="170" height="221"><path d="M50 4C25 4 6 23 6 48c0 33 44 76 44 76s44-43 44-76C94 23 75 4 50 4z" fill="#E3262B"/><circle cx="50" cy="48" r="17" fill="#FFD60A"/></svg>'
            f'<div class="visit" id="ad-visit">VISIT</div>'
            f'<div class="brand" id="ad-brand">NS BROTHERS</div>'
            f'<div class="city" id="ad-city">GAYA</div>'
            f'<div class="addr-lines">{lines}</div>'
            f"</div></div>"
        )
    elif kind == "phone":
        body = (
            f'<div class="clip graphic phone" id="g-{sid}" data-start="{fmt(cs)}" data-duration="{fmt(dur)}" data-track-index="{track}">'
            f'<div class="ph-content">'
            f'<div class="ph-brand" id="ph-ns">NS</div><div class="ph-brand" id="ph-bro">BROTHERS</div>'
            f'<div class="ph-call" id="ph-call">CALL NOW</div>'
            f'<div class="ph-num" id="ph-n1">+91 94708 54055</div>'
            f'<div class="ph-num" id="ph-n2">+91 75418 54737</div>'
            f'<div class="ph-sd" id="ph-sd">SCHOOL DRESS</div>'
            f'<div class="ph-addr" id="ph-addr">Chandauthi More, Gaya</div>'
            f"</div></div>"
        )
    return f'<div class="scene" id="w-{sid}" style="z-index:{z}">{body}</div>'


def build():
    scenes = "\n      ".join(scene_html(i, s) for i, s in enumerate(SCENES))

    title = (
        '<div class="clip title" id="title" data-start="0" data-duration="6.1" data-track-index="9" style="z-index:12">'
        '<div class="t-ns" id="t-ns">NS BROTHERS</div>'
        '<div class="t-sd" id="t-sd">SCHOOL DRESS · GAYA</div>'
        '<div class="t-dav" id="t-dav">DAV UNIFORM COLLECTION</div></div>'
    )
    caps = "\n      ".join(
        f'<div class="caption clip" id="cap{i}" data-start="{fmt(s)}" data-duration="{fmt(e - s)}" data-track-index="20">'
        f'<span class="cap-box">{caption_html(t)}</span></div>'
        for i, (s, e, t) in enumerate(CAPTIONS)
    )
    items = "\n      ".join(
        f'<div class="item clip" id="item-{sid}" data-start="{fmt(t)}" '
        f'data-duration="{fmt(next(s[2] for s in SCENES if s[0] == sid) - t)}" data-track-index="{21 + n % 2}">'
        f'<span class="item-box">{label}</span></div>'
        for n, (sid, t, label) in enumerate(ITEMS)
    )
    audio = "\n      ".join(
        f'<audio id="sfx{i}" src="assets/{s}" data-start="{fmt(max(st, 0))}" data-duration="{fmt(d)}" '
        f'data-track-index="{40 + i % 4}" data-volume="{v}"></audio>'
        for i, (s, st, d, v) in enumerate(sorted(SFX, key=lambda x: x[1]))
    )

    # Timeline JS
    js = []
    trans = {
        "whipL": ("{x:1080, skewX:-10, filter:'blur(36px)'}", "{x:0, skewX:0, filter:'blur(0px)'}", "power3.out"),
        "whipR": ("{x:-1080, skewX:10, filter:'blur(36px)'}", "{x:0, skewX:0, filter:'blur(0px)'}", "power3.out"),
        "whipUp": ("{y:1920, filter:'blur(36px)'}", "{y:0, filter:'blur(0px)'}", "expo.out"),
        "zoom": ("{scale:1.6, opacity:0, filter:'blur(28px)'}", "{scale:1, opacity:1, filter:'blur(0px)'}", "power2.out"),
    }
    for i, (sid, start, end, kind, src, ms, tr, tag) in enumerate(SCENES):
        cs = start if i == 0 else start - X
        if tr:
            frm, to, ease = trans[tr]
            js.append(f"tl.fromTo('#w-{sid}', {frm}, {{...{to}, duration:{X + 0.08}, ease:'{ease}'}}, {cs:.2f});")
            js.append(f"tl.fromTo('#flash', {{opacity:0}}, {{opacity:0.35, duration:0.12, yoyo:true, repeat:1, ease:'sine.inOut'{'' if i == 1 else ', immediateRender:false'}}}, {start - 0.12:.2f});")
        if kind in ("video", "tour"):
            js.append(f"tl.fromTo('#kb-{sid}', {{scale:1}}, {{scale:1.07, duration:{end - cs:.2f}, ease:'none'}}, {cs:.2f});")
            if tag:
                js.append(f"tl.from('#tag-{sid}', {{x:-80, opacity:0, duration:0.45, ease:'back.out(1.8)'}}, {start + 0.15:.2f});")
        if kind == "poster":
            js.append(f"tl.from('#ps-{sid}', {{y:-60, opacity:0, duration:0.4, ease:'power3.out'}}, {start + 0.05:.2f});")
            js.append(f"tl.fromTo('#pc-{sid}', {{rotation:-2}}, {{rotation:1.5, scale:1.04, duration:{end - start + X:.2f}, ease:'none'}}, {cs:.2f});")
            js.append(f"tl.from('#pl-{sid}', {{y:60, opacity:0, duration:0.45, ease:'back.out(1.6)'}}, {start + 0.15:.2f});")

    js += [
        # opener title
        "tl.from('#t-ns', {scale:2.2, opacity:0, filter:'blur(20px)', duration:0.55, ease:'expo.out'}, 0.25);",
        "tl.from('#t-sd', {y:30, opacity:0, duration:0.4, ease:'power2.out'}, 0.7);",
        "tl.from('#t-dav', {scaleX:0, duration:0.5, ease:'power4.out'}, 4.2);",
        # one stop
        "tl.from('#os1', {x:-900, filter:'blur(30px)', duration:0.4, ease:'expo.out'}, 38.05);",
        "tl.from('#os2', {x:900, filter:'blur(30px)', duration:0.4, ease:'expo.out'}, 38.3);",
        "tl.from('#os3', {y:40, opacity:0, duration:0.4, ease:'power2.out'}, 38.65);",
        "tl.fromTo('#g-onestop', {scale:1}, {scale:1.06, duration:1.95, ease:'none'}, 37.65);",
        # address
        "tl.from('#pin', {y:-400, duration:0.6, ease:'bounce.out'}, 41.65);",
        "tl.from('#ad-visit', {opacity:0, y:20, duration:0.3, ease:'power2.out'}, 41.9);",
        "tl.from('#ad-brand', {opacity:0, scale:1.4, duration:0.4, ease:'power3.out'}, 42.0);",
        "tl.from('#ad-city', {opacity:0, scale:0.5, duration:0.5, ease:'back.out(2)'}, 42.2);",
    ]
    for j, (t, _) in enumerate(ADDRESS_LINES):
        js.append(f"tl.from('#al{j}', {{x:-120, opacity:0, duration:0.4, ease:'power3.out'}}, {t:.2f});")
    js += [
        "tl.fromTo('#pin', {rotation:-4}, {rotation:4, duration:1.2, yoyo:true, repeat:3, ease:'sine.inOut'}, 42.3);",
        # phone
        "tl.from('#ph-ns', {y:-200, opacity:0, duration:0.5, ease:'expo.out'}, 46.6);",
        "tl.from('#ph-bro', {y:200, opacity:0, duration:0.5, ease:'expo.out'}, 46.7);",
        "tl.from('#ph-call', {opacity:0, y:24, duration:0.5, ease:'power2.out'}, 46.95);",
        "tl.from('#ph-n1', {scale:0.6, opacity:0, duration:0.45, ease:'back.out(2)'}, 47.1);",
        "tl.from('#ph-n2', {scale:0.6, opacity:0, duration:0.45, ease:'back.out(2)'}, 52.0);",
        "tl.from('#ph-sd', {scaleX:0, duration:0.45, ease:'power4.out'}, 55.75);",
        "tl.from('#ph-addr', {opacity:0, y:20, duration:0.4, ease:'power2.out'}, 56.2);",
        "tl.fromTo('.ph-content', {scale:1}, {scale:1.05, duration:11.8, ease:'none'}, 46.75);",
        "tl.to('#fade', {opacity:1, duration:0.45, ease:'power1.in'}, 58.1);",
    ]
    for i, (s, e, t) in enumerate(CAPTIONS):
        js.append(f"tl.from('#cap{i} .cap-box', {{y:40, scale:0.85, opacity:0, duration:0.28, ease:'back.out(2)'}}, {s:.2f});")
    for sid, t, _ in ITEMS:
        js.append(f"tl.from('#item-{sid} .item-box', {{scale:2.4, opacity:0, rotation:-6, duration:0.3, ease:'expo.out'}}, {t:.2f});")
    js.append(f"tl.set({{}}, {{}}, {DURATION});")

    template = Path(__file__).with_name("template.html").read_text()
    html = (
        template.replace("{{DURATION}}", fmt(DURATION))
        .replace("{{SCENES}}", scenes)
        .replace("{{TITLE}}", title)
        .replace("{{CAPTIONS}}", caps)
        .replace("{{ITEMS}}", items)
        .replace("{{AUDIO}}", audio)
        .replace("{{TIMELINE}}", "\n      ".join(js))
    )
    Path(__file__).parent.parent.joinpath("index.html").write_text(html)


if __name__ == "__main__":
    build()
