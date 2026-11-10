/*
 * Reel Engine — one renderer shared by the live builder (builder/index.html)
 * and the Hyperframes composition (index.html).
 *
 * Everything is a pure function of SOURCE time: render(t) sets every style from t
 * and the config, with no internal state. The Hyperframes render drives it through a
 * GSAP proxy, and the builder drives it from the playing <video>.
 *
 * Coordinates are authored on a 1080x1920 stage; the source footage is 1920x1080.
 */
(function (global) {
  "use strict";

  var STAGE_W = 1080, STAGE_H = 1920, SRC_W = 1920, SRC_H = 1080, CONFIG_VERSION = 2;

  var STOP = new Set(("i me my we our you your he she it its they them a an the and or but so if of to in on at for from with " +
    "as is was were be been am are do did does have had has this that these those there here then than when what which who " +
    "just even really very literally going get got go up out about would could should will can i'm i've don't it's").split(" "));

  /* ---------- presets (style fingerprints from the creator library) ---------- */
  var PRESETS = {
    editorial: {
      name: "Editorial", source: "@simar-visuals",
      accent: "#4b3cf0", text: "#ffffff",
      captions: { bodyFont: "Inter", bodyWeight: 400, keyFont: "Instrument Serif", keyItalic: true, keyWeight: 400,
        keyStyle: "serif", keyLine: true, bodySize: 46, keySize: 132, uppercase: false, maxWords: 5, reveal: "word" },
      look: { grade: "cool", vignette: 0.45, bottomFade: 0.55, grain: 0.05 },
      motion: { capIn: 0.2, capRise: 16, capBlur: 6, keyIn: 0.34, keyScale: 1.22, callIn: 0.38, callBounce: 1, punch: 0.08, push: 0.035 },
      callout: "editorial"
    },
    gold: {
      name: "Gold Hero", source: "@vyron-media",
      accent: "#ffb81c", text: "#ffffff",
      captions: { bodyFont: "Poppins", bodyWeight: 600, keyFont: "Poppins", keyItalic: false, keyWeight: 800,
        keyStyle: "glow", keyLine: true, bodySize: 44, keySize: 128, uppercase: false, maxWords: 4, reveal: "word" },
      look: { grade: "warm", vignette: 0.6, bottomFade: 0.7, grain: 0.04 },
      motion: { capIn: 0.16, capRise: 12, capBlur: 4, keyIn: 0.26, keyScale: 1.5, callIn: 0.34, callBounce: 1.4, punch: 0.1, push: 0.04 },
      callout: "glass"
    },
    karaoke: {
      name: "Bold Karaoke", source: "workspace default",
      accent: "#3b82f6", text: "#ffffff",
      captions: { bodyFont: "Montserrat", bodyWeight: 900, keyFont: "Montserrat", keyItalic: false, keyWeight: 900,
        keyStyle: "color", keyLine: false, bodySize: 78, keySize: 78, uppercase: true, maxWords: 3, reveal: "chunk" },
      look: { grade: "neutral", vignette: 0.35, bottomFade: 0.4, grain: 0.05 },
      motion: { capIn: 0.14, capRise: 20, capBlur: 0, keyIn: 0.12, keyScale: 1.12, callIn: 0.3, callBounce: 1.2, punch: 0.07, push: 0.03 },
      callout: "glass"
    }
  };

  var FONTS = ["Inter", "Instrument Serif", "Poppins", "Montserrat", "Bebas Neue", "Playfair Display", "Archivo Black"];
  var EASES = ["smooth", "linear", "in", "out", "snap"];

  function clone(o) { return JSON.parse(JSON.stringify(o)); }

  function defaultConfig(presetId, data) {
    var id = PRESETS[presetId] ? presetId : "editorial", p = PRESETS[id];
    return {
      version: CONFIG_VERSION,
      preset: id,
      accent: p.accent,
      text: p.text,
      captions: Object.assign({ on: true, y: 63, scale: 1, autoKey: true }, clone(p.captions)),
      look: Object.assign({ punch: true, kenBurns: true, progress: false }, clone(p.look)),
      motion: clone(p.motion),
      calloutStyle: p.callout,
      framing: (data ? data.shots : []).map(function (s) {
        return { x: s.angle === "side" ? 0.56 : 0.51, zoom: 1 };
      }),
      camera: { keys: [], shake: 0 },          // virtual camera keyframes on top of the per-shot framing
      speed: { on: false, points: [] },        // speed ramp: [{t: source seconds, v: rate}]
      keyWords: {},   // word index -> true (always key) | false (never key)
      textEdits: {},  // word index -> replacement text
      callouts: [
        { on: true, kind: "card", start: 12.2, dur: 2.4, label: "#001 · First watch", title: "£15 Timex", x: 0.5, y: 41, path: null },
        { on: true, kind: "card", start: 21.7, dur: 2.2, label: "#002 · Age 18", title: "First Rolex", x: 0.5, y: 41, path: null },
        { on: true, kind: "stat", start: 25.0, dur: 1.9, label: "watches owned", title: "50+", x: 0.5, y: 41, path: null },
        { on: true, kind: "card", start: 29.4, dur: 3.2, label: "#003 · The grail", title: "Patek Philippe Nautilus 5711R", x: 0.5, y: 41, path: null }
      ]
    };
  }

  /* Bring an older saved config up to the current shape without losing edits. */
  function migrate(cfg, data) {
    if (!cfg || typeof cfg !== "object") return defaultConfig("editorial", data);
    var base = defaultConfig(cfg.preset, data);
    var out = Object.assign({}, base, cfg);
    ["captions", "look", "motion", "camera", "speed"].forEach(function (k) { out[k] = Object.assign({}, base[k], cfg[k] || {}); });
    if (!Array.isArray(out.camera.keys)) out.camera.keys = [];
    if (!Array.isArray(out.speed.points)) out.speed.points = [];
    if (!Array.isArray(out.framing) || out.framing.length !== base.framing.length) out.framing = base.framing;
    out.callouts = (cfg.callouts || base.callouts).map(function (c) {
      return Object.assign({ x: 0.5, y: 41, path: null }, c);
    });
    out.keyWords = cfg.keyWords || {};
    out.textEdits = cfg.textEdits || {};
    out.version = CONFIG_VERSION;
    return out;
  }

  /* Switch preset but keep the user's footage-specific edits. */
  function applyPreset(cfg, presetId) {
    var fresh = defaultConfig(presetId);
    ["framing", "keyWords", "textEdits", "callouts", "camera", "speed"].forEach(function (k) { fresh[k] = cfg[k]; });
    fresh.captions.y = cfg.captions.y;
    fresh.captions.on = cfg.captions.on;
    fresh.look.punch = cfg.look.punch;
    fresh.look.kenBurns = cfg.look.kenBurns;
    fresh.look.progress = cfg.look.progress;
    return fresh;
  }

  /* ---------- easing + helpers ---------- */
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function prog(t, start, dur) { return dur <= 0 ? (t >= start ? 1 : 0) : clamp((t - start) / dur, 0, 1); }
  function outCubic(p) { return 1 - Math.pow(1 - p, 3); }
  function outExpo(p) { return p >= 1 ? 1 : 1 - Math.pow(2, -10 * p); }
  function outBackK(p, k) { var c1 = 1.70158 * k, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); }
  function inOut(p) { return p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; }
  function hash(n) { var x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
  function ease(name, p) {
    switch (name) {
      case "linear": return p;
      case "in": return p * p * p;
      case "out": return outCubic(p);
      case "snap": return outExpo(p);
      default: return inOut(p);
    }
  }
  /* Smooth deterministic noise for handheld shake. */
  function noise(t, seed) {
    return Math.sin(t * 1.7 + seed) * 0.5 + Math.sin(t * 3.1 + seed * 2.3) * 0.3 + Math.sin(t * 7.3 + seed * 4.1) * 0.2;
  }

  /* ---------- virtual camera ---------- */
  var CAM_ID = { x: 0, y: 0, zoom: 1, rot: 0 };
  function cameraAt(cfg, t) {
    var keys = (cfg.camera && cfg.camera.keys || []).slice().sort(function (a, b) { return a.t - b.t; });
    var c;
    if (!keys.length) c = Object.assign({}, CAM_ID);
    else if (t <= keys[0].t) c = pick(keys[0]);
    else if (t >= keys[keys.length - 1].t) c = pick(keys[keys.length - 1]);
    else {
      for (var i = 0; i < keys.length - 1; i++) {
        var a = keys[i], b = keys[i + 1];
        if (t >= a.t && t <= b.t) {
          var p = ease(b.ease || "smooth", prog(t, a.t, b.t - a.t));
          c = { x: lerp(a.x, b.x, p), y: lerp(a.y, b.y, p), zoom: lerp(a.zoom, b.zoom, p), rot: lerp(a.rot, b.rot, p) };
          break;
        }
      }
    }
    var sh = cfg.camera && cfg.camera.shake || 0;
    if (sh > 0) {
      c.x += noise(t, 1.3) * 0.012 * sh;
      c.y += noise(t, 4.7) * 0.012 * sh;
      c.rot += noise(t, 9.1) * 0.8 * sh;
    }
    return c;
  }
  function pick(k) { return { x: k.x || 0, y: k.y || 0, zoom: k.zoom || 1, rot: k.rot || 0 }; }
  function lerp(a, b, p) { return (a || 0) + ((b || 0) - (a || 0)) * p; }

  /* ---------- speed ramp (time remap) ---------- */
  function rateAt(cfg, tSrc) {
    var pts = (cfg.speed && cfg.speed.points || []).slice().sort(function (a, b) { return a.t - b.t; });
    if (!cfg.speed || !cfg.speed.on || !pts.length) return 1;
    if (tSrc <= pts[0].t) return pts[0].v;
    if (tSrc >= pts[pts.length - 1].t) return pts[pts.length - 1].v;
    for (var i = 0; i < pts.length - 1; i++) {
      var a = pts[i], b = pts[i + 1];
      if (tSrc >= a.t && tSrc <= b.t) return lerp(a.v, b.v, inOut(prog(tSrc, a.t, b.t - a.t)));
    }
    return 1;
  }
  /* Table mapping output time <-> source time. Deterministic (fixed step). */
  function speedMap(cfg, duration) {
    var step = 1 / 240, src = [0], out = [0], ts = 0, to = 0;
    while (ts < duration) {
      var r = clamp(rateAt(cfg, ts + step / 2), 0.2, 4);
      ts = Math.min(duration, ts + step); to += step / r;
      src.push(ts); out.push(to);
    }
    function interp(xs, ys, x) {
      if (x <= xs[0]) return ys[0];
      if (x >= xs[xs.length - 1]) return ys[ys.length - 1];
      var lo = 0, hi = xs.length - 1;
      while (hi - lo > 1) { var m = (lo + hi) >> 1; if (xs[m] <= x) lo = m; else hi = m; }
      return ys[lo] + (ys[hi] - ys[lo]) * (x - xs[lo]) / (xs[hi] - xs[lo]);
    }
    return {
      on: !!(cfg.speed && cfg.speed.on && cfg.speed.points.length),
      outDuration: to,
      srcAt: function (tOut) { return interp(out, src, tOut); },
      outAt: function (tSrc) { return interp(src, out, tSrc); },
      rateAt: function (tSrc) { return clamp(rateAt(cfg, tSrc), 0.2, 4); }
    };
  }

  /* ---------- caption chunking ---------- */
  function wordText(cfg, words, i) {
    return cfg.textEdits && cfg.textEdits[i] != null ? cfg.textEdits[i] : words[i].t;
  }
  function bare(s) { return s.toLowerCase().replace(/[^a-z0-9£$€+']/g, ""); }

  function buildChunks(cfg, data) {
    var words = data.words, chunks = [], cur = null, maxW = cfg.captions.maxWords;
    for (var i = 0; i < words.length; i++) {
      var w = words[i], prev = words[i - 1];
      var brk = !cur || cur.idx.length >= maxW ||
        (prev && /[.,!?;:]$/.test(wordText(cfg, words, i - 1))) ||
        (prev && w.s - prev.e > 0.45);
      if (brk) { cur = { idx: [], s: w.s, e: w.e }; chunks.push(cur); }
      cur.idx.push(i); cur.e = w.e;
    }
    var keyCount = 0;
    chunks.forEach(function (c, ci) {
      var forced = c.idx.filter(function (i) { return cfg.keyWords[i] === true; });
      var key = forced, reason = forced.length ? "forced" : null;
      if (!key.length && cfg.captions.autoKey) {
        var best = -1, bestScore = 0, bestWhy = null;
        c.idx.forEach(function (i, k) {
          if (cfg.keyWords[i] === false) return;
          var raw = wordText(cfg, words, i), b = bare(raw);
          if (!b || STOP.has(b)) return;
          var score = b.length >= 5 ? b.length : 0, why = "long";
          if (/\d/.test(b)) { score += 8; why = "number"; }
          else if (/^[A-Z£$]/.test(raw) && k > 0) { score += 4; why = "name"; }
          if (score > bestScore) { bestScore = score; best = i; bestWhy = why; }
        });
        if (best >= 0 && bestScore >= 6) { key = [best]; reason = bestWhy; }
      }
      c.key = new Set(key);
      c.keyReason = reason;
      c.punch = key.length ? (keyCount++ % 2 === 0) : false;
      var next = chunks[ci + 1];
      c.show = next ? Math.min(c.e + 0.6, next.s - 0.04) : c.e + 0.8;
    });
    return chunks;
  }

  /* ---------- styles (injected once) ---------- */
  var CSS = "" +
    ".re-stage{position:relative;width:1080px;height:1920px;overflow:hidden;background:#050507;transform-origin:0 0;" +
    "--re-accent:#4b3cf0;--re-text:#fff;contain:strict}" +
    ".re-cam{position:absolute;inset:0;transform-origin:50% 50%}" +
    ".re-face{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;will-change:transform}" +
    ".re-face video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}" +
    ".re-layer{position:absolute;inset:0;pointer-events:none}" +
    ".re-vig{background:radial-gradient(ellipse 75% 60% at 50% 42%,transparent 45%,#000 100%)}" +
    ".re-fade{background:linear-gradient(to top,#000 0%,rgba(0,0,0,.55) 18%,transparent 40%)}" +
    ".re-grain{background-image:radial-gradient(rgba(255,255,255,.9) 1px,transparent 1px),radial-gradient(rgba(0,0,0,.9) 1px,transparent 1px);" +
    "background-size:3px 3px,5px 5px;mix-blend-mode:overlay}" +
    ".re-prog{position:absolute;left:0;top:0;height:10px;background:var(--re-accent);transform-origin:0 0;width:100%}" +
    ".re-cap{position:absolute;left:90px;right:90px;display:flex;flex-wrap:wrap;justify-content:center;align-items:baseline;" +
    "row-gap:0;text-align:center;transform:translateY(-50%);line-height:1.05}" +
    ".re-br{flex-basis:100%;height:0}" +
    ".re-w{position:relative;display:inline-block;isolation:isolate;white-space:nowrap;color:var(--re-text);" +
    "text-shadow:0 3px 18px rgba(0,0,0,.55)}" +
    ".re-blk{position:absolute;left:-.12em;right:-.12em;top:.08em;bottom:.02em;background:var(--re-accent);z-index:-1;transform-origin:0 50%;transform:scaleX(0)}" +
    ".re-k-serif{color:var(--re-accent);text-shadow:0 0 40px rgba(0,0,0,.35)}" +
    ".re-k-color{color:var(--re-accent)}" +
    ".re-k-glow .re-tx{background:linear-gradient(180deg,color-mix(in srgb,var(--re-accent) 45%,#fff) 0%,var(--re-accent) 55%,color-mix(in srgb,var(--re-accent) 80%,#b34700) 100%);" +
    "-webkit-background-clip:text;background-clip:text;color:transparent}" +
    ".re-k-glow{text-shadow:none}" +
    ".re-stroke{text-shadow:0 0 2px #000,3px 3px 0 #000,-3px 3px 0 #000,3px -3px 0 #000,-3px -3px 0 #000,0 6px 24px rgba(0,0,0,.6)}" +
    ".re-call{position:absolute;display:flex;flex-direction:column;align-items:center;gap:10px;" +
    "padding:26px 46px 30px;border-radius:30px;max-width:860px;text-align:center}" +
    ".re-call.glass{background:linear-gradient(135deg,rgba(255,255,255,.16),rgba(255,255,255,.05));" +
    "border:1.5px solid rgba(255,255,255,.22);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.3),0 24px 60px rgba(0,0,0,.45);backdrop-filter:blur(18px) saturate(1.2)}" +
    ".re-call.editorial{background:#e4e0d6;color:#121212;border-radius:6px;box-shadow:0 30px 70px rgba(0,0,0,.5)}" +
    ".re-call .re-cl{font:600 30px/1 'Inter',system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--re-accent)}" +
    ".re-call .re-ct{font-size:76px;line-height:1;color:#fff}" +
    ".re-call.editorial .re-ct{color:#121212}" +
    ".re-call.stat .re-ct{font-size:170px}";

  function injectCSS(doc) {
    if (doc.getElementById("re-engine-css")) return;
    var s = doc.createElement("style"); s.id = "re-engine-css"; s.textContent = CSS;
    doc.head.appendChild(s);
  }

  /* point along a polyline (normalized coords) by arc length */
  function pathPoint(path, p) {
    if (!path || path.length < 2) return null;
    var lens = [0], total = 0;
    for (var i = 1; i < path.length; i++) {
      total += Math.hypot((path[i][0] - path[i - 1][0]) * STAGE_W, (path[i][1] - path[i - 1][1]) * STAGE_H);
      lens.push(total);
    }
    if (total === 0) return path[0];
    var d = p * total;
    for (var j = 1; j < lens.length; j++) {
      if (d <= lens[j]) {
        var f = (d - lens[j - 1]) / (lens[j] - lens[j - 1] || 1);
        return [lerp(path[j - 1][0], path[j][0], f), lerp(path[j - 1][1], path[j][1], f)];
      }
    }
    return path[path.length - 1];
  }

  /* ---------- engine ---------- */
  function create(stage, data, config, opts) {
    opts = opts || {};
    var doc = stage.ownerDocument;
    injectCSS(doc);
    stage.classList.add("re-stage");

    var cam = stage.querySelector(".re-cam");
    if (!cam) { cam = doc.createElement("div"); cam.className = "re-cam"; stage.insertBefore(cam, stage.firstChild); }
    var face = stage.querySelector(".re-face");
    if (!face) { face = doc.createElement("div"); face.className = "re-face"; }
    if (face.parentNode !== cam) cam.appendChild(face);
    if (opts.video && opts.video.parentNode !== face) face.appendChild(opts.video);
    var video = opts.video || face.querySelector("video");

    function layer(cls) { var d = doc.createElement("div"); d.className = "re-layer " + cls; stage.appendChild(d); return d; }
    var vig = layer("re-vig"), fade = layer("re-fade"), grain = layer("re-grain");
    var capLayer = layer("re-caps"), callLayer = layer("re-calls");
    var progEl = doc.createElement("div"); progEl.className = "re-prog"; stage.appendChild(progEl);

    var cfg, chunks, chunkEls, callEls;

    function fontStack(f) {
      var serif = /Serif|Playfair/.test(f);
      return "'" + f + "'," + (serif ? "Georgia,serif" : "system-ui,sans-serif");
    }

    function build() {
      var c = cfg.captions;
      stage.style.setProperty("--re-accent", cfg.accent);
      stage.style.setProperty("--re-text", cfg.text);
      chunks = buildChunks(cfg, data);
      capLayer.textContent = "";
      chunkEls = chunks.map(function (ch, ci) {
        var box = doc.createElement("div");
        box.className = "re-cap";
        box.dataset.chunk = ci;
        box.style.top = c.y + "%";
        box.style.columnGap = Math.round(c.bodySize * c.scale * 0.3) + "px";
        var els = ch.idx.map(function (i, k) {
          var isKey = ch.key.has(i);
          if (isKey && c.keyLine && k > 0) { var br = doc.createElement("span"); br.className = "re-br"; box.appendChild(br); }
          var w = doc.createElement("span");
          w.className = "re-w" + (isKey ? " re-k re-k-" + c.keyStyle : "") + (c.keyStyle === "color" ? " re-stroke" : "");
          w.dataset.word = i;
          var blk = doc.createElement("span"); blk.className = "re-blk"; w.appendChild(blk);
          var tx = doc.createElement("span"); tx.className = "re-tx";
          var txt = wordText(cfg, data.words, i);
          tx.textContent = c.uppercase ? txt.toUpperCase() : txt;
          w.appendChild(tx);
          var useKeyFont = isKey && c.keyStyle !== "color";
          w.style.fontFamily = fontStack(useKeyFont ? c.keyFont : c.bodyFont);
          w.style.fontWeight = useKeyFont ? c.keyWeight : c.bodyWeight;
          w.style.fontStyle = useKeyFont && c.keyItalic ? "italic" : "normal";
          w.style.fontSize = Math.round((useKeyFont ? c.keySize : c.bodySize) * c.scale) + "px";
          if (isKey && c.keyStyle === "block") { w.style.color = "#fff"; }
          box.appendChild(w);
          if (isKey && c.keyLine && k < ch.idx.length - 1) { var br2 = doc.createElement("span"); br2.className = "re-br"; box.appendChild(br2); }
          return { el: w, blk: blk, i: i, key: isKey };
        });
        capLayer.appendChild(box);
        return { box: box, words: els };
      });

      callLayer.textContent = "";
      callEls = (cfg.callouts || []).map(function (co, k) {
        var el = doc.createElement("div");
        el.className = "re-call " + (cfg.calloutStyle === "editorial" ? "editorial" : "glass") + (co.kind === "stat" ? " stat" : "");
        el.dataset.callout = k;
        var lab = doc.createElement("div"); lab.className = "re-cl"; lab.textContent = co.label || "";
        var tit = doc.createElement("div"); tit.className = "re-ct"; tit.textContent = co.title || "";
        tit.style.fontFamily = fontStack(c.keyFont);
        tit.style.fontWeight = c.keyWeight;
        tit.style.fontStyle = c.keyItalic ? "italic" : "normal";
        if (co.kind === "stat") { el.appendChild(tit); el.appendChild(lab); } else { el.appendChild(lab); el.appendChild(tit); }
        callLayer.appendChild(el);
        var m = co.kind === "stat" ? /^([^\d]*)(\d+)(.*)$/.exec(co.title || "") : null;
        return { el: el, tit: tit, co: co, num: m ? { pre: m[1], n: +m[2], post: m[3] } : null };
      });

      var L = cfg.look;
      vig.style.opacity = L.vignette;
      fade.style.opacity = L.bottomFade;
      grain.style.opacity = L.grain;
      progEl.style.display = L.progress ? "block" : "none";
      if (video) video.style.filter = gradeFilter(L.grade);
    }

    function gradeFilter(g) {
      switch (g) {
        case "warm": return "contrast(1.1) saturate(1.18) sepia(.16) brightness(.96)";
        case "cool": return "contrast(1.1) saturate(.92) hue-rotate(6deg) brightness(.95)";
        case "mono": return "grayscale(1) contrast(1.18) brightness(.95)";
        case "none": return "none";
        default: return "contrast(1.08) saturate(1.08) brightness(.97)";
      }
    }

    function shotAt(t) {
      var s = data.shots;
      for (var i = 0; i < s.length; i++) if (t < s[i].e) return i;
      return s.length - 1;
    }

    function punchAt(t) {
      if (!cfg.look.punch) return 1;
      var amt = cfg.motion.punch, z = 1;
      for (var i = 0; i < chunks.length; i++) {
        var ch = chunks[i];
        if (!ch.punch) continue;
        if (t < ch.s - 0.1 || t > ch.show + 0.2) continue;
        var pin = outExpo(prog(t, ch.s - 0.1, 0.18));
        var pout = 1 - inOut(prog(t, ch.show, 0.2));
        z = Math.max(z, 1 + amt * Math.min(pin, pout));
      }
      return z;
    }

    function render(t) {
      var M = cfg.motion;
      /* face framing = per-shot framing + virtual camera */
      var si = shotAt(t), shot = data.shots[si], fr = cfg.framing[si] || { x: 0.5, zoom: 1 };
      var cm = cameraAt(cfg, t);
      var kb = cfg.look.kenBurns ? 1 + M.push * prog(t, shot.s, shot.e - shot.s) : 1;
      var s = (STAGE_H / SRC_H) * fr.zoom * cm.zoom * kb * punchAt(t);
      var W = SRC_W * s, H = SRC_H * s;
      var cx = fr.x + cm.x, cy = 0.36 + cm.y;
      var x = clamp(STAGE_W / 2 - cx * W, STAGE_W - W, 0);
      var y = clamp(STAGE_H * 0.36 - cy * H, STAGE_H - H, 0);
      face.style.transform = "translate(" + x.toFixed(2) + "px," + y.toFixed(2) + "px) scale(" + s.toFixed(5) + ")";
      var rr = cm.rot * Math.PI / 180, cover = 1 + Math.abs(Math.sin(rr)) * 0.9;
      cam.style.transform = cm.rot ? "rotate(" + cm.rot.toFixed(3) + "deg) scale(" + cover.toFixed(4) + ")" : "";

      var f = Math.floor(t * 30);
      grain.style.backgroundPosition = Math.floor(hash(f) * 50) + "px " + Math.floor(hash(f + 7) * 50) + "px," +
        Math.floor(hash(f + 3) * 50) + "px " + Math.floor(hash(f + 11) * 50) + "px";

      progEl.style.transform = "scaleX(" + clamp(t / data.duration, 0, 1).toFixed(4) + ")";

      /* captions */
      var c = cfg.captions;
      for (var k = 0; k < chunks.length; k++) {
        var ch = chunks[k], ce = chunkEls[k];
        var visible = c.on && t >= ch.s - 0.08 && t < ch.show;
        if (!visible) { ce.box.style.visibility = "hidden"; continue; }
        ce.box.style.visibility = "visible";
        ce.box.style.opacity = (1 - prog(t, ch.show - 0.12, 0.12)).toFixed(3);
        for (var j = 0; j < ce.words.length; j++) styleWord(ce.words[j], ch, j, t);
      }

      /* callouts */
      for (var m = 0; m < callEls.length; m++) {
        var ca = callEls[m], co = ca.co;
        var on = co.on && t >= co.start && t < co.start + co.dur;
        if (!on) { ca.el.style.visibility = "hidden"; continue; }
        ca.el.style.visibility = "visible";
        var pi = outBackK(prog(t, co.start, M.callIn), M.callBounce), po = inOut(prog(t, co.start + co.dur - 0.25, 0.25));
        ca.el.style.opacity = (Math.min(1, prog(t, co.start, M.callIn * 0.55)) * (1 - po)).toFixed(3);
        var pt = pathPoint(co.path, inOut(prog(t, co.start, co.dur)));
        var sc = (0.9 + 0.1 * pi).toFixed(4);
        if (pt) {
          ca.el.style.left = (pt[0] * 100).toFixed(3) + "%";
          ca.el.style.top = (pt[1] * 100).toFixed(3) + "%";
          ca.el.style.transform = "translate(-50%,-50%) scale(" + sc + ")";
        } else {
          ca.el.style.left = ((co.x != null ? co.x : 0.5) * 100).toFixed(3) + "%";
          ca.el.style.top = (co.y != null ? co.y : 41) + "%";
          ca.el.style.transform = "translateX(-50%) translateY(" + ((1 - pi) * 60 - po * 30).toFixed(1) + "px) scale(" + sc + ")";
        }
        if (ca.num) {
          var n = Math.round(ca.num.n * outCubic(prog(t, co.start + 0.05, 0.8)));
          ca.tit.textContent = ca.num.pre + n + ca.num.post;
        }
      }
    }

    function styleWord(w, ch, j, t) {
      var c = cfg.captions, M = cfg.motion, word = data.words[w.i];
      var start = c.reveal === "chunk" ? ch.s - 0.08 : word.s - 0.06;
      var el = w.el;
      if (c.keyStyle === "color" && !w.key) {
        var p0 = outCubic(prog(t, ch.s - 0.08, M.capIn));
        var active = t >= word.s && (j === ch.idx.length - 1 || t < data.words[ch.idx[j + 1]].s);
        var spoken = t >= word.s;
        el.style.color = active ? cfg.accent : "";
        el.style.transform = "translateY(" + ((1 - p0) * M.capRise).toFixed(1) + "px) scale(" + (active ? 1.08 : 1) + ")";
        el.style.filter = "";
        el.style.opacity = (p0 * (spoken || c.reveal === "chunk" ? 1 : 0.55)).toFixed(3);
        return;
      }
      if (w.key) {
        var ks = c.keyStyle, kstart = word.s - 0.06;
        if (ks === "color") {
          var pc = outCubic(prog(t, ch.s - 0.08, M.capIn));
          var act = t >= word.s, pp = outBackK(prog(t, word.s, M.keyIn), 1);
          el.style.opacity = pc.toFixed(3);
          el.style.transform = "scale(" + (act ? 1 + (M.keyScale - 1) * pp : 1).toFixed(4) + ")";
          el.style.color = act ? cfg.accent : "";
          return;
        }
        if (ks === "glow") {
          var pg = prog(t, kstart, M.keyIn);
          el.style.opacity = Math.min(1, pg * 2.5).toFixed(3);
          el.style.transform = "scale(" + (M.keyScale - (M.keyScale - 1) * outBackK(pg, 1)).toFixed(4) + ")";
          el.style.filter = "blur(" + ((1 - outCubic(pg)) * 14).toFixed(1) + "px) drop-shadow(0 0 26px color-mix(in srgb," + cfg.accent + " 65%,transparent))";
          return;
        }
        if (ks === "block") {
          var pb = prog(t, kstart, M.keyIn);
          el.style.opacity = Math.min(1, pb * 3).toFixed(3);
          el.style.transform = "translateY(" + ((1 - outCubic(pb)) * 18).toFixed(1) + "px) scale(" + (M.keyScale - (M.keyScale - 1) * outExpo(pb)).toFixed(4) + ")";
          w.blk.style.transform = "scaleX(" + outExpo(pb).toFixed(4) + ")";
          return;
        }
        var ps = prog(t, kstart, M.keyIn);
        el.style.opacity = Math.min(1, ps * 2.2).toFixed(3);
        el.style.transform = "scale(" + (M.keyScale - (M.keyScale - 1) * outExpo(ps)).toFixed(4) + ")";
        el.style.filter = "blur(" + ((1 - outCubic(ps)) * 10).toFixed(1) + "px)";
        return;
      }
      var p = prog(t, start, M.capIn), e = outCubic(p);
      el.style.opacity = e.toFixed(3);
      el.style.transform = "translateY(" + ((1 - e) * M.capRise).toFixed(1) + "px)";
      el.style.filter = p < 1 && M.capBlur > 0 ? "blur(" + ((1 - e) * M.capBlur).toFixed(1) + "px)" : "";
    }

    function setConfig(next) { cfg = next; build(); }
    setConfig(config);

    return {
      render: render,
      setConfig: setConfig,
      chunks: function () { return chunks; },
      config: function () { return cfg; },
      camera: function (t) { return cameraAt(cfg, t); }
    };
  }

  global.ReelEngine = {
    create: create, defaultConfig: defaultConfig, applyPreset: applyPreset, migrate: migrate,
    buildChunks: buildChunks, wordText: wordText, cameraAt: cameraAt, speedMap: speedMap, rateAt: rateAt,
    PRESETS: PRESETS, FONTS: FONTS, EASES: EASES, STAGE_W: STAGE_W, STAGE_H: STAGE_H, CONFIG_VERSION: CONFIG_VERSION
  };
})(typeof window !== "undefined" ? window : this);
