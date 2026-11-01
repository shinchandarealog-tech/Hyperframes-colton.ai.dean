#!/usr/bin/env python3
"""Generate index.html for the GCN Silver Merchant Diwali reel from the shot list
in scripts/shots.json. Re-run after editing the shot list:  python3 scripts/build.py
"""
import json, html, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
cfg = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf-8"))

TOTAL = cfg["total"]
VO_END = cfg["vo_end"]
XF = 0.5          # crossfade length (incoming starts XF before the cut)
TAIL = 0.1        # outgoing keeps playing this long after the cut
shots = cfg["shots"]
END_T = cfg["endcard_at"]

def f(x):  # frame-snap at 30fps
    return round(round(x * 30) / 30, 4)

clips_html, kp_html, hl_html, js = [], [], [], []

for i, s in enumerate(shots):
    t0 = s["t"]
    t1 = shots[i + 1]["t"] if i + 1 < len(shots) else END_T
    start = 0 if i == 0 else f(t0 - XF)
    end = f(min(t1 + TAIL + (XF if i + 1 == len(shots) else 0), TOTAL))
    dur = f(end - start)
    ms = s.get("ms", 0.0)
    if i > 0:
        ms = max(0.0, ms - XF)
    sid = f"s{i:02d}"
    pos = s.get("pos", "50% 50%")
    if s.get("img"):
        media = f'<img class="clip" id="{sid}-v" src="assets/{s["img"]}" data-start="{start}" data-duration="{dur}" data-track-index="{i % 2}" alt="" />'
    else:
        media = f'<video id="{sid}-v" src="assets/clips/{s["clip"]}.mp4" data-start="{start}" data-duration="{dur}" data-media-start="{f(ms)}" data-track-index="{i % 2}" muted playsinline style="object-position:{pos}"></video>'
    clips_html.append(
        f'''    <div class="shot" id="{sid}" style="z-index:{10 + i}">
      <div class="kb" id="{sid}-kb">
        {media}
      </div>
    </div>''')
    # ken-burns drift (alternating push-in / pull-out, slight pan)
    if not s.get("still"):
        z0, z1 = (1.0, 1.07) if i % 2 == 0 else (1.07, 1.0)
        dx = s.get("pan", 0)
        js.append(f'tl.fromTo("#{sid}-kb", {{scale:{z0}, x:0}}, {{scale:{z1}, x:{dx}, duration:{f(dur)}, ease:"none"}}, {start});')
    for h in s.get("hl", []):
        hid = f'hl{len(hl_html):02d}'
        hl_html.append(f'    <div class="hl clip" id="{hid}" data-start="{f(h["t0"])}" data-duration="{f(h["t1"] - h["t0"])}" data-track-index="{6 + len(hl_html) % 2}" style="top:{h["top"]}px;height:{h["h"]}px;left:{h.get("l",30)}px;right:{h.get("r",30)}px"><i></i></div>')
        js.append(f'tl.from("#{hid}", {{opacity:0, scale:1.06, duration:0.35, ease:"power2.out"}}, {f(h["t0"])});')
        js.append(f'tl.fromTo("#{hid} i", {{xPercent:-120}}, {{xPercent:420, duration:0.9, ease:"power2.inOut"}}, {f(h["t0"] + 0.15)});')
        js.append(f'tl.to("#{hid}", {{opacity:0, duration:0.25, ease:"power1.in"}}, {f(h["t1"] - 0.25)});')
    if i > 0:
        kind = s.get("tr", "leak")
        if kind == "none":
            pass
        elif kind == "push":
            js.append(f'tl.set("#{sid}", {{opacity:0}}, 0);')
            js.append(f'tl.fromTo("#{sid}", {{opacity:0, y:140, filter:"blur(18px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:{XF + 0.1}, ease:"power2.out"}}, {start});')
        elif kind == "zoom":
            js.append(f'tl.set("#{sid}", {{opacity:0}}, 0);')
            js.append(f'tl.fromTo("#{sid}", {{opacity:0, scale:1.25, filter:"blur(22px) brightness(1.6)"}}, {{opacity:1, scale:1, filter:"blur(0px) brightness(1)", duration:{XF + 0.1}, ease:"power3.out"}}, {start});')
        else:  # leak / blur crossfade
            js.append(f'tl.set("#{sid}", {{opacity:0}}, 0);')
            js.append(f'tl.fromTo("#{sid}", {{opacity:0, filter:"blur(20px) brightness(1.35)"}}, {{opacity:1, filter:"blur(0px) brightness(1)", duration:{XF + 0.1}, ease:"sine.inOut"}}, {start});')
        if kind in ("leak", "zoom"):
            T = f(t0 - XF * 0.6)
            js.append(f'tl.fromTo("#leak-a", {{opacity:0, xPercent:-30}}, {{opacity:0.75, xPercent:5, duration:0.3333, ease:"sine.in", immediateRender:false}}, {T});')
            js.append(f'tl.to("#leak-a", {{opacity:0, xPercent:30, duration:0.45, ease:"sine.out"}}, {f(T + 0.3333)});')
            js.append(f'tl.fromTo("#leak-b", {{opacity:0, yPercent:20}}, {{opacity:0.55, yPercent:-5, duration:0.4, ease:"sine.in", immediateRender:false}}, {f(T + 0.05)});')
            js.append(f'tl.to("#leak-b", {{opacity:0, yPercent:-25, duration:0.45, ease:"sine.out"}}, {f(T + 0.45)});')

    # key-phrase text (only on shots without baked-in text)
    if s.get("text"):
        kid = f"kp{i:02d}"
        k_start = f(t0 + s.get("text_delay", 0.25))
        k_end = f(t1 + 0.05)
        lines = []
        for li, line in enumerate(s["text"]):
            words = "".join(f'<span class="w">{html.escape(w)}</span> ' for w in line.split())
            cls = ("l1" if li == 0 else "l2") + (" latin" if s.get("latin") else "")
            lines.append(f'<div class="{cls}">{words.strip()}</div>')
        kp_html.append(
            f'''    <div class="kp clip" id="{kid}" data-start="{k_start}" data-duration="{f(k_end - k_start)}" data-track-index="{4 + (i % 2)}">
      <div class="kp-inner">{"".join(lines)}<div class="rule"></div></div>
    </div>''')
        js.append(f'tl.to("#scrim", {{opacity:1, duration:0.4, ease:"sine.out"}}, {k_start});')
        js.append(f'tl.to("#scrim", {{opacity:0, duration:0.4, ease:"sine.in"}}, {f(t1 - 0.55)});')
        js.append(f'tl.from("#{kid} .w", {{y:36, opacity:0, filter:"blur(10px)", duration:0.55, ease:"power3.out", stagger:0.09}}, {f(k_start + 0.05)});')
        js.append(f'tl.from("#{kid} .rule", {{scaleX:0, opacity:0, duration:0.7, ease:"expo.out"}}, {f(k_start + 0.25)});')
        js.append(f'tl.from("#{kid} .kp-inner", {{scale:0.94, duration:1.2, ease:"sine.out"}}, {k_start});')
        js.append(f'tl.to("#{kid} .kp-inner", {{opacity:0, filter:"blur(12px)", duration:0.4, ease:"power2.in"}}, {f(t1 - 0.55)});')

# ---- end card ----
E = END_T
js += [
    f'tl.fromTo("#endcard", {{opacity:0}}, {{opacity:1, duration:0.8, ease:"sine.inOut"}}, {f(E - 0.4)});',
    f'tl.from("#ec-logo", {{scale:0.82, opacity:0, filter:"blur(16px)", duration:1.1, ease:"power3.out"}}, {f(E)});',
    f'tl.fromTo("#ec-glint", {{xPercent:-160}}, {{xPercent:300, duration:1.1, ease:"power2.inOut"}}, {f(E + 1.0)});',
    f'tl.fromTo("#ec-glint", {{xPercent:-160}}, {{xPercent:300, duration:1.1, ease:"power2.inOut", immediateRender:false}}, {f(E + 3.6)});',
    *[f'tl.from("#ec-tag .t{k}", {{y:22, opacity:0, filter:"blur(8px)", duration:0.6, ease:"power3.out"}}, {f(tt - 0.1)});' for k, tt in enumerate(cfg["tag_times"])],
    f'tl.fromTo("#ec-rays", {{rotation:0, opacity:0}}, {{rotation:24, opacity:0.55, duration:{f(TOTAL - E)}, ease:"none"}}, {f(E)});',
    f'tl.from("#ec-line", {{scaleX:0, duration:0.9, ease:"expo.out"}}, {f(cfg["tag_times"][0] - 0.2)});',
    f'tl.from("#endcard .ec-info > *", {{y:24, opacity:0, duration:0.6, ease:"power2.out", stagger:0.12}}, {f(cfg["info_at"])});',
    f'tl.from("#ec-cta .w", {{y:30, opacity:0, filter:"blur(8px)", duration:0.6, ease:"back.out(1.4)", stagger:0.08}}, {f(cfg["cta_at"])});',
    f'tl.to("#logo-badge", {{opacity:0, duration:0.5, ease:"power1.in"}}, {f(E - 0.3)});',
    *([f'tl.to("#logo-badge", {{y:{cfg["logo_lift"]["y"]}, duration:0.5, ease:"power2.inOut"}}, {f(cfg["logo_lift"]["t"])});'] if cfg.get("logo_lift") else []),
    f'tl.to("#fade-black", {{opacity:1, duration:0.9, ease:"power1.in"}}, {f(TOTAL - 0.9)});',
]
# small logo: entrance + periodic shimmer
js.insert(0, 'tl.set("#logo-glint", {xPercent:-150}, 0);')
js.insert(0, 'tl.from("#logo-badge", {opacity:0, y:-16, scale:0.9, duration:0.9, ease:"power2.out"}, 0.3);')
n_sh = int((E - 3) // 6)
for k in range(n_sh):
    js.append(f'tl.fromTo("#logo-glint", {{xPercent:-150}}, {{xPercent:300, duration:0.9, ease:"power1.inOut", immediateRender:false}}, {f(2.5 + 6 * k)});')
# bokeh drift (deterministic)
js.append(f'tl.fromTo(".bk", {{y:0}}, {{y:-260, duration:{TOTAL}, ease:"none", stagger:0}}, 0);')
js.append(f'tl.fromTo("#vig", {{opacity:0.85}}, {{opacity:1, duration:4, ease:"sine.inOut", yoyo:true, repeat:{math.ceil(TOTAL / 4) - 1}}}, 0);')

bokeh = []
for k in range(9):
    x = (k * 0.618034 * 1080 + 90) % 1080
    y = 300 + (abs(math.sin(k * 1.7 + 0.3)) * 1700)
    s = 10 + 26 * abs(math.sin(k * 2.3 + 0.7))
    o = 0.10 + 0.22 * abs(math.cos(k * 1.1))
    bokeh.append(f'<i class="bk" style="left:{x:.0f}px;top:{y:.0f}px;width:{s:.0f}px;height:{s:.0f}px;opacity:{o:.2f}"></i>')

cta_words = "".join(f'<span class="w">{w}</span> ' for w in cfg["cta"].split())

page = f'''<!doctype html>
<html lang="hi" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>GCN Silver Merchant – Diwali Special</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Poppins:wght@400;500;600&family=Tiro+Devanagari+Hindi&display=block" />
    <style>
      :root {{
        --bg: #0b0a08;
        --silver: #e9e4da;
        --gold: #d4a94f;
        --flame: #ffd98a;
        --font-hi: "Tiro Devanagari Hindi", serif;
        --font-brand: "Cinzel", serif;
        --font-info: "Poppins", sans-serif;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--bg); }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: var(--bg); }}
      .shot {{ position: absolute; inset: 0; overflow: hidden; will-change: opacity, filter, transform; }}
      .kb {{ position: absolute; inset: 0; }}
      .shot video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}

      /* grade + texture */
      #warm {{ position: absolute; inset: 0; z-index: 80; pointer-events: none; mix-blend-mode: soft-light;
        background: radial-gradient(ellipse 120% 80% at 50% 40%, rgba(255, 205, 140, 0.18), rgba(20, 12, 4, 0.25)); }}
      #vig {{ position: absolute; inset: 0; z-index: 81; pointer-events: none;
        background: radial-gradient(ellipse 85% 70% at 50% 48%, transparent 45%, rgba(5, 4, 2, 0.78) 100%); }}
      #grain {{ position: absolute; inset: 0; z-index: 82; pointer-events: none; opacity: 0.55;
        background-image:
          radial-gradient(rgba(255,255,255,.035) 1px, transparent 1px),
          radial-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
          radial-gradient(rgba(0,0,0,.05) 1px, transparent 1px);
        background-size: 3px 3px, 5px 5px, 7px 7px; background-position: 0 0, 1px 2px, 2px 1px; }}
      .bk {{ position: absolute; z-index: 83; border-radius: 50%; pointer-events: none; mix-blend-mode: screen;
        background: radial-gradient(circle, rgba(255, 217, 138, .95), rgba(255, 180, 80, 0) 70%); }}
      .leak {{ position: absolute; z-index: 84; pointer-events: none; mix-blend-mode: screen; opacity: 0; }}
      #leak-a {{ width: 1700px; height: 1700px; left: -500px; top: 100px;
        background: radial-gradient(circle, rgba(255, 214, 140, .95) 0%, rgba(255, 160, 60, .45) 35%, rgba(255, 120, 30, 0) 68%); }}
      #leak-b {{ width: 1400px; height: 1400px; left: 200px; top: 700px;
        background: radial-gradient(circle, rgba(255, 240, 210, .9) 0%, rgba(255, 190, 110, .35) 40%, rgba(255, 150, 60, 0) 70%); }}

      /* key phrases */
      .kp {{ position: absolute; left: 0; right: 0; top: 1140px; height: 520px; z-index: 90;
        display: flex; align-items: center; justify-content: center; padding: 0 90px; }}
      #scrim {{ position: absolute; left: 0; right: 0; top: 1060px; height: 680px; z-index: 89; opacity: 0; pointer-events: none;
        background: radial-gradient(ellipse 75% 50% at 50% 50%, rgba(8, 6, 3, .72), rgba(8, 6, 3, 0) 100%); }}
      .kp-inner {{ text-align: center; max-width: 900px; }}
      .kp .l1 {{ font-family: var(--font-hi); font-size: 92px; line-height: 1.32; color: #f4f0e8;
        text-shadow: 0 0 22px rgba(255, 230, 190, .45), 0 0 4px rgba(255, 255, 255, .35), 0 4px 12px rgba(0,0,0,.75); }}
      .kp .l2 {{ font-family: var(--font-hi); font-size: 60px; line-height: 1.35; margin-top: 6px; color: var(--flame);
        text-shadow: 0 0 22px rgba(255, 190, 90, .55), 0 3px 10px rgba(0,0,0,.7); }}
      .kp .w {{ display: inline-block; }}
      .kp .rule {{ width: 260px; height: 3px; margin: 26px auto 0; border-radius: 2px;
        background: linear-gradient(90deg, rgba(212,169,79,0), var(--gold), rgba(212,169,79,0)); }}

      /* small logo badge, top-right */
      #logo-badge {{ position: absolute; top: 64px; right: 46px; width: 170px; z-index: 95; overflow: hidden;
        filter: drop-shadow(0 4px 14px rgba(0,0,0,.7)); }}
      #logo-badge img {{ width: 100%; display: block; }}
      .gmask {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none;
        -webkit-mask-image: url(assets/logo.png); mask-image: url(assets/logo.png);
        -webkit-mask-size: 100% 100%; mask-size: 100% 100%; }}
      #logo-glint, #ec-glint {{ position: absolute; top: -20%; bottom: -20%; width: 35%; left: 0;
        background: linear-gradient(100deg, rgba(255,255,255,0), rgba(255,255,255,.85), rgba(255,255,255,0)); }}

      /* end card */
      #endcard {{ position: absolute; inset: 0; z-index: 96; opacity: 0;
        background: radial-gradient(ellipse 80% 55% at 50% 38%, #2a2012 0%, #120e08 55%, #070604 100%);
        display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 0 90px 140px; }}
      #ec-logo {{ position: relative; width: 620px; overflow: hidden; }}
      #ec-logo img {{ width: 100%; display: block; filter: drop-shadow(0 0 40px rgba(255, 200, 110, .25)); }}
      #ec-tag {{ margin-top: 34px; font-family: var(--font-brand); font-weight: 500; font-size: 38px; letter-spacing: 0.28em;
        color: var(--gold); text-shadow: 0 0 18px rgba(212,169,79,.4); }}
      #ec-line {{ width: 520px; height: 2px; margin: 40px 0 44px;
        background: linear-gradient(90deg, rgba(212,169,79,0), var(--gold), rgba(212,169,79,0)); }}
      .ec-info {{ display: flex; flex-direction: column; align-items: center; gap: 26px; text-align: center; }}
      .ec-phone {{ font-family: var(--font-info); font-weight: 600; font-size: 60px; color: #fff; letter-spacing: .02em;
        font-variant-numeric: tabular-nums; }}
      .ec-phone small {{ display: block; font-weight: 500; font-size: 36px; color: var(--silver); opacity: .85; margin-top: 4px; }}
      .ec-addr {{ font-family: var(--font-info); font-size: 32px; line-height: 1.45; color: var(--silver); opacity: .9; }}
      .ec-addr b {{ font-family: var(--font-brand); font-weight: 700; color: var(--gold); letter-spacing: .14em; font-size: 26px; display: block; }}
      #ec-cta {{ margin-top: 54px; font-family: var(--font-hi); font-size: 54px; line-height: 1.35; text-align: center; color: var(--flame);
        text-shadow: 0 0 24px rgba(255, 190, 90, .5); max-width: 880px; }}
      #ec-cta .w {{ display: inline-block; }}
      #ec-rays {{ position: absolute; left: 50%; top: 520px; width: 1800px; height: 1800px; margin: -900px 0 0 -900px; z-index: -1;
        background: repeating-conic-gradient(from 0deg, rgba(255, 210, 140, .07) 0deg 6deg, rgba(255, 210, 140, 0) 6deg 18deg);
        -webkit-mask-image: radial-gradient(circle, #000 0%, rgba(0,0,0,0) 60%); mask-image: radial-gradient(circle, #000 0%, rgba(0,0,0,0) 60%); }}
      #endcard {{ isolation: isolate; }}
      #ec-tag span {{ display: inline-block; }}
      #ec-tag .sep {{ color: rgba(212,169,79,.6); }}
      .kp .latin {{ font-family: var(--font-brand); letter-spacing: .08em; }}
      .kp .l2.latin {{ font-family: var(--font-info); letter-spacing: 0; font-size: 44px; color: var(--silver); }}
      .shot img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      .hl {{ position: absolute; left: 30px; right: 30px; z-index: 92; border: 4px solid var(--gold); border-radius: 30px; overflow: hidden;
        box-shadow: 0 0 40px rgba(255, 200, 100, .7), inset 0 0 40px rgba(255, 200, 100, .35); }}
      .hl i {{ position: absolute; top: 0; bottom: 0; left: 0; width: 22%; transform: skewX(-20deg);
        background: linear-gradient(90deg, rgba(255,230,180,0), rgba(255,230,180,.45), rgba(255,230,180,0)); mix-blend-mode: screen; }}
      #fade-black {{ position: absolute; inset: 0; z-index: 99; background: #000; opacity: 0; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(clips_html)}
    <div id="warm"></div>
    <div id="vig"></div>
    <div id="grain"></div>
    {"".join(bokeh)}
    <div class="leak" id="leak-a"></div>
    <div class="leak" id="leak-b"></div>
    <div id="scrim"></div>
{chr(10).join(hl_html)}
{chr(10).join(kp_html)}
    <div id="logo-badge"><img src="assets/logo.png" alt="GCN Silver Merchant" /><div class="gmask"><div id="logo-glint"></div></div></div>
    <div id="endcard">
      <div id="ec-rays"></div>
      <div id="ec-logo"><img src="assets/logo.png" alt="GCN Silver Merchant" /><div class="gmask"><div id="ec-glint"></div></div></div>
      <div id="ec-tag"><span class="t0">TRUST</span> <span class="t1"><span class="sep">·</span> PURITY</span> <span class="t2"><span class="sep">·</span> TRADITION</span></div>
      <div id="ec-line"></div>
      <div class="ec-info">
        <div class="ec-phone">📞 91354 60121<small>06123 186632 &nbsp;|&nbsp; 06124572659</small></div>
        <div class="ec-addr"><b>WHOLESALE</b>3rd Floor, New Chaurasia Complex, Near Axis ATM, Bakarganj, Patna</div>
        <div class="ec-addr"><b>RETAIL SHOP</b>Bari Path, Near Axis ATM, Bakarganj, Patna</div>
      </div>
      <div id="ec-cta">{cta_words.strip()}</div>
    </div>
    <div id="fade-black"></div>

    <audio id="vo" src="assets/voiceover.mp3" data-start="0" data-duration="{round(VO_END, 3)}" data-track-index="10" data-volume="1"></audio>
    <audio id="music" src="assets/music-diwali.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="11" data-volume="{cfg.get("music_volume", 0.22)}"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + "      ").join(js)}
      tl.to({{}}, {{ duration: {TOTAL} }}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page)
print("wrote index.html:", len(shots), "shots, total", TOTAL, "s")
