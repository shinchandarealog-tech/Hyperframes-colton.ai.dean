// Touch-first click-to-edit for Hyperframes compositions.
// The preview is the real composition (Hyperframes player + runtime). Edits are
// applied live as the same CSS block the server writes into index.html.
import {
  FRAME,
  FONTS,
  buildCss,
  cleanItems,
  sanitizeHtml,
  isValidSelector,
  editedAabb,
  outsideSafe,
  snapOffset,
} from "/lib/edits.mjs";

const $ = (id) => document.getElementById(id);
const player = $("player");
const stage = $("stage");
const zoomer = $("zoomer");
const overlay = $("overlay");
const frameEl = $("frame");
const selbox = $("selbox");
const badge = $("badge");
const texted = $("texted");
const panel = $("panel");
const statusEl = $("status");

// ---------- state ----------
let items = {}; // selector -> edit item (what is saved)
let originals = {}; // selector -> original inner HTML (for undoing text edits)
let past = [];
let future = [];
let committed = "{}"; // JSON of items at last commit
let sel = null; // { key, el, kind }
let doc = null; // iframe document
let view = { z: 1, tx: 0, ty: 0 };
let safeOn = false;
let editingText = false;
let duration = 0;

try {
  safeOn = localStorage.getItem("hf-editor-safe") === "1";
} catch {}

// ---------- boot ----------
async function boot() {
  injectParentFonts();
  buildPanel();
  layout();
  const r = await fetch("/api/state").then((x) => x.json());
  items = cleanItems(r.items);
  originals = r.originals || {};
  committed = JSON.stringify(items);
  document.title = `${r.project} — Reel Editor`;
  setStatus("Loading preview…");
  player.addEventListener("ready", onPlayerReady);
  if (player.ready) onPlayerReady();
  player.addEventListener("timeupdate", onTime);
  player.addEventListener("play", () => syncPlayButton());
  player.addEventListener("pause", () => syncPlayButton());
  player.addEventListener("durationchange", onDuration);
  setSafe(safeOn);
  requestAnimationFrame(loop);
}

function onPlayerReady() {
  const d = player.iframeElement?.contentDocument;
  if (!d) return setStatus("Preview could not load", "bad");
  doc = d;
  if (!doc.getElementById("hf-edits")) {
    const st = doc.createElement("style");
    st.id = "hf-edits";
    doc.head.appendChild(st);
  }
  // Stop the composition's own click handlers from seeing editor taps.
  doc.documentElement.style.touchAction = "none";
  onDuration();
  applyLive();
  setStatus("All changes saved", "ok");
  layout();
}

function onDuration() {
  duration = Number(player.duration) || duration;
  $("scrub").max = String(duration || 1);
}

// ---------- layout / zoom ----------
function baseFit() {
  const w = stage.clientWidth;
  const h = stage.clientHeight;
  const pad = 12;
  const fw = Math.min(w - pad * 2, ((h - pad * 2) * FRAME.width) / FRAME.height);
  const fh = (fw * FRAME.height) / FRAME.width;
  return { w: fw, h: fh, x: (w - fw) / 2, y: (h - fh) / 2 };
}
function layout() {
  const b = baseFit();
  zoomer.style.width = `${b.w}px`;
  zoomer.style.height = `${b.h}px`;
  zoomer.style.transform = `translate(${b.x + view.tx}px, ${b.y + view.ty}px) scale(${view.z})`;
}
window.addEventListener("resize", () => {
  layout();
  placePanel();
});
$("fit").addEventListener("click", () => {
  view = { z: 1, tx: 0, ty: 0 };
  layout();
});

// Frame rectangle in overlay coordinates, and frame-px -> screen-px factor.
function frameRect() {
  const fr = (player.iframeElement || player).getBoundingClientRect();
  const or = overlay.getBoundingClientRect();
  return { x: fr.left - or.left, y: fr.top - or.top, w: fr.width, h: fr.height, k: fr.width / FRAME.width, ox: or.left, oy: or.top };
}
const toFrame = (clientX, clientY, F = frameRect()) => ({ x: (clientX - F.ox - F.x) / F.k, y: (clientY - F.oy - F.y) / F.k });

// ---------- finding editable things ----------
const INLINE = new Set(["SPAN", "B", "STRONG", "I", "EM", "BR", "SMALL", "U", "MARK", "SUP", "SUB"]);
const SKIP = new Set(["VIDEO", "AUDIO", "HTML", "BODY", "SCRIPT", "STYLE", "TEMPLATE", "IFRAME"]);

function isPureText(el) {
  if (!el.textContent.trim()) return false;
  for (const d of el.querySelectorAll("*")) if (!INLINE.has(d.tagName.toUpperCase())) return false;
  return true;
}
function hasOwnText(el) {
  for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) return true;
  return false;
}
function isBig(el) {
  const r = el.getBoundingClientRect();
  return r.width * r.height > FRAME.width * FRAME.height * 0.8;
}
function compRoot() {
  return doc.querySelector("[data-composition-id]") || doc.body;
}

// From whatever was hit, find the unit to select: a whole caption/title, a sticker, an image.
function unitFrom(hit) {
  if (!hit || !doc) return null;
  const root = compRoot();
  if (!root.contains(hit) || hit === root) return null;
  const svg = hit.closest("svg");
  if (svg) {
    let u = svg;
    let p = svg.parentElement;
    while (p && p !== root && p.children.length === 1 && !p.textContent.trim() && !isBig(p)) {
      u = p;
      p = p.parentElement;
    }
    return { el: u, kind: "graphic" };
  }
  const tag = hit.tagName.toUpperCase();
  if (SKIP.has(tag)) return null;
  if (tag === "IMG" || tag === "CANVAS") return isBig(hit) ? null : { el: hit, kind: "image" };
  if (isPureText(hit)) {
    let u = hit;
    while (u.parentElement && u.parentElement !== root && isPureText(u.parentElement) && !isBig(u.parentElement)) u = u.parentElement;
    if (isBig(u)) return null;
    return { el: u, kind: "text" };
  }
  if (hasOwnText(hit) && !isBig(hit)) return { el: hit, kind: "text" };
  const bg = doc.defaultView.getComputedStyle(hit).backgroundImage;
  if (bg && bg !== "none" && !isBig(hit)) return { el: hit, kind: "image" };
  return null;
}

function isShown(el) {
  const w = doc.defaultView;
  for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
    const cs = w.getComputedStyle(n);
    if (cs.display === "none" || cs.visibility === "hidden" || Number(cs.opacity) < 0.02) return false;
  }
  const r = el.getBoundingClientRect();
  return r.width > 0 && r.height > 0;
}

function keyFor(el) {
  if (el.id && isValidSelector(`#${el.id}`)) return `#${el.id}`;
  const path = [];
  let n = el;
  while (n && n.parentElement) {
    if (n.id && isValidSelector(`#${n.id}`)) break;
    path.unshift(`:nth-child(${[...n.parentElement.children].indexOf(n) + 1})`);
    n = n.parentElement;
  }
  if (!n || !n.id) return null;
  const k = [`#${n.id}`, ...path].join(" > ");
  return isValidSelector(k) ? k : null;
}

function pick(clientX, clientY) {
  if (!doc) return null;
  const p = toFrame(clientX, clientY);
  if (p.x < 0 || p.y < 0 || p.x > FRAME.width || p.y > FRAME.height) return null;
  for (const hit of doc.elementsFromPoint(p.x, p.y)) {
    const u = unitFrom(hit);
    if (!u || !isShown(u.el)) continue;
    const key = keyFor(u.el);
    if (key) return { key, el: u.el, kind: u.kind };
  }
  return null;
}

// Element box with our move/scale/rotate removed, in frame px.
function baseBox(el) {
  const s = el.style;
  const keep = [s.translate, s.rotate, s.scale];
  s.translate = s.rotate = s.scale = "none";
  const r = el.getBoundingClientRect();
  [s.translate, s.rotate, s.scale] = keep;
  return { cx: r.left + r.width / 2, cy: r.top + r.height / 2, w: r.width, h: r.height };
}

// ---------- applying edits ----------
function applyLive() {
  if (!doc) return;
  const st = doc.getElementById("hf-edits");
  if (st) st.textContent = buildCss(items);
  const keys = new Set([...Object.keys(originals), ...Object.keys(items).filter((k) => typeof items[k].html === "string")]);
  for (const k of keys) {
    let el;
    try {
      el = doc.querySelector(k);
    } catch {
      continue;
    }
    if (!el) continue;
    const want = typeof items[k]?.html === "string" ? items[k].html : originals[k];
    if (want !== undefined && el.innerHTML !== want) el.innerHTML = want;
  }
}

function item(key = sel?.key) {
  if (!items[key]) items[key] = {};
  if (sel && key === sel.key && !items[key].kind) items[key].kind = sel.kind;
  return items[key];
}

function commit() {
  items = cleanItems(items);
  const now = JSON.stringify(items);
  if (now === committed) return;
  past.push(committed);
  if (past.length > 200) past.shift();
  future = [];
  committed = now;
  afterChange();
}
function undo() {
  if (!past.length) return;
  finishTextEdit(false);
  future.push(committed);
  committed = past.pop();
  items = JSON.parse(committed);
  afterChange();
}
function redo() {
  if (!future.length) return;
  finishTextEdit(false);
  past.push(committed);
  committed = future.pop();
  items = JSON.parse(committed);
  afterChange();
}
function afterChange() {
  applyLive();
  if (sel && items[sel.key]?.deleted) select(null);
  refreshPanel();
  $("undo").disabled = !past.length;
  $("redo").disabled = !future.length;
  save();
}
$("undo").addEventListener("click", undo);
$("redo").addEventListener("click", redo);

// ---------- saving ----------
let saveTimer = null;
let saving = false;
let pending = false;
function save() {
  setStatus("Saving…");
  clearTimeout(saveTimer);
  saveTimer = setTimeout(flush, 250);
}
async function flush() {
  saveTimer = null;
  if (saving) {
    pending = true;
    return;
  }
  saving = true;
  const body = JSON.stringify({ items: JSON.parse(committed) });
  try {
    const r = await fetch("/api/edits", { method: "POST", headers: { "content-type": "application/json" }, body, keepalive: body.length < 60000 });
    if (!r.ok) throw new Error(await r.text());
    setStatus("All changes saved", "ok");
  } catch (e) {
    setStatus("Not saved — retrying…", "bad");
    pending = true;
    await new Promise((ok) => setTimeout(ok, 2000));
  }
  saving = false;
  if (pending) {
    pending = false;
    flush();
  }
}
function setStatus(t, cls = "") {
  statusEl.textContent = t;
  statusEl.className = `status ${cls}`;
}
window.addEventListener("beforeunload", (e) => {
  if (saving || pending || saveTimer) {
    flush();
  }
});

// ---------- selection ----------
function select(s) {
  if (editingText) finishTextEdit(true);
  sel = s;
  $("hint").hidden = !!s;
  refreshPanel();
  draw();
}

// ---------- playback ----------
function pause() {
  if (!player.paused) player.pause();
}
function syncPlayButton() {
  $("play").textContent = player.paused ? "▶" : "❚❚";
  $("play").setAttribute("aria-label", player.paused ? "Play" : "Pause");
}
$("play").addEventListener("click", () => {
  if (player.paused) {
    finishTextEdit(true);
    player.play();
  } else player.pause();
  setTimeout(syncPlayButton, 50);
});
function fmt(t) {
  const m = Math.floor(t / 60);
  return `${m}:${(t - m * 60).toFixed(1).padStart(4, "0")}`;
}
function onTime() {
  const t = Number(player.currentTime) || 0;
  if (!scrubbing) $("scrub").value = String(t);
  $("time").textContent = fmt(t);
}
let scrubbing = false;
$("scrub").addEventListener("pointerdown", () => {
  scrubbing = true;
  pause();
});
$("scrub").addEventListener("input", () => {
  const t = Number($("scrub").value);
  player.seek(t);
  $("time").textContent = fmt(t);
});
$("scrub").addEventListener("change", () => (scrubbing = false));
window.addEventListener("pointerup", () => (scrubbing = false));

// ---------- safe zone ----------
function setSafe(on) {
  safeOn = on;
  $("safe").setAttribute("aria-pressed", String(on));
  $("safezone").hidden = !on;
  try {
    localStorage.setItem("hf-editor-safe", on ? "1" : "0");
  } catch {}
}
$("safe").addEventListener("click", () => setSafe(!safeOn));

// ---------- drawing (every frame) ----------
let lastOutlines = 0;
function loop(ts) {
  draw(ts);
  requestAnimationFrame(loop);
}
function draw(ts = performance.now()) {
  const F = frameRect();
  Object.assign(frameEl.style, { left: `${F.x}px`, top: `${F.y}px`, width: `${F.w}px`, height: `${F.h}px` });
  if (!doc) return;

  if (sel && (!sel.el.isConnected || !isShown(sel.el))) {
    // Playhead moved past it: hide the box but keep the selection.
    selbox.hidden = true;
    if (!panel.hidden && !editingText) panel.hidden = true;
  } else if (sel) {
    const e = items[sel.key] || {};
    const b = baseBox(sel.el);
    const s = e.scale ?? 1;
    selbox.hidden = editingText;
    Object.assign(selbox.style, {
      left: `${F.x + (b.cx + (e.x || 0)) * F.k}px`,
      top: `${F.y + (b.cy + (e.y || 0)) * F.k}px`,
      // never smaller than a finger, so the corner handles don't pile up
      width: `${Math.max(44, b.w * s * F.k)}px`,
      height: `${Math.max(44, b.h * s * F.k)}px`,
      transform: `translate(-50%, -50%) rotate(${e.rotate || 0}deg)`,
    });
    const bad = outsideSafe(editedAabb(b, e));
    selbox.classList.toggle("bad", bad);
    if (panel.hidden && !editingText) {
      panel.hidden = false;
      placePanel();
    }
  } else selbox.hidden = true;

  // Red outlines on everything outside the safe zone (only while it's on).
  if (safeOn && ts - lastOutlines > 120) {
    lastOutlines = ts;
    drawOutlines();
  } else if (!safeOn && $("outlines").childElementCount) $("outlines").replaceChildren();
}

let unitCache = null;
function allUnits() {
  if (unitCache && unitCache.doc === doc) return unitCache.list;
  const seen = new Set();
  const list = [];
  for (const el of compRoot().querySelectorAll("*")) {
    const u = unitFrom(el);
    if (u && !seen.has(u.el)) {
      seen.add(u.el);
      list.push(u.el);
    }
  }
  unitCache = { doc, list };
  return list;
}
function drawOutlines() {
  const out = [];
  for (const el of allUnits()) {
    if (sel && el === sel.el) continue;
    if (!isShown(el)) continue;
    const r = el.getBoundingClientRect();
    const b = { left: r.left, right: r.right, top: r.top, bottom: r.bottom };
    if (!outsideSafe(b)) continue;
    const d = document.createElement("div");
    d.className = "outline";
    Object.assign(d.style, {
      left: `${(r.left / FRAME.width) * 100}%`,
      top: `${(r.top / FRAME.height) * 100}%`,
      width: `${(r.width / FRAME.width) * 100}%`,
      height: `${(r.height / FRAME.height) * 100}%`,
    });
    out.push(d);
  }
  $("outlines").replaceChildren(...out);
}

function showGuides(lineX, lineY) {
  const gx = $("guide-x");
  const gy = $("guide-y");
  gx.hidden = lineX === null || lineX === undefined;
  gy.hidden = lineY === null || lineY === undefined;
  if (!gx.hidden) gx.style.left = `${(lineX / FRAME.width) * 100}%`;
  if (!gy.hidden) gy.style.top = `${(lineY / FRAME.height) * 100}%`;
}

// ---------- gestures ----------
const pointers = new Map();
let g = null; // current gesture
let lastTap = { t: 0, key: null, x: 0, y: 0 };

function selCentreScreen(F = frameRect()) {
  const e = items[sel.key] || {};
  const b = baseBox(sel.el);
  return { x: F.ox + F.x + (b.cx + (e.x || 0)) * F.k, y: F.oy + F.y + (b.cy + (e.y || 0)) * F.k, b };
}
function insideSel(clientX, clientY) {
  if (!sel || selbox.hidden) return false;
  const F = frameRect();
  const c = selCentreScreen(F);
  const e = items[sel.key] || {};
  const s = (e.scale ?? 1) * F.k;
  const r = (-(e.rotate || 0) * Math.PI) / 180;
  const dx = clientX - c.x;
  const dy = clientY - c.y;
  const lx = dx * Math.cos(r) - dy * Math.sin(r);
  const ly = dx * Math.sin(r) + dy * Math.cos(r);
  const pad = 10;
  return Math.abs(lx) <= Math.max(44, c.b.w * s) / 2 + pad && Math.abs(ly) <= Math.max(44, c.b.h * s) / 2 + pad;
}

overlay.addEventListener("pointerdown", (ev) => {
  if (editingText && texted.contains(ev.target)) return; // typing / placing the caret
  ev.preventDefault();
  overlay.setPointerCapture?.(ev.pointerId);
  pointers.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
  pause();
  if (editingText) finishTextEdit(true);

  if (pointers.size === 2) return startTwoFinger();
  if (pointers.size > 2) return;

  const handle = ev.target.closest?.(".h");
  if (handle && sel) {
    const c = selCentreScreen();
    const e = item();
    g = {
      type: handle.dataset.h === "rot" ? "rotate" : "resize",
      cx: c.x,
      cy: c.y,
      d0: Math.hypot(ev.clientX - c.x, ev.clientY - c.y) || 1,
      a0: Math.atan2(ev.clientY - c.y, ev.clientX - c.x),
      scale0: e.scale ?? 1,
      rot0: e.rotate || 0,
      moved: false,
    };
    return;
  }

  let target = null;
  if (insideSel(ev.clientX, ev.clientY)) target = sel;
  else target = pick(ev.clientX, ev.clientY);

  if (target) {
    if (!sel || target.el !== sel.el) select(target);
    const e = items[target.key] || {};
    g = { type: "move", sx: ev.clientX, sy: ev.clientY, x0: e.x || 0, y0: e.y || 0, base: baseBox(target.el), moved: false };
  } else {
    if (sel) select(null);
    g = { type: "pan", sx: ev.clientX, sy: ev.clientY, tx0: view.tx, ty0: view.ty, moved: false };
  }
});

function startTwoFinger() {
  const [a, b] = [...pointers.values()];
  const d0 = Math.hypot(b.x - a.x, b.y - a.y) || 1;
  const a0 = Math.atan2(b.y - a.y, b.x - a.x);
  const mid = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
  if (sel && !selbox.hidden) {
    const e = item();
    g = { type: "pinch", d0, a0, scale0: e.scale ?? 1, rot0: e.rotate || 0, moved: true };
  } else {
    const or = stage.getBoundingClientRect();
    g = { type: "zoom", d0, mid0: { x: mid.x - or.left, y: mid.y - or.top }, view0: { ...view }, moved: true };
  }
}

overlay.addEventListener("pointermove", (ev) => {
  if (!pointers.has(ev.pointerId)) return;
  pointers.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
  if (!g) return;
  const F = frameRect();

  if (g.type === "move") {
    const dxs = ev.clientX - g.sx;
    const dys = ev.clientY - g.sy;
    if (!g.moved && Math.hypot(dxs, dys) < 6) return;
    g.moved = true;
    const e = item();
    e.x = g.x0 + dxs / F.k;
    e.y = g.y0 + dys / F.k;
    const snap = snapOffset(editedAabb(g.base, e), 10 / F.k);
    e.x += snap.dx;
    e.y += snap.dy;
    showGuides(snap.lineX, snap.lineY);
    badge.hidden = true;
    applyLive();
  } else if (g.type === "resize") {
    const d = Math.hypot(ev.clientX - g.cx, ev.clientY - g.cy);
    g.moved = true;
    item().scale = Math.max(0.05, g.scale0 * (d / g.d0));
    showBadge(`${Math.round(item().scale * 100)}%`);
    applyLive();
  } else if (g.type === "rotate") {
    g.moved = true;
    let deg = g.rot0 + ((Math.atan2(ev.clientY - g.cy, ev.clientX - g.cx) - g.a0) * 180) / Math.PI;
    deg = snapAngle(deg);
    item().rotate = deg;
    showBadge(`${Math.round(deg)}°`);
    applyLive();
  } else if (g.type === "pinch" && pointers.size >= 2) {
    const [a, b] = [...pointers.values()];
    const d = Math.hypot(b.x - a.x, b.y - a.y);
    const ang = Math.atan2(b.y - a.y, b.x - a.x);
    const e = item();
    e.scale = Math.max(0.05, g.scale0 * (d / g.d0));
    e.rotate = snapAngle(g.rot0 + ((ang - g.a0) * 180) / Math.PI);
    showBadge(`${Math.round(e.scale * 100)}% · ${Math.round(e.rotate)}°`);
    applyLive();
  } else if (g.type === "zoom" && pointers.size >= 2) {
    const [a, b] = [...pointers.values()];
    const d = Math.hypot(b.x - a.x, b.y - a.y);
    const z = Math.min(6, Math.max(1, g.view0.z * (d / g.d0)));
    const base = baseFit();
    // keep the point under the fingers still
    const px = (g.mid0.x - base.x - g.view0.tx) / g.view0.z;
    const py = (g.mid0.y - base.y - g.view0.ty) / g.view0.z;
    view = { z, tx: g.mid0.x - base.x - px * z, ty: g.mid0.y - base.y - py * z };
    if (z === 1) view.tx = view.ty = 0;
    layout();
  } else if (g.type === "pan") {
    const dx = ev.clientX - g.sx;
    const dy = ev.clientY - g.sy;
    if (!g.moved && Math.hypot(dx, dy) < 6) return;
    g.moved = true;
    if (view.z > 1) {
      view.tx = g.tx0 + dx;
      view.ty = g.ty0 + dy;
      layout();
    }
  }
});

function snapAngle(deg) {
  const near = Math.round(deg / 45) * 45;
  return Math.abs(deg - near) < 4 ? near : deg;
}
function showBadge(t) {
  badge.textContent = t;
  badge.hidden = false;
}

function endPointer(ev) {
  if (!pointers.has(ev.pointerId)) return;
  pointers.delete(ev.pointerId);
  if (!g) return;
  if (pointers.size === 1 && (g.type === "pinch" || g.type === "zoom")) {
    // one finger lifted: end the pinch, keep the gesture closed until all fingers are up
    if (g.type === "pinch") commit();
    g = { type: "none", moved: true };
    hideFeedback();
    return;
  }
  if (pointers.size > 0) return;
  const was = g;
  g = null;
  hideFeedback();
  if (was.moved) {
    if (was.type !== "pan" && was.type !== "zoom" && was.type !== "none") commit();
    return;
  }
  // A tap. Double-tap on selected text -> edit the words in place.
  const now = performance.now();
  if (sel && was.type === "move") {
    const dbl = lastTap.key === sel.key && now - lastTap.t < 400 && Math.hypot(ev.clientX - lastTap.x, ev.clientY - lastTap.y) < 30;
    if (dbl && sel.kind === "text") {
      lastTap = { t: 0, key: null };
      startTextEdit();
      return;
    }
    lastTap = { t: now, key: sel.key, x: ev.clientX, y: ev.clientY };
  }
}
function hideFeedback() {
  showGuides(null, null);
  badge.hidden = true;
}
overlay.addEventListener("pointerup", endPointer);
overlay.addEventListener("pointercancel", endPointer);
document.addEventListener("gesturestart", (e) => e.preventDefault());
document.addEventListener("dblclick", (e) => e.preventDefault());

// ---------- in-place text editing ----------
function startTextEdit() {
  if (!sel || sel.kind !== "text") return;
  pause();
  const F = frameRect();
  const e = items[sel.key] || {};
  const b = baseBox(sel.el);
  const cs = doc.defaultView.getComputedStyle(sel.el);
  const props = [
    "fontFamily", "fontSize", "fontWeight", "fontStyle", "lineHeight", "letterSpacing", "textAlign", "textTransform",
    "color", "textShadow", "webkitTextStroke", "paintOrder", "whiteSpace", "wordSpacing", "paddingTop", "paddingRight",
    "paddingBottom", "paddingLeft",
  ];
  texted.removeAttribute("style");
  for (const p of props) texted.style[p] = cs[p];
  const s = (e.scale ?? 1) * F.k;
  Object.assign(texted.style, {
    left: `${F.x + (b.cx + (e.x || 0)) * F.k}px`,
    top: `${F.y + (b.cy + (e.y || 0)) * F.k}px`,
    width: `${b.w}px`,
    minHeight: `${b.h}px`,
    transformOrigin: "0 0",
    transform: `rotate(${e.rotate || 0}deg) scale(${s}) translate(-50%, -50%)`,
  });
  texted.innerHTML = sel.el.innerHTML;
  texted.hidden = false;
  selbox.hidden = true;
  editingText = true;
  sel.el.style.visibility = "hidden";
  texted.focus();
  const range = document.createRange();
  range.selectNodeContents(texted);
  const s2 = getSelection();
  s2.removeAllRanges();
  s2.addRange(range);
  $("p-done").textContent = "Done typing";
}

// Turn what the user typed into the small set of tags we keep.
function normalise(node) {
  let out = "";
  node.childNodes.forEach((n, i) => {
    if (n.nodeType === 3) out += n.textContent.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    else if (n.nodeType === 1) {
      const t = n.tagName.toLowerCase();
      if (t === "br") out += "<br>";
      else if (t === "div" || t === "p") out += (i > 0 && !out.endsWith("<br>") ? "<br>" : "") + normalise(n);
      else if (["span", "b", "strong", "i", "em"].includes(t)) {
        const cls = t === "span" && n.getAttribute("class") ? ` class="${n.getAttribute("class").replace(/[^\w -]/g, "")}"` : "";
        out += `<${t}${cls}>${normalise(n)}</${t}>`;
      } else out += normalise(n);
    }
  });
  return out;
}

function finishTextEdit(keep) {
  if (!editingText) return;
  editingText = false;
  texted.hidden = true;
  $("p-done").textContent = "Done";
  if (sel) sel.el.style.visibility = "";
  if (keep && sel) {
    let html = sanitizeHtml(normalise(texted).replace(/(<br>)+$/, ""));
    if (html !== sel.el.innerHTML && texted.textContent.trim()) {
      if (!(sel.key in originals) && items[sel.key]?.html === undefined) originals[sel.key] = sel.el.innerHTML;
      item().html = html;
      applyLive();
      commit();
    }
  }
  texted.blur();
}
texted.addEventListener("keydown", (e) => {
  if (e.key === "Escape") finishTextEdit(false);
  if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) finishTextEdit(true);
  e.stopPropagation();
});

// ---------- style panel ----------
const SWATCHES = ["#ffffff", "#000000", "#f7f2b8", "#ffd60a", "#ff3b30", "#34c759", "#0a84ff"];
function buildPanel() {
  const f = $("p-font");
  f.append(new Option("(original font)", ""));
  for (const name of Object.keys(FONTS)) f.append(new Option(name, name));
  const sw = $("p-swatches");
  for (const c of SWATCHES) {
    const b = document.createElement("button");
    b.className = "swatch";
    b.style.background = c;
    b.dataset.c = c;
    b.setAttribute("aria-label", `Colour ${c}`);
    b.addEventListener("click", () => setProp({ color: c }, true));
    sw.append(b);
  }
  f.addEventListener("change", () => {
    const v = f.value;
    const e = item();
    if (v) e.fontFamily = v;
    else delete e.fontFamily;
    applyLive();
    commit();
  });
  $("p-color").addEventListener("input", (ev) => setProp({ color: ev.target.value }, false));
  $("p-color").addEventListener("change", () => commit());

  const size = $("p-size");
  size.addEventListener("input", () => setSize(Number(size.value), false));
  size.addEventListener("change", () => commit());
  $("p-size-minus").addEventListener("click", () => setSize(Number(size.value) - (sel.kind === "text" ? 2 : 5), true));
  $("p-size-plus").addEventListener("click", () => setSize(Number(size.value) + (sel.kind === "text" ? 2 : 5), true));

  for (const [id, prop] of [["p-bold", "bold"], ["p-outline", "outline"], ["p-shadow", "shadow"]]) {
    $(id).addEventListener("click", () => setProp({ [prop]: $(id).getAttribute("aria-pressed") !== "true" }, true));
  }
  const op = $("p-opacity");
  op.addEventListener("input", () => setProp({ opacity: Number(op.value) / 100 }, false));
  op.addEventListener("change", () => commit());

  $("p-edit").addEventListener("click", () => startTextEdit());
  $("p-delete").addEventListener("click", () => {
    if (!sel) return;
    item().deleted = true;
    applyLive();
    commit();
    select(null);
  });
  $("p-reset").addEventListener("click", () => {
    if (!sel) return;
    const e = items[sel.key];
    if (!e) return;
    // Keep text changes; reset position/size/style.
    items[sel.key] = e.html !== undefined ? { kind: e.kind, html: e.html } : {};
    applyLive();
    commit();
  });
  $("p-done").addEventListener("click", () => {
    if (editingText) finishTextEdit(true);
    else select(null);
  });
  // Panel taps must not reach the preview.
  panel.addEventListener("pointerdown", (e) => e.stopPropagation());
}

function setProp(p, doCommit) {
  if (!sel) return;
  Object.assign(item(), p);
  applyLive();
  if (doCommit) commit();
  refreshPanel();
}
function setSize(v, doCommit) {
  if (!sel) return;
  if (sel.kind === "text") {
    item().fontSize = Math.max(10, Math.min(300, v));
  } else {
    item().scale = Math.max(0.05, v / 100);
  }
  applyLive();
  if (doCommit) commit();
  refreshPanel();
}

function refreshPanel() {
  if (!sel || !doc) {
    panel.hidden = true;
    return;
  }
  const e = items[sel.key] || {};
  const cs = doc.defaultView.getComputedStyle(sel.el);
  const isText = sel.kind === "text";
  panel.classList.toggle("graphic", !isText);
  $("p-font").value = e.fontFamily || "";
  if (isText) {
    const fs = e.fontSize ?? parseFloat(cs.fontSize);
    $("p-size").min = "10";
    $("p-size").max = "200";
    $("p-size").value = String(Math.round(fs));
    $("p-size-val").textContent = `${Math.round(fs)}px`;
    $("p-size-lab").textContent = "Size";
  } else {
    const sc = Math.round((e.scale ?? 1) * 100);
    $("p-size").min = "10";
    $("p-size").max = "400";
    $("p-size").value = String(sc);
    $("p-size-val").textContent = `${sc}%`;
    $("p-size-lab").textContent = "Size";
  }
  const color = e.color || rgbToHex(isText ? cs.color : graphicColour(sel.el));
  $("p-color").value = color || "#ffffff";
  $("p-swatches").querySelectorAll(".swatch").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.c === color)));
  $("p-swatches").parentElement.hidden = sel.kind === "image";
  const bold = e.bold ?? Number(cs.fontWeight) >= 600;
  const outline = e.outline ?? (isText ? parseFloat(cs.webkitTextStrokeWidth || "0") > 0 : false);
  const shadow = e.shadow ?? (isText ? cs.textShadow !== "none" : false);
  $("p-bold").setAttribute("aria-pressed", String(bold));
  $("p-outline").setAttribute("aria-pressed", String(outline));
  $("p-shadow").setAttribute("aria-pressed", String(shadow));
  const op = Math.round((e.opacity ?? 1) * 100);
  $("p-opacity").value = String(op);
  $("p-opacity-val").textContent = `${op}%`;
  if (!panel.hidden || !selbox.hidden) {
    panel.hidden = false;
    placePanel();
  }
}

function graphicColour(el) {
  const shape = el.querySelector?.("path, circle, rect, polygon, ellipse") || el;
  return doc.defaultView.getComputedStyle(shape).fill;
}
function rgbToHex(c) {
  const m = String(c || "").match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!m) return /^#[0-9a-f]{6}$/i.test(c) ? c.toLowerCase() : null;
  return "#" + [m[1], m[2], m[3]].map((n) => Number(n).toString(16).padStart(2, "0")).join("");
}

// Phones: the panel docks under the preview (the preview shrinks, nothing is covered).
// Tablets: it floats above or below the selection, never on top of it; if there
// is no room it docks too.
function setDocked(on) {
  if (document.body.classList.contains("docked") === on) return;
  document.body.classList.toggle("docked", on);
  layout();
}
function placePanel() {
  if (editingText) return;
  if (panel.hidden) {
    if (!g) setDocked(false);
    return;
  }
  const vw = window.innerWidth;
  if (vw < 600 || selbox.hidden) {
    if (!g) setDocked(true);
    return;
  }
  const pw = panel.offsetWidth;
  const ph = panel.offsetHeight;
  const r = selbox.getBoundingClientRect();
  const sr = stage.getBoundingClientRect();
  const gap = 56; // leaves room for the rotate handle
  const roomAbove = r.top - gap - sr.top;
  const roomBelow = sr.bottom - (r.bottom + 24);
  let top = null;
  if (roomBelow >= ph) top = r.bottom + 24;
  else if (roomAbove >= ph) top = r.top - gap - ph;
  if (top === null) {
    if (!g) setDocked(true);
    return;
  }
  if (document.body.classList.contains("docked")) {
    if (g) return;
    setDocked(false);
    return; // layout changed; the next tick places it
  }
  const left = Math.min(vw - pw - 8, Math.max(8, r.left + r.width / 2 - pw / 2));
  panel.style.left = `${left}px`;
  panel.style.top = `${top}px`;
}
setInterval(() => {
  if (!g) placePanel();
}, 300);
new ResizeObserver(() => layout()).observe(stage);

// ---------- fonts in the editor page (for the in-place text box) ----------
function injectParentFonts() {
  const all = {};
  for (const name of Object.keys(FONTS)) all[`#x-${name.replace(/\W/g, "")}`] = { fontFamily: name };
  const css = buildCss(all, "/project/assets/fonts/").split("\n").filter((l) => l.startsWith("@font-face")).join("\n");
  const st = document.createElement("style");
  st.textContent = css;
  document.head.append(st);
}

// ---------- keyboard (bonus) ----------
document.addEventListener("keydown", (e) => {
  if (editingText || e.target.tagName === "INPUT" || e.target.tagName === "SELECT") return;
  const mod = e.metaKey || e.ctrlKey;
  if (mod && e.key.toLowerCase() === "z") {
    e.preventDefault();
    e.shiftKey ? redo() : undo();
  } else if (mod && e.key.toLowerCase() === "y") {
    e.preventDefault();
    redo();
  } else if ((e.key === "Delete" || e.key === "Backspace") && sel) {
    e.preventDefault();
    $("p-delete").click();
  } else if (e.key === "Escape") select(null);
  else if (e.key === "Enter" && sel?.kind === "text") {
    e.preventDefault();
    startTextEdit();
  } else if (e.key === " ") {
    e.preventDefault();
    $("play").click();
  } else if (sel && e.key.startsWith("Arrow")) {
    e.preventDefault();
    pause();
    const step = e.shiftKey ? 10 : 1;
    const it = item();
    if (e.key === "ArrowLeft") it.x = (it.x || 0) - step;
    if (e.key === "ArrowRight") it.x = (it.x || 0) + step;
    if (e.key === "ArrowUp") it.y = (it.y || 0) - step;
    if (e.key === "ArrowDown") it.y = (it.y || 0) + step;
    applyLive();
    clearTimeout(nudgeTimer);
    nudgeTimer = setTimeout(commit, 400);
  }
});
let nudgeTimer = null;

boot().catch((e) => setStatus(`Error: ${e.message}`, "bad"));

// For automated tests.
window.__editor = {
  get items() {
    return items;
  },
  get selected() {
    return sel?.key ?? null;
  },
  get canUndo() {
    return past.length > 0;
  },
  get canRedo() {
    return future.length > 0;
  },
  frameRect,
  flushNow: () => {
    clearTimeout(saveTimer);
    return flush();
  },
};
