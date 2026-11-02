// Generates index.html (full, 74.27s) and compositions/short.html (42.57s) from ONE cue list.
// Cue times are in FULL-master time (assets/full.mp4); the short version remaps them via RANGES.
// Run: node scripts/build.mjs
import { writeFileSync, mkdirSync, copyFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const FPS = 30;
const snap = (t) => Math.round(t * FPS) / FPS;

// ───────────────────────── icons (flat SVG, palette-only) ─────────────────────────
const G1 = "#8BD94A", G2 = "#3FAE3A", G3 = "#2C8A2A", Y1 = "#FFE07A", Y2 = "#FFC93C", P1 = "#E8336E", P2 = "#6B3FB8", INK = "#16240F";
const ICON = {
  earth: `<svg viewBox="0 0 200 200"><defs><radialGradient id="eg" cx="35%" cy="30%"><stop offset="0" stop-color="${G1}"/><stop offset="1" stop-color="${G3}"/></radialGradient></defs><circle cx="100" cy="100" r="92" fill="url(#eg)" stroke="#fff" stroke-width="8"/><path d="M48 70c18-14 40-10 46 4 5 12-10 18-4 30 6 13-8 26-24 22-14-4-30-22-26-38 1-7 3-13 8-18zM118 40c18 2 34 14 40 30-10 6-24 2-30 10-6 7 4 20-6 26-12 6-22-8-20-22 2-16-4-24 2-34 3-6 8-10 14-10zM112 132c14-4 30 2 36 12-8 16-26 26-40 26-6-12-6-32 4-38z" fill="${Y1}" opacity=".9"/></svg>`,
  sprout: `<svg viewBox="0 0 200 220"><path d="M100 210V110" stroke="${G3}" stroke-width="12" stroke-linecap="round"/><path d="M100 120C60 120 28 92 24 46c46-2 76 26 76 74z" fill="${G2}" stroke="#fff" stroke-width="6"/><path d="M100 104c4-44 34-72 80-70-4 46-36 72-80 70z" fill="${G1}" stroke="#fff" stroke-width="6"/><ellipse cx="100" cy="210" rx="60" ry="10" fill="${INK}" opacity=".35"/></svg>`,
  bin: `<svg viewBox="0 0 200 230"><rect x="40" y="60" width="120" height="160" rx="18" fill="${G2}" stroke="#fff" stroke-width="7"/><rect x="28" y="36" width="144" height="30" rx="12" fill="${Y2}" stroke="#fff" stroke-width="7"/><rect x="82" y="18" width="36" height="22" rx="8" fill="${Y2}" stroke="#fff" stroke-width="6"/><path d="M78 100v90M100 100v90M122 100v90" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".9"/></svg>`,
  heartleaf: `<svg viewBox="0 0 200 190"><path d="M100 178C40 134 10 100 10 62 10 30 34 10 62 10c18 0 30 10 38 22 8-12 20-22 38-22 28 0 52 20 52 52 0 38-30 72-90 116z" fill="${G2}" stroke="#fff" stroke-width="8"/><path d="M100 160V48M100 92l-28-22M100 118l30-24" stroke="${G1}" stroke-width="8" stroke-linecap="round"/></svg>`,
  recycle: `<svg viewBox="0 0 200 200"><g fill="${G2}" stroke="#fff" stroke-width="6" stroke-linejoin="round"><path d="M100 18l34 58h-22l-12-20-26 44-30-18z"/><path d="M168 132l-34 58-12-20h24l-26-44 30-16z" transform="rotate(4 100 100)"/><path d="M32 132l34 58 10-20H52l26-44-30-16z" transform="rotate(-4 100 100)"/></g></svg>`,
  brush: `<svg viewBox="0 0 200 200"><rect x="92" y="10" width="22" height="110" rx="10" fill="${Y2}" stroke="#fff" stroke-width="6" transform="rotate(30 100 100)"/><path d="M58 128c14-10 34-6 40 8 6 16-6 38-40 52-6-22-16-48 0-60z" fill="${G2}" stroke="#fff" stroke-width="6"/></svg>`,
  bottlePlain: `<svg viewBox="0 0 240 300"><rect x="6" y="6" width="228" height="288" rx="26" fill="#fff"/><path d="M104 40h32v26c18 10 26 24 26 44v140c0 14-10 24-24 24h-36c-14 0-24-10-24-24V110c0-20 8-34 26-44z" fill="#E9EEF0" stroke="#9AA6AC" stroke-width="5"/><rect x="100" y="28" width="40" height="18" rx="5" fill="#9AA6AC"/><path d="M60 70l120 170M180 70L60 240" stroke="${P1}" stroke-width="16" stroke-linecap="round"/></svg>`,
  bottlePainted: `<svg viewBox="0 0 240 300"><rect x="6" y="6" width="228" height="288" rx="26" fill="#fff"/><path d="M104 40h32v26c18 10 26 24 26 44v140c0 14-10 24-24 24h-36c-14 0-24-10-24-24V110c0-20 8-34 26-44z" fill="${G2}" stroke="${G3}" stroke-width="5"/><path d="M80 120h80M80 150h80M80 180h80M80 210h80M80 240h80" stroke="${Y2}" stroke-width="12"/><path d="M118 70c-10-20 4-34 20-36-2 16-8 28-20 36z" fill="${G1}"/><rect x="100" y="28" width="40" height="18" rx="5" fill="${G3}"/><circle cx="196" cy="252" r="30" fill="${G2}" stroke="#fff" stroke-width="5"/><path d="M182 252l10 10 18-20" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  leaf: `<svg viewBox="0 0 60 60"><path d="M6 54C6 24 26 6 54 6c0 30-18 48-48 48z" fill="currentColor"/><path d="M8 52L40 20" stroke="#fff" stroke-width="3" opacity=".7"/></svg>`,
  check: `<svg viewBox="0 0 40 40"><path d="M9 21l7 7 15-16" stroke="${INK}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
};

// ───────────────────────── element builders ─────────────────────────
const els = []; // {id, html, layer: 'behind'|'front'}
const cues = []; // {id, type, t, out, ...}
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
const chars = (text) => [...text].map((c) => (c === " " ? `<span class="sp"> </span>` : `<span class="ch">${esc(c)}</span>`)).join("");

function kw(id, text, { y, size = 160, style = "green", layer = "front", anim = "drop", t, out, x = 540, max = 1000 }) {
  els.push({ id, layer, html: `<div id="${id}" class="kw ${style}" style="top:${y - size * 0.62}px;left:${x}px;font-size:${size}px;max-width:${max}px">${chars(text)}</div>` });
  cues.push({ id, type: "kw", anim, t, out });
}
function cn(id, words, times, { y, size = 52, layer = "front", out, x = 540 }) {
  els.push({ id, layer, html: `<div id="${id}" class="cn" style="top:${y - size * 0.62}px;left:${x}px;font-size:${size}px">${words.map((w) => `<span class="w">${esc(w)}</span>`).join(" ")}</div>` });
  cues.push({ id, type: "cn", times, t: times[0], out });
}
function obj(id, icon, { x, y, w, rot = 0, t, out, anim = "pop", layer = "front" }) {
  els.push({ id, layer, html: `<div id="${id}" class="obj" style="left:${x - w / 2}px;top:${y - w / 2}px;width:${w}px;--r:${rot}deg">${ICON[icon]}</div>` });
  cues.push({ id, type: "obj", anim, t, out, rot });
}
function pill(id, text, { x = 540, y, dot = G1, t, out, size = 46 }) {
  els.push({ id, layer: "front", html: `<div id="${id}" class="pill" style="left:${x}px;top:${y}px;font-size:${size}px"><i style="background:${dot}"></i>${esc(text)}</div>` });
  cues.push({ id, type: "obj", anim: "pill", t, out, rot: 0 });
}
function badge(id, n, { t, out }) {
  els.push({ id, layer: "front", html: `<div id="${id}" class="badge"><span class="bl">${ICON.leaf}</span>TARIKA <b>${n}</b>/3</div>` });
  cues.push({ id, type: "obj", anim: "badge", t, out, rot: 0 });
}
function html(id, inner, cls, style, cue) {
  els.push({ id, layer: cue.layer || "front", html: `<div id="${id}" class="${cls}" style="${style}">${inner}</div>` });
  cues.push({ id, ...cue });
}

// ───────────────────────── THE PLAN (full-master time) ─────────────────────────
// Shot map (full): T1 0–8.1667 | kids 8.1667–12.1 | T2 12.1–20.2667 | Tip1 planting 20.2667–28.6333 |
// Tip2 dustbin 28.6333–37.6 | Tip3 bottle 37.6–45.1333 | artists 45.1333–61.2333 | T3 CTA 61.2333–74.2667
const END_FULL = 2228 / FPS;
const FLASHES = [8.1667, 12.1, 20.2667, 28.6333, 37.6, 45.1333, 61.2333];
const TEACHERS = [
  { id: "t1", start: 0, end: 8.1667, matte: "assets/matte-t1.webm", matteStart: 0, scale: [1.32, 1.37], origin: "50% 0%" },
  { id: "t2", start: 12.1, end: 20.2667, matte: "assets/matte-t2.webm", matteStart: 12.1, scale: [1.32, 1.37], origin: "50% 15%" },
  { id: "t3", start: 61.2333, end: END_FULL, matte: "assets/matte-t3.webm", matteStart: 61.2, scale: [1.12, 1.17], origin: "50% 38%" },
];

// Beat 1 · T1 hook — keyword behind head on frame 1 (ref A @0.0), Teen cheezein, GREEN behind head
kw("b1-dharti", "Dharti", { y: 300, size: 230, style: "green", layer: "behind", anim: "slideL", t: 0, out: 1.55 });
obj("b1-earth", "earth", { x: 880, y: 620, w: 190, rot: -8, t: 0.3, out: 1.55 });
cn("b1-c1", ["ko", "agar", "bachana", "hai"], [0.49, 0.63, 0.91, 1.4], { y: 640, out: 1.55 });
cn("b1-c2", ["to", "bachchon", "ko"], [1.61, 1.75, 2.04], { y: 640, out: 3.85 });
kw("b1-teen", "Teen Cheezein", { y: 1080, size: 140, style: "yellow", anim: "drop", t: 2.47, out: 3.85 });
cn("b1-c3", ["sikhana", "hai"], [3.01, 3.5], { y: 1230, out: 3.85 });
cn("b1-c4", ["chhoti", "chhoti", "aadaton", "se", "hi"], [3.92, 4.25, 4.7, 5.15, 5.4], { y: 640, out: 5.66 });
cn("b1-c5", ["future", "ko"], [5.69, 6.0], { y: 640, out: 6.65 });
kw("b1-green", "GREEN", { y: 300, size: 290, style: "green", layer: "behind", anim: "drop", t: 6.27, out: 8.1667 });
obj("b1-sprout", "sprout", { x: 175, y: 640, w: 200, rot: -6, t: 6.35, out: 8.1667, anim: "grow" });
cn("b1-c6", ["banana", "hai"], [6.69, 7.05], { y: 640, out: 8.1667 });

// Beat 2 · kids shout — giant stacked words + leaf burst (ref B "Haan!" @3.3)
kw("b2-happy", "Happy", { y: 200, size: 150, style: "yellow", anim: "pop", t: 8.27, out: 12.1 });
kw("b2-env", "Environment", { y: 395, size: 150, style: "green", anim: "drop", t: 8.6, out: 12.1, max: 1060 });
kw("b2-day", "Day!", { y: 600, size: 180, style: "brand", anim: "pop", t: 9.4, out: 12.1 });
cues.push({ id: "b2-burst", type: "burst", t: 9.42, out: 10.8 });

// Beat 3 · T2 brand + "3" counter (ref A logo @9.0 + counter @18.0)
cn("b3-c1", ["Aaj"], [12.15], { y: 860, out: 13.5 });
kw("b3-brand1", "Rhyming Kid's", { y: 360, size: 150, style: "brand", layer: "behind", anim: "drop", t: 12.41, out: 15.05 });
kw("b3-brand2", "Corner", { y: 720, size: 150, style: "brand", layer: "front", anim: "slideR", t: 12.95, out: 15.05 });
cn("b3-c2", ["par", "hum", "sikhayenge"], [13.54, 13.76, 14.04], { y: 860, out: 15.05 });
html("b3-counter", `<svg viewBox="0 0 300 300"><circle cx="150" cy="150" r="128" fill="rgba(22,36,15,.82)" stroke="rgba(255,255,255,.18)" stroke-width="16"/><circle class="ring" cx="150" cy="150" r="128" fill="none" stroke="${Y2}" stroke-width="16" stroke-linecap="round" transform="rotate(-90 150 150)" stroke-dasharray="804.25" stroke-dashoffset="804.25"/></svg><span class="num">0</span>`,
  "counter", "left:390px;top:880px;width:300px;height:300px", { type: "counter", t: 15.12, out: 20.2667, to: 3 });
kw("b3-tarike", "Simple Tarike", { y: 1290, size: 120, style: "white", anim: "drop", t: 15.41, out: 20.2667 });
cn("b3-c3", ["apne", "bachchon", "ko"], [16.29, 16.63, 17.04], { y: 1420, out: 17.88 });
pill("b3-nature", "Nature Friendly", { y: 1390, dot: G1, t: 17.92, out: 20.2667, size: 50 });
cn("b3-c4", ["banane", "ke"], [18.92, 19.2], { y: 1530, out: 20.2667 });

// Beat 4 · Tip 1 planting (one benefit = one shot, ref B @9.6)
badge("b4-badge", 1, { t: 20.35, out: 28.6333 });
cn("b4-c1", ["Bachche", "seekh", "rahe"], [20.3, 20.63, 20.85], { y: 1180, out: 22.4 });
kw("b4-podha", "Podha Lagana", { y: 1330, size: 130, style: "yellow", anim: "drop", t: 20.99, out: 22.4 });
cn("b4-c2", ["aur", "usko"], [22.48, 22.65], { y: 1180, out: 23.85 });
kw("b4-naam", "Naam Dena", { y: 1330, size: 140, style: "white", anim: "slideL", t: 23.08, out: 23.85 });
html("b4-tag", `<span>Mr. Green</span>`, "nametag", "left:640px;top:1440px", { type: "obj", anim: "pop", t: 23.2, out: 23.85, rot: -8 });
cn("b4-c3", ["Jaise", "podha", "badhta", "hai"], [23.91, 24.21, 24.63, 25.0], { y: 1330, out: 25.55 });
obj("b4-sprout", "sprout", { x: 540, y: 1130, w: 180, t: 24.21, out: 25.55, anim: "grow" });
cn("b4-c4", ["bachchon", "ka", "nature", "ke", "saath"], [25.6, 25.74, 26.37, 26.81, 26.93], { y: 1180, out: 28.6333 });
kw("b4-bond", "Bond", { y: 1340, size: 170, style: "green", anim: "pop", t: 27.21, out: 28.6333 });
obj("b4-heart", "heartleaf", { x: 830, y: 1290, w: 150, rot: 10, t: 27.25, out: 28.6333 });
cn("b4-c5", ["bhi", "badhta", "hai"], [27.48, 27.77, 28.02], { y: 1470, out: 28.6333 });

// Beat 5 · Tip 2 dustbin (3D-object drop like ref B map pin @9.8)
badge("b5-badge", 2, { t: 28.7, out: 37.6 });
cn("b5-c1", ["Apne", "aas", "paas", "ka"], [28.71, 28.82, 29.01, 29.2], { y: 330, out: 29.98 });
kw("b5-kachra", "Kachra", { y: 480, size: 160, style: "white", anim: "slideR", t: 29.36, out: 29.98 });
kw("b5-dustbin", "Dustbin", { y: 480, size: 170, style: "green", anim: "drop", t: 30.0, out: 32.25 });
obj("b5-bin", "bin", { x: 880, y: 300, w: 170, rot: 8, t: 30.02, out: 32.25, anim: "dropBounce" });
cn("b5-c2", ["mein", "daalna", "seekh", "rahe", "hain"], [30.72, 30.92, 31.42, 31.6, 31.8], { y: 640, out: 32.25 });
cn("b5-c3", ["Jab", "bachche", "bachpan", "se"], [32.32, 32.45, 32.89, 33.14], { y: 290, out: 35.05 });
cn("b5-c4", ["safai", "ki"], [33.45, 33.81], { y: 375, out: 35.05 });
kw("b5-zimm", "Zimmedari", { y: 530, size: 150, style: "yellow", anim: "drop", t: 33.95, out: 35.05 });
cn("b5-c5", ["tabhi", "to", "desh"], [35.12, 35.41, 35.49], { y: 330, out: 37.6 });
kw("b5-swachh", "Swachh", { y: 480, size: 140, style: "white", anim: "slideL", t: 35.82, out: 36.3 });
kw("b5-hara", "Hara-Bhara", { y: 480, size: 150, style: "green", anim: "drop", t: 36.33, out: 37.6 });
cues.push({ id: "b5-sweep", type: "sweep", t: 36.33, out: 37.2 });

// Beat 6 · Tip 3 bottle → canvas (tilted cards like ref B @18.0, before/after flip)
badge("b6-badge", 3, { t: 37.66, out: 45.1333 });
cn("b6-c1", ["Aapke", "ghar", "mein", "jo"], [37.66, 37.78, 37.96, 38.26], { y: 1220, out: 40.25 });
kw("b6-plastic", "Plastic Bottle", { y: 1370, size: 120, style: "white", anim: "drop", t: 38.42, out: 40.25 });
html("b6-card", `<div class="face front">${ICON.bottlePlain}</div><div class="face back">${ICON.bottlePainted}</div>`, "card3d", "left:760px;top:600px;width:240px;height:300px", { type: "card", t: 38.5, flip: 44.13, out: 45.1333, rot: 8 });
pill("b6-kachra", "Kachra?", { x: 540, y: 1480, dot: P1, t: 39.2, out: 40.25 });
cn("b6-c2", ["hamare"], [40.32], { y: 1220, out: 43.05 });
kw("b6-brand", "Rhyming Kid's Corner", { y: 1360, size: 96, style: "brand", anim: "slideL", t: 40.61, out: 43.05, max: 1040 });
cn("b6-c3", ["ke", "bachchon", "ke", "liye"], [41.78, 41.95, 42.46, 42.67], { y: 1480, out: 43.05 });
cn("b6-c4", ["woh", "ek", "sundar", "sa"], [43.12, 43.41, 43.6, 43.9], { y: 1220, out: 45.1333 });
kw("b6-canvas", "Canvas", { y: 1380, size: 190, style: "yellow", anim: "drop", t: 44.13, out: 45.1333 });

// Beat 7 · artists → vases/pen stands → recycling (+ 1/2/3 ticks callback)
cn("b7-c1", ["Is"], [45.32], { y: 1180, out: 47.65 });
kw("b7-world", "World Environment Day", { y: 1330, size: 100, style: "green", anim: "drop", t: 45.37, out: 47.65, max: 1040 });
obj("b7-earth", "earth", { x: 540, y: 1000, w: 150, t: 45.5, out: 47.65 });
cn("b7-c2", ["hamare", "chhote", "chhote"], [47.72, 48.18, 48.55], { y: 1180, out: 49.85 });
kw("b7-artists", "Artists", { y: 1340, size: 190, style: "yellow", anim: "drop", t: 48.98, out: 49.85 });
obj("b7-brush", "brush", { x: 900, y: 960, w: 150, rot: 12, t: 49.0, out: 49.85 });
cn("b7-c3", ["waste", "bottles", "ko"], [49.92, 50.21, 50.68], { y: 1180, out: 51.85 });
kw("b7-paint", "Paint Karke", { y: 1340, size: 150, style: "white", anim: "slideR", t: 50.82, out: 51.85 });
cn("b7-c4", ["unhe", "bana", "diya", "hai", "super", "cool"], [51.92, 52.21, 52.52, 52.84, 53.24, 53.65], { y: 1180, out: 56.05 });
pill("b7-vases", "Flower Vases", { x: 540, y: 1290, dot: P1, t: 53.96, out: 56.05, size: 56 });
pill("b7-pens", "Pen Stands", { x: 540, y: 1420, dot: Y2, t: 55.02, out: 56.05, size: 56 });
cn("b7-c5", ["Isse", "woh", "sirf", "padh", "nahi", "rahe"], [56.12, 56.41, 56.6, 56.97, 57.2, 57.42], { y: 1300, out: 58.05 });
cn("b7-c6", ["balki", "real", "life", "mein"], [58.12, 58.41, 58.65, 58.94], { y: 1180, out: 61.2333 });
kw("b7-recycle", "Recycling", { y: 1340, size: 170, style: "green", anim: "drop", t: 59.12, out: 61.2333 });
obj("b7-rec", "recycle", { x: 540, y: 1000, w: 170, t: 59.15, out: 61.2333, anim: "spin" });
cn("b7-c7", ["karna", "seekh", "rahe", "hain"], [59.75, 59.95, 60.24, 60.47], { y: 1470, out: 61.2333 });
html("b7-ticks", [1, 2, 3].map((n) => `<span class="tk"><b>${n}</b>${ICON.check}</span>`).join(""), "ticks", "", { type: "ticks", t: 59.9, out: 61.2333 });

// Beat 8 · T3 CTA — question behind head, comment bubble, follow card (ref B DM bubble @29.8, ref A caps CTA @22.5)
cn("b8-c1", ["Aaj", "Environment", "Day", "par"], [61.32, 61.62, 62.3, 62.55], { y: 430, out: 64.3 });
cn("b8-c2", ["apne", "bachche", "ko"], [63.05, 63.43, 63.73], { y: 520, out: 64.3 });
kw("b8-kaunsi", "Kaunsi Seekh", { y: 700, size: 150, style: "yellow", layer: "behind", anim: "drop", t: 64.36, out: 66.05 });
cn("b8-c3", ["di", "hai?"], [65.17, 65.3], { y: 960, out: 66.05 });
html("b8-bubble", `<div class="av"></div><div class="tx"><b>Comment</b> mein zaroor bataiye</div><div class="dots"><i></i><i></i><i></i></div>`, "bubble", "left:90px;top:1180px", { type: "obj", anim: "bubble", t: 66.12, out: 67.75, rot: 0 });
cn("b8-c4", ["aur", "green", "future", "ke", "liye"], [67.8, 67.92, 68.21, 68.47, 68.62], { y: 1130, out: END_FULL, layer: "front" });
html("b8-follow", `<div class="logo"><span>RKC</span></div><div class="fname">Rhyming Kid's Corner<small>Preschool</small></div><div class="fbtn">Follow</div>`, "follow", "left:90px;top:1230px", { type: "obj", anim: "bubble", t: 68.97, out: END_FULL, rot: 0 });
kw("b8-name", "RHYMING KID'S CORNER", { y: 1500, size: 84, style: "brand", anim: "drop", t: 70.11, out: END_FULL, max: 1040 });
cn("b8-thanks", ["Thank", "you!"], [72.12, 72.4], { y: 1630, out: END_FULL });

// SFX (full time) — subtle; ≤ ~5 per 10 s
const SFX = [
  ...FLASHES.map((t) => ({ t: t - 0.22, f: "whoosh.mp3", v: 0.22 })),
  { t: 0.3, f: "pop.mp3", v: 0.18 }, { t: 6.27, f: "sparkle.mp3", v: 0.16 }, { t: 9.42, f: "pop.mp3", v: 0.2 },
  { t: 15.12, f: "pop.mp3", v: 0.18 }, { t: 23.2, f: "pop.mp3", v: 0.16 }, { t: 30.02, f: "pop.mp3", v: 0.2 },
  { t: 36.33, f: "sparkle.mp3", v: 0.14 }, { t: 44.13, f: "pop.mp3", v: 0.2 }, { t: 53.96, f: "pop.mp3", v: 0.16 },
  { t: 55.02, f: "pop.mp3", v: 0.16 }, { t: 59.15, f: "sparkle.mp3", v: 0.15 }, { t: 66.12, f: "pop.mp3", v: 0.18 },
  { t: 68.97, f: "pop.mp3", v: 0.18 },
];

// ───────────────────────── short-version remap ─────────────────────────
// [fullStart, fullEnd, shortStart]
const RANGES = [
  [0, 12.1, 0], [12.1, 19.9667, 12.1], [20.4267, 23.6933, 19.9667], [28.8133, 32.08, 23.2333],
  [47.6833, 55.8833, 26.5], [66.0333, 73.9, 34.7],
];
const END_SHORT = 1277 / FPS;
const SHORT_EXTRA = (add) => {
  add({ id: "s-badge3", type: "obj", anim: "badge", t: 26.53, out: 34.7, rot: 0 }, `<div id="s-badge3" class="badge"><span class="bl">${ICON.leaf}</span>TARIKA <b>3</b>/3</div>`);
};
function remap(t) { for (const [a, b, s] of RANGES) if (t >= a - 1e-6 && t < b - 1e-6) return t - a + s; return null; }
function rangeEndShort(t) { for (const [a, b, s] of RANGES) if (t >= a - 1e-6 && t < b - 1e-6) return b - a + s; return null; }

// ───────────────────────── page generator ─────────────────────────
function page(version) {
  const isShort = version === "short";
  const P = "";
  const END = isShort ? END_SHORT : END_FULL;
  let vCues = [], vEls = [], flashes, teachers, sfx;
  if (!isShort) {
    vCues = cues.map((c) => ({ ...c })); vEls = els; flashes = FLASHES;
    teachers = TEACHERS.map((t) => ({ ...t, mediaStart: t.start - t.matteStart }));
    sfx = SFX;
  } else {
    const keep = new Set();
    for (const c of cues) {
      // a cue belongs to the range it overlaps (it may start up to 1.5 s before the in-point: clamp it to the in-point)
      const R = RANGES.find(([ra, rb]) => c.t < rb - 1e-6 && c.out > ra + 0.2 && c.t > ra - 1.5);
      if (!R) continue;
      const [ra, rb, rs] = R; const shift = rs - ra;
      const t = Math.max(c.t, ra) + shift, end = rb + shift;
      const n = { ...c, t, out: Math.min(c.out + shift, end) };
      if (c.times) n.times = c.times.map((x, i) => Math.max(x, ra + i * 0.06) + shift);
      if (c.flip) n.flip = c.flip + shift;
      vCues.push(n); keep.add(c.id);
    }
    // bursts/sweeps whose start is inside a range are kept by the loop above
    vEls = els.filter((e) => keep.has(e.id));
    SHORT_EXTRA((cue, h) => { vCues.push(cue); vEls = [...vEls, { id: cue.id, layer: "front", html: h }]; });
    flashes = RANGES.slice(1).map((r) => r[2]);
    teachers = [
      { id: "t1", start: 0, end: 8.1667, matte: "assets/matte-t1.webm", mediaStart: 0, scale: [1.32, 1.37], origin: "50% 0%" },
      { id: "t2", start: 12.1, end: 19.9667, matte: "assets/matte-t2.webm", mediaStart: 0, scale: [1.32, 1.37], origin: "50% 15%" },
      { id: "t3", start: 34.7, end: END_SHORT, matte: "assets/matte-t3.webm", mediaStart: 66.0333 - 61.2, scale: [1.12, 1.17], origin: "50% 38%" },
    ];
    sfx = SFX.map((s) => ({ ...s, t: remap(s.t + (s.f === "whoosh.mp3" ? 0.22 : 0)) })).filter((s) => s.t !== null && s.f !== "whoosh.mp3");
    sfx.push(...flashes.map((t) => ({ t: t - 0.22, f: "whoosh.mp3", v: 0.22 })));
  }
  const id = isShort ? "rkc-short" : "main";
  const src = isShort ? "assets/short.mp4" : "assets/full.mp4";
  const aud = isShort ? "assets/short.m4a" : "assets/full.m4a";
  const D = END.toFixed(4);
  const behind = vEls.filter((e) => e.layer === "behind").map((e) => e.html).join("\n        ");
  const front = vEls.filter((e) => e.layer !== "behind").map((e) => e.html).join("\n        ");
  const mattes = teachers.map((t) => `<video id="m-${t.id}" class="fill" src="${P}${t.matte}" muted playsinline data-start="${t.start}" data-duration="${(t.end - t.start).toFixed(4)}" data-media-start="${t.mediaStart.toFixed(4)}" data-track-index="${3 + teachers.indexOf(t)}"></video>`).join("\n        ");
  const sfxHtml = sfx.map((s, i) => `<audio id="sfx-${i}" src="${P}assets/sfx/${s.f}" data-start="${snap(Math.max(0, s.t)).toFixed(4)}" data-duration="1.2" data-track-index="${20 + i}" data-volume="${s.v}"></audio>`).join("\n    ");
  const leaves = Array.from({ length: 14 }, (_, i) => `<div class="lf" style="color:${[G1, G2, Y2, P1][i % 4]}">${ICON.leaf}</div>`).join("");

  const cfg = { cues: vCues.map((c) => ({ ...c, t: snap(c.t), out: snap(c.out), times: c.times && c.times.map(snap), flip: c.flip && snap(c.flip) })), flashes, teachers, END };
  return `<!doctype html>
<html lang="hi" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Rhyming Kid's Corner — Environment Day${isShort ? " (short)" : ""}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <link rel="stylesheet" href="${P}reel.css" />
  </head>
  <body>
    <!-- GENERATED by scripts/build.mjs — edit the cue list there, not this file. -->
    <div id="root" data-composition-id="${id}" data-start="0" data-duration="${D}" data-width="1080" data-height="1920">
      <div id="cam-main" class="cam">
        <video id="v-main" class="fill" src="${P}${src}" muted playsinline data-start="0" data-duration="${D}" data-track-index="0"></video>
      </div>
      <div id="behind" class="layer clip" data-start="0" data-duration="${D}" data-track-index="2">
        ${behind}
      </div>
      <div id="cam-matte" class="cam">
        ${mattes}
      </div>
      <div id="front" class="layer clip" data-start="0" data-duration="${D}" data-track-index="10">
        ${front}
        <div id="burst" class="burst">${leaves}</div>
        <div id="sweep" class="sweep"></div>
        <div id="flash" class="flash"></div>
      </div>
    </div>
    <audio id="a-main" src="${P}${aud}" data-start="0" data-duration="${D}" data-track-index="1" data-volume="1"></audio>
    ${sfxHtml}
    <script>window.__REEL = ${JSON.stringify(cfg)};</script>
    <script src="${P}reel.js"></script>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      window.__buildReel(tl, window.__REEL);
      window.__timelines["${id}"] = tl;
    </script>
  </body>
</html>
`;
}

mkdirSync(join(ROOT, "compositions"), { recursive: true });
writeFileSync(join(ROOT, "index.html"), page("full"));
// The short is its own sibling project (one root composition per project; assets duplicated, not symlinked).
const SHORT = join(ROOT, "..", "rkc-environment-day-short");
mkdirSync(join(SHORT, "assets/sfx"), { recursive: true });
writeFileSync(join(SHORT, "index.html"), page("short"));
for (const f of ["reel.js", "reel.css", "DESIGN.md", "hyperframes.json", ".gitignore"]) copyFileSync(join(ROOT, f), join(SHORT, f));
for (const f of ["short.mp4", "short.m4a", "matte-t1.webm", "matte-t2.webm", "matte-t3.webm", "sfx/whoosh.mp3", "sfx/pop.mp3", "sfx/sparkle.mp3"])
  if (existsSync(join(ROOT, "assets", f))) copyFileSync(join(ROOT, "assets", f), join(SHORT, "assets", f));
writeFileSync(join(SHORT, "meta.json"), JSON.stringify({ id: "rkc-environment-day-short", name: "rkc-environment-day-short" }, null, 2) + "\n");
writeFileSync(join(SHORT, "package.json"), JSON.stringify({ name: "rkc-environment-day-short", private: true, type: "module",
  scripts: { dev: "npx --yes hyperframes@0.9.1 preview", check: "npx --yes hyperframes@0.9.1 check", render: "npx --yes hyperframes@0.9.1 render" } }, null, 2) + "\n");
writeFileSync(join(SHORT, "README.md"), "# RKC Environment Day — 42s cut-down\n\nGENERATED by `../rkc-environment-day/scripts/build.mjs` (same cue list as the full version). Edit there, then `node scripts/build.mjs` from the full project.\n");
console.log(`built index.html (${END_FULL.toFixed(2)}s, ${cues.length} cues) + ../rkc-environment-day-short/index.html (${END_SHORT.toFixed(2)}s)`);
