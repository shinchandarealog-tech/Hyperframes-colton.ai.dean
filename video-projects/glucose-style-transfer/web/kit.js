// kit.js — "09 Glucose" style engine. Every number comes from spec/*.md (measured on the reference).
// Frame-by-frame: initT(i) builds template i and returns its frame count; renderT(f) sets frame f.
const FPS = 24000 / 1001, CW = 1080, CH = 1920;
const SAFE = { x0: 84, x1: 900, y1: 1520 };            // Instagram safe zone
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const LERP = (a, b, p) => a + (b - a) * p;
const EZ = {
  lin: t => t, sineo: t => Math.sin(t * Math.PI / 2), sineio: t => -(Math.cos(Math.PI * t) - 1) / 2,
  p2o: t => 1 - (1 - t) ** 3, p3o: t => 1 - (1 - t) ** 4, p2i: t => t ** 3,
  p3io: t => t < .5 ? 8 * t ** 4 : 1 - (-2 * t + 2) ** 4 / 2,
  circ: t => Math.sqrt(1 - (t - 1) ** 2), expo: t => t >= 1 ? 1 : 1 - 2 ** (-10 * t),
  back: s => t => 1 + (s + 1) * (t - 1) ** 3 + s * (t - 1) ** 2,
};
const P = (f, t0, d, ez = EZ.p2o) => ez(cl((f - t0) / d));
function rng(seed) { let s = seed >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ t >>> 15, t | 1); t ^= t + Math.imul(t ^ t >>> 7, t | 61); return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

// ---------- palette (STYLE.md) ----------
const COL = {
  white: '#fffaf6', cream: '#f9e6c0', creamPill: '#fbf1d6', creamPill2: '#fcedda', pillInk: '#825d54', pillInk2: '#d9bba3',
  rust: '#8f2e1e', rustInk: '#88291d', rustDark: '#7e2019', darkBox: '#4a1c14', darkPill: '#441611',
  peach: '#e8b39a', grey: '#3e3e3e', label: '#8a8a8a', brownText: '#8a5a3a',
  gOrangeV: 'linear-gradient(180deg,#e07a1f,#f6a944)', gOrangeH: 'linear-gradient(90deg,#f19428,#f5c84a)',
  gYellow: 'linear-gradient(180deg,#f7e98a,#e9c74a)', gPale: 'linear-gradient(180deg,#f9e2b0,#e9c27a)',
  gGold: 'linear-gradient(180deg,#c88d5a,#e9c8a0 55%,#b07040)',
};
const SANS = "'Outfit'", SERIF = "'DM Serif Display'";

// ---------- context ----------
let C = null;
function H(tag, css, parent, html) {
  const e = document.createElement(tag); if (css) e.style.cssText = css; if (html != null) e.innerHTML = html;
  (parent || C.par).appendChild(e); return e;
}
const U = fn => C.ups.push(fn);
const EV = (f, t) => C.ev.push([Math.round(f), t]);
const pad4 = n => String(n).padStart(4, '0');
function e2o(k) { for (const [e0, o0, n] of EDL) if (k >= e0 && k < e0 + n) return o0 + k - e0; const l = EDL[EDL.length - 1]; return Math.min(window.RAW_F - 1, l[1] + (k - l[0])); }   // past the end: the raw tail runs on
function setSrc(img, src) { if (img.dataset.s === src) return Promise.resolve(); img.dataset.s = src; img.src = src; return img.decode().catch(() => {}); }

// word helpers (1-based word index into WORDS = edit-time words)
const clean = s => s.replace(/[,.?!]/g, '');
const wd = i => WORDS[i - 1].w;
const wds = (a, b) => { const r = []; for (let i = a; i <= b; i++) r.push(wd(i)); return r; };

// ---------- layers ----------
function Stage() {
  const st = document.getElementById('stage'); st.innerHTML = '';
  const root = document.createElement('div'); root.style.cssText = `position:absolute;left:0;top:0;width:${CW}px;height:${CH}px;overflow:hidden;transform-origin:50% 50%`;
  st.appendChild(root); return root;
}
function Aroll(c, o = {}) {
  const wrap = H('div', 'position:absolute;inset:0;overflow:hidden');
  const img = H('img', `position:absolute;left:0;top:0;width:${CW}px;height:${CH}px;transform-origin:${c.camO[0]}px ${c.camO[1]}px`, wrap);
  c.loads.push(f => setSrc(img, `${window.AROLL_DIR || '../aroll/f'}/a_${pad4(e2o(c.E0 + f) + 1)}.jpg`));
  U(f => { img.style.transform = `scale(${c.cam(f)})`; });
  return wrap;
}
function Matte(c) {   // the speaker cut out (rembg), drawn ABOVE text => text sits behind the person
  const wrap = H('div', 'position:absolute;inset:0;overflow:hidden;z-index:5;pointer-events:none');
  const img = H('img', `position:absolute;left:0;top:0;width:${CW}px;height:${CH}px;transform-origin:${c.camO[0]}px ${c.camO[1]}px`, wrap);
  c.loads.push(f => setSrc(img, `matte/m_${pad4(e2o(c.E0 + f) + 1)}.png`));
  U(f => { img.style.transform = `scale(${c.cam(f)})`; });
}
// camera presets (STYLE.md / Camera)
const CAM = {
  hook: f => LERP(1.28, 1.0, P(f, 1.5, 50, EZ.circ)),                 // zoom-out 1.28->1 circ.out 50 f
  intro: f => LERP(1.058, 1.0, P(f, 0, 14.5, EZ.sineo)),               // new-speaker zoom-out sine.out 14.5 f
  drift: n => f => 1.0 + 0.0008 * f,                                   // slow push-in (~1.00->1.12 / 150 f)
  push: t0 => f => LERP(1.0, 1.18, P(f, t0, 32.5, EZ.circ)),           // emphasis push-in circ.out 32.5 f
};

// ---------- pages ----------
function Page(c, a, b, build, o = {}) {      // visible a <= f < b, hard swap; o.fadeOut = frames
  const prev = C.par; const pg = H('div', 'position:absolute;inset:0;z-index:2'); C.par = pg;
  const rec = { el: pg, a, b, free: !!o.free, items: [] }; c.pages.push(rec); C.page = rec;
  build(); C.par = prev; C.page = null;
  U(f => {
    let op = (f >= a && f < b) ? 1 : 0;
    if (op && o.fadeOut) op = 1 - P(f, b - o.fadeOut, o.fadeOut, EZ.lin);
    pg.style.opacity = op; pg.style.visibility = op > 0 ? 'visible' : 'hidden';
  });
  return pg;
}

// Stack: column of lines anchored at the bottom (lines joining push the stack up = measured stackRise)
function Stack(c, o) {
  const al = o.align || 'center';
  const el = H('div', `position:absolute;display:flex;flex-direction:column;align-items:${al === 'left' ? 'flex-start' : 'center'};` +
    (al === 'left' ? `left:${o.x}px;` : `left:${o.x}px;transform:translateX(-50%);`) + `width:max-content;`);
  const st = { el, o, lines: [], kind: 'stack' }; C.page && C.page.items.push(st);
  if (o.bottom != null) { el.style.bottom = (CH - o.bottom) + 'px'; } else { el.style.top = (o.top ?? 1200) + 'px'; }
  return st;
}
function Line(st, o = {}) {
  const outer = H('div', `position:relative;overflow:visible;margin-top:${o.mt ?? 0}px;margin-left:${o.indent ?? 0}px`, st.el);
  const el = H('div', `display:flex;align-items:baseline;white-space:nowrap;gap:${o.gap ?? 0}px;justify-content:${st.o.align === 'left' ? 'flex-start' : 'center'}`, outer);
  const ln = { outer, el, items: [], V: 1e9 }; st.lines.push(ln);
  // line height grows when its first item appears (stackRise: dy +36 -> 0, back.out(1.7) ~10 f)
  C.fin.push(() => {
    ln.h = outer.offsetHeight;
    U(f => { const p = P(f, ln.V, 10, EZ.back(1.7)); outer.style.height = (ln.h * (f >= ln.V ? Math.max(p, 0.001) : 0)) + 'px'; outer.style.opacity = f >= ln.V ? 1 : 0; });
  });
  return ln;
}
function fontCss(o) {
  return `font-family:${o.serif ? SERIF : SANS};font-weight:${o.wt ?? (o.serif ? 400 : 300)};font-style:${o.ital ? 'italic' : 'normal'};` +
    `font-size:${o.size}px;line-height:${o.lh ?? 1.0};letter-spacing:${o.ls ?? (o.serif ? -0.04 : -0.06)}em;color:${o.color || COL.white};` +
    (o.color === '#3e3e3e' ? 'text-shadow:0 0 14px rgba(255,248,238,.85),0 0 4px rgba(255,248,238,.7);' : '');   // charcoal on her white top: soft cream halo so it also reads over skin
}
// sans word(s): wordBlur (blur 10->0 + opacity, 4 f power2.out) + width grow circ.out 8 f (line re-centres)
function Words(ln, words, Vs, o) {
  words.forEach((w, k) => {
    const sp = H('span', fontCss(o) + `display:inline-block;overflow:visible;padding-right:${k < words.length - 1 ? 0.24 * o.size : 0}px`, ln.el, w);
    const V = Vs[k]; ln.V = Math.min(ln.V, V); EV(V, 'word');
    C.fin.push(() => { const W = sp.offsetWidth; sp.style.width = W + 'px'; sp._W = W;
      U(f => { const g = P(f, V - 1, 8, EZ.circ); sp.style.width = (W * (f >= V - 1 ? Math.max(g, .001) : 0)) + 'px';
        const p = P(f, V, 4, EZ.p2o); sp.style.opacity = p; sp.style.filter = p < 1 ? `blur(${10 * (1 - p)}px)` : ''; }); });
  });
}
// serif accent word: letterBlur (L->R, stagger 1.5 f, each 6 f: blur 14->0, x -12->0) or letterFlicker (random order over 5-6 f)
function Accent(ln, text, V, o) {
  const wrap = H('span', `position:relative;display:inline-block;${o.wrapCss || ''}`, ln.el);
  const word = H('span', fontCss(o) + `display:inline-block;position:relative;z-index:1;${o.css || ''}`, wrap);
  const letters = [...text].map(ch => H('span', `display:inline-block;white-space:pre`, word, ch === ' ' ? ' ' : ch));
  ln.V = Math.min(ln.V, V); EV(V, o.mode === 'flicker' ? 'group' : 'word');
  const mode = o.mode || 'blur', n = letters.length, R = rng(o.seed || (text.length * 977 + V));
  const order = letters.map((_, i) => i).sort(() => R() - .5); const rank = []; order.forEach((li, r) => rank[li] = r);
  const span = o.flickerSpan ?? 6;
  letters.forEach((L, i) => {
    U(f => {
      if (mode === 'blur') { const p = P(f, V + 1.5 * i, 6, EZ.p2o); L.style.opacity = p; L.style.filter = p < 1 ? `blur(${14 * (1 - p)}px)` : ''; L.style.transform = `translateX(${-12 * (1 - p)}px)`; }
      else if (mode === 'flicker') { const t = V + rank[i] * span / n; const p = P(f, t, 2, EZ.lin); L.style.opacity = p; }
      else { L.style.opacity = f >= V ? 1 : 0; }
    });
  });
  if (o.grad) C.fin.push(() => {        // gradient spans the whole word: each letter gets the same gradient, offset
    const W = word.offsetWidth, Hh = word.offsetHeight;
    letters.forEach(L => { L.style.backgroundImage = o.grad; L.style.backgroundSize = `${W}px ${Hh}px`; L.style.backgroundPosition = `${-L.offsetLeft}px 0`;
      L.style.webkitBackgroundClip = 'text'; L.style.backgroundClip = 'text'; L.style.color = 'transparent'; if (o.glow) L.style.textShadow = 'none'; });
    if (o.glow) word.style.filter = `drop-shadow(0 0 18px ${o.glow})`;
  });
  if (o.shadow) word.style.filter = (word.style.filter || '') + ' ' + o.shadow;
  // width grow so a multi-item line re-centres as the accent arrives
  if (o.grow !== false) C.fin.push(() => { const W = wrap.offsetWidth; U(f => { const g = P(f, V - 1, 8, EZ.circ); wrap.style.width = (W * (f >= V - 1 ? Math.max(g, .001) : 0)) + 'px'; }); });
  return { wrap, word, letters, V };
}
// box / pill / bar behind an accent (measured variants)
const u = v => typeof v === 'number' ? v + 'px' : v;
function BoxBehind(acc, o) {
  const b = H('div', `position:absolute;z-index:0;background:${o.color};border-radius:${o.r ?? 14}px;` +
    `left:${-(o.px ?? 28)}px;right:${-(o.px ?? 28)}px;top:${u(o.top ?? -(o.py ?? 14))};bottom:${u(o.bottom ?? -(o.py ?? 14))};opacity:${o.alpha ?? 1}`, acc.wrap);
  const V = o.V ?? acc.V + 2, mode = o.mode || 'wipeL'; EV(V, o.mode === 'growC' ? 'pill' : 'marker');
  U(f => {
    if (mode === 'wipeL') { const p = P(f, V, o.dur ?? 7, EZ.p3o); b.style.transformOrigin = 'left center'; b.style.transform = `scaleX(${p})`; b.style.visibility = f >= V ? 'visible' : 'hidden'; }
    else if (mode === 'growC') { // 6 px line at the centre -> full width, text clipped inside
      const p = P(f, V, o.dur ?? 10, EZ.p3o); const ins = `inset(0 calc(${50 * (1 - p)}% - ${3 * (1 - p)}px) round ${o.r ?? 22}px)`;
      acc.wrap.style.clipPath = f >= V ? ins : 'inset(0 50% 0 50%)';
    } else if (mode === 'maskLR') { const p = P(f, V, o.dur ?? 12, EZ.p2o); acc.wrap.style.clipPath = `inset(-20px ${100 * (1 - p)}% -20px -40px)`; }
  });
  if (mode !== 'wipeL') acc.letters.forEach(L => { L.style.opacity = 1; });
  return b;
}
function Underline(acc, o = {}) {
  const u = H('div', `position:absolute;left:${o.l ?? -6}px;right:${o.rr ?? -6}px;bottom:${o.bot ?? -14}px;height:${o.th ?? 4}px;background:${o.color || COL.cream};transform-origin:left center`, acc.wrap || acc);
  const V = o.V; EV(V, 'marker');
  U(f => { const p = P(f, V, 12, EZ.circ); u.style.transform = `scaleX(${p})`; u.style.visibility = f >= V ? 'visible' : 'hidden'; });
  return u;
}
// free-positioned elements
function Abs(css, html) { return H('div', 'position:absolute;' + css, C.par, html); }
function BlurIn(el, V, o = {}) { // generic blur-fade enter (IG card 18 px/10 f, deco)
  U(f => { const p = P(f, V, o.dur ?? 10, EZ.p2o); el.style.opacity = f >= V ? p : 0; el.style.filter = p < 1 ? `blur(${(o.blur ?? 18) * (1 - p)}px)` : '';
    el.style.transform = `${o.base || ''} translateY(${(o.dy ?? 40) * (1 - p)}px)`; });
}
function IGCard(c, o) {   // measured layout at scale 1: avatar Ø299 @ (238,540) | handle 60px @ x443 ...
  const s = o.scale ?? 1;
  const el = Abs(`left:${o.x}px;top:${o.y}px;width:${960 * s}px;height:${320 * s}px;z-index:3`);
  const inner = H('div', `position:absolute;left:0;top:0;width:960px;height:320px;transform-origin:0 0;transform:scale(${s})`, el);
  H('div', `position:absolute;left:0;top:0;width:300px;height:300px;border-radius:50%;background:conic-gradient(from 200deg,#feda75,#fa7e1e,#d62976,#962fbf,#c13584,#feda75)`, inner);
  H('div', `position:absolute;left:8px;top:8px;width:284px;height:284px;border-radius:50%;background:#f4ece4`, inner);
  const av = H('div', `position:absolute;left:14px;top:14px;width:272px;height:272px;border-radius:50%;background:${o.avatar || 'linear-gradient(135deg,#d9b9a0,#a87862)'};display:flex;align-items:center;justify-content:center;font:500 96px ${SANS};color:#fff8f0;letter-spacing:.02em;overflow:hidden`, inner, o.initials || '');
  H('div', `position:absolute;left:372px;top:96px;font:600 60px ${SANS};letter-spacing:-0.02em;color:#161616;white-space:nowrap;display:flex;align-items:center;gap:14px`, inner,
    `${o.handle}<svg width="36" height="36" viewBox="0 0 24 24"><path fill="#3897f0" d="M12 1l2.6 2.2 3.4-.4.9 3.3 3 1.7-1.3 3.2 1.3 3.2-3 1.7-.9 3.3-3.4-.4L12 23l-2.6-2.2-3.4.4-.9-3.3-3-1.7L3.4 13 2.1 9.8l3-1.7.9-3.3 3.4.4z"/><path d="M7.5 12.3l3 3 6-6.2" stroke="#fff" stroke-width="2.2" fill="none"/></svg><span style="font:400 40px ${SANS};color:#555;margin-left:6px">···</span>`);
  H('div', `position:absolute;left:372px;top:178px;font:400 30px ${SANS};letter-spacing:.02em;color:#555;white-space:nowrap`, inner, o.name);
  H('div', `position:absolute;left:372px;top:228px;font:400 36px ${SANS};color:#222;white-space:nowrap;word-spacing:4px`, inner, o.stats);
  BlurIn(el, o.V ?? 3, { blur: 18, dy: 40, dur: 10 }); EV(o.V ?? 3, 'tag');
  C.page && C.page.items.push({ kind: 'abs', el });
  return el;
}
function Stroke(d, o) {   // drawn circle / arrow: stroke-dash 0->100 %, power2.out 12-14 f
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); svg.setAttribute('width', CW); svg.setAttribute('height', CH);
  svg.style.cssText = 'position:absolute;left:0;top:0;z-index:4;overflow:visible'; C.par.appendChild(svg);
  const p = document.createElementNS('http://www.w3.org/2000/svg', 'path'); p.setAttribute('d', d); p.setAttribute('fill', 'none');
  p.setAttribute('stroke', o.color); p.setAttribute('stroke-width', o.w ?? 3); p.setAttribute('stroke-linecap', 'round'); svg.appendChild(p);
  let head; if (o.arrow) { head = document.createElementNS('http://www.w3.org/2000/svg', 'path'); head.setAttribute('d', o.arrow); head.setAttribute('fill', 'none'); head.setAttribute('stroke', o.color); head.setAttribute('stroke-width', o.w ?? 3); head.setAttribute('stroke-linecap', 'round'); svg.appendChild(head); }
  EV(o.V, 'marker');
  C.fin.push(() => { const L = p.getTotalLength(); p.style.strokeDasharray = L;
    U(f => { const q = P(f, o.V, o.dur ?? 12, EZ.p2o); p.style.strokeDashoffset = L * (1 - q); p.style.visibility = f >= o.V ? 'visible' : 'hidden'; if (head) head.style.opacity = q > 0.95 ? 1 : 0; }); });
}
function LineToBox(o) {   // 6 px rust line grows L->R (4 f) then height -> box (6 f power3.out); content clipped inside
  const b = Abs(`left:${o.x}px;top:${o.y}px;width:${o.w}px;height:${o.h}px;z-index:3;overflow:hidden;border-radius:${o.r ?? 16}px`);
  const bg = H('div', `position:absolute;inset:0;background:${o.color || COL.rust}`, b);
  const content = H('div', `position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding-left:${o.padL ?? 34}px`, b, o.html);
  EV(o.V, 'pill');
  U(f => { const a = P(f, o.V, 4, EZ.p2o), h = P(f, o.V + 4, 6, EZ.p3o);
    const hh = 6 + (o.h - 6) * h; b.style.clipPath = `inset(${(o.h - hh) / 2}px ${100 * (1 - a)}% ${(o.h - hh) / 2}px 0 round ${o.r ?? 16}px)`;
    b.style.visibility = f >= o.V ? 'visible' : 'hidden'; content.style.opacity = P(f, o.V + 6, 4); });
  C.page && C.page.items.push({ kind: 'abs', el: b });
  return b;
}
function Deco(glyph, o) {   // floating "?" (S08): peach serif, ±12°, blur-fade in, float ±6 px
  const d = Abs(`left:${o.x}px;top:${o.y}px;font:400 ${o.size ?? 200}px ${SERIF};color:${o.color || COL.peach};opacity:.8;z-index:1`, glyph);
  U(f => { const p = P(f, o.V, 10, EZ.p2o); d.style.opacity = 0.8 * (f >= o.V ? p : 0); d.style.filter = p < 1 ? `blur(${12 * (1 - p)}px)` : '';
    d.style.transform = `rotate(${o.rot}deg) translateY(${6 * Math.sin((f + o.x) / 14)}px)`; });
  EV(o.V, 'group'); return d;
}
// b-roll: still image / cut-out with linear push-in (+ optional rotate); pages run on twos
function Img(src, o) {
  const el = Abs(`left:${o.cx - o.w / 2}px;top:${o.cy - o.h / 2}px;width:${o.w}px;height:${o.h}px;z-index:${o.z ?? 1};${o.css || ''}`);
  const im = H('img', `width:100%;height:100%;object-fit:cover;display:block;${o.icss || ''}`, el); im.src = src; C.imgs.push(im);
  U(f => { const t = cl(f / Math.max(1, (o.dur ?? C.N))); const s = LERP(o.s0 ?? 1, o.s1 ?? 1.06, o.ez ? o.ez(t) : t);
    const r = LERP(o.r0 ?? 0, o.r1 ?? 0, t); el.style.transform = `scale(${s}) rotate(${r}deg)`; });
  return el;
}
function Bg(css) { return Abs('inset:0;z-index:0;' + css); }

// ---------- safety: faceSafe() + igSafe() (run after layout, before frame 0) ----------
function chinMax(c, a, b) { let m = 0; for (let f = Math.max(0, a); f < Math.min(c.N, b); f++) { const o = e2o(c.E0 + f); const fc = FACES[Math.min(o, FACES.length - 1)]; const z = c.cam(f); const y = c.camO[1] + (fc[1] - c.camO[1]) * z; m = Math.max(m, y); } return m; }
function rectOf(el) { const r = el.getBoundingClientRect(), s = document.getElementById('stage').getBoundingClientRect(); return { x0: r.left - s.left, y0: r.top - s.top, x1: r.right - s.left, y1: r.bottom - s.top }; }
function fitPages(c) {
  const rep = [];
  for (const pg of c.pages) {
    // final (all visible) layout for measuring
    const saved = [];
    pg.el.querySelectorAll('*').forEach(e => { saved.push([e, e.style.cssText]); e.style.opacity = 1; e.style.filter = ''; e.style.clipPath = ''; e.style.visibility = 'visible'; });
    pg.el.style.opacity = 1; pg.el.style.visibility = 'visible';
    // line heights at full size
    const lines = []; pg.el.querySelectorAll('div').forEach(d => { if (d.style.height !== '' && d.parentElement && d.parentElement.style.flexDirection === 'column') lines.push(d); });
    let U0 = { x0: 1e9, y0: 1e9, x1: -1e9, y1: -1e9 };
    for (const it of pg.items) { const r = rectOf(it.el); if (r.x1 - r.x0 < 2) continue; U0 = { x0: Math.min(U0.x0, r.x0), y0: Math.min(U0.y0, r.y0), x1: Math.max(U0.x1, r.x1), y1: Math.max(U0.y1, r.y1) }; }
    saved.forEach(([e, css]) => e.style.cssText = css);
    if (U0.x1 < 0) continue;
    let dx = 0, dy = 0, sc = 1; const chin = c.speaker && !pg.free ? chinMax(c, pg.a, pg.b) + 24 : -1;
    const w = U0.x1 - U0.x0, h = U0.y1 - U0.y0;
    if (chin > 0) {
      // client-specific text band: below the chin, on her white top (x 215-805), centred at 510; never over the face, inside IG safe
      const Z = c.zone || { x0: 240, x1: 790 };
      sc = Math.min(1, (Z.x1 - Z.x0) / w, (SAFE.y1 - chin) / h);
      dx = (Z.x0 + Z.x1) / 2 - w * sc / 2 - U0.x0;
      dy = Math.min(0, SAFE.y1 - (U0.y0 + h * sc)); if (U0.y0 + dy < chin) dy = chin - U0.y0;
    } else {
      if (U0.y1 > SAFE.y1) dy = SAFE.y1 - U0.y1;
      if (U0.x1 > SAFE.x1) dx = SAFE.x1 - U0.x1;                                // igSafe: move first
      if (U0.x0 + dx < SAFE.x0) { if (w > SAFE.x1 - SAFE.x0) sc = (SAFE.x1 - SAFE.x0) / w; dx = SAFE.x0 - U0.x0; }
    }
    pg.el.style.transformOrigin = `${U0.x0}px ${U0.y0}px`;
    pg.el.style.transform = `translate(${dx}px,${dy}px) scale(${sc})`;
    rep.push({ page: [pg.a, pg.b], box: [U0.x0, U0.y0, U0.x1, U0.y1].map(Math.round), chin: Math.round(chin), dx: Math.round(dx), dy: Math.round(dy), scale: +sc.toFixed(3),
      final: [U0.x0 + dx, U0.y0 + dy, U0.x0 + dx + (U0.x1 - U0.x0) * sc, U0.y0 + dy + (U0.y1 - U0.y0) * sc].map(Math.round) });
  }
  return rep;
}

// ---------- template registry ----------
const TPL = [];
function T(name, wa, wb, type, build, o = {}) { TPL.push({ name, wa, wb, type, build, o }); }
window.initT = async function (i) {
  const t = TPL[i]; const st = Stage();
  const s0 = Math.max(0, WORDS[t.wa - 1].s - (t.o.pre ?? 0.30)), s1 = Math.min(EDIT_DUR, WORDS[t.wb - 1].e + (t.o.post ?? 0.40));
  const E0 = Math.round(s0 * FPS), N = Math.round(s1 * FPS) - E0;
  C = { root: st, par: st, ups: [], fin: [], loads: [], ev: [], pages: [], imgs: [], E0, N, s0: E0 / FPS, speaker: t.type === 'speaker', twos: t.type === 'broll',
    camO: t.o.camO || [490, 560], cam: f => 1, blurIn: t.o.blurIn, blurOut: t.o.blurOut };
  C.v = (wi, lead = 1) => Math.round(WORDS[wi - 1].s * FPS) - E0 - lead;     // frame where word wi APPEARS (lead f before spoken)
  t.build(C);
  await document.fonts.ready; await Promise.all(C.imgs.map(im => im.decode().catch(() => {})));
  C.fin.forEach(fn => fn());
  window.__fit = fitPages(C);
  return { N, s0: E0 / FPS, E0, name: t.name, type: t.type, ev: C.ev, fit: window.__fit };
};
window.renderT = async function (f) {
  const ff = C.twos ? f - (f % 2) : f;     // b-roll pages on twos (measured)
  await Promise.all(C.loads.map(l => l(f)));
  for (const u of C.ups) u(ff);
  let bl = 0;
  if (C.blurIn) { const [b, d] = C.blurIn; bl = Math.max(bl, b * (1 - P(ff, 0, d, EZ.p2o))); }
  if (C.blurOut) { const [b, d] = C.blurOut; bl = Math.max(bl, b * P(ff, C.N - d, d, EZ.p2i)); }
  C.root.style.filter = bl > 0.05 ? `blur(${bl}px)` : '';
  C.root.style.transform = bl > 0.05 ? `scale(${1 + bl / 140})` : '';   // overscan so the stage crops the blur's dark fringe
};
window.TPLN = () => TPL.length;
window.TPLNAME = i => TPL[i].name;
