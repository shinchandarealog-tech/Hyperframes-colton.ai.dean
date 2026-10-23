/* C1 — Editorial Headline.
 * A question, statement or title carried by typography alone.
 * Lines reveal through masks on their spoken word; inline {{text|style@time}}
 * markup sets mono / dim / accent / warn segments, optionally timed.
 *
 * spec: { start, end, lines: [{ text, at, tone }], size?, exit?, suppressCaptions? }
 */
(function () {
  var MS = window.MS;
  var STYLE_COLOR = { accent: "accent", warn: "warn" };

  MS.components.headline = function (ctx, spec) {
    var P = ctx.P;
    var tl = ctx.tl;
    var landscape = ctx.aspect === "landscape";
    var zone = landscape ? P.zones.primary : P.zones.stage;

    if (!landscape) {
      if (ctx.frame.modeAt(spec.start) !== "split")
        console.warn("[MS] headline " + spec.id + " needs the SPLIT stage in portrait");
      ctx.occupy(spec.start - 0.2, spec.end + 0.3);
    }
    if (spec.suppressCaptions) ctx.suppress.push([spec.start - 0.05, spec.end]);

    var box = MS.el("div", "ms-headline" + (landscape ? " is-on-footage" : ""), ctx.overlay);
    MS.place(box, zone);
    box.style.fontSize = (spec.size || P.type.headline) + "px";
    box.style.justifyContent = landscape ? "flex-start" : "center";

    var inners = [];
    spec.lines.forEach(function (ln, i) {
      var line = MS.el("div", "ms-hl-line", box);
      line.setAttribute("data-layout-allow-overflow", ""); // the line is a reveal mask
      var inner = MS.el("span", "ms-hl-inner" + (ln.tone === "dim" ? " is-dim" : ""), line);
      MS.parseMarkup(ln.text).forEach(function (seg) {
        if (!seg.style) {
          inner.appendChild(document.createTextNode(seg.text));
          return;
        }
        var span = MS.el("span", "ms-hl-" + seg.style, inner, seg.text);
        var colorKey = STYLE_COLOR[seg.style];
        if (colorKey && seg.at != null) {
          // timed emphasis: starts in the line's color, shifts on the spoken word
          span.classList.add("is-pending");
          tl.to(span, { color: MS.COLOR[colorKey], duration: 0.3, ease: MS.EASE.emphasis }, MS.snap(seg.at));
        }
      });
      var at = ln.at != null ? ln.at : spec.start + 0.1 + i * 0.08;
      tl.from(inner, { yPercent: 115, duration: MS.DUR.standard, ease: MS.EASE.enter }, MS.snap(at));
      inners.push(inner);
    });

    var firstAt = Math.min.apply(
      null,
      spec.lines.map(function (ln, i) {
        return ln.at != null ? ln.at : spec.start + 0.1 + i * 0.08;
      }),
    );
    tl.set(box, { autoAlpha: 0 }, 0);
    tl.set(box, { autoAlpha: 1 }, MS.snap(firstAt));

    if (spec.exit !== false) {
      var out = MS.snap(spec.end - 0.05);
      tl.to(inners, { yPercent: -115, duration: 0.3, ease: MS.EASE.exit, stagger: 0.04 }, out);
      tl.set(box, { autoAlpha: 0 }, MS.snap(out + 0.3 + 0.04 * inners.length));
    }
  };
})();
