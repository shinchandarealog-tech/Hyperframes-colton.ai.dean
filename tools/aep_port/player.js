// aep_port player — renders extracted After Effects comps in a browser canvas.
// Supports what the Hook & Captions pack uses: precomps, solids, nulls, parenting,
// keyframes (linear / bezier / hold), expressions (run verbatim after operator
// rewriting), Essential Property overrides, Fill + Transform effects, text layers
// with range / expression selectors (position, scale, rotation, opacity, blur),
// comp-bounds clipping, and media placeholders.
"use strict";
(function () {
const FONT_MAP = {
  "NHaasGroteskDSPro-75Bd": { family: "Inter Display", weight: 700, style: "normal" },
  "PlayfairDisplay-Italic": { family: "Playfair Display", weight: 400, style: "italic" },
};
const INTERP = { 6612: "linear", 6613: "bezier", 6614: "hold" };

// ---------- vector helpers used by compiled expressions ----------
function unwrap(x) {
  if (x instanceof PropRef) return x.value;
  if (Array.isArray(x) && x.some((e) => e instanceof PropRef)) return x.map(unwrap);
  return x;
}
function vec(op, a, b) {
  a = unwrap(a); b = unwrap(b);
  const A = Array.isArray(a), B = Array.isArray(b);
  if (!A && !B) return op(a, b);
  if (A && B) { const n = Math.max(a.length, b.length); const r = []; for (let i = 0; i < n; i++) r.push(op(a[i] ?? 0, b[i] ?? 0)); return r; }
  return A ? a.map((v) => op(v, b)) : b.map((v) => op(a, v));
}
const H = {
  __add: (a, b) => { const ua = unwrap(a), ub = unwrap(b);
    if (typeof ua === "string" || typeof ub === "string") return ua + ub;
    // AE: adding vectors of different length keeps the longer length
    return vec((x, y) => x + y, ua, ub); },
  __sub: (a, b) => vec((x, y) => x - y, a, b),
  __mul: (a, b) => vec((x, y) => x * y, a, b),
  __div: (a, b) => vec((x, y) => x / y, a, b),
  __neg: (a) => { a = unwrap(a); return Array.isArray(a) ? a.map((v) => -v) : -a; },
  add: (a, b) => H.__add(a, b), sub: (a, b) => H.__sub(a, b), mul: (a, b) => H.__mul(a, b), div: (a, b) => H.__div(a, b),
  clamp: (v, lo, hi) => { v = unwrap(v); lo = unwrap(lo); hi = unwrap(hi);
    const c1 = (x, i) => Math.min(Math.max(x, Array.isArray(lo) ? lo[i] : lo), Array.isArray(hi) ? hi[i] : hi);
    return Array.isArray(v) ? v.map(c1) : c1(v, 0); },
  length: (a, b) => { a = unwrap(a); if (b !== undefined) a = H.__sub(a, b); return Array.isArray(a) ? Math.hypot(...a) : Math.abs(a); },
  normalize: (a) => { a = unwrap(a); const l = Math.hypot(...a) || 1; return a.map((v) => v / l); },
  dot: (a, b) => unwrap(a).reduce((s, v, i) => s + v * unwrap(b)[i], 0),
  degreesToRadians: (d) => unwrap(d) * Math.PI / 180,
  radiansToDegrees: (r) => unwrap(r) * 180 / Math.PI,
};
function interp(fn, t, a, b, c, d) {
  t = unwrap(t);
  if (c === undefined) { c = a; d = b; a = 0; b = 1; }
  a = unwrap(a); b = unwrap(b); c = unwrap(c); d = unwrap(d);
  let u = b === a ? (t >= b ? 1 : 0) : (t - a) / (b - a);
  u = Math.min(1, Math.max(0, u));
  const k = fn(u);
  return vec((x, y) => x + (y - x) * k, c, d);
}
H.linear = (...a) => interp((u) => u, ...a);
H.ease = (...a) => interp((u) => u * u * (3 - 2 * u), ...a);
H.easeIn = (...a) => interp((u) => u * u, ...a);
H.easeOut = (...a) => interp((u) => 1 - (1 - u) * (1 - u), ...a);

// deterministic random (AE seedRandom semantics are approximated)
function mulberry(seed) { return function () { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

// ---------- keyframe interpolation ----------
function solveBezierX(x0, x1, x2, x3, x) {
  let lo = 0, hi = 1;
  for (let i = 0; i < 40; i++) {
    const u = (lo + hi) / 2, m = 1 - u;
    const bx = m * m * m * x0 + 3 * m * m * u * x1 + 3 * m * u * u * x2 + u * u * u * x3;
    if (bx < x) lo = u; else hi = u;
  }
  return (lo + hi) / 2;
}
function bez(p0, p1, p2, p3, u) { const m = 1 - u; return m * m * m * p0 + 3 * m * m * u * p1 + 3 * m * u * u * p2 + u * u * u * p3; }
function interpKeys(keys, t) {
  if (t <= keys[0].t) return keys[0].v;
  const last = keys[keys.length - 1];
  if (t >= last.t) return last.v;
  let i = 0; while (keys[i + 1].t < t) i++;
  const k1 = keys[i], k2 = keys[i + 1];
  const o = INTERP[k1.oi] || "linear", inn = INTERP[k2.ii] || "linear";
  if (o === "hold") return k1.v;
  const dt = k2.t - k1.t, u = (t - k1.t) / dt;
  const v1 = k1.v, v2 = k2.v;
  if (typeof v1 !== "number" && !Array.isArray(v1)) return u < 1 ? v1 : v2; // text docs etc.
  if (o === "linear" && inn === "linear") return vec((a, b) => a + (b - a) * u, v1, v2);
  const oe = k1.oe || [], ie = k2.ie || [];
  const dims = Array.isArray(v1) ? v1.length : 1;
  const ease1 = (j) => oe[Math.min(j, oe.length - 1)] || { speed: 0, influence: 16.666 };
  const ease2 = (j) => ie[Math.min(j, ie.length - 1)] || { speed: 0, influence: 16.666 };
  const curve = (a, b, e1, e2) => {
    const i1 = o === "linear" ? 0 : e1.influence / 100, i2 = inn === "linear" ? 0 : e2.influence / 100;
    const s1 = o === "linear" ? (b - a) / dt : e1.speed, s2 = inn === "linear" ? (b - a) / dt : e2.speed;
    const x1 = k1.t + dt * i1, y1 = a + s1 * dt * i1, x2 = k2.t - dt * i2, y2 = b - s2 * dt * i2;
    const uu = solveBezierX(k1.t, x1, x2, k2.t, t);
    return bez(a, y1, y2, b, uu);
  };
  if (dims === 1) return curve(v1, v2, ease1(0), ease2(0));
  if (oe.length <= 1 && ie.length <= 1) {
    // spatial / single-ease: ease the distance along the (straight) path
    const L = Math.hypot(...v2.map((b, j) => b - v1[j]));
    if (L < 1e-9) return v1;
    const d = curve(0, L, ease1(0), ease2(0));
    return v1.map((a, j) => a + (v2[j] - a) * d / L);
  }
  return v1.map((a, j) => curve(a, v2[j], ease1(j), ease2(j)));
}

// ---------- property model ----------
let EPOCH = 0;
class Prop {
  constructor(layer, node) { this.layer = layer; this.node = node; this.cache = new Map(); this.epoch = -1; this.busy = false; }
  get name() { return this.node.name; }
  raw(t) { const n = this.node; return n.keys && n.keys.length ? interpKeys(n.keys, t) : n.value; }
  valueAt(t, extra) {
    const n = this.node;
    const ov = this.layer.comp.overrideFor(this);
    if (ov !== undefined) return ov;
    if (!n.js || n.disabled) return this.raw(t);
    if (this.epoch !== EPOCH) { this.cache.clear(); this.epoch = EPOCH; }
    const key = extra ? t + "|" + extra.textIndex : t;
    if (this.cache.has(key)) return this.cache.get(key);
    if (this.busy) return this.raw(t);  // cycle guard
    this.busy = true;
    let v;
    try { v = unwrap(runExpr(this, t, extra)); if (v === undefined || (typeof v === "number" && isNaN(v))) v = this.raw(t); }
    catch (e) { v = this.raw(t); if (!n.warned) { n.warned = 1; console.warn("expr error", this.layer.name, n.name, String(e)); } }
    this.busy = false;
    this.cache.set(key, v);
    return v;
  }
}
class PropRef {  // what an expression sees when it touches a property
  constructor(prop, t) { this.prop = prop; this.t = t; }
  get value() { return this.prop.valueAt(this.t); }
  valueAtTime(t) { return this.prop.valueAt(unwrap(t)); }
  get numKeys() { return (this.prop.node.keys || []).length; }
  key(i) { const k = this.prop.node.keys[i - 1]; return { time: k.t, value: k.v }; }
  nearestKey(t) { const ks = this.prop.node.keys || []; let b = 0; ks.forEach((k, i) => { if (Math.abs(k.t - t) < Math.abs(ks[b].t - t)) b = i; }); return { time: ks[b].t, value: ks[b].v, index: b + 1 }; }
  valueOf() { return this.value; }
  toString() { return String(this.value); }
  get length() { const v = this.value; return Array.isArray(v) ? v.length : undefined; }
}

const EXPR_FN = new Function("__ctx", "__src", "with (__ctx) { return eval(__src); }");
function runExpr(prop, t, extra) {
  const L = prop.layer, comp = L.comp;
  let rng = mulberry(L.index * 7919 + 17);
  const ctx = Object.assign(Object.create(null), H, {
    time: t, thisComp: comp.api(t), thisLayer: L.api(t), thisProperty: new PropRef(prop, t),
    get value() { return prop.raw(t); },
    valueAtTime: (tt) => prop.raw(unwrap(tt)),
    velocity: 0, speed: 0,
    index: L.index + 1, inPoint: L.inPoint, outPoint: L.outPoint, startTime: L.startTime,
    effect: (n) => L.api(t).effect(n),
    transform: L.api(t).transform, text: L.api(t).text,
    width: L.width, height: L.height,
    sourceRectAtTime: (tt, inc) => L.sourceRect(tt === undefined ? t : unwrap(tt)),
    timeToFrames: (tt = t, fps = comp.fps) => Math.floor(unwrap(tt) * fps + 1e-6),
    framesToTime: (f, fps = comp.fps) => unwrap(f) / fps,
    seedRandom: (s, timeless) => { rng = mulberry(Math.floor(unwrap(s)) * 9973 + (timeless ? 0 : Math.floor(t * comp.fps))); },
    random: (a, b) => { if (a === undefined) return rng(); if (b === undefined) { b = a; a = Array.isArray(unwrap(b)) ? unwrap(b).map(() => 0) : 0; }
      a = unwrap(a); b = unwrap(b); return Array.isArray(a) ? a.map((x, i) => x + (b[i] - x) * rng()) : a + (b - a) * rng(); },
    gaussRandom: (a, b) => ctx.random(a, b),
    noise: () => 0,
    wiggle: () => prop.raw(t),
    loopOut: () => prop.raw(t), loopIn: () => prop.raw(t),
    comp: (n) => L.engine.compByName(n).api(t),
    essentialProperty: (n) => comp.essential(n, t),
    textIndex: extra ? extra.textIndex : 0, textTotal: extra ? extra.textTotal : 0,
    console, Math, isNaN, Number, Array, String, parseFloat, parseInt,
  });
  return EXPR_FN(ctx, prop.node.js);
}

function flatProps(nodes, out = []) { for (const n of nodes || []) { out.push(n); if (n.props) flatProps(n.props, out); } return out; }
function findChild(node, match) { return (node.props || []).find((p) => p.match === match); }

class Layer {
  constructor(comp, d) {
    this.comp = comp; this.engine = comp.engine; this.d = d;
    this.name = d.name; this.index = d.index; this.inPoint = d.in; this.outPoint = d.out; this.startTime = d.start;
    this.stretch = d.stretch || 100; this.props = new Map();
    const tr = d.props.find((p) => p.match === "ADBE Transform Group");
    this.tr = {};
    for (const m of ["ADBE Anchor Point", "ADBE Position", "ADBE Scale", "ADBE Rotate Z", "ADBE Opacity"]) {
      const n = tr && findChild(tr, m); if (n) this.tr[m] = this.prop(n);
    }
    const fx = d.props.find((p) => p.match === "ADBE Effect Parade");
    this.effects = (fx && fx.props || []).map((e) => ({ node: e, name: e.name, match: e.match,
      params: (e.props || []).filter((q) => q.match !== "ADBE Effect Built In Params") }));
    const ov = d.props.find((p) => p.match === "ADBE Layer Overrides");
    this.overrides = (ov && ov.props || []).filter((p) => !p.props).map((n) => ({ node: n, prop: this.prop(n) }));
    const tx = d.props.find((p) => p.match === "ADBE Text Properties");
    if (tx) this.text = new TextLayer(this, tx);
    const src = d.source || {};
    this.kind = d.type === "TextLayer" ? "text" : d.type === "ShapeLayer" ? "shape" : src.kind === "CompItem" ? "comp" : src.color ? "solid" : "footage";
    this.width = src.w || comp.w; this.height = src.h || comp.h;
  }
  prop(n) { if (!this.props.has(n)) this.props.set(n, new Prop(this, n)); return this.props.get(n); }
  get source() { return this.d.source && this.d.source.id != null ? this.engine.comps[String(this.d.source.id)] : null; }
  effectApi(t, sel) {
    let e;
    if (typeof sel === "number") e = this.effects[sel - 1];
    else e = this.effects.find((x) => x.name === sel) || this.effects.find((x) => x.match === sel);
    if (!e) throw new Error(`effect ${sel} not found on ${this.name}`);
    const layer = this;
    const f = function (p) {
      p = unwrap(p);
      let q;
      if (typeof p === "number") q = e.params[p - 1];
      else q = e.params.find((x) => x.name === p) || e.params.find((x) => x.match === p);
      if (!q) throw new Error(`param ${p} not found in ${e.name}`);
      return new PropRef(layer.prop(q), t);
    };
    f.param = f; f.active = true; f.effectName = e.name;
    return f;
  }
  api(t) {
    const L = this;
    const trRef = (m) => (L.tr[m] ? new PropRef(L.tr[m], t) : undefined);
    return {
      name: L.name, index: L.index + 1, inPoint: L.inPoint, outPoint: L.outPoint, startTime: L.startTime,
      width: L.width, height: L.height,
      effect: (n) => L.effectApi(t, unwrap(n)),
      transform: { get position() { return trRef("ADBE Position"); }, get scale() { return trRef("ADBE Scale"); },
                   get rotation() { return trRef("ADBE Rotate Z"); }, get opacity() { return trRef("ADBE Opacity"); },
                   get anchorPoint() { return trRef("ADBE Anchor Point"); } },
      get position() { return trRef("ADBE Position"); }, get scale() { return trRef("ADBE Scale"); },
      get rotation() { return trRef("ADBE Rotate Z"); }, get opacity() { return trRef("ADBE Opacity"); },
      get anchorPoint() { return trRef("ADBE Anchor Point"); },
      text: L.text ? { sourceText: L.text.sourceText(t) } : undefined,
      sourceRectAtTime: (tt) => L.sourceRect(tt === undefined ? t : unwrap(tt)),
      toComp: (p) => L.matrix(t).apply(unwrap(p)),
    };
  }
  tv(m, t, dflt) { const p = this.tr[m]; return p ? p.valueAt(t) : dflt; }
  localMatrix(t) {
    const a = this.tv("ADBE Anchor Point", t, [0, 0]), p = this.tv("ADBE Position", t, [0, 0]);
    const s = this.tv("ADBE Scale", t, [100, 100]), r = this.tv("ADBE Rotate Z", t, 0);
    const k = this.fitScale || 1;
    return Mat.T(p[0], p[1]).mul(Mat.R(r)).mul(Mat.S(k * s[0] / 100, k * s[1] / 100)).mul(Mat.T(-a[0], -a[1]));
  }
  matrix(t) {
    let m = this.localMatrix(t);
    if (this.d.parent != null) { const P = this.comp.layers.find((l) => l.index === this.d.parent); if (P) m = P.matrix(t).mul(m); }
    return m;
  }
  sourceRect(t) {
    if (this.text) return this.text.bounds(this.localTime(t));
    return { left: 0, top: 0, width: this.width, height: this.height };
  }
  localTime(t) { return (t - this.startTime) * 100 / this.stretch; }
  active(t) { return this.d.enabled && t >= this.inPoint - 1e-6 && t < this.outPoint - 1e-6; }
}

class Mat {
  constructor(a = 1, b = 0, c = 0, d = 1, e = 0, f = 0) { Object.assign(this, { a, b, c, d, e, f }); }
  static T(x, y) { return new Mat(1, 0, 0, 1, x, y); }
  static S(x, y) { return new Mat(x, 0, 0, y, 0, 0); }
  static R(deg) { const r = deg * Math.PI / 180, c = Math.cos(r), s = Math.sin(r); return new Mat(c, s, -s, c, 0, 0); }
  mul(m) { return new Mat(this.a * m.a + this.c * m.b, this.b * m.a + this.d * m.b, this.a * m.c + this.c * m.d,
                          this.b * m.c + this.d * m.d, this.a * m.e + this.c * m.f + this.e, this.b * m.e + this.d * m.f + this.f); }
  apply(p) { return [this.a * p[0] + this.c * p[1] + this.e, this.b * p[0] + this.d * p[1] + this.f]; }
}

// ---------- text ----------
class TextLayer {
  constructor(layer, node) {
    this.layer = layer;
    this.docProp = layer.prop(findChild(node, "ADBE Text Document"));
    const more = findChild(node, "ADBE Text More Options");
    this.grouping = more ? (findChild(more, "ADBE Text Anchor Point Option") || {}).value || 1 : 1;
    this.groupAlign = more ? (findChild(more, "ADBE Text Anchor Point Align") || {}).value || [0, 0] : [0, 0];
    const anims = findChild(node, "ADBE Text Animators");
    this.animators = (anims && anims.props || []).map((a) => {
      const sels = findChild(a, "ADBE Text Selectors"), pr = findChild(a, "ADBE Text Animator Properties");
      const props = {};
      for (const p of (pr && pr.props) || []) if (p.mod || p.js || (p.keys && p.keys.length)) props[p.match] = layer.prop(p);
      const selectors = ((sels && sels.props) || []).map((s) => {
        const all = flatProps(s.props); const get = (m) => all.find((x) => x.match === m);
        const P = (m) => (get(m) ? layer.prop(get(m)) : null);
        return { kind: s.match, start: P("ADBE Text Percent Start"), end: P("ADBE Text Percent End"), offset: P("ADBE Text Percent Offset"),
          amount: P("ADBE Text Selector Max Amount"), exprAmount: P("ADBE Text Expressible Amount"),
          basedOn: (get("ADBE Text Range Type2") || {}).value || 1, mode: (get("ADBE Text Selector Mode") || {}).value || 1,
          shape: (get("ADBE Text Range Shape") || {}).value || 1, easeHigh: P("ADBE Text Levels Max Ease"), easeLow: P("ADBE Text Levels Min Ease") };
      });
      return { name: a.name, props, selectors };
    });
  }
  doc(t) { const d = this.docProp.valueAt(t); const o = this.layer.engine.textOverride(this.layer); return o != null ? Object.assign({}, d, { text: o }) : d; }
  sourceText(t) { const d = this.doc(t); return d.text; }
  font(d) { const f = FONT_MAP[d.font] || { family: "Inter Display", weight: 700, style: "normal" }; return `${f.style} ${f.weight} ${d.font_size}px "${f.family}"`; }
  layout(t) {
    const d = this.doc(t), ctx = this.layer.engine.measureCtx;
    ctx.font = this.font(d);
    let text = d.all_caps ? d.text.toUpperCase() : d.text;
    const lines = text.split(/\r\n|\r|\n|\u0003/);
    const lead = d.auto_leading ? d.font_size * 1.2 : d.leading;
    const track = (d.tracking || 0) * d.font_size / 1000;
    const chars = []; let word = -1, inWord = false, ci = 0, cx = 0;
    lines.forEach((line, li) => {
      const w = ctx.measureText(line).width + track * Math.max(0, line.length - 1);
      const x0 = d.justification === 7415 ? -w / 2 : d.justification === 7414 ? -w : 0;
      for (let i = 0; i < line.length; i++) {
        const ch = line[i], space = /\s/.test(ch);
        if (!space && !inWord) word++;
        inWord = !space;
        const x = x0 + ctx.measureText(line.slice(0, i)).width + track * i, cw = ctx.measureText(ch).width;
        chars.push({ ch, x, y: li * lead, w: cw, line: li, word: space ? -1 : word, index: ci++, nonSpace: space ? -1 : cx++ });
      }
      inWord = false;
    });
    const m = ctx.measureText("Hg");
    return { d, chars, lines: lines.length, words: word + 1, nonSpace: cx, ascent: m.actualBoundingBoxAscent, descent: m.actualBoundingBoxDescent };
  }
  bounds(t) {
    const L = this.layout(t); if (!L.chars.length) return { left: 0, top: 0, width: 0, height: 0 };
    const capA = L.d.font_size * 0.72;
    let x0 = Infinity, x1 = -Infinity;
    for (const c of L.chars) { x0 = Math.min(x0, c.x); x1 = Math.max(x1, c.x + c.w); }
    const top = -capA, bottom = (L.lines - 1) * (L.chars[L.chars.length - 1].y / Math.max(1, L.lines - 1) || 0) + L.descent * 0.3;
    return { left: x0, top, width: x1 - x0, height: bottom - top };
  }
  selectorAmount(s, t, unit, total) {
    if (s.kind === "ADBE Text Expressible Selector") {
      let v = s.exprAmount.valueAt(t, { textIndex: unit + 1, textTotal: total });
      v = Array.isArray(v) ? v[0] : v; return v / 100;
    }
    const st = s.start.valueAt(t), en = s.end.valueAt(t), off = s.offset.valueAt(t);
    let S = (st + off) / 100 * total, E = (en + off) / 100 * total; if (S > E) [S, E] = [E, S];
    const c = unit + 0.5;
    const eh = s.easeHigh ? s.easeHigh.valueAt(t) / 100 : 0, el = s.easeLow ? s.easeLow.valueAt(t) / 100 : 0;
    const easeLv = (v) => { if (eh === 0 && el === 0) return v; const u = solveBezierX(0, el, 1 - eh, 1, v); return bez(0, 0, 1, 1, u); };
    let v;
    const ramp = () => (E - S < 1e-9 ? (c >= E ? 1 : 0) : Math.min(1, Math.max(0, (c - S) / (E - S))));
    switch (s.shape) {
      case 2: v = easeLv(ramp()); break;                 // ramp up
      case 3: v = easeLv(1 - ramp()); break;             // ramp down
      case 4: { const r = ramp(); v = easeLv(1 - Math.abs(2 * r - 1)); if (c < S || c > E) v = 0; break; }  // triangle
      default: { const lo = Math.max(unit, S), hi = Math.min(unit + 1, E); v = Math.max(0, hi - lo); }      // square
    }
    const amt = s.amount ? s.amount.valueAt(t) / 100 : 1;
    return v * amt;
  }
  draw(ctx, t, M, opacity) {
    const L = this.layout(t), d = L.d;
    const unitsFor = (b) => (b === 1 ? L.chars.length : b === 2 ? L.nonSpace : b === 3 ? L.words : L.lines);
    const unitOf = (c, b) => (b === 1 ? c.index : b === 2 ? c.nonSpace : b === 3 ? c.word : c.line);
    // per-frame animator property values (constant across characters)
    const animVals = this.animators.map((a) => { const o = {}; for (const k in a.props) o[k] = a.props[k].valueAt(t); return o; });
    const fill = d.fill_color || [1, 1, 1];
    const fillCss = `rgb(${fill.map((x) => Math.round(x * 255)).join(",")})`;
    ctx.save();
    ctx.font = this.font(d); ctx.textBaseline = "alphabetic";
    // word / line groups for anchor grouping
    const groupBox = {};
    for (const c of L.chars) { if (c.word < 0) continue; const k = this.grouping === 2 ? "w" + c.word : this.grouping === 3 ? "l" + c.line : this.grouping === 4 ? "a" : "c" + c.index;
      const g = groupBox[k] || (groupBox[k] = { x0: Infinity, x1: -Infinity, y: c.y }); g.x0 = Math.min(g.x0, c.x); g.x1 = Math.max(g.x1, c.x + c.w); }
    for (const c of L.chars) {
      if (c.word < 0) continue;
      let px = 0, py = 0, sx = 100, sy = 100, rot = 0, op = 1, blur = 0;
      this.animators.forEach((a, ai) => {
        let amt = 0;
        a.selectors.forEach((s, si) => { const b = s.basedOn; const u = unitOf(c, b); if (u < 0) return;
          const v = this.selectorAmount(s, t, u, unitsFor(b)); amt = si === 0 ? v : s.mode === 3 ? amt * v : amt + v; });
        amt = Math.max(0, Math.min(1, amt));
        if (amt === 0) return;
        const v = animVals[ai];
        const P = v["ADBE Text Position 3D"]; if (P) { px += P[0] * amt; py += P[1] * amt; }
        const S = v["ADBE Text Scale 3D"]; if (S) { sx *= (100 + (S[0] - 100) * amt) / 100; sy *= (100 + (S[1] - 100) * amt) / 100; }
        const R = v["ADBE Text Rotation"]; if (R !== undefined) rot += R * amt;
        const O = v["ADBE Text Opacity"]; if (O !== undefined) op *= (100 + (O - 100) * amt) / 100;
        const B = v["ADBE Text Blur"]; if (B) blur += (Array.isArray(B) ? B[0] : B) * amt;
      });
      if (op <= 0.001 || Math.abs(sx) < 1e-4 || Math.abs(sy) < 1e-4) continue;
      const k = this.grouping === 2 ? "w" + c.word : this.grouping === 3 ? "l" + c.line : this.grouping === 4 ? "a" : "c" + c.index;
      const g = groupBox[k];
      const ax = (g.x0 + g.x1) / 2 + this.groupAlign[0] / 100 * (g.x1 - g.x0), ay = c.y + this.groupAlign[1] / 100 * d.font_size;
      const m = M.mul(Mat.T(px + ax, py + ay)).mul(Mat.R(rot)).mul(Mat.S(sx / 100, sy / 100)).mul(Mat.T(c.x - ax, c.y - ay));
      ctx.setTransform(m.a, m.b, m.c, m.d, m.e, m.f);
      ctx.globalAlpha = opacity * op;
      const scale = Math.sqrt(Math.abs(M.a * M.d - M.b * M.c));
      ctx.filter = blur > 0.05 ? `blur(${(blur * 0.5 * scale).toFixed(2)}px)` : "none";
      ctx.fillStyle = fillCss;
      ctx.fillText(c.ch, 0, 0);
    }
    ctx.restore();
  }
}

// ---------- composition ----------
class Comp {
  constructor(engine, c) {
    this.engine = engine; this.d = c; this.id = String(c.id); this.name = c.name; this.w = c.w; this.h = c.h; this.fps = c.fps;
    this.layers = c.layers.map((l) => new Layer(this, l));
    this.ovStack = [];
  }
  api(t) { const C = this; return { name: C.name, width: C.w, height: C.h, frameDuration: 1 / C.fps, numLayers: C.layers.length,
    layer: (n) => { n = unwrap(n); const L = typeof n === "number" ? C.layers.find((l) => l.index === n - 1) : C.layers.find((l) => l.name === n);
      if (!L) throw new Error("layer " + n + " not found in " + C.name); return L.api(t); } }; }
  overrideFor(prop) {
    const ov = this.ovStack[this.ovStack.length - 1]; if (!ov) return undefined;
    const L = prop.layer; for (const e of L.effects) if (e.params.includes(prop.node) && ov.has(e.name)) return ov.get(e.name);
    return undefined;
  }
  essential(n, t) { return undefined; }
  canvas() { const c = this.engine.newCanvas(this.w, this.h); return c; }
}

class Engine {
  constructor(spec, opts = {}) {
    this.spec = spec; this.opts = opts; this.comps = {};
    for (const [id, c] of Object.entries(spec.comps)) this.comps[id] = new Comp(this, c);
    this.root = this.comps[String(spec.root)];
    const mc = document.createElement("canvas"); this.measureCtx = mc.getContext("2d");
    this.pool = []; this.mediaCache = new Map(); this.mediaWant = new Set();
  }
  compByName(n) { return Object.values(this.comps).find((c) => c.name === n); }
  // ---- auto-fit: widen single-text "chunk" comps to fit their (new) text, keep alignment,
  // then reflow sibling chunks that share a row so the template's gaps are preserved.
  autofit() {
    const fitted = new Map();  // comp id -> {dW, just}
    for (const c of Object.values(this.comps)) {
      const texts = c.layers.filter((l) => l.text);
      if (texts.length !== 1 || c.layers.some((l) => l.kind === "comp")) continue;
      const L = texts[0], tEnd = c.d.duration - 1 / c.fps;
      EPOCH++;
      const lay = L.text.layout(tEnd); if (!lay.chars.length) continue;
      const M = L.localMatrix(tEnd);
      let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
      const mc = this.measureCtx; mc.font = L.text.font(lay.d);
      for (const ch of lay.chars) { if (ch.word < 0) continue; const mm = mc.measureText(ch.ch);
        for (const xx of [ch.x, ch.x + ch.w]) for (const yy of [ch.y - mm.actualBoundingBoxAscent, ch.y + mm.actualBoundingBoxDescent]) {
          const q = M.apply([xx, yy]); x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]); y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]); } }
      const W = c.w, margin = Math.max(6, 0.03 * lay.d.font_size), need = (x1 - x0) + 2 * margin;
      const just = lay.d.justification;
      // vertical: grow only when glyphs (e.g. descenders) would be cut, keep the block centred
      const Hh = c.h, mY = 4;
      if (y0 < 0 || y1 > Hh) {
        const H2 = Math.ceil(Math.max(Hh, (y1 - y0) + 2 * mY)), dy = (H2 - (y1 - y0)) / 2 - y0;
        const pos = L.tr["ADBE Position"].node; pos.value = [pos.value[0], pos.value[1] + dy, ...pos.value.slice(2)];
        c.h = H2; c.d.h = H2;
        const f0 = fitted.get(c.id) || { dW: 0, just }; f0.dH = H2 - Hh; fitted.set(c.id, f0);
      }
      if (x0 >= margin * 0.5 && x1 <= W - margin * 0.5) continue;
      const W2 = Math.ceil(Math.max(W, need));
      const target0 = just === 7415 ? (W2 - (x1 - x0)) / 2 : just === 7414 ? W2 - margin - (x1 - x0) : margin;
      const dx = target0 - x0;
      const pos = L.tr["ADBE Position"].node; pos.value = [pos.value[0] + dx, ...pos.value.slice(1)];
      c.w = W2; c.d.w = W2;
      const f1 = fitted.get(c.id) || { dH: 0 }; f1.dW = W2 - W; f1.just = just; fitted.set(c.id, f1);
    }
    if (!fitted.size) return;
    const shiftX = (x, f) => (f.just === 7415 ? x + f.dW / 2 : f.just === 7414 ? x + f.dW : x);
    for (const c of Object.values(this.comps)) {
      const kids = c.layers.filter((l) => l.kind === "comp" && l.source && fitted.has(l.source.id));
      if (!kids.length) continue;
      const tEnd = c.d.duration - 1 / c.fps;
      const before = new Map();
      for (const L of c.layers.filter((l) => l.kind === "comp" && l.source && l.source.layers.some((q) => q.text))) {
        EPOCH++; const M = L.matrix(tEnd); const src = L.source; const f = fitted.get(src.id);
        const oldW = src.w - (f ? f.dW || 0 : 0), oldH = src.h - (f ? f.dH || 0 : 0);
        // old on-screen box uses the old width and old anchor
        const a = L.tv("ADBE Anchor Point", tEnd, [0, 0]);
        const l0 = M.apply([0, oldH / 2])[0], r0 = M.apply([oldW, oldH / 2])[0];
        before.set(L, { l: l0, r: r0, y: M.apply([oldW / 2, oldH / 2])[1], sx: (r0 - l0) / oldW });
      }
      for (const L of kids) {   // keep each chunk's anchor on the same glyph position
        const f = fitted.get(L.source.id);
        const an = L.tr["ADBE Anchor Point"].node; an.value = [shiftX(an.value[0], f), an.value[1] + (f.dH || 0) / 2, ...an.value.slice(2)];
        for (const e of L.effects) if (e.match === "ADBE Geometry2") for (const m of ["ADBE Geometry2-0001", "ADBE Geometry2-0002"]) {
          const n = e.params.find((p) => p.match === m); n.value = [shiftX(n.value[0], f), n.value[1] + (f.dH || 0) / 2]; }
      }
      // rows: group by vertical centre
      const items = [...before.entries()].map(([L, b]) => ({ L, ...b }));
      const rows = [];
      for (const it of items.sort((p, q) => p.y - q.y)) {
        const r = rows.find((r) => Math.abs(r.y - it.y) < 40); if (r) r.items.push(it); else rows.push({ y: it.y, items: [it] });
      }
      for (const r of rows) {
        r.items.sort((p, q) => p.l - q.l);
        if (r.items.length < 2) continue;
        EPOCH++;
        const after = r.items.map((it) => { const M = it.L.matrix(tEnd), w = it.L.source.w, h = it.L.source.h;
          return { l: M.apply([0, h / 2])[0], r: M.apply([w, h / 2])[0] }; });
        const just = (fitted.get(r.items[0].L.source.id) || {}).just;
        // left-aligned rows keep the first chunk; right-aligned keep the last; centred keep the centre
        let cursor = after[0].l; const shifts = [0];
        for (let i = 1; i < r.items.length; i++) {
          const gap = r.items[i].l - r.items[i - 1].r; const w = after[i].r - after[i].l;
          const want = after[i - 1].r + shifts[i - 1] + gap; shifts.push(want - after[i].l);
        }
        let adj = 0;
        const oldL = r.items[0].l, oldR = r.items[r.items.length - 1].r;
        const newL = after[0].l + shifts[0], newR = after[after.length - 1].r + shifts[shifts.length - 1];
        if (just === 7414) adj = oldR - newR; else if (just === 7415) adj = (oldL + oldR) / 2 - (newL + newR) / 2;
        r.items.forEach((it, i) => { const pn = it.L.tr["ADBE Position"].node; pn.value = [pn.value[0] + shifts[i] + adj, ...pn.value.slice(1)]; });
      }
      // keep every row inside the frame's safe area (6% side margins): scale the row down if needed
      if (c === this.root || c.w >= 1000) {
        const safeL = c.w * 0.06, safeR = c.w * 0.94;
        for (const r of rows) {
          EPOCH++;
          const box = () => { let l = Infinity, rr = -Infinity; for (const it of r.items) { const M = it.L.matrix(tEnd), w = it.L.source.w, h = it.L.source.h;
            l = Math.min(l, M.apply([0, h / 2])[0]); rr = Math.max(rr, M.apply([w, h / 2])[0]); } return [l, rr]; };
          let [l, rr] = box();
          if (l >= safeL - 1 && rr <= safeR + 1) continue;
          const just = (fitted.get(r.items[0].L.source.id) || {}).just;
          const avail = just === 7414 ? Math.min(rr, safeR) - safeL : just === 7415 ? safeR - safeL : safeR - Math.max(l, safeL);
          const k = Math.min(1, avail / (rr - l));
          const pivot = just === 7414 ? rr : just === 7415 ? (l + rr) / 2 : l;
          for (const it of r.items) { it.L.fitScale = (it.L.fitScale || 1) * k; const pn = it.L.tr["ADBE Position"].node;
            pn.value = [pivot + (pn.value[0] - pivot) * k, ...pn.value.slice(1)]; }
          EPOCH++; [l, rr] = box();
          const sh = l < safeL ? safeL - l : rr > safeR ? safeR - rr : 0;
          if (sh) for (const it of r.items) { const pn = it.L.tr["ADBE Position"].node; pn.value = [pn.value[0] + sh, ...pn.value.slice(1)]; }
        }
      }
    }
    EPOCH++;
  }

  newCanvas(w, h) { const c = document.createElement("canvas"); c.width = Math.ceil(w); c.height = Math.ceil(h); return c; }
  textOverride(layer) { const t = this.opts.texts || {}; const key = layer.comp.name + "/" + layer.name; return t[key] ?? null; }
  mediaFrame(name, local) {
    const m = (this.opts.media || {})[name]; if (!m) return null;
    const idx = Math.max(0, Math.min(m.frames - 1, Math.floor(local * m.fps + 1e-6)));
    const url = m.pattern.replace("%05d", String(idx).padStart(5, "0"));
    if (this.mediaCache.has(url)) return this.mediaCache.get(url);
    this.mediaWant.add(url); return null;
  }
  async loadWanted() {
    const urls = [...this.mediaWant]; this.mediaWant.clear();
    await Promise.all(urls.map(async (u) => { const im = new Image(); im.src = u; await im.decode(); this.mediaCache.set(u, im); }));
    if (this.mediaCache.size > 400) { const keep = new Set(urls); for (const k of [...this.mediaCache.keys()]) if (!keep.has(k)) this.mediaCache.delete(k); }
  }
  // essential-property overrides: parent layer -> child comp control effects
  overridesFor(L, t) {
    if (!L.overrides.length) return null;
    const m = new Map();
    for (const o of L.overrides) {
      const v = o.prop.valueAt(t);
      const name = Array.isArray(v) && v.length === 4 ? "Text Color" : o.node.name;
      m.set(name, v);
    }
    return m;
  }
  renderComp(comp, t, ov) {
    const cv = comp.canvas(), ctx = cv.getContext("2d");
    comp.ovStack.push(ov);
    try {
      for (let i = comp.layers.length - 1; i >= 0; i--) {
        const L = comp.layers[i];
        if (!L.active(t) || L.d.adjustment || L.d.guide || L.kind === "shape" || L.d.null) continue;
        this.drawLayer(ctx, L, t);
      }
    } finally { comp.ovStack.pop(); }
    return cv;
  }
  drawLayer(ctx, L, t) {
    let opacity = L.tv("ADBE Opacity", t, 100) / 100;
    if (opacity <= 0) return;
    let M = L.matrix(t);
    let buf = null;
    const local = L.localTime(t);
    if (L.kind === "comp") {
      const src = L.source;
      if (src && src.layers.length === 0) {
        buf = this.newCanvas(src.w, src.h);
        const im = this.mediaFrame(src.name, local);
        if (im) { const c = buf.getContext("2d"); const s = Math.max(src.w / im.naturalWidth, src.h / im.naturalHeight);
          const w = im.naturalWidth * s, h = im.naturalHeight * s; c.drawImage(im, (src.w - w) / 2, (src.h - h) / 2, w, h); }
        else if (!(this.opts.media || {})[src.name]) { const c = buf.getContext("2d"); c.fillStyle = "#3a3a3a"; c.fillRect(0, 0, src.w, src.h); }
      } else if (src) buf = this.renderComp(src, local, this.overridesFor(L, t));
    } else if (L.kind === "solid") {
      buf = this.newCanvas(L.width, L.height); const c = buf.getContext("2d"); const col = L.d.source.color;
      c.fillStyle = `rgb(${col.map((x) => Math.round(x * 255)).join(",")})`; c.fillRect(0, 0, L.width, L.height);
    }
    // effects
    let fillColor = null;
    for (const e of L.effects) {
      if (e.match === "ADBE Fill") {
        const col = L.prop(e.params.find((p) => p.match === "ADBE Fill-0002")).valueAt(t);
        const fop = e.params.find((p) => p.match === "ADBE Fill-0005"); fillColor = { col, op: fop ? L.prop(fop).valueAt(t) : 1 };
      } else if (e.match === "ADBE Geometry2") {
        const g = (m) => L.prop(e.params.find((p) => p.match === m)).valueAt(t);
        const a = g("ADBE Geometry2-0001"), p = g("ADBE Geometry2-0002"), sh = g("ADBE Geometry2-0003"), sw = g("ADBE Geometry2-0004");
        const uni = g("ADBE Geometry2-0011"), r = g("ADBE Geometry2-0007"), o = g("ADBE Geometry2-0008");
        const sx = sw / 100, sy = (uni ? sw : sh) / 100;
        M = M.mul(Mat.T(p[0], p[1])).mul(Mat.R(r)).mul(Mat.S(sx, sy)).mul(Mat.T(-a[0], -a[1]));
        opacity *= o / 100;
      }
    }
    if (L.kind === "text") {
      // text renders straight into comp space; Fill recolours via a temp buffer
      if (fillColor) {
        const tmp = this.newCanvas(ctx.canvas.width, ctx.canvas.height), tc = tmp.getContext("2d");
        L.text.draw(tc, t, M, 1); recolor(tmp, fillColor);
        ctx.save(); ctx.globalAlpha = opacity; ctx.drawImage(tmp, 0, 0); ctx.restore();
      } else L.text.draw(ctx, t, M, opacity);
      return;
    }
    if (!buf) return;
    if (fillColor) recolor(buf, fillColor);
    ctx.save(); ctx.setTransform(M.a, M.b, M.c, M.d, M.e, M.f); ctx.globalAlpha = Math.min(1, opacity);
    ctx.imageSmoothingQuality = "high"; ctx.drawImage(buf, 0, 0); ctx.restore();
  }
  async renderFrame(t, target) {
    EPOCH++;
    let cv = this.renderComp(this.root, t, null);
    if (this.mediaWant.size) { await this.loadWanted(); EPOCH++; cv = this.renderComp(this.root, t, null); }
    const ctx = target.getContext("2d"); ctx.clearRect(0, 0, target.width, target.height); ctx.drawImage(cv, 0, 0);
  }
}
function recolor(canvas, { col, op }) {
  const c = canvas.getContext("2d"); c.save(); c.globalCompositeOperation = "source-atop"; c.globalAlpha = op;
  c.fillStyle = `rgb(${col.slice(0, 3).map((x) => Math.round(x * 255)).join(",")})`; c.fillRect(0, 0, canvas.width, canvas.height); c.restore();
}
window.AEPort = { Engine };
})();
