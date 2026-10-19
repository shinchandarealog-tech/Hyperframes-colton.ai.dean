/* Shared motion helpers (Apple-keynote blur-focus language). Inlined by scripts/build-comps.py. */
window.FX = window.FX || {
  // Wrap every [data-split] element: words → .fx-w, letters → .fx-c.
  split(root) {
    root.querySelectorAll("[data-split]").forEach((el) => {
      const words = el.textContent.trim().split(/\s+/);
      el.innerHTML = words
        .map((w) => `<span class="fx-w">${[...w].map((c) => `<span class="fx-c">${c}</span>`).join("")}</span>`)
        .join(" ");
    });
  },
  // Letters of an element (falls back to the element itself).
  words(root, sel) {
    const el = root.querySelector(sel);
    const cs = el.querySelectorAll(".fx-c");
    return cs.length ? cs : el;
  },
  // Letter-by-letter focus-in with a cyan light-flash (reference signature); per-word blur for other targets.
  blurIn(tl, targets, t, o = {}) {
    const list = targets.length !== undefined ? [...targets] : [targets];
    if (list.length && list[0].classList && list[0].classList.contains("fx-c")) {
      const each = o.cstagger ?? Math.min(0.035, 0.9 / list.length);
      tl.from(list, { opacity: 0, y: o.y ?? 22, scale: o.scale ?? 0.55, filter: "blur(12px) brightness(2.6)",
        duration: o.dur ?? 0.5, ease: o.ease ?? "expo.out", stagger: each }, t);
      const grad = list[0].closest(".fx-grad");
      if (!grad) {
        tl.from(list, { color: "#a6e6ff", textShadow: "0 0 14px rgba(150,225,255,1), 0 0 34px rgba(80,180,255,0.95)",
          duration: 0.7, ease: "power2.out", stagger: each }, t);
      }
      return;
    }
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
    FX.blurIn(tl, label.querySelectorAll(".fx-c").length ? label.querySelectorAll(".fx-c") : label, t + 0.02, { y: 0 });
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
