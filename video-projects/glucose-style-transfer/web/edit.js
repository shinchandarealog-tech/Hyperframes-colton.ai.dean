// edit.js — full edit. Opening = the reference's sections in order (S01 S02 S03 S04 S05 S06 S07 [S08 deleted] S09 S10 S11),
// then the remaining approved templates, each used once. Word indices = web/words.js.
const TP = n => TPL[n - 1];                 // template by its number (T01 = 1)
const FACEC = [610, 620];                   // zoom centre: between her face centre (x 624, y 573) and chin (999)

// --- templates re-targeted onto the sentence that sits at that point of the timeline (same components, new words)
const S04_GOMODE = c => {                   // = T04 style (S04): photo, giant gold word BETWEEN the photo and its cut-out
  Img('img/p_family.jpg', { cx: 540, cy: 960, w: 1240, h: 2200, s0: 1.0, s1: 1.08, z: 0 });
  Page(c, 0, c.N, () => {
    Words(Line(Stack(c, { x: 90, top: 380, align: 'left' })), ['I', 'know', 'it’s', 'always'], [c.v(25), c.v(26), c.v(27), c.v(28)], { size: 80, color: '#f3e3cf' });
    Accent(Line(Stack(c, { x: 470, top: 500 })), 'go-mode', c.v(29, LEAD_A), { serif: 1, size: 240, grad: COL.gGold, ls: -0.04 });
  }, { free: true });
  Img('img/p_family_cut.png', { cx: 540, cy: 960, w: 1240, h: 2200, s0: 1.0, s1: 1.08, z: 3 });
};
const S05_MOM = c => {                      // = T05 style (S05): sans line + orange italic serif
  Aroll(c);
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: X, bottom: BOT });
    Words(Line(s), ['but', 'now', 'I’m', 'a'], [c.v(31), c.v(32), c.v(33), c.v(34)], { size: 84, color: INK });
    Accent(Line(s, { mt: 4 }), 'mom', c.v(35, LEAD_A), { serif: 1, ital: 1, size: 150, grad: COL.gOrangeH, shadow: SH });
  });
};
const T19_OPP = c => {                      // = T19 (new): lead + three rust pills, one per spoken phrase
  Aroll(c);
  Page(c, 0, c.N, () => {
    const s = Stack(c, { x: X, bottom: BOT });
    Words(Line(s), ['so', 'I', 'was', 'like,'], [c.v(83), c.v(84), c.v(85), c.v(86)], { size: 68, color: INK });
    [['if the opportunity', 87], ['is there', 90], ['why not take it?', 92]].forEach(([t, i]) => {
      const a = Accent(Line(s, { mt: 10 }), t, c.v(i, 3), { serif: 1, ital: 1, size: 72, color: '#fbe9d6', mode: 'none', grow: false, wrapCss: 'padding:2px 30px 12px;' });
      BoxBehind(a, { color: COL.rust, r: 22, px: 0, py: 0, top: 0, bottom: 0, mode: 'growC', dur: 10 });
    });
  });
};
const T14_HELP = c => {                     // = T14 style (S15): 3x3 photo grid pop + title
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
    Words(Line(s), ['but', 'I', 'had'], [c.v(96), c.v(97), c.v(98)], { size: 72, color: COL.grey });
    Accent(Line(s, { mt: -2 }), 'so much help.', c.v(99, LEAD_A), { serif: 1, ital: 1, size: 140, color: '#3e3f3e' });
  }, { free: true });
};

// [build, type, first word, label, options, template it comes from]
const SEGS = [
  [TP(1).build, 'speaker', 1, 'S01 hook', { cam: 'keep' }, 'T01'],
  [TP(2).build, 'speaker', 10, 'S02 intro + blur-out', { cam: 'keep', blurOut: [15, 6] }, 'T02'],
  [TP(3).build, 'broll', 17, 'S03 cut-out on brown', { blurIn: [40, 6] }, 'T03'],
  [S04_GOMODE, 'broll', 25, 'S04 giant word behind person', {}, 'T04'],
  [S05_MOM, 'speaker', 31, 'S05 sans + orange serif', {}, 'T05'],
  [TP(6).build, 'speaker', 36, 'S06 big orange-yellow word', {}, 'T06'],
  [TP(7).build, 'speaker', 40, 'S07 serif + underline', {}, 'T07'],
  [TP(9).build, 'broll', 46, 'S09 label box + drawn circle', {}, 'T09'],
  [TP(10).build, 'speaker', 51, 'S10 rust bar', {}, 'T10'],
  [TP(11).build, 'speaker', 55, 'S11 pill + blur-out', { blurOut: [10, 6] }, 'T11'],
  [TP(16).build, 'speaker', 61, 'S17 rust CAPS + arrow + box', {}, 'T16'],
  [TP(18).build, 'speaker', 69, 'S19 blur-in hero word', { blurIn: [14, 8] }, 'T18'],
  [TP(15).build, 'speaker', 72, 'S16 underline -> dark pill', {}, 'T15'],
  [TP(12).build, 'broll', 77, 'S12-13 engraved word + carousel', { blurIn: [40, 6] }, 'T12'],
  [T19_OPP, 'speaker', 83, 'NEW list of pills', {}, 'T19'],
  [T14_HELP, 'broll', 96, 'S15 photo grid', {}, 'T14'],
  [TP(20).build, 'speaker', 102, 'NEW end card', {}, 'T20'],
];
// global frame boundaries: a segment starts 0.04 s before its first word; rounded once for the whole video
window.RAW_F = 855; const TAIL = 13;      // the last shot runs on into the raw footage after her last word, so the end card holds >= 1 s
const BOUNDS = SEGS.map((s, k) => k === 0 ? 0 : Math.round((WORDS[s[2] - 1].s - 0.04) * FPS)).concat([EDIT_F + TAIL]);

// camera on the speaker (skill 8.2): hook + S02 copy the reference; every other speaker shot = ONE sine move, alternating in/out,
// starting where the previous one stopped, range 1.00-1.12, <= 10 % per shot, ~7.5 %/s
const CAMS = (() => { let z = 1.0, dir = 1; return SEGS.map((s, k) => {
  if (s[1] !== 'speaker') return null;
  if (s[4].cam === 'keep') { z = 1.0; return 'keep'; }
  const n = BOUNDS[k + 1] - BOUNDS[k], dz = Math.min(0.10, 0.075 * n / FPS);
  if (z + dir * dz > 1.12 || z + dir * dz < 1.0) dir = -dir;
  const z0 = z, z1 = Math.min(1.12, Math.max(1.0, z + dir * dz)); z = z1; dir = -dir; return [z0, z1];
}); })();

window.SEGN = () => SEGS.length;
window.initS = async function (k) {
  const s = SEGS[k], st = Stage(), E0 = BOUNDS[k], N = BOUNDS[k + 1] - E0;
  C = { root: st, par: st, ups: [], fin: [], loads: [], ev: [], pages: [], imgs: [], E0, N, s0: E0 / FPS, speaker: s[1] === 'speaker', twos: s[1] === 'broll',
    camO: FACEC, cam: f => 1, blurIn: s[4].blurIn, blurOut: s[4].blurOut };
  C.v = (wi, lead = 1) => Math.round(WORDS[wi - 1].s * FPS) - E0 - lead;
  const cm = CAMS[k];
  if (cm === 'keep') C.camO = [490, 560];                          // template's own measured move (hook 1.28->1, S02 1.058->1)
  s[0](C);
  if (cm) { const [z0, z1] = cm; C.cam = f => LERP(z0, z1, EZ.sineio(cl(f / Math.max(1, N - 1)))); }
  await document.fonts.ready; await Promise.all(C.imgs.map(im => im.decode().catch(() => {})));
  C.fin.forEach(fn => fn());
  const fit = fitPages(C);
  return { k, E0, N, label: s[3], tpl: s[5], type: s[1], cam: cm, ev: C.ev.map(([f, t]) => [f + E0, t]), fit };
};
