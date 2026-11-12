// tpl.js — 20 templates on the client's own sentences. T01-T18 = the reference's sections in order (S12+S13 are one
// continuous move -> one template). T19-T20 = NEW, built only from reference parts.
// Word indices refer to web/words.js (edit time). Speaker captions sit below the chin (fitPages() checks every frame).
const LEAD_S = 1, LEAD_A = 8;      // measured: sans words 0-2 f before the voice, serif accents 6-15 f
const BOT = 1500;                  // default stack bottom (IG safe y <= 1520)
const X = 492;
// The client wears WHITE: below-chin captions sit on white fabric, so speaker pages use the reference's own inks for light grounds
// (#3e3e3e measured on its light b-roll pages, rust #8f2e1e on its peach-wall titles). Gradient words get a soft shadow.
const INK = '#3e3e3e', SH = 'drop-shadow(0 3px 9px rgba(60,28,12,.5))';                     // centre of the IG safe zone (84..900)

// T01 — S01 hook: zoom-out 1.28->1, IG card, sans line + serif CAPS on dark box, page swap, orange-gradient CAPS flicker
T('Hook - zoom-out, IG card, dark box, orange flicker word', 1, 9, 'speaker', c => {
  c.cam = CAM.hook; Aroll(c);
  const swap = c.v(8, LEAD_S);
  Page(c, 0, c.N, () => { IGCard(c, { x: 120, y: 1040, scale: 0.78, handle: 'client.handle', name: 'CLIENT NAME', stats: '<b>—</b> posts&nbsp;&nbsp; <b>—</b> followers&nbsp;&nbsp; <b>—</b> following', initials: 'CN', V: 3 }); }, { free: true }).__ig = 1;
  Page(c, 0, swap, () => {
    const s = Stack(c, { x: X, bottom: 1518 });
    const l1 = Line(s); Words(l1, ['I’ve', 'always', 'known', 'that'], [c.v(1, LEAD_S), c.v(2, LEAD_S), c.v(3, LEAD_S), c.v(4, LEAD_S)], { size: 66, color: INK });
    const l2 = Line(s, { mt: 14 }); const a = Accent(l2, 'I WANT MORE', c.v(5, LEAD_A), { serif: 1, ital: 1, size: 90, color: COL.white, mode: 'blur' });
    BoxBehind(a, { color: COL.darkBox, alpha: 0.92, r: 14, px: 24, py: 8, mode: 'wipeL', dur: 7 });
  });
  Page(c, swap, c.N, () => {
    const s = Stack(c, { x: X, bottom: 1518 });
    Words(Line(s), ['for'], [swap], { size: 72, color: INK });
    Accent(Line(s, { mt: 4 }), 'MYSELF', c.v(9, LEAD_A), { serif: 1, size: 104, grad: COL.gOrangeV, mode: 'flicker', flickerSpan: 5, shadow: SH });
  });
}, { pre: 0.05 });

// T02 — S02: stair-step left lines + yellow italic glow word, blur-through out
T('Stair-step lines + yellow glow word + blur-out', 10, 16, 'speaker', c => {
  c.cam = CAM.intro; Aroll(c);
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: 150, bottom: BOT, align: 'left' });
    Words(Line(s), ['but', 'also', 'when'], [c.v(10), c.v(11), c.v(12)], { size: 84, color: INK });
    Words(Line(s, { indent: 60, mt: 4 }), ['I', 'became', 'a'], [c.v(13), c.v(14), c.v(15)], { size: 84, color: INK });
    Accent(Line(s, { indent: 150, mt: 4 }), 'mom', c.v(16, LEAD_A), { serif: 1, ital: 1, size: 150, grad: COL.gYellow, glow: 'rgba(247,233,138,.55)', shadow: SH });
  });
}, { blurOut: [15, 6] });

// T03 — S03: cut-out object on flat brown, sans lead + cream pill (growC), page rotate, on twos
T('B-roll cut-out on brown + cream pill', 17, 24, 'broll', c => {
  Bg('background:radial-gradient(ellipse at 50% 55%,#82615a 0%,#6a4a44 75%)');
  Img('img/c_laptop.png', { cx: 540, cy: 1150, w: 640, h: 944, s0: 0.82, s1: 1.0, ez: EZ.circ, dur: 42, r1: -3, icss: 'object-fit:contain;filter:drop-shadow(0 30px 60px rgba(0,0,0,.35))', z: 1 });
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: 540, top: 300 });
    Words(Line(s), ['I', 'just', 'sat'], [c.v(17), c.v(18), c.v(19)], { size: 112, color: '#fbf2d7' });
    const a = Accent(Line(s, { mt: 22 }), 'MYSELF DOWN', c.v(20, 4), { serif: 1, ital: 1, size: 120, color: COL.pillInk, mode: 'none', grow: false, wrapCss: 'padding:6px 34px 14px;' });
    BoxBehind(a, { color: COL.creamPill, r: 22, px: 0, py: 0, top: 0, bottom: 0, mode: 'growC', dur: 8 });
  }, { free: true });
}, { blurIn: [40, 6] });

// T04 — S04: full-bleed photo, giant gold-gradient word BETWEEN the photo and its own cut-out, on twos
T('B-roll photo, giant gold word behind the people', 31, 35, 'broll', c => {
  Img('img/p_family.jpg', { cx: 540, cy: 960, w: 1240, h: 2200, s0: 1.0, s1: 1.08, z: 0 });
  Page(c, 0, c.N, () => {
    Words(Line(Stack(c, { x: 90, top: 380, align: 'left' })), ['but', 'now', 'I’m', 'a'], [c.v(31), c.v(32), c.v(33), c.v(34)], { size: 80, color: '#f3e3cf' });
    Accent(Line(Stack(c, { x: 410, top: 520 })), 'mom', c.v(35, LEAD_A), { serif: 1, size: 320, grad: COL.gGold, ls: -0.04 });
  }, { free: true });
  Img('img/p_family_cut.png', { cx: 540, cy: 960, w: 1240, h: 2200, s0: 1.0, s1: 1.08, z: 3 });
}, { pre: 0.35, post: 0.6 });

// T05 — S05: speaker, sans line + orange-gradient italic serif (3-line stack)
T('Sans line + orange italic serif', 92, 95, 'speaker', c => {
  c.cam = CAM.drift(); Aroll(c);
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: X, bottom: BOT });
    Words(Line(s), ['why', 'not'], [c.v(92), c.v(93)], { size: 84, color: INK });
    Accent(Line(s, { mt: 4 }), 'take it?', c.v(94, LEAD_A), { serif: 1, ital: 1, size: 132, grad: COL.gOrangeH, shadow: SH });
  });
}, { pre: 0.5, post: 0.5 });

// T06 — S06: sans + big italic orange->yellow word (183 px)
T('Sans + big italic orange-yellow word', 36, 39, 'speaker', c => {
  c.cam = CAM.drift(); Aroll(c);
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: X, bottom: BOT });
    Words(Line(s), ['I', 'need', 'to'], [c.v(36), c.v(37), c.v(38)], { size: 86, color: INK });
    Accent(Line(s, { mt: -6 }), 'relax', c.v(39, LEAD_A), { serif: 1, ital: 1, size: 183, grad: COL.gOrangeH, shadow: SH });
  });
}, { pre: 0.3, post: 0.4 });

// T07 — S07: cream serif line + underline growing from the left
T('Cream serif line + underline', 40, 45, 'speaker', c => {
  c.cam = CAM.drift(); Aroll(c);
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: X, bottom: BOT });
    Words(Line(s), ['I', 'need', 'to'], [c.v(40), c.v(41), c.v(42)], { size: 76, color: INK });
    const l2 = Line(s, { mt: 8 });
    const w = H('span', 'position:relative;display:inline-flex;align-items:baseline', l2.el);
    const sub = { el: w, items: [], V: 1e9 }; Words(sub, ['enjoy', 'the', 'journey'], [c.v(43), c.v(44), c.v(45)], { serif: 1, size: 110, color: COL.rust, ls: -0.03 });
    l2.V = sub.V; Underline(w, { V: c.v(45), color: COL.rust, th: 4, bot: -12 });
  });
}, { pre: 0.3, post: 0.4 });

// T08 — S08: rust sans lead + rust serif CAPS (random flicker) + rust pill + floating "?"
T('Rust CAPS flicker + rust pill + floating ?', 83, 91, 'speaker', c => {
  c.cam = CAM.drift(); Aroll(c);
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: X, bottom: BOT });
    Words(Line(s), ['so', 'I', 'was', 'like,'], [83, 84, 85, 86].map(i => c.v(i)), { size: 72, color: COL.rustDark, wt: 400 });
    Words(Line(s, { mt: 2 }), ['if', 'the'], [87, 88].map(i => c.v(i)), { size: 72, color: COL.rustDark, wt: 400 });
    Accent(Line(s, { mt: 6 }), 'OPPORTUNITY', c.v(89, LEAD_A), { serif: 1, size: 110, color: COL.rustInk, mode: 'flicker', flickerSpan: 12 });
    const l3 = Line(s, { mt: 14 });
    const a = Accent(l3, 'is there', c.v(90, 2), { size: 64, wt: 400, color: COL.cream, mode: 'none', grow: false, wrapCss: 'padding:4px 26px 12px;' });
    BoxBehind(a, { color: COL.rust, r: 12, px: 0, py: 0, top: 0, bottom: 0, mode: 'growC', dur: 8 });
    Deco('?', { x: 40, y: 1000, rot: -12, V: c.v(87), size: 170 }); Deco('?', { x: 800, y: 980, rot: 10, V: c.v(88), size: 200 }); Deco('?', { x: 730, y: 1400, rot: 14, V: c.v(90), size: 130 });
  });
}, { pre: 0.25, post: 0.35 });

// T09 — S09: photo page, grey label box the word lands in, serif italic, hand-drawn circle; on twos
T('B-roll photo + label box + drawn circle', 46, 50, 'broll', c => {
  Img('img/p_momlift.jpg', { cx: 540, cy: 960, w: 1240, h: 2200, s0: 1.0, s1: 1.05, z: 0 });
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: 70, top: 1180, align: 'left' });
    const l1 = Line(s); Words(l1, ['stay'], [c.v(46)], { size: 70, color: '#f6efe6' });
    const lb = H('span', `display:inline-block;margin-left:14px;padding:2px 14px 8px;background:rgba(138,138,138,.85);border-radius:4px;${fontCss({ size: 70, color: '#fff' })}`, l1.el, 'present');
    U(f => { lb.style.opacity = f >= c.v(46) ? 1 : 0; lb.style.color = f >= c.v(47) ? '#fff' : 'transparent'; });   // box first, empty; the word lands in it
    EV(c.v(46), 'chip');
    const l2 = Line(s, { mt: 4 }); Words(l2, ['for', 'my'], [c.v(48), c.v(49)], { size: 70, color: '#f6efe6' });
    Accent(l2, 'child', c.v(50, LEAD_A), { serif: 1, ital: 1, size: 150, color: '#fff8ee', wrapCss: 'margin-left:16px' });
    Stroke('M 600 140 C 790 140 800 520 600 520 C 400 520 395 150 615 150', { V: c.v(48), dur: 14, color: '#d9a46a', w: 4 });
  }, { free: true });
}, { pre: 0.3, post: 0.4 });

// T10 — S10: big italic cream word with a rust bar behind its lower half, bar grows from the left
T('Rust bar behind big italic word', 51, 54, 'speaker', c => {
  c.cam = CAM.drift(); Aroll(c);
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: X, bottom: BOT });
    Words(Line(s), ['because', 'I’m', 'a'], [c.v(51), c.v(52), c.v(53)], { size: 80, color: INK });
    const a = Accent(Line(s, { mt: -4 }), 'mother', c.v(54, LEAD_A), { serif: 1, ital: 1, size: 200, color: '#fdf6eb', shadow: SH });
    BoxBehind(a, { color: COL.rust, r: 0, px: 50, top: '57%', bottom: '7%', mode: 'wipeL', dur: 10, V: c.v(54, LEAD_A) + 4 });
  });
}, { pre: 0.3, post: 0.45 });

// T11 — S11: sans lead + ghost cream pill (growC from a centre line), blur-through out
T('Sans + cream pill grows from centre + blur-out', 55, 60, 'speaker', c => {
  c.cam = CAM.drift(); Aroll(c);
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: X, bottom: BOT });
    Words(Line(s), ['she', 'doesn’t', 'have'], [c.v(55), c.v(56), c.v(57)], { size: 80, color: INK });
    const a = Accent(Line(s, { mt: 16 }), 'ANY OTHER MOM', c.v(58, 3), { serif: 1, ital: 1, size: 92, color: '#fbe9d6', mode: 'none', grow: false, wrapCss: 'padding:4px 30px 12px;' });
    BoxBehind(a, { color: COL.rust, r: 26, px: 0, py: 0, top: 0, bottom: 0, mode: 'growC', dur: 12 });
  });
}, { pre: 0.3, post: 0.35, blurOut: [10, 6] });

// T12 — S12+S13: photo with engraved word -> page shrinks into a card -> carousel of photo cards with italic labels; on twos
T('B-roll engraved word, card shrink, carousel', 77, 82, 'broll', c => {
  Bg('background:#f1e6c8');
  const shrinkAt = c.v(80, 2), slide = 9;
  const pageEl = Abs('left:0;top:0;width:1080px;height:1920px;z-index:2;overflow:hidden;transform-origin:540px 1000px');
  const prev = C.par; C.par = pageEl;
  const ph = Img('img/p_sunrise.jpg', { cx: 540, cy: 960, w: 1240, h: 2200, s0: 1.0, s1: 1.06, z: 0 });
  const g = Accent(Line(Stack(c, { x: 700, top: 300 })), 'GOD', c.v(77, LEAD_A), { serif: 1, size: 250, color: 'rgba(60,24,8,.62)', css: 'mix-blend-mode:multiply;text-shadow:0 2px 0 rgba(255,220,170,.35)' });
  C.par = prev;
  // carousel strip
  const cards = [['img/card_0.jpg', 'A CHILD'], ['img/card_1.jpg', 'A CAREER'], ['img/card_3.jpg', 'A FAMILY']];
  const strip = Abs('left:0;top:0;width:1080px;height:1920px;z-index:1');
  const cw = 400, ch = 660, gap = 70, cy = 1000;
  const els = cards.map(([src, lab], k) => {
    const d = H('div', `position:absolute;left:${540 - cw / 2 + (k + 1) * (cw + gap)}px;top:${cy - ch / 2}px;width:${cw}px;height:${ch}px`, strip);
    const im = H('img', `width:100%;height:100%;object-fit:cover;border-radius:6px;display:block`, d); im.src = src; C.imgs.push(im);
    H('div', `position:absolute;left:50%;top:-118px;transform:translateX(-50%);white-space:nowrap;${fontCss({ serif: 1, ital: 1, size: 84, color: COL.rust })}`, d, lab);
    return d;
  });
  const lab0 = H('div', `position:absolute;left:540px;top:${cy - ch / 2 - 118}px;transform:translateX(-50%);white-space:nowrap;z-index:3;${fontCss({ serif: 1, ital: 1, size: 84, color: COL.rust })}`, C.par, 'GOD');
  const steps = [shrinkAt + 12, shrinkAt + 24, shrinkAt + 36].filter(t => t + 8 < c.N);   // only slides that finish before the cut   // one card per 12 f (reference: ~14 f), power3.inOut 8 f
  U(f => {
    const p = P(f, shrinkAt, 4, EZ.p3io); const sc = LERP(1, cw / 1080, p);
    pageEl.style.transform = `scale(${sc})`; pageEl.style.borderRadius = p > 0 ? `${6 / sc}px` : '0';
    let off = 0, blur = 0; steps.forEach(t => { const q = P(f, t, 8, EZ.p3io); off += q; if (q > 0 && q < 1) blur = 12; });
    const dx = -off * (cw + gap) * (f >= shrinkAt + 4 ? 1 : 0);
    strip.style.transform = `translateX(${dx}px)`; strip.style.filter = blur ? `blur(${blur}px)` : '';
    strip.style.visibility = f >= shrinkAt ? 'visible' : 'hidden';
    pageEl.style.translate = `${dx}px 0`; lab0.style.translate = `${dx}px 0`; lab0.style.opacity = f >= shrinkAt + 4 ? 1 : 0;
    pageEl.style.filter = blur ? `blur(${blur}px)` : ''; if (f === shrinkAt + 2 || steps.some(t => f === t + 2)) EV(f, 'whoosh');
  });
}, { pre: 0.35, post: 1.45, blurIn: [40, 6] });

// T13 — S14: cut-out on light grey + bold serif title + 4 italic labels around; on twos
T('B-roll cut-out diagram + 4 italic labels', 96, 101, 'broll', c => {
  Bg('background:radial-gradient(ellipse at 50% 55%,#f2f2f2 0%,#d6d6d6 85%)');
  Img('img/c_mombaby.png', { cx: 540, cy: 1130, w: 600, h: 720, s0: 0.95, s1: 1.02, icss: 'object-fit:contain;-webkit-mask-image:linear-gradient(180deg,#000 72%,transparent 98%),linear-gradient(90deg,transparent 0%,#000 14%);-webkit-mask-composite:source-in;mask-composite:intersect' });
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: 540, top: 330 });
    Words(Line(s), ['but', 'I', 'had'], [c.v(96), c.v(97), c.v(98)], { size: 72, color: COL.grey });
    Accent(Line(s, { mt: -8 }), 'so much help.', c.v(99, LEAD_A), { serif: 1, ital: 1, size: 150, color: '#3d3e3e' });
    [['Family', 120, 830], ['Faith', 770, 790], ['Patience', 100, 1380], ['Friends', 740, 1430]].forEach(([t, x, y], k) => {
      const d = Abs(`left:${x}px;top:${y}px;${fontCss({ serif: 1, ital: 1, size: 54, color: COL.grey })};white-space:nowrap`, t);
      const V = c.v(100) + 3 * k; EV(V, 'word');
      U(f => { const p = P(f, V, 4); d.style.opacity = p; d.style.filter = p < 1 ? `blur(${10 * (1 - p)}px)` : ''; });
    });
  }, { free: true });
}, { pre: 0.3, post: 0.45 });

// T14 — S15: 3x3 photo grid, tilted -2°, tiles pop in random order (back.out(1.7) 6 f, stagger 1 f); on twos
T('B-roll 3x3 photo grid pop + title', 102, 108, 'broll', c => {
  Bg('background:#e9e9e9');
  const grid = Abs('left:84px;top:640px;width:912px;height:1110px;z-index:1;transform:rotate(-2deg)');
  const R = rng(7); const order = [...Array(9).keys()].sort(() => R() - .5);
  for (let k = 0; k < 9; k++) {
    const t = H('img', `position:absolute;left:${(k % 3) * 312}px;top:${Math.floor(k / 3) * 378}px;width:300px;height:366px;object-fit:cover;border-radius:4px`, grid); t.src = `img/tile_${k}.jpg`; C.imgs.push(t);
    const V = 2 + order.indexOf(k); if (order.indexOf(k) === 0) EV(V, 'chip');
    U(f => { const p = P(f, V, 6, EZ.back(1.7)); t.style.opacity = f >= V ? Math.min(1, p * 2) : 0; t.style.transform = `scale(${LERP(0.85, 1, p)})`; });
  }
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: 540, top: 250 });
    Words(Line(s), ['I', 'had', 'such', 'a', 'great'], [102, 103, 104, 105, 106].map(i => c.v(i)), { size: 64, color: COL.grey });
    Accent(Line(s, { mt: -2 }), 'support system', c.v(107, LEAD_A), { serif: 1, size: 132, color: '#3e3f3e' });
  }, { free: true });
}, { pre: 0.3, post: 0.4 });

// T15 — S16: page 1 cream serif + underline -> page 2 dark pill revealed by a L->R mask wipe
T('Underline page, then dark pill mask-wipe', 72, 76, 'speaker', c => {
  c.cam = CAM.drift(); Aroll(c);
  const sw = c.v(75, LEAD_A + 4);
  Page(c, 0, sw, () => {
    const s = Stack(c, { x: X, bottom: BOT });
    const l = Line(s); const w = H('span', 'position:relative;display:inline-flex;align-items:baseline', l.el);
    const sub = { el: w, V: 1e9 }; Words(sub, ['but', 'on', 'the'], [c.v(72), c.v(73), c.v(74)], { serif: 1, size: 96, color: COL.rust, ls: -0.03 });
    l.V = sub.V; Underline(w, { V: c.v(74), color: COL.rust, th: 3, bot: -10 });
  });
  Page(c, sw, c.N, () => {
    const s = Stack(c, { x: X, bottom: BOT });
    const a = Accent(Line(s), 'other hand', sw, { serif: 1, ital: 1, size: 132, color: '#fefaf2', mode: 'none', grow: false, wrapCss: 'padding:8px 40px 26px;' });
    BoxBehind(a, { color: COL.darkPill, r: 22, px: 0, py: 0, top: 0, bottom: 0, mode: 'maskLR', dur: 12, V: sw });
  });
}, { pre: 0.3, post: 0.45 });

// T16 — S17: rust italic CAPS flicker + rust CAPS sans + hand-drawn arrow -> line grows into a box; page fades out (4 f)
T('Rust CAPS + drawn arrow + line-to-box', 61, 68, 'speaker', c => {
  c.cam = CAM.drift(); Aroll(c);
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: 510, top: 1100 });
    Accent(Line(s), 'SO I HAVE', c.v(61, 4), { serif: 1, ital: 1, size: 108, color: COL.rustInk, mode: 'flicker', flickerSpan: 8, lh: 0.95 });
    Accent(Line(s, { mt: -6 }), 'TO DO', c.v(64, 4), { serif: 1, ital: 1, size: 108, color: COL.rustInk, mode: 'flicker', flickerSpan: 5, lh: 0.95 });
    Words(Line(s, { mt: 2 }), ['WHAT', 'IT'], [c.v(66), c.v(67)].map(v => v - 4), { size: 58, wt: 400, color: COL.rustDark, ls: -0.02 });
    Stroke('M 380 1342 C 320 1352 290 1380 296 1420', { V: c.v(66), dur: 12, color: COL.rust, w: 4, arrow: 'M 278 1400 L 296 1424 L 315 1398' });
    LineToBox({ x: 250, y: 1432, w: 300, h: 86, V: c.v(68, 6), color: COL.rust, r: 14,
      html: `<div style="${fontCss({ serif: 1, ital: 1, size: 76, color: '#fff3e4' })}">takes</div>` });
  }, { fadeOut: 4, noFit: false });
}, { pre: 0.25, post: 0.55 });

// T17 — S18: huge rust CAPS BEHIND the speaker (person matte on top), left stack flickers out, giant title flickers in, push-in 1.18
T('Giant rust title behind the speaker + push-in', 25, 30, 'speaker', c => {
  const p2 = c.v(29, 6);
  c.camO = [760, 480]; c.cam = f => (f < p2 ? 1 + 0.0006 * f : CAM.push(p2)(f) * (1 + 0.0006 * p2)); Aroll(c); Matte(c);
  Page(c, 0, p2, () => {
    const s = Stack(c, { x: 60, top: 170, align: 'left' });
    [['I', 25], ['KNOW', 26], ['IT’S', 27], ['ALWAYS', 28]].forEach(([w, i], k) => Accent(Line(s, { mt: -18 }), w, c.v(i, 3), { serif: 1, size: 150, color: '#8f2f1f', mode: 'flicker', flickerSpan: 4, lh: 0.95, grow: false }));
  }, { free: true });
  Page(c, p2, c.N, () => {
    const s = Stack(c, { x: 40, top: 150, align: 'left' });
    Accent(Line(s), 'GO-', p2, { serif: 1, size: 300, color: '#8f2f1f', mode: 'flicker', flickerSpan: 6, lh: 0.86, grow: false });
    Accent(Line(s, { mt: -10 }), 'MODE', c.v(30, 4), { serif: 1, size: 300, color: '#8f2f1f', mode: 'flicker', flickerSpan: 6, lh: 0.86, grow: false });
  }, { free: true });
}, { pre: 0.2, post: 0.35, blurOut: [21, 6] });

// T18 — S19: blur-in, left-aligned stack + pale-yellow italic hero word
T('Blur-in, left stack + pale-yellow hero word', 69, 71, 'speaker', c => {
  c.cam = CAM.drift(); Aroll(c);
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: 120, bottom: BOT, align: 'left' });
    Words(Line(s), ['to', 'be'], [c.v(69), c.v(70)], { size: 78, wt: 400, color: INK });
    Accent(Line(s, { mt: -10 }), 'present.', c.v(71, LEAD_A), { serif: 1, ital: 1, size: 210, grad: COL.gPale, shadow: SH });
  });
}, { pre: 0.5, post: 0.6, blurIn: [14, 8] });

// T19 — NEW: list of three — sans lead, then three cream pills (growC) with rust italic serif, one per spoken phrase
T('NEW - list of three cream pills', 36, 50, 'speaker', c => {
  c.cam = CAM.drift(); Aroll(c);
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: X, bottom: BOT });
    Words(Line(s), ['I', 'need', 'to'], [c.v(36), c.v(37), c.v(38)], { size: 68, color: INK });
    [['relax', 39], ['enjoy the journey', 43], ['stay present', 46]].forEach(([t, i]) => {
      const a = Accent(Line(s, { mt: 10 }), t, c.v(i, 3), { serif: 1, ital: 1, size: 72, color: '#fbe9d6', mode: 'none', grow: false, wrapCss: 'padding:2px 30px 12px;' });
      BoxBehind(a, { color: COL.rust, r: 22, px: 0, py: 0, top: 0, bottom: 0, mode: 'growC', dur: 10 });
    });
  });
}, { pre: 0.3, post: 0.4 });

// T20 — NEW: end card — IG profile card + rust "Follow" pill + cream serif line with underline
T('NEW - end card: IG profile + follow pill', 102, 108, 'speaker', c => {
  c.cam = CAM.drift(); Aroll(c);
  Page(c, 0, c.N, () => { IGCard(c, { x: 120, y: 1060, scale: 0.78, handle: 'client.handle', name: 'CLIENT NAME', stats: '<b>—</b> posts&nbsp;&nbsp; <b>—</b> followers&nbsp;&nbsp; <b>—</b> following', initials: 'CN', V: 2 }); }, { free: true });
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: X, bottom: BOT });
    const l = Line(s); const w = H('span', 'position:relative;display:inline-flex;align-items:baseline', l.el);
    const sub = { el: w, V: 1e9 }; Words(sub, ['a', 'great', 'support', 'system'], [c.v(105), c.v(106), c.v(107), c.v(108)], { serif: 1, size: 70, color: COL.rust, ls: -0.03 });
    l.V = sub.V; Underline(w, { V: c.v(108), color: COL.rust, th: 3, bot: -10 });
    const pill = Line(s, { mt: 22 });
    const a = Accent(pill, 'Follow for more', c.v(107), { size: 54, wt: 400, color: '#fbe9d6', mode: 'none', grow: false, wrapCss: 'padding:6px 30px 14px;' });
    BoxBehind(a, { color: COL.rust, r: 14, px: 0, py: 0, top: 0, bottom: 0, mode: 'growC', dur: 8 });
  });
}, { pre: 0.3, post: 0.9 });
