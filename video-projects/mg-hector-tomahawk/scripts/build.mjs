// Builds index.html for one design option (A | B | C) from the shared beat sheet.
// usage: node scripts/build.mjs A   (run from the project folder)
import { writeFileSync } from "node:fs";
import { BEATS, MATTE_ON, ZOOMS, MASKS, FLASHES, SFX, DURATION } from "./beats.mjs";

const V = (process.argv[2] || "A").toUpperCase();
if (!["A", "B", "C"].includes(V)) throw new Error("variant must be A, B or C");

// ---- deterministic PRNG (mulberry32) -------------------------------------------------
function rng(seed) {
  return () => {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// Split text into per-letter spans with seeded scatter offsets.
function chars(text, seed, hiIdx = []) {
  const r = rng(seed);
  return [...text].map((c, i) => {
    if (c === " ") return `<span class="sp"> </span>`;
    const dx = Math.round((r() - 0.5) * 520), dy = Math.round((r() - 0.5) * 420);
    const rot = Math.round((r() - 0.5) * 70), dl = (r() * 0.16).toFixed(3);
    const hi = hiIdx.includes(i) ? " hi" : "";
    return `<span class="ch${hi}" data-dx="${dx}" data-dy="${dy}" data-r="${rot}" data-dl="${dl}">${esc(c)}</span>`;
  }).join("");
}
// Pick 1–2 accent letters for two-tone words (deterministic).
const accentIdx = (t) => { const L = [...t].map((c, i) => (c.trim() ? i : -1)).filter((i) => i >= 0);
  return L.length < 4 ? [L[L.length - 1]] : [L[Math.floor(L.length / 2)], L[L.length - 1]]; };
// Fit a single-line word to width: px = maxWidth / (chars * em-width), capped.
const fit = (t, em, cap, width = 980) => Math.min(cap, Math.floor(width / (Math.max(t.length, 1) * em)));

const isMatte = (t) => MATTE_ON.some(([a, b]) => t >= a && t < b);

// ---- per-variant card markup ----------------------------------------------------------
function cardHTML(b, i) {
  const seed = 1000 + i * 37;
  const behind = isMatte(b.t);
  const k = b.kind;
  let pos = "low", layer = "front", inner = "";

  if (V === "A") {
    if (k === "hero" || k === "cta") {
      pos = k === "cta" ? "low" : "top"; layer = behind && k === "hero" ? "behind" : "front";
      inner = `<div class="w gold" style="font-size:${fit(b.text, 0.52, 330, 940)}px">${esc(b.text)}</div>` +
        (b.sub ? `<div class="sub cyan">${esc(b.sub)}</div>` : "");
    } else if (k === "num") {
      inner = `<div class="w cyan scat" style="font-size:${fit(b.text, 0.5, 260)}px">${chars(b.text, seed)}</div>` +
        (b.sub ? `<div class="sub white">${esc(b.sub)}</div>` : "");
    } else if (k === "stack") {
      inner = b.lines.map((l, j) => `<div class="w cyan scat line" data-ld="${b.ld[j]}" style="font-size:${fit(l, 0.5, j === 0 ? 190 : 120)}px">${chars(l, seed + j)}</div>`).join("");
    } else if (k === "price") {
      pos = "top";
      inner = `<div class="w lime scat" style="font-size:${fit(b.text, 0.5, 230)}px">${chars(b.text, seed)}</div><div class="sub white">${esc(b.sub)}</div>`;
    } else if (k === "end") {
      pos = "mid";
      inner = b.lines.map((l, j) => `<div class="w gold line whipline" data-ld="${b.ld[j]}" style="font-size:${fit(l, 0.52, 300, 940)}px">${esc(l)}</div>`).join("") +
        `<div class="sub cyan big">${esc(b.sub)}</div>`;
    }
  }

  if (V === "B") {
    const two = (t, cap, em = 0.5) => `<div class="w two" style="font-size:${fit(t, em, cap)}px">${chars(t, seed, accentIdx(t))}</div>`;
    if (k === "hero" || k === "cta") {
      inner = two(b.text, 210) + (b.sub ? `<div class="script">${esc(b.sub)}</div>` : "");
    } else if (k === "num") {
      pos = "mid";
      inner = `<div class="w yel" style="font-size:${fit(b.text, 0.5, 280)}px">${esc(b.text)}</div>` + (b.sub ? `<div class="script">${esc(b.sub)}</div>` : "");
    } else if (k === "stack") {
      inner = b.lines.map((l, j) => `<div class="w two line" data-ld="${b.ld[j]}" style="font-size:${fit(l, 0.5, j === 0 ? 190 : 130)}px">${chars(l, seed + j, [0])}</div>`).join("");
    } else if (k === "price") {
      pos = "top";
      const [a, c] = b.text.split(".");
      inner = `<div class="w chrome" style="font-size:230px">${esc(a)}<span class="y">.</span>${esc(c)}</div><div class="script">${esc(b.subB || b.sub)}</div>`;
    } else if (k === "end") {
      pos = "mid";
      inner = `<div class="tilt">` + b.lines.concat([b.sub]).map((l, j) => `<div class="w two line" data-ld="${b.ld[j] ?? 0.6}" style="font-size:${fit(l, 0.5, 230)}px">${chars(l, seed + j, accentIdx(l))}</div>`).join("") + `</div>`;
    }
  }

  if (V === "C") {
    if (k === "hero" || k === "cta") {
      pos = "top"; layer = behind ? "behind" : "front";
      inner = `<div class="w red tw" style="font-size:${fit(b.text, 0.52, 300, 940)}px">${chars(b.text, seed)}</div>` +
        (b.sub ? `<div class="sub white tsub">${esc(b.sub)}</div>` : "");
    } else if (k === "num") {
      inner = `<div class="hud"><div class="slash"></div><div class="hv tw" style="font-size:${fit(b.text, 0.5, 200, 640)}px">${chars(b.text, seed)}</div>${b.sub ? `<div class="hs">${esc(b.sub)}</div>` : ""}</div>`;
    } else if (k === "stack") {
      inner = b.lines.map((l, j) => `<div class="w ${j === 0 ? "red" : "white"} tw line" data-ld="${b.ld[j]}" style="font-size:${fit(l, 0.5, j === 0 ? 200 : 110)}px">${chars(l, seed + j)}</div>`).join("") + `<div class="uline"></div>`;
    } else if (k === "price") {
      pos = "top";
      inner = `<div class="callout"><i class="br tl"></i><i class="br tr"></i><i class="br bl"></i><i class="br brr"></i><div class="clab">${esc(b.sub)}</div><div class="cval tw">${chars(b.text, seed)}</div></div><div class="leader"></div>`;
    } else if (k === "end") {
      pos = "mid";
      inner = b.lines.map((l, j) => `<div class="hud line" data-ld="${b.ld[j]}"><div class="slash"></div><div class="hv" style="font-size:${fit(l, 0.5, 170, 820)}px">${esc(l)}</div></div>`).join("") +
        `<div class="sub red big">${esc(b.sub)}</div>`;
    }
  }

  const dur = (b.end - b.t).toFixed(2);
  if (b.front) layer = "front";
  let subCard = "";
  if (layer === "behind" && b.sub) {
    const m = inner.match(/font-size:(\d+)px/); const size = m ? +m[1] : 260;
    inner = inner.replace(/<div class="sub[^"]*">[^<]*<\/div>/, "");
    subCard = `<div id="c${i}s" class="card clip front pos-top subcard" data-kind="subcard" data-start="${b.t}" data-duration="${dur}" data-track-index="${60 + i}" style="padding-top:${190 + Math.round(size * 0.93) + 6}px"><div class="inner"><div class="sub ${V === "C" ? "white" : "cyan"} big">${esc(b.sub)}</div></div></div>`;
  }
  return subCard + `<div id="c${i}" class="card clip ${layer} pos-${pos} k-${k}" data-kind="${k}" data-start="${b.t}" data-duration="${dur}" data-track-index="${20 + i}"><div class="inner">${inner}</div></div>`;
}

const cards = BEATS.map(cardHTML).join("\n      ");
const masks = MASKS.map((m, i) => `<div id="mask${i}" class="mask clip" data-start="${m.t}" data-duration="${(m.end - m.t).toFixed(2)}" data-track-index="${80 + i}" style="left:${m.x}px;top:${m.y}px;width:${m.w}px;height:${m.h}px"></div>`).join("\n      ");
const sfx = SFX.map((s, i) => `<audio id="sfx${i}" src="assets/${s.f}" data-start="${s.t}" data-duration="${s.d}" data-track-index="${100 + i}" data-volume="${s.v}"></audio>`).join("\n      ");
const flashes = FLASHES.map((t, i) => `<div id="fl${i}" class="flash clip" data-start="${t}" data-duration="0.3" data-track-index="${90 + i}"></div>`).join("\n      ");

const html = `<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <!-- GENERATED by scripts/build.mjs — Option ${V}. Edit beats.mjs / build.mjs, not this file. -->
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family:'Anton'; src:url('assets/fonts/anton-400.woff2') format('woff2'); font-weight:400; font-style:normal; }
      :root { --gold: linear-gradient(180deg,#FFFBEA 0%,#FFE680 32%,#F5C800 55%,#D88A00 82%,#9A5200 100%);
              --cyan:#39D5F5; --red:#E0162B; --lime:#B8FF1A; }
      * { margin:0; padding:0; box-sizing:border-box; }
      html, body { width:1080px; height:1920px; overflow:hidden; background:#000; }
      #root { position:relative; width:1080px; height:1920px; overflow:hidden; }
      .vw { position:absolute; inset:0; transform-origin:50% 32%; }
      .vw video { width:100%; height:100%; object-fit:cover; display:block; }
      #plateWrap { z-index:1; } #matteWrap { z-index:3; }
      .card { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; pointer-events:none; }
      .card.behind { z-index:2; } .card.front { z-index:6; }
      .pos-top { justify-content:flex-start; padding-top:190px; }
      .pos-low { justify-content:flex-end; padding-bottom:250px; }
      .pos-mid { justify-content:center; }
      .inner { display:flex; flex-direction:column; align-items:center; width:100%; padding:0 40px; }
      .w { line-height:.92; white-space:nowrap; text-transform:uppercase; }
      .ch, .sp { display:inline-block; white-space:pre; }
      .sub { font:800 italic 64px/1 'Barlow Condensed'; letter-spacing:.02em; margin-top:10px; text-transform:uppercase;
             text-shadow:0 4px 0 rgba(0,0,0,.55),0 0 22px rgba(0,0,0,.6); white-space:nowrap; }
      .sub.big { font-size:84px; }
      .sub.cyan { color:#DFF8FF; text-shadow:0 0 18px rgba(57,213,245,.9),0 4px 0 rgba(0,0,0,.6); }
      .sub.white { color:#fff; } .sub.red { color:var(--red); text-shadow:0 0 20px rgba(224,22,43,.6),0 4px 0 #000; }
      .mask { position:absolute; z-index:4; backdrop-filter:blur(26px) brightness(.55); -webkit-backdrop-filter:blur(26px) brightness(.55);
              border-radius:40px;
              -webkit-mask-image:radial-gradient(ellipse closest-side,#000 62%,transparent 100%); mask-image:radial-gradient(ellipse closest-side,#000 62%,transparent 100%); }
      .flash { position:absolute; inset:0; z-index:9; background:radial-gradient(ellipse at 50% 40%,#fff 0%,rgba(255,255,255,.85) 45%,rgba(255,255,255,0) 100%); opacity:0; }

      /* ---------- Option A: Behind-Head Chrome ---------- */
      .vA .gold, body.vA .gold { font-family:'Anton'; font-style:normal; transform:skewX(-9deg);
        background:var(--gold); -webkit-background-clip:text; background-clip:text; color:transparent;
        filter:drop-shadow(0 6px 0 rgba(0,0,0,.55)) drop-shadow(0 0 26px rgba(245,180,0,.55)); }
      body.vA .cyan.w { font:800 italic 200px/0.95 'Barlow Condensed'; color:#E9FBFF;
        text-shadow:0 0 14px rgba(57,213,245,.95),0 0 38px rgba(57,213,245,.7),0 6px 0 rgba(0,40,60,.8); }
      body.vA .lime { font:800 italic 220px/0.95 'Barlow Condensed'; color:var(--lime);
        text-shadow:0 0 22px rgba(184,255,26,.85),0 0 60px rgba(184,255,26,.45),0 6px 0 rgba(0,0,0,.7); }

      /* ---------- Option B: Spec Pop + Script ---------- */
      body.vB .two { font:900 italic 200px/0.95 'Barlow Condensed'; color:#fff;
        text-shadow:0 2px 0 #c9c9c9,0 6px 0 rgba(0,0,0,.65),0 0 30px rgba(0,0,0,.55); }
      body.vB .two .hi, body.vB .y { color:#FFC21A; text-shadow:0 0 22px rgba(255,170,0,.8),0 6px 0 rgba(0,0,0,.6); }
      body.vB .yel { font:900 italic 260px/0.95 'Barlow Condensed'; color:#FFD23A;
        text-shadow:0 0 26px rgba(255,150,0,.9),0 0 70px rgba(255,120,0,.45),0 6px 0 rgba(60,25,0,.85); }
      body.vB .chrome { font:900 italic 230px/0.95 'Barlow Condensed'; color:#fff;
        text-shadow:0 2px 0 #bbb,0 8px 0 rgba(0,0,0,.6),0 0 40px rgba(255,255,255,.35); }
      body.vB .script { font:400 86px/1 'Kaushan Script'; color:#fff; margin-top:-26px; transform:rotate(-4deg);
        text-shadow:0 4px 0 rgba(0,0,0,.6),0 0 20px rgba(0,0,0,.6); white-space:nowrap; text-transform:none; }
      body.vB .tilt { transform:rotate(-7deg); display:flex; flex-direction:column; align-items:center; }

      /* ---------- Option C: HUD / Red Workshop ---------- */
      body.vC .red.w { font-family:'Anton'; color:var(--red); transform:skewX(-10deg);
        background:linear-gradient(180deg,#FF6B6B 0%,#E0162B 45%,#8E0012 100%); -webkit-background-clip:text; background-clip:text; color:transparent;
        filter:drop-shadow(0 6px 0 rgba(0,0,0,.6)) drop-shadow(0 0 18px rgba(0,0,0,.6)); }
      body.vC .white.w { font:800 italic 110px/1 'Barlow Condensed'; color:#fff; text-shadow:0 5px 0 rgba(0,0,0,.65),0 0 18px rgba(0,0,0,.6); }
      body.vC .hud { position:relative; display:flex; flex-direction:column; align-items:flex-start; align-self:flex-start;
        margin-left:20px; padding:18px 70px 20px 70px; background:linear-gradient(90deg,rgba(8,8,10,.92),rgba(8,8,10,.78) 70%,rgba(8,8,10,0));
        border-bottom:6px solid #fff; transform:skewX(-10deg); margin-bottom:14px; }
      body.vC .slash { position:absolute; left:0; top:0; bottom:0; width:34px; background:var(--red); transform-origin:50% 100%; }
      body.vC .hv { font:800 italic 200px/0.95 'Barlow Condensed'; color:#fff; text-shadow:0 0 20px rgba(255,255,255,.25); white-space:nowrap; }
      body.vC .hs { font:700 54px/1 'Barlow Condensed'; color:var(--red); letter-spacing:.12em; text-transform:uppercase; margin-top:6px; white-space:nowrap; }
      body.vC .uline { width:620px; height:12px; margin-top:14px; background:linear-gradient(90deg,rgba(224,22,43,0),var(--red) 20%,var(--red) 80%,rgba(224,22,43,0)); box-shadow:0 0 22px rgba(224,22,43,.8); transform-origin:0 50%; }
      body.vC .tsub { margin-top:6px; }
      body.vC .callout { position:relative; padding:26px 54px 30px; background:rgba(6,6,8,.82); text-align:center; }
      body.vC .br { position:absolute; width:46px; height:46px; border:7px solid #fff; }
      body.vC .br.tl { left:-10px; top:-10px; border-right:0; border-bottom:0; } body.vC .br.tr { right:-10px; top:-10px; border-left:0; border-bottom:0; }
      body.vC .br.bl { left:-10px; bottom:-10px; border-right:0; border-top:0; } body.vC .br.brr { right:-10px; bottom:-10px; border-left:0; border-top:0; }
      body.vC .clab { font:700 46px/1 'Barlow Condensed'; color:var(--red); letter-spacing:.14em; text-transform:uppercase; white-space:nowrap; }
      body.vC .cval { font:800 italic 210px/0.95 'Barlow Condensed'; color:var(--lime); text-shadow:0 0 24px rgba(184,255,26,.75),0 6px 0 rgba(0,0,0,.7); white-space:nowrap; }
      body.vC .leader { width:8px; height:220px; background:linear-gradient(#fff,rgba(255,255,255,0)); margin-top:10px; transform-origin:50% 0; }
    </style>
  </head>
  <body class="v${V}">
    <div id="root" data-composition-id="main" data-start="0" data-duration="${DURATION}" data-width="1080" data-height="1920">
      <div class="vw" id="plateWrap"><video id="plate" src="assets/source.mp4" muted playsinline data-start="0" data-duration="${DURATION}" data-track-index="0"></video></div>
      <div class="vw" id="matteWrap"><video id="matte" src="assets/matte.webm" muted playsinline data-start="0" data-duration="${DURATION}" data-track-index="1"></video></div>
      <audio id="vo" src="assets/source.mp4" data-start="0" data-duration="${DURATION}" data-track-index="2" data-volume="1"></audio>
      ${masks}
      ${cards}
      ${flashes}
      ${sfx}
    </div>
    <script>
      (() => {
        const V = ${JSON.stringify(V)};
        const tl = gsap.timeline({ paused: true });
        const MATTE_ON = ${JSON.stringify(MATTE_ON)};
        const ZOOMS = ${JSON.stringify(ZOOMS)};

        // Matte layer only while the host is on screen (crowd shots would false-positive).
        // (#matteWrap starts visible in CSS because MATTE_ON[0] begins at 0)
        MATTE_ON.forEach(([a, b]) => { if (a > 0) tl.set("#matteWrap", { opacity: 1 }, a); tl.set("#matteWrap", { opacity: 0 }, b); });

        // Fast pace without touching audio: punch-in jump-zooms on plate + matte together.
        ZOOMS.forEach(([t, s]) => tl.set(["#plateWrap", "#matteWrap"], { scale: s }, t));

        // Chapter accents: white flash at the big section cuts.
        document.querySelectorAll(".flash").forEach((f) => {
          const t = +f.dataset.start;
          tl.fromTo(f, { opacity: 0.85 }, { opacity: 0, duration: 0.233, ease: "power2.out" }, t);
        });

        const D = (el) => +el.dataset.start;
        const scatterIn = (root, t) => root.querySelectorAll(".ch").forEach((c) => {
          tl.from(c, { x: +c.dataset.dx, y: +c.dataset.dy, rotation: +c.dataset.r, scale: 1.9, opacity: 0,
            duration: 0.4, ease: "power3.out" }, t + +c.dataset.dl);
        });
        const typeIn = (root, t, step = 0.033) => root.querySelectorAll(".ch").forEach((c, i) => {
          tl.from(c, { opacity: 0, scale: 1.45, duration: 0.1, ease: "power2.out" }, t + i * step);
        });

        document.querySelectorAll(".card").forEach((card) => {
          const t = D(card) + 0.033, k = card.dataset.kind;
          const inner = card.querySelector(".inner");
          const end = t + +card.dataset.duration;
          // camera-never-sleeps drift on every card
          tl.fromTo(inner, { scale: 1 }, { scale: 1.045, duration: +card.dataset.duration, ease: "none" }, D(card));

          if (k === "subcard") { tl.from(card.querySelector(".sub"), { y: 36, opacity: 0, duration: 0.3, ease: "back.out(1.7)" }, t + 0.133); return; }
          if (V === "A") {
            if (k === "hero" || k === "cta") {
              const w = card.querySelector(".w");
              if (k === "cta") tl.from(w, { scale: 2.4, opacity: 0, filter: "blur(18px)", duration: 0.267, ease: "expo.out" }, t);
              else tl.from(w, { xPercent: -75, opacity: 0, filter: "blur(22px)", duration: 0.233, ease: "expo.out" }, t);
              const s = card.querySelector(".sub"); if (s) tl.from(s, { y: 40, opacity: 0, duration: 0.3, ease: "back.out(1.7)" }, t + 0.133);
            } else if (k === "num" || k === "price") {
              scatterIn(card.querySelector(".w"), t);
              tl.from(card.querySelector(".w"), { textShadow: "0 0 0px rgba(57,213,245,0)", duration: 0.3, ease: "power2.out" }, t + 0.4);
              const s = card.querySelector(".sub"); if (s) tl.from(s, { y: 30, opacity: 0, duration: 0.267, ease: "power2.out" }, t + 0.3);
            } else if (k === "stack") {
              card.querySelectorAll(".line").forEach((l) => scatterIn(l, t + +l.dataset.ld));
            } else if (k === "end") {
              card.querySelectorAll(".whipline").forEach((l, j) => tl.from(l, { xPercent: j % 2 ? 80 : -80, opacity: 0, filter: "blur(20px)", duration: 0.3, ease: "expo.out" }, t + +l.dataset.ld));
              tl.from(card.querySelector(".sub"), { scale: 1.8, opacity: 0, duration: 0.3, ease: "back.out(1.6)" }, t + 0.9);
            }
          }

          if (V === "B") {
            const pop = (el, at) => tl.from(el, { scale: 1.55, opacity: 0, filter: "blur(16px)", duration: 0.3, ease: "back.out(1.6)" }, at);
            if (k === "stack" || k === "end") card.querySelectorAll(".line").forEach((l) => pop(l, t + +l.dataset.ld));
            else pop(card.querySelector(".w"), t);
            const sc = card.querySelector(".script");
            if (sc) tl.from(sc, { clipPath: "inset(0% 100% 0% 0%)", duration: 0.4, ease: "power2.out" }, t + 0.167);
          }

          if (V === "C") {
            if (k === "hero" || k === "cta") {
              typeIn(card.querySelector(".w"), t);
              const s = card.querySelector(".sub"); if (s) tl.from(s, { y: 30, opacity: 0, duration: 0.233, ease: "power3.out" }, t + 0.2);
            } else if (k === "num") {
              tl.from(card.querySelector(".hud"), { xPercent: -115, duration: 0.267, ease: "expo.out" }, t);
              tl.from(card.querySelector(".slash"), { scaleY: 0, duration: 0.2, ease: "power2.out" }, t + 0.133);
              typeIn(card.querySelector(".hv"), t + 0.1);
              const s = card.querySelector(".hs"); if (s) tl.from(s, { opacity: 0, x: -30, duration: 0.2, ease: "power2.out" }, t + 0.3);
            } else if (k === "stack") {
              card.querySelectorAll(".line").forEach((l) => typeIn(l, t + +l.dataset.ld, 0.028));
              tl.from(card.querySelector(".uline"), { scaleX: 0, duration: 0.3, ease: "expo.out" }, t + 0.2);
            } else if (k === "price") {
              tl.from(card.querySelector(".callout"), { scale: 1.35, opacity: 0, duration: 0.3, ease: "back.out(1.5)" }, t);
              tl.from(card.querySelector(".leader"), { scaleY: 0, duration: 0.3, ease: "power2.out" }, t + 0.2);
              typeIn(card.querySelector(".cval"), t + 0.2, 0.04);
            } else if (k === "end") {
              card.querySelectorAll(".hud").forEach((h) => tl.from(h, { xPercent: -115, duration: 0.3, ease: "expo.out" }, t + +h.dataset.ld));
              tl.from(card.querySelector(".sub"), { scale: 1.8, opacity: 0, duration: 0.3, ease: "back.out(1.6)" }, t + 0.9);
            }
          }
        });

        tl.to({}, { duration: ${DURATION} }, 0); // fill the slot (Law #11)
        window.__timelines["main"] = tl;
      })();
    </script>
  </body>
</html>
`;
writeFileSync("index.html", html);
console.log(`index.html written — Option ${V}, ${BEATS.length} beats`);
