/* Motion System — core.
 * Content-agnostic: knows aspect-ratio profiles, timing helpers, and how to
 * mount a clip (footage map + beat script + transcript) onto a root composition.
 * Components register themselves on MS.components and receive a `ctx`.
 * Everything runs synchronously at load (render contract: no async timelines).
 */
(function () {
  var MS = (window.MS = window.MS || {});
  MS.components = MS.components || {};
  MS.FPS = 30;

  // Snap a time to the frame grid so tween ends land on whole frames.
  MS.snap = function (t) {
    return Math.round(t * MS.FPS) / MS.FPS;
  };

  // Approved tokens, mirrored for GSAP (CSS vars can't be read as eases).
  MS.EASE = { enter: "power3.out", move: "power2.inOut", emphasis: "expo.out", exit: "power2.in" };
  MS.DUR = { micro: 0.18, standard: 0.45, structural: 0.8 };
  MS.COLOR = {
    text: "#F4F1EA",
    textDim: "rgba(244,241,234,0.62)",
    accent: "#3D7BFF",
    warn: "#FF9F43",
    nearBlack: "#0B0B0D",
  };

  /* Aspect profiles. Components read layout from here — never hard-code a
   * frame size. Rects are [x, y, w, h] in composition pixels. */
  MS.PROFILES = {
    landscape: {
      W: 1920,
      H: 1080,
      margin: 96,
      // The speaker is centered; the open wall on the left is the primary zone.
      zones: { primary: [96, 150, 640, 470] },
      type: { headline: 76, label: 52, eyebrow: 28 }, // 28 px = phone reading floor (2.6% of short side)
      captions: {
        // aside: on the footage's open side, sharing the headline's left edge —
        // used when the footage map declares an openSide.
        aside: { size: 42, maxChars: 40, bottom: 360, align: "left", maxWidth: 470 },
        bottom: { size: 44, maxChars: 44, bottom: 64, align: "center", maxWidth: 1240 },
        lifted: { size: 44, maxChars: 44, bottom: 290, align: "center", maxWidth: 1240 },
      },
      speaker: { modes: { frame: { scale: 1, y: 0, clipTop: 0 } }, defaultMode: "frame", follow: 0 },
    },
    portrait: {
      W: 1080,
      H: 1920,
      margin: 64,
      safe: { top: 220, bottom: 380, right: 140 },
      seamY: 960,
      // Graphic stage above the speaker (SPLIT layout), inside the safe zones.
      zones: { stage: [64, 220, 876, 700] },
      type: { headline: 100, label: 60, eyebrow: 28 },
      captions: {
        seam: { size: 48, maxChars: 40, bottom: 1920 - 932, align: "left", maxWidth: 876 },
        top: { size: 48, maxChars: 40, top: 236, align: "left", maxWidth: 876 },
        stage: { size: 70, maxChars: 52, align: "left", maxWidth: 876 },
        chest: { size: 56, maxChars: 34, bottom: 420, align: "center", maxWidth: 876 },
      },
      speaker: {
        // SPLIT: native-resolution 1080×960 crop under the stage (no upscale).
        // FULL: 608×1080 crop scaled 1.78× to fill the frame (softer — use briefly).
        modes: {
          split: { scale: 1, y: 960 - 40, clipTop: 960 },
          full: { scale: 1920 / 1080, y: 0, clipTop: 0 },
        },
        defaultMode: "split",
        follow: 0.6, // how much the crop follows the head (0 = locked, 1 = glued)
        modeDur: 0.5,
        modeLead: 0.25,
      },
    },
  };

  /* Helpers ------------------------------------------------------------- */

  MS.el = function (tag, cls, parent, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  };

  MS.place = function (e, rect) {
    e.style.left = rect[0] + "px";
    e.style.top = rect[1] + "px";
    e.style.width = rect[2] + "px";
    e.style.height = rect[3] + "px";
  };

  // Inline markup for display text: "in the next {{10 years|mono}}" or
  // "pretty {{pricey.|warn@18.03}}". Returns [{text, style, at}].
  MS.parseMarkup = function (s) {
    var out = [];
    var re = /\{\{(.+?)\|([\w-]+)(?:@([\d.]+))?\}\}/g;
    var last = 0;
    var m;
    while ((m = re.exec(s))) {
      if (m.index > last) out.push({ text: s.slice(last, m.index) });
      out.push({ text: m[1], style: m[2], at: m[3] != null ? parseFloat(m[3]) : null });
      last = re.lastIndex;
    }
    if (last < s.length) out.push({ text: s.slice(last) });
    return out;
  };

  function rectContains(r, x, y) {
    return x >= r[0] && x <= r[2] && y >= r[1] && y <= r[3];
  }
  MS.rectsOverlap = function (a, b) {
    return a[0] < b[2] && a[2] > b[0] && a[1] < b[3] && a[3] > b[1];
  };

  /* Mount --------------------------------------------------------------- */

  MS.mount = function (opts) {
    var root = opts.root;
    var clipId = opts.clip;
    var clip = window.MS_CLIPS[clipId];
    var footage = window.MS_FOOTAGE[clipId];
    var words = window.MS_TRANSCRIPTS[clipId];
    var W = +root.getAttribute("data-width");
    var H = +root.getAttribute("data-height");
    var aspect = W >= H ? "landscape" : "portrait";
    var P = MS.PROFILES[aspect];
    var duration = +root.getAttribute("data-duration");
    root.setAttribute("data-aspect", aspect);
    root.style.width = W + "px"; // don't rely on the runtime to size the root
    root.style.height = H + "px";

    var tl = gsap.timeline({ paused: true });
    var overlay = root.querySelector(".ms-overlay");

    var ctx = {
      aspect: aspect,
      P: P,
      W: W,
      H: H,
      tl: tl,
      root: root,
      overlay: overlay,
      clip: clip,
      footage: footage,
      words: words,
      duration: duration,
      stageUse: [], // portrait: [start, end, region] where a component uses the stage
      suppress: [], // intervals where captions stay hidden (graphic says the words)
      // region: "all" (whole stage) or "lower" (bottom part + the seam)
      occupy: function (a, b, region) {
        ctx.stageUse.push([a, b, region || "all"]);
      },
      // → null | "all" | "lower" for the busiest use overlapping [t0, t1]
      stageBusy: function (t0, t1) {
        var r = null;
        ctx.stageUse.forEach(function (u) {
          if (t0 < u[1] && t1 > u[0]) r = r === "all" || u[2] === "all" ? "all" : u[2];
        });
        return r;
      },
      // true if a source-space point sits where the accent would merge with footage
      accentBlocked: function (sx, sy) {
        return (footage.avoidAccent || []).some(function (a) {
          return rectContains(a.rect, sx, sy);
        });
      },
    };

    MS.components.speakerFrame(ctx);

    (clip.beats || []).forEach(function (beat) {
      var spec = Object.assign({}, beat, beat[aspect] || {});
      if (spec.skip) return;
      var fn = MS.components[spec.component];
      if (!fn) throw new Error("[MS] unknown component: " + spec.component);
      fn(ctx, spec);
    });

    if (clip.captions !== false) MS.components.captions(ctx, clip.captions || {});

    tl.set({}, {}, duration); // pad to the slot (Law 11)
    MS.ctx = ctx; // exposed for preview debugging
    return ctx; // the entry file registers ctx.tl on window.__timelines (lint reads it there)
  };
})();
