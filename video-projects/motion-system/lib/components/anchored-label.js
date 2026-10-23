/* C2 — Anchored Label.
 * Ties a short fact to a point on the speaker with a hairline leader, so the
 * graphic reads as attached to the footage rather than pasted on top.
 *
 * spec: { start, end, title: { text, at }, note?: { text, at } }
 * Geometry comes from the footage map via ctx.frame; never from pixel constants
 * in the beat script.
 *  - landscape: anchor beside the head (open-wall side), label to its left.
 *  - portrait SPLIT: label in the stage, leader drops across the seam to the
 *    top of the speaker's head.
 *  - portrait FULL: label under the chin, short vertical leader.
 */
(function () {
  var MS = window.MS;

  MS.components.anchoredLabel = function (ctx, spec) {
    var P = ctx.P;
    var tl = ctx.tl;
    var f = ctx.frame;
    var head = f.head;
    var tRef = spec.title.at;
    var mode = f.modeAt(tRef);

    // Average head position over the label's window (the label holds still).
    var n = 0;
    var hx = 0;
    var ft = 0;
    for (var t = spec.start; t <= spec.end; t += 0.25) {
      hx += f.headX(t);
      ft += f.faceTop(t);
      n++;
    }
    hx /= n;
    ft /= n;

    var labelSize = spec.size || P.type.label;
    var box = MS.el("div", "ms-label", ctx.overlay);
    var title = MS.el("div", "ms-label-title", box, spec.title.text);
    var note = spec.note ? MS.el("div", "ms-label-note", box, spec.note.text) : null;
    title.style.fontSize = labelSize + "px";
    if (note) note.style.fontSize = P.type.eyebrow + "px";

    var A; // anchor (composition px)
    var path; // leader points, starting at the anchor
    var srcPt; // anchor in source px (for the accent check)
    var gap = 18;

    if (ctx.aspect === "landscape") {
      srcPt = [hx - head.width / 2 - 34, ft + 150];
      A = f.map(tRef, srcPt[0], srcPt[1]);
      var leaderLen = 150;
      var Lx = A.x - leaderLen;
      path = [[A.x, A.y], [Lx, A.y]];
      box.classList.add("is-on-footage", "is-right");
      box.style.right = ctx.W - (Lx - gap) + "px";
      box.style.top = A.y - labelSize * 0.62 + "px";
    } else if (mode === "split") {
      ctx.occupy(spec.start - 0.2, spec.end + 0.3, "lower");
      srcPt = [hx - 110, ft - head.hairAbove - 10];
      A = f.map(tRef, srcPt[0], srcPt[1]);
      var stage = P.zones.stage;
      var labelY = stage[1] + stage[3] - 150; // lower part of the stage
      box.style.left = P.margin + "px";
      box.style.top = labelY - labelSize * 0.62 + "px";
      var estW = spec.title.text.length * labelSize * 0.56;
      var Lx2 = P.margin + estW + gap;
      path = [[A.x, A.y], [A.x, labelY], [Math.min(Lx2, A.x - 24), labelY]];
    } else {
      srcPt = [hx - 140, head.chinY + 60];
      A = f.map(tRef, srcPt[0], srcPt[1]);
      var below = A.y + 70;
      box.classList.add("is-on-footage");
      box.style.left = P.margin + "px";
      box.style.top = below + "px";
      path = [[A.x, A.y], [A.x, below - 6]];
    }

    // Leader + anchor dot in one SVG layer.
    var svgNS = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("class", "ms-label-svg");
    svg.setAttribute("width", ctx.W);
    svg.setAttribute("height", ctx.H);
    svg.setAttribute("viewBox", "0 0 " + ctx.W + " " + ctx.H);
    ctx.overlay.insertBefore(svg, box);
    var line = document.createElementNS(svgNS, "path");
    line.setAttribute(
      "d",
      path
        .map(function (p, i) {
          return (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1);
        })
        .join(" "),
    );
    line.setAttribute("pathLength", "1");
    line.setAttribute("class", "ms-label-leader");
    svg.appendChild(line);
    var dot = document.createElementNS(svgNS, "circle");
    dot.setAttribute("cx", A.x.toFixed(1));
    dot.setAttribute("cy", A.y.toFixed(1));
    dot.setAttribute("r", ctx.aspect === "landscape" ? 6 : 7);
    var blocked = ctx.accentBlocked(srcPt[0], srcPt[1]);
    dot.setAttribute("fill", blocked ? MS.COLOR.text : MS.COLOR.accent);
    svg.appendChild(dot);

    // Choreography: dot → leader draws outward → label wipes in from the leader end.
    var t0 = MS.snap(tRef - 0.4);
    tl.set([svg, box], { autoAlpha: 0 }, 0);
    tl.set([svg, box], { autoAlpha: 1 }, t0);
    tl.from(dot, { scale: 0, transformOrigin: "50% 50%", duration: MS.DUR.micro, ease: MS.EASE.emphasis }, t0);
    tl.fromTo(line, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.35, ease: MS.EASE.move }, MS.snap(t0 + 0.08));
    var wipeFrom = box.classList.contains("is-right") || ctx.aspect === "portrait" ? "inset(0 0 0 100%)" : "inset(0 100% 0 0)";
    tl.fromTo(title, { clipPath: wipeFrom }, { clipPath: "inset(0 0% 0 0%)", duration: 0.35, ease: MS.EASE.enter }, MS.snap(tRef));
    if (note) tl.from(note, { autoAlpha: 0, y: 8, duration: 0.3, ease: MS.EASE.enter }, MS.snap(spec.note.at));

    var out = MS.snap(spec.end);
    tl.to(box, { autoAlpha: 0, duration: 0.24, ease: MS.EASE.exit }, out);
    tl.to(line, { strokeDashoffset: -1, duration: 0.3, ease: MS.EASE.exit }, out);
    tl.to(dot, { scale: 0, duration: MS.DUR.micro, ease: MS.EASE.exit }, MS.snap(out + 0.18));
    tl.set(svg, { autoAlpha: 0 }, MS.snap(out + 0.4));
  };
})();
