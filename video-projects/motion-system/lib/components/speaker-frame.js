/* C8 — Speaker Frame.
 * Frames the source footage for the current aspect ratio and exposes a mapping
 * from source pixels to composition pixels so other components can anchor to
 * the speaker. The footage itself is never graded or filtered.
 *
 * DOM: .ms-speaker (clip-path) > .ms-stage (translate + scale) > .ms-track (x follow) > <video>
 * A source point (sx, sy) lands at:  x = W/2 + s·(sx − c(t)),  y = stageY + s·sy
 * where c(t) is the crop center (follows the head by `follow`).
 */
(function () {
  var MS = window.MS;

  MS.components.speakerFrame = function (ctx) {
    var P = ctx.P;
    var cfg = P.speaker;
    var tl = ctx.tl;
    var src = ctx.footage.source;
    var head = ctx.footage.head;
    var wrap = ctx.root.querySelector(".ms-speaker");
    var stage = ctx.root.querySelector(".ms-stage");
    var track = ctx.root.querySelector(".ms-track");

    // Smoothed head track (3-tap moving average) so the crop never jitters.
    var raw = head.samples;
    var smooth = raw.map(function (s, i) {
      var a = raw[Math.max(0, i - 1)][1];
      var b = raw[Math.min(raw.length - 1, i + 1)][1];
      return [s[0], (a + 2 * s[1] + b) / 4, s[2]];
    });
    var mean =
      smooth.reduce(function (acc, s) {
        return acc + s[1];
      }, 0) / smooth.length;

    function lerpSample(t, idx) {
      if (t <= smooth[0][0]) return smooth[0][idx];
      for (var i = 1; i < smooth.length; i++) {
        if (t <= smooth[i][0]) {
          var a = smooth[i - 1];
          var b = smooth[i];
          var k = (t - a[0]) / (b[0] - a[0]);
          return a[idx] + (b[idx] - a[idx]) * k;
        }
      }
      return smooth[smooth.length - 1][idx];
    }
    var headX = function (t) {
      return lerpSample(t, 1);
    };
    var faceTop = function (t) {
      return lerpSample(t, 2);
    };
    var cropCenter = function (t) {
      return cfg.follow ? mean + cfg.follow * (headX(t) - mean) : src.width / 2;
    };

    // Layout modes over time (portrait only; landscape stays "frame").
    var schedule = ((ctx.clip.layout || {})[ctx.aspect] || []).slice();
    if (!schedule.length || schedule[0].at > 0) schedule.unshift({ at: 0, mode: cfg.defaultMode });
    function modeAt(t) {
      var m = schedule[0].mode;
      schedule.forEach(function (s) {
        var switchAt = s.at === 0 ? 0 : s.at - (cfg.modeLead || 0);
        if (t >= switchAt) m = s.mode;
      });
      return m;
    }

    // Logical layout at t: switches exactly on the beat time (no camera lead).
    // Captions and other content decisions use this; modeAt() is the visual state.
    function layoutAt(t) {
      var m = schedule[0].mode;
      schedule.forEach(function (s) {
        if (t >= s.at) m = s.mode;
      });
      return m;
    }

    function stageVars(mode) {
      var m = cfg.modes[mode];
      return { x: ctx.W / 2 - m.scale * (src.width / 2), y: m.y, scale: m.scale };
    }

    // Initial state
    var m0 = schedule[0].mode;
    gsap.set(stage, Object.assign({ transformOrigin: "0 0" }, stageVars(m0)));
    gsap.set(wrap, { clipPath: "inset(" + cfg.modes[m0].clipTop + "px 0px 0px 0px)" });
    gsap.set(track, { x: src.width / 2 - cropCenter(0) });

    // Crop follows the head between samples (linear, matches the mapping below).
    if (cfg.follow) {
      for (var i = 1; i < smooth.length; i++) {
        var t0 = smooth[i - 1][0];
        var t1 = smooth[i][0];
        tl.to(track, { x: src.width / 2 - cropCenter(t1), duration: t1 - t0, ease: "none" }, t0);
      }
    }

    // Mode changes: an eased camera move, starting slightly before the beat.
    var seam = ctx.root.querySelector(".ms-seam");
    for (var j = 1; j < schedule.length; j++) {
      var s = schedule[j];
      var at = MS.snap(s.at - (cfg.modeLead || 0));
      var d = cfg.modeDur || 0.5;
      tl.to(stage, Object.assign({ duration: d, ease: MS.EASE.move }, stageVars(s.mode)), at);
      tl.to(wrap, { clipPath: "inset(" + cfg.modes[s.mode].clipTop + "px 0px 0px 0px)", duration: d, ease: MS.EASE.move }, at);
      if (seam) tl.to(seam, { opacity: cfg.modes[s.mode].clipTop ? 1 : 0, duration: d * 0.6, ease: MS.EASE.move }, at);
    }
    if (seam) gsap.set(seam, { opacity: cfg.modes[m0].clipTop ? 1 : 0 });

    // Public API for other components.
    ctx.frame = {
      modeAt: modeAt,
      layoutAt: layoutAt,
      headX: headX,
      faceTop: faceTop,
      head: head,
      // Source px → composition px at time t (valid while not mid mode-change).
      map: function (t, sx, sy) {
        var m = cfg.modes[modeAt(t)];
        return { x: ctx.W / 2 + m.scale * (sx - cropCenter(t)), y: m.y + m.scale * sy, scale: m.scale };
      },
      // Visible head box in composition px at time t.
      headBox: function (t) {
        var cx = headX(t);
        var top = faceTop(t) - head.hairAbove;
        var a = this.map(t, cx - head.width / 2, top);
        var b = this.map(t, cx + head.width / 2, head.chinY);
        return [a.x, a.y, b.x, b.y];
      },
      // Gesture windows as composition-px rects.
      gestureRects: function (t0, t1) {
        var self = this;
        return (ctx.footage.gestures || [])
          .filter(function (g) {
            return t0 < g.end && t1 > g.start;
          })
          .map(function (g) {
            var t = Math.max(t0, g.start);
            var a = self.map(t, g.rect[0], g.rect[1]);
            var b = self.map(t, g.rect[2], g.rect[3]);
            return [a.x, a.y, b.x, b.y];
          });
      },
    };
  };
})();
