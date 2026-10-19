/* Shared motion helpers (Apple-keynote blur-focus language). Inlined by scripts/build-comps.py. */
window.FX = window.FX || {
  // Wrap each word of every [data-split] element in a .fx-w span.
  split(root) {
    root.querySelectorAll("[data-split]").forEach((el) => {
      const words = el.textContent.trim().split(/\s+/);
      el.innerHTML = words.map((w) => `<span class="fx-w">${w}</span>`).join(" ");
    });
  },
  words(root, sel) {
    const el = root.querySelector(sel);
    const ws = el.querySelectorAll(".fx-w");
    return ws.length ? ws : el;
  },
  // Blur → sharp focus-in, per word.
  blurIn(tl, targets, t, o = {}) {
    tl.from(
      targets,
      {
        opacity: 0,
        filter: `blur(${o.blur ?? 16}px)`,
        y: o.y ?? 24,
        scale: o.scale ?? 0.9,
        duration: o.dur ?? 0.5,
        ease: o.ease ?? "expo.out",
        stagger: o.stagger ?? 0.06,
      },
      t,
    );
  },
  // Whole-block defocus exit.
  blurOut(tl, targets, t, o = {}) {
    tl.to(
      targets,
      {
        opacity: 0,
        filter: `blur(${o.blur ?? 14}px)`,
        y: o.y ?? -12,
        scale: o.scale ?? 1.03,
        duration: o.dur ?? 0.3,
        ease: o.ease ?? "power2.in",
      },
      t,
    );
  },
  // Glow-flash entry for glass chips: over-bright cyan → settle.
  glowIn(tl, target, t, o = {}) {
    // (no CSS filter here — filtered glass renders black in the capture engine)
    tl.from(target, { opacity: 0, scaleX: 0.6, scaleY: 0.4, duration: o.dur ?? 0.45, ease: "expo.out" }, t);
    tl.from(target, { boxShadow: "inset 0 0 60px rgba(190,240,255,1), 0 0 90px 24px rgba(125,211,252,0.95)", borderColor: "rgba(220,248,255,1)",
      duration: (o.dur ?? 0.45) + 0.35, ease: "power2.out" }, t);
  },
  // Dashed ring spins → filled blue badge + drawn tick; label focuses in alongside.
  check(tl, row, t) {
    const ring = row.querySelector(".ring");
    const fill = row.querySelector(".fill");
    const tick = row.querySelector(".tick");
    const label = row.querySelector(".lbl");
    tl.from(ring, { opacity: 0, scale: 0.5, svgOrigin: "30 30", duration: 0.25, ease: "power2.out" }, t);
    tl.to(ring, { rotation: 200, svgOrigin: "30 30", duration: 0.55, ease: "none" }, t);
    FX.blurIn(tl, label.querySelectorAll(".fx-w").length ? label.querySelectorAll(".fx-w") : label, t + 0.02, { y: 0, scale: 0.96, stagger: 0.05 });
    tl.from(fill, { scale: 0, svgOrigin: "30 30", duration: 0.32, ease: "back.out(2.2)" }, t + 0.38);
    tl.fromTo(tick, { strokeDashoffset: 44 }, { strokeDashoffset: 0, duration: 0.22, ease: "power2.out" }, t + 0.48);
    tl.to(ring, { opacity: 0, duration: 0.2, ease: "power1.out" }, t + 0.5);
  },
  checkSvg() {
    return `<svg viewBox="0 0 60 60"><circle class="ring" cx="30" cy="30" r="27" fill="none" stroke="#9bdcff" stroke-width="3.5" stroke-dasharray="7 6"/><circle class="fill" cx="30" cy="30" r="28" fill="#3b82f6"/><path class="tick" d="M17 31 L26 40 L43 21" fill="none" stroke="#fff" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="44"/></svg>`;
  },
  // mulberry32 seeded PRNG (determinism)
  rng(seed) {
    let a = seed >>> 0;
    return () => {
      a = (a + 0x6d2b79f5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  },
  // Count a number into an element (seek-safe: driven by a tweened proxy).
  count(tl, el, from, to, t, dur, fmt, ease = "power2.out") {
    const p = { v: from };
    el.textContent = fmt(from);
    tl.to(p, { v: to, duration: dur, ease, onUpdate: () => (el.textContent = fmt(p.v)) }, t);
  },
};
