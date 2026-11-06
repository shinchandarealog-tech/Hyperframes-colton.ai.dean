// Shared by the editor server (Node) and the editor page (browser).
// Turns the edit list saved in edit-data/edits.json into the CSS block that
// lives inside index.html — so the Studio preview, this editor's preview and
// `npx hyperframes render` all read exactly the same styles.

export const FRAME = { width: 1080, height: 1920 };

// Meta safe area: top 14%, bottom 35%, sides 6% of a 1080x1920 frame.
export const SAFE = {
  left: FRAME.width * 0.06, // 64.8
  right: FRAME.width * (1 - 0.06), // 1015.2
  top: FRAME.height * 0.14, // 268.8
  bottom: FRAME.height * (1 - 0.35), // 1248
};

export const MARK_START = "<!-- hf-editor:start (managed by scripts/editor — edit in the editor, not by hand) -->";
export const MARK_END = "<!-- hf-editor:end -->";

// Fonts bundled with the editor (scripts/editor/fonts). Picking one copies the
// woff2 files into the project's assets/fonts so preview and render match.
export const FONTS = {
  Inter: { slug: "inter", weights: [400, 600, 700, 800], fallback: "sans-serif" },
  Poppins: { slug: "poppins", weights: [400, 600, 700, 800], fallback: "sans-serif" },
  Montserrat: { slug: "montserrat", weights: [400, 600, 700, 800], fallback: "sans-serif" },
  Anton: { slug: "anton", weights: [400], fallback: "sans-serif" },
  "Bebas Neue": { slug: "bebas-neue", weights: [400], fallback: "sans-serif" },
  "Playfair Display": { slug: "playfair-display", weights: [400, 600, 700, 800], fallback: "serif" },
  "DM Serif Display": { slug: "dm-serif-display", weights: [400], fallback: "serif" },
  "Permanent Marker": { slug: "permanent-marker", weights: [400], fallback: "cursive" },
};

export const fontFile = (family, weight) => `${FONTS[family].slug}-latin-${weight}-normal.woff2`;

export function fontFilesFor(items) {
  const files = new Set();
  for (const e of Object.values(items || {})) {
    if (e && !e.deleted && e.fontFamily && FONTS[e.fontFamily]) {
      for (const w of FONTS[e.fontFamily].weights) files.add(fontFile(e.fontFamily, w));
    }
  }
  return [...files].sort();
}

// Selectors are the keys of the edit list. Only two shapes are allowed, so a
// saved key can never inject CSS or HTML:  #id   or   #id > :nth-child(n) > ...
const SEL_RE = /^#[A-Za-z_][\w-]*( > :nth-child\([1-9]\d{0,3}\))*$/;
export const isValidSelector = (s) => typeof s === "string" && s.length < 300 && SEL_RE.test(s);

const num = (v, lo, hi, d) => {
  const n = Number(v);
  if (!Number.isFinite(n)) return d;
  return Math.min(hi, Math.max(lo, n));
};
const round = (n, p = 2) => Math.round(n * 10 ** p) / 10 ** p;
const COLOR_RE = /^#[0-9a-fA-F]{6}$/;

// Normalises one item: drops unknown fields and clamps numbers.
export function cleanItem(e) {
  const o = {};
  if (!e || typeof e !== "object") return o;
  if (e.kind === "text" || e.kind === "graphic" || e.kind === "image") o.kind = e.kind;
  if ("x" in e) o.x = round(num(e.x, -4000, 4000, 0));
  if ("y" in e) o.y = round(num(e.y, -4000, 4000, 0));
  if ("scale" in e) o.scale = round(num(e.scale, 0.05, 20, 1), 4);
  if ("rotate" in e) o.rotate = round(num(e.rotate, -3600, 3600, 0));
  if ("fontSize" in e) o.fontSize = round(num(e.fontSize, 6, 600, 48), 1);
  if ("opacity" in e) o.opacity = round(num(e.opacity, 0, 1, 1), 3);
  if (typeof e.fontFamily === "string" && FONTS[e.fontFamily]) o.fontFamily = e.fontFamily;
  if (typeof e.color === "string" && COLOR_RE.test(e.color)) o.color = e.color.toLowerCase();
  for (const k of ["bold", "outline", "shadow", "deleted"]) if (typeof e[k] === "boolean") o[k] = e[k];
  if (typeof e.html === "string") o.html = sanitizeHtml(e.html);
  return o;
}

export function cleanItems(items) {
  const out = {};
  for (const [sel, e] of Object.entries(items || {})) {
    if (!isValidSelector(sel)) continue;
    const c = cleanItem(e);
    if (Object.keys(c).some((k) => k !== "kind")) out[sel] = c;
  }
  return out;
}

// Text edits: keep only plain text, line breaks and a few inline tags
// (span with a class, b/strong/i/em). Everything else is escaped.
const ALLOWED_TAG = /^<(\/?)(span|b|strong|i|em|br)(\s+class="[\w -]*")?\s*\/?>$/i;
export function sanitizeHtml(html) {
  let out = "";
  const re = /<[^>]*>|[^<]+|</g;
  let m;
  while ((m = re.exec(String(html).slice(0, 5000))) !== null) {
    const t = m[0];
    if (t.startsWith("<") && t.length > 1) {
      const a = t.match(ALLOWED_TAG);
      if (a) {
        const name = a[2].toLowerCase();
        if (name === "br") out += "<br>";
        else if (a[1]) out += `</${name}>`;
        else out += `<${name}${name === "span" && a[3] ? a[3] : ""}>`;
      } else out += escapeText(t);
    } else out += escapeText(t);
  }
  return out;
}
function escapeText(t) {
  return t
    .replace(/&(?![a-zA-Z]{2,8};|#\d{1,6};|#x[0-9a-fA-F]{1,6};)/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// The CSS rule for one item. Uses the individual `translate` / `rotate` /
// `scale` properties and `filter: opacity()` so it stacks on top of any GSAP
// animation (which writes `transform` / `opacity`) instead of fighting it.
export function ruleFor(sel, e) {
  const target = `html body ${sel}`;
  if (e.deleted) return `${target} { display: none !important; }`;
  const d = [];
  if (e.x || e.y) d.push(`translate: ${round(e.x || 0)}px ${round(e.y || 0)}px`);
  if (e.rotate) d.push(`rotate: ${round(e.rotate)}deg`);
  if (e.scale !== undefined && e.scale !== 1) d.push(`scale: ${round(e.scale, 4)}`);
  const isText = e.kind !== "graphic" && e.kind !== "image";
  if (isText) {
    if (e.fontFamily) d.push(`font-family: "${e.fontFamily}", ${FONTS[e.fontFamily].fallback}`);
    if (e.fontSize) d.push(`font-size: ${e.fontSize}px`);
    if (e.color) d.push(`color: ${e.color}`);
    if (e.bold !== undefined) d.push(`font-weight: ${e.bold ? 800 : 400}`);
    if (e.outline === true) d.push(`-webkit-text-stroke: 0.08em #000`, `paint-order: stroke fill`);
    if (e.outline === false) d.push(`-webkit-text-stroke: 0`);
    if (e.shadow === true)
      d.push(`text-shadow: 0 3px 8px rgba(0,0,0,0.75), 0 0 18px rgba(0,0,0,0.5), 0 0 2px rgba(0,0,0,0.8)`);
    if (e.shadow === false) d.push(`text-shadow: none`);
  }
  const filters = [];
  if (e.opacity !== undefined && e.opacity !== 1) filters.push(`opacity(${e.opacity})`);
  if (!isText && e.outline === true)
    filters.push(`drop-shadow(2px 0 0 #000) drop-shadow(-2px 0 0 #000) drop-shadow(0 2px 0 #000) drop-shadow(0 -2px 0 #000)`);
  if (!isText && e.shadow === true) filters.push(`drop-shadow(0 4px 10px rgba(0,0,0,0.6))`);
  if (filters.length) d.push(`filter: ${filters.join(" ")}`);
  let css = d.length ? `${target} { ${d.join("; ")}; }` : "";
  if (e.kind === "graphic" && e.color) {
    const shapes = ["path", "circle", "rect", "polygon", "ellipse", "line", "polyline"]
      .map((t) => `${target} ${t}`)
      .join(", ");
    css += `${css ? "\n" : ""}${shapes} { fill: ${e.color}; }`;
  }
  return css;
}

export function buildCss(items, fontBase = "assets/fonts/") {
  const parts = [];
  const used = new Set();
  for (const e of Object.values(items || {})) if (e && !e.deleted && e.fontFamily) used.add(e.fontFamily);
  for (const fam of [...used].sort()) {
    for (const w of FONTS[fam].weights) {
      parts.push(
        `@font-face { font-family: "${fam}"; font-weight: ${w}; font-style: normal; font-display: block; src: url("${fontBase}${fontFile(fam, w)}") format("woff2"); }`
      );
    }
  }
  for (const [sel, e] of Object.entries(items || {})) {
    const r = ruleFor(sel, e);
    if (r) parts.push(r);
  }
  return parts.join("\n");
}

export function managedBlock(items) {
  const css = buildCss(items);
  return `${MARK_START}\n    <style id="hf-edits">\n${css}\n    </style>\n    ${MARK_END}`;
}

// Bounding box (axis aligned) of an element's box after our move/scale/rotate.
// base = {cx, cy, w, h} in frame pixels with our edits removed.
export function editedAabb(base, e) {
  const s = e.scale ?? 1;
  const r = ((e.rotate || 0) * Math.PI) / 180;
  const w = base.w * s;
  const h = base.h * s;
  const hw = (Math.abs(w * Math.cos(r)) + Math.abs(h * Math.sin(r))) / 2;
  const hh = (Math.abs(w * Math.sin(r)) + Math.abs(h * Math.cos(r))) / 2;
  const cx = base.cx + (e.x || 0);
  const cy = base.cy + (e.y || 0);
  return { left: cx - hw, right: cx + hw, top: cy - hh, bottom: cy + hh, cx, cy };
}

export function outsideSafe(b, tol = 0.5) {
  return b.left < SAFE.left - tol || b.right > SAFE.right + tol || b.top < SAFE.top - tol || b.bottom > SAFE.bottom + tol;
}

// Snap a box's edges/centre to the safe-zone edges and the frame centre lines.
export const SNAP_X = [SAFE.left, FRAME.width / 2, SAFE.right];
export const SNAP_Y = [SAFE.top, FRAME.height / 2, SAFE.bottom];
export function snapOffset(b, threshold) {
  const pick = (vals, lines) => {
    let best = null;
    for (const v of vals)
      for (const l of lines) {
        const d = l - v;
        if (Math.abs(d) <= threshold && (best === null || Math.abs(d) < Math.abs(best.d))) best = { d, line: l };
      }
    return best;
  };
  const sx = pick([b.left, b.cx, b.right], SNAP_X);
  const sy = pick([b.top, b.cy, b.bottom], SNAP_Y);
  return { dx: sx ? sx.d : 0, dy: sy ? sy.d : 0, lineX: sx ? sx.line : null, lineY: sy ? sy.line : null };
}
