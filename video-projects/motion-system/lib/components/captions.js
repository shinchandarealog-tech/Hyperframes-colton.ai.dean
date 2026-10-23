/* C7 — Captions.
 * Phrase-chunked, word-synced captions whose size, position, line length and
 * alignment come from the aspect profile, not from a single shared layout.
 *
 * Placements:
 *  landscape  bottom  — centered over the chest; `lifted` above the hands when
 *                       a gesture window would collide with the caption box.
 *  portrait   seam    — small, left-aligned, just above the speaker when a
 *                       component occupies the stage.
 *             top     — top of the stage when a component uses its lower part
 *                       (e.g. a label whose leader crosses the seam).
 *             stage   — large editorial captions filling the stage when it is
 *                       otherwise empty (SPLIT layout).
 *             chest   — centered over the chest in FULL layout.
 * Words brighten as they're spoken (fill model); no pops, no pills, no strokes.
 * Captions hide while a graphic is already showing the same words (ctx.suppress).
 */
(function () {
  var MS = window.MS;
  // Prefer starting a new phrase on these words once the current one has some body.
  var BREAK_BEFORE = /^(so|but|and|or|because|before|after|over|if|when|which|while|until)$/i;
  var KEEP_WITH_NEXT = /^(a|an|the|my|your|our|their|his|her|its|of|to|in|for|on|at|by|with|from)$/i;

  MS.components.captions = function (ctx, opts) {
    var P = ctx.P;
    var tl = ctx.tl;
    var C = P.captions;
    var words = ctx.words;

    function suppressed(w) {
      return ctx.suppress.some(function (s) {
        return w.start >= s[0] && w.start < s[1];
      });
    }
    function basePlacement(w) {
      if (ctx.aspect === "landscape") return "bottom";
      if (ctx.frame.modeAt(w.start) === "full") return "chest";
      var busy = ctx.stageBusy(w.start, w.end);
      return busy === "all" ? "seam" : busy === "lower" ? "top" : "stage";
    }

    // 1a. Clauses (runs of contiguous, unsuppressed words ending at , . ? !).
    //     Each clause gets ONE placement — its majority — so a caption never
    //     jumps position mid-thought when a graphic hands the stage over.
    var clauses = [];
    var cl = null;
    words.forEach(function (w, i) {
      if (suppressed(w)) {
        cl = null;
        return;
      }
      if (!cl) clauses.push((cl = []));
      cl.push(i);
      if (/[,.?!]$/.test(w.text)) cl = null;
    });
    // Fold very short comma clauses ("Now,") into the following clause.
    for (var ci = clauses.length - 2; ci >= 0; ci--) {
      var a = clauses[ci];
      var b = clauses[ci + 1];
      var short = a.map(function (i) { return words[i].text; }).join(" ").length < 12;
      if (short && /,$/.test(words[a[a.length - 1]].text) && b[0] === a[a.length - 1] + 1) {
        clauses.splice(ci, 2, a.concat(b));
      }
    }
    var placeOf = {};
    clauses.forEach(function (c) {
      var votes = {};
      var best = null;
      c.forEach(function (i) {
        var p = basePlacement(words[i]);
        votes[p] = (votes[p] || 0) + 1;
        if (!best || votes[p] >= votes[best]) best = p;
      });
      c.forEach(function (i) {
        placeOf[i] = best;
      });
    });

    // 1b. Split each clause into phrases that fit the placement's budget:
    //     hard splits at pauses, then balanced splits near the middle that
    //     prefer starting the second half on a conjunction ("so", "but"…).
    function textOf(idxs) {
      return idxs
        .map(function (i) {
          return words[i].text;
        })
        .join(" ");
    }
    function split(idxs, lim) {
      var text = textOf(idxs);
      if (text.length <= lim || idxs.length < 2) return [idxs];
      var best = -1;
      var bestScore = Infinity;
      for (var j = 1; j < idxs.length; j++) {
        var left = textOf(idxs.slice(0, j)).length;
        var right = text.length - left - 1;
        if (left < 8 || right < 8) continue;
        var score = Math.abs(left - right) - (BREAK_BEFORE.test(words[idxs[j]].text) ? 16 : 0);
        // don't strand a function word from what it introduces ("your | finances")
        if (KEEP_WITH_NEXT.test(words[idxs[j - 1]].text)) score += 24;
        if (score < bestScore) {
          bestScore = score;
          best = j;
        }
      }
      if (best < 0) return [idxs];
      return split(idxs.slice(0, best), lim).concat(split(idxs.slice(best), lim));
    }
    var groups = [];
    clauses.forEach(function (c) {
      var place = placeOf[c[0]];
      var runs = [[c[0]]];
      for (var k = 1; k < c.length; k++) {
        if (words[c[k]].start - words[c[k - 1]].end > 0.35) runs.push([]);
        runs[runs.length - 1].push(c[k]);
      }
      runs.forEach(function (run) {
        split(run, C[place].maxChars).forEach(function (idxs) {
          groups.push({
            place: place,
            text: textOf(idxs),
            words: idxs.map(function (i) {
              return words[i];
            }),
          });
        });
      });
    });

    // 2. Visibility windows (one group on screen at a time).
    groups.forEach(function (g, i) {
      g.in = MS.snap(Math.max(0, g.words[0].start - 0.06));
      var last = g.words[g.words.length - 1];
      g.out = MS.snap(last.end + 0.5);
      var next = groups[i + 1];
      if (next) {
        var nextIn = MS.snap(Math.max(0, next.words[0].start - 0.06));
        g.out = Math.min(g.out, nextIn);
      }
      // end before a graphic that takes over these words
      ctx.suppress.forEach(function (s) {
        if (s[0] > g.in) g.out = Math.min(g.out, MS.snap(s[0]));
      });
      g.out = Math.min(g.out, ctx.duration);
    });

    // 3. Landscape: lift above the hands when a gesture collides with the box.
    if (ctx.aspect === "landscape") {
      groups.forEach(function (g) {
        var cfg = C.bottom;
        var estW = Math.min(cfg.maxWidth, g.text.length * cfg.size * 0.55);
        var box = [ctx.W / 2 - estW / 2, ctx.H - cfg.bottom - cfg.size * 1.3, ctx.W / 2 + estW / 2, ctx.H - cfg.bottom];
        // lift only for a real collision: the gesture must overlap the box for
        // ≥ 0.4 s or ≥ 30% of the phrase — brief brushes don't justify a jump
        var hit = (ctx.footage.gestures || []).some(function (gw) {
          var t0 = Math.max(g.in, gw.start);
          var t1 = Math.min(g.out, gw.end);
          if (t1 <= t0) return false;
          var r = ctx.frame.gestureRects(t0, t1)[0];
          var long = t1 - t0 >= 0.4 || (t1 - t0) / (g.out - g.in) >= 0.3;
          return long && r && MS.rectsOverlap(r, box);
        });
        if (hit) g.place = "lifted";
      });
      // Hysteresis: don't drop back down for one short phrase between two lifts.
      for (var gi = 1; gi < groups.length - 1; gi++) {
        var g = groups[gi];
        if (g.place === "bottom" && groups[gi - 1].place === "lifted" && groups[gi + 1].place === "lifted" && g.out - g.in < 1.2)
          g.place = "lifted";
      }
    }

    // 4. Build DOM + timeline.
    var layer = MS.el("div", "ms-captions", ctx.overlay);
    groups.forEach(function (g, gi) {
      var cfg = C[g.place];
      var el = MS.el("div", "ms-cap is-" + g.place + " is-" + cfg.align, layer);
      el.id = "ms-cap-" + gi;
      var inner = MS.el("div", "ms-cap-text", el);
      inner.style.fontSize = cfg.size + "px";
      inner.style.maxWidth = cfg.maxWidth + "px";
      if (g.place === "stage") {
        MS.place(el, P.zones.stage);
      } else {
        if (cfg.top != null) el.style.top = cfg.top + "px";
        else el.style.bottom = cfg.bottom + "px";
        if (ctx.aspect === "portrait") {
          el.style.left = P.margin + "px";
          el.style.width = P.zones.stage[2] + "px";
        }
      }
      g.words.forEach(function (w, wi) {
        var s = MS.el("span", "ms-cap-word", inner, w.text);
        if (wi < g.words.length - 1) inner.appendChild(document.createTextNode(" "));
        tl.to(s, { opacity: 1, duration: 0.08, ease: "none" }, MS.snap(Math.max(g.in, w.start)));
      });

      tl.set(el, { autoAlpha: 0 }, 0);
      tl.fromTo(el, { autoAlpha: 0, y: 10 }, { autoAlpha: 1, y: 0, duration: 0.16, ease: MS.EASE.enter }, g.in);
      var fadeAt = Math.max(g.in + 0.16, g.out - 0.1);
      tl.to(el, { autoAlpha: 0, duration: 0.1, ease: MS.EASE.exit }, MS.snap(fadeAt));
      tl.set(el, { autoAlpha: 0 }, MS.snap(fadeAt + 0.1)); // hard kill
    });

    ctx.captionGroups = groups;
  };
})();
