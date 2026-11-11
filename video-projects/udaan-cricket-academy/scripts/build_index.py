# Generates index.html from the shot list. Run: python3 scripts/build_index.py
SEGS = [  # id, start, duration
 ("s01",0.00,2.30),("s02",2.30,2.90),("s03",5.20,5.00),("s04",10.20,2.00),("s05",12.20,3.55),
 ("s06",15.75,2.60),("s07",18.35,0.52),("s08",18.87,0.45),("s09",19.32,1.08),("s10",20.40,1.60),
 ("s11",22.00,1.55),("s12",23.55,1.35),("s13",24.90,1.50),("s14",26.40,1.25),("s15",27.65,1.25),
 ("s16",28.90,6.30),("s18",39.00,4.00),("s19",43.00,3.45),("s20",46.45,4.85),("s21",51.30,6.00),
]
SPLIT = (35.20, 3.80)
TOTAL = 57.30
FLASH = [10.20, 15.75, 28.90, 35.20, 39.00, 43.00, 51.30]   # scene boundaries

vids = []
for i,(sid,st,du) in enumerate(SEGS):
    vids.append(f'''    <div class="vw" id="w-{sid}"><video id="{sid}" class="full" src="assets/seg/{sid}.mp4" data-start="{st:.2f}" data-duration="{du:.2f}" data-track-index="{i%2}" muted playsinline></video></div>''')
ss, sd = SPLIT
split = f'''    <div id="split-bg" class="clip" data-start="{ss:.2f}" data-duration="{sd:.2f}" data-track-index="2"></div>
    <div class="vw half top" id="w-s17t"><video id="s17t" src="assets/seg/s17-top.mp4" data-start="{ss:.2f}" data-duration="{sd:.2f}" data-track-index="3" muted playsinline></video></div>
    <div class="vw half bot" id="w-s17b"><video id="s17b" src="assets/seg/s17-bot.mp4" data-start="{ss:.2f}" data-duration="{sd:.2f}" data-track-index="4" muted playsinline></video></div>
    <div id="split-line" class="clip" data-start="{ss:.2f}" data-duration="{sd:.2f}" data-track-index="5"></div>'''
flashes = "\n".join(f'    <div id="fl{i}" class="flash clip" data-start="{max(0,t-0.08):.2f}" data-duration="0.40" data-track-index="{6+i%2}"></div>' for i,t in enumerate(FLASH))

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1080, height=1920">
<title>Udaan Cricket Academy — Admissions Reel</title>
<script src="assets/gsap.min.js"></script>
<style>
  @font-face{{font-family:"Barlow Condensed";font-weight:700;src:url("assets/fonts/barlow-condensed-latin-700-normal.woff2") format("woff2");}}
  @font-face{{font-family:"Barlow Condensed";font-weight:800;src:url("assets/fonts/barlow-condensed-latin-800-normal.woff2") format("woff2");}}
  html,body{{margin:0;padding:0;background:#14213D;}}
  #root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#14213D;font-family:"Barlow Condensed",sans-serif;}}
  .vw{{position:absolute;inset:0;overflow:hidden;transform-origin:50% 50%;}}
  .vw video{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}}
  .vw.half{{inset:auto 0 auto 0;height:960px;}}
  .vw.half.top{{top:0;}} .vw.half.bot{{top:960px;}}
  #split-bg{{position:absolute;inset:0;background:#14213D;}}
  #split-line{{position:absolute;left:0;top:952px;width:1080px;height:16px;background:#D7192A;transform-origin:0 50%;z-index:6;box-shadow:0 0 0 4px #fff;}}
  #w-s17t,#w-s17b{{z-index:5;}}
  .flash{{position:absolute;inset:0;background:#fff;z-index:40;opacity:0;pointer-events:none;}}
  #logo{{position:absolute;top:64px;right:44px;width:200px;height:auto;z-index:50;filter:drop-shadow(0 6px 14px rgba(0,0,0,.45));}}

  /* headline blocks — sit in the lower-middle, clear of Reels UI (bottom 380px) */
  .hl{{position:absolute;left:0;right:0;top:1180px;display:flex;flex-direction:column;align-items:center;gap:18px;z-index:30;}}
  .hl .main{{background:#14213D;color:#fff;font-weight:800;font-size:92px;line-height:1;letter-spacing:1px;padding:18px 34px 14px;text-transform:uppercase;box-shadow:0 10px 30px rgba(0,0,0,.35);}}
  .hl .main em{{font-style:normal;color:#ff3b4b;}}
  .hl .row{{display:flex;gap:12px;align-items:center;}}
  .hl .chip{{background:#D7192A;color:#fff;font-weight:800;font-size:64px;line-height:1;padding:12px 22px 10px;text-transform:uppercase;box-shadow:0 8px 24px rgba(0,0,0,.35);}}
  .hl .dot{{width:16px;height:16px;border-radius:50%;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,.5);}}
  #hl-train .chip{{font-size:86px;}}
  #hl-train .chip.navy{{background:#14213D;}}
</style>
</head>
<body>
  <div id="root" data-composition-id="udaan-reel" data-start="0" data-duration="{TOTAL:.2f}" data-width="1080" data-height="1920">
{chr(10).join(vids)}
{split}

    <!-- Scene 3 headline: 15.75–26.40 -->
    <div id="hl-coach" class="hl clip" data-start="15.85" data-duration="10.55" data-track-index="10">
      <div class="main" id="hc-main">Professional <em>Coaching</em></div>
      <div class="row">
        <div class="chip" id="hc-1">Bat</div><div class="dot" id="hd-1"></div>
        <div class="chip" id="hc-2">Bowl</div><div class="dot" id="hd-2"></div>
        <div class="chip" id="hc-3">Field</div><div class="dot" id="hd-3"></div>
        <div class="chip" id="hc-4">Fitness</div>
      </div>
    </div>

    <!-- Scene 4 headline: 26.40–28.90 -->
    <div id="hl-train" class="hl clip" data-start="26.45" data-duration="2.45" data-track-index="11">
      <div class="row"><div class="chip navy" id="ht-1">Train</div></div>
      <div class="row"><div class="chip" id="ht-2">Improve</div></div>
      <div class="row"><div class="chip navy" id="ht-3">Perform</div></div>
    </div>

{flashes}

    <img id="logo" class="clip" src="assets/logo.png" alt="Udaan Cricket Academy" data-start="0" data-duration="{TOTAL:.2f}" data-track-index="20">

    <audio id="vo" src="assets/vo.mp3" data-start="0" data-duration="55.72" data-track-index="30" data-volume="1"></audio>
  </div>

<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  const SEGS = {[[s, st] for s, st, _ in SEGS]};

  // punch-in on every cut (wrappers, never the <video> itself)
  SEGS.forEach(([id, st], i) => {{
    const short = (st >= 18.3 && st < 28.9);          // fast montage = harder punch
    tl.fromTo("#w-" + id, {{ scale: short ? 1.14 : 1.07 }},
      {{ scale: 1, duration: short ? 0.35 : 0.6, ease: i % 2 ? "power3.out" : "expo.out" }}, st);
  }});
  // slow push on longer holds so nothing feels static
  [["s03",5.2,5.0],["s16",28.9,6.3],["s20",46.45,4.85],["s21",51.3,6.0]].forEach(([id,st,du]) => {{
    tl.to("#w-" + id, {{ scale: 1.06, duration: du - 0.6, ease: "none" }}, st + 0.6);
  }});

  // white flash at scene boundaries
  {FLASH}.forEach((t, i) => {{
    tl.fromTo("#fl" + i, {{ opacity: 0 }}, {{ opacity: 0.85, duration: 0.08, ease: "none" }}, Math.max(0, t - 0.08));
    tl.to("#fl" + i, {{ opacity: 0, duration: 0.3, ease: "power2.out" }}, Math.max(0.08, t));
  }});

  // logo entrance
  tl.from("#logo", {{ scale: 0.6, opacity: 0, duration: 0.6, ease: "back.out(1.8)" }}, 0.15);

  // split screen (35.2): top from left, bottom from right, red divider wipes
  tl.from("#w-s17t", {{ xPercent: -100, duration: 0.5, ease: "expo.out" }}, 35.2);
  tl.from("#w-s17b", {{ xPercent: 100, duration: 0.5, ease: "expo.out" }}, 36.85);
  tl.from("#split-line", {{ scaleX: 0, duration: 0.45, ease: "power3.inOut" }}, 35.35);

  // scene 3 headline — chips pop on the VO words
  tl.from("#hc-main", {{ y: 60, opacity: 0, duration: 0.5, ease: "power3.out" }}, 15.95);
  [["#hc-1",18.35],["#hd-1",18.6],["#hc-2",18.87],["#hd-2",19.1],["#hc-3",19.32],["#hd-3",19.8],["#hc-4",20.05]].forEach(([s,t],i) => {{
    tl.from(s, {{ scale: 0.3, opacity: 0, duration: 0.28, ease: i % 2 ? "power2.out" : "back.out(2.5)" }}, t);
  }});

  // scene 4 headline — TRAIN / IMPROVE / PERFORM stacked
  tl.from("#ht-1", {{ x: -500, opacity: 0, duration: 0.35, ease: "expo.out" }}, 26.5);
  tl.from("#ht-2", {{ x: 500, opacity: 0, duration: 0.35, ease: "power3.out" }}, 27.25);
  tl.from("#ht-3", {{ scale: 0.4, opacity: 0, duration: 0.35, ease: "back.out(2)" }}, 27.95);

  // end: hold on the CTA card, gentle fade on the very last beat
  tl.to("#root", {{ opacity: 1, duration: 0.01 }}, {TOTAL - 0.01:.2f});
  window.__timelines["udaan-reel"] = tl;
</script>
</body>
</html>
'''
open("index.html","w").write(html)
print("written")
