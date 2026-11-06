#!/usr/bin/env node
// Hyperframes touch editor — tap-to-edit on top of the real composition.
//
//   node scripts/editor/server.mjs video-projects/<project>            # start editor (port 3010)
//   node scripts/editor/server.mjs video-projects/<project> --port 4000
//   node scripts/editor/server.mjs video-projects/<project> --apply    # re-write edits.json into index.html, then exit
//
// Every edit is saved to <project>/edit-data/edits.json AND written into the
// project's index.html (a managed <style id="hf-edits"> block + changed text),
// which is the same file `npx hyperframes preview` and `render` use.

import http from "node:http";
import { readFile, writeFile, rename, stat, mkdir, copyFile } from "node:fs/promises";
import { createReadStream, existsSync } from "node:fs";
import { join, resolve, dirname, extname, normalize, sep, basename } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import { cleanItems, managedBlock, fontFilesFor, MARK_START, MARK_END } from "./lib/edits.mjs";
import { parse, findBySelector, innerHtml, replaceInner } from "./lib/html.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const WORKSPACE = resolve(HERE, "../..");

function vendorFile(name) {
  try {
    const req = createRequire(join(WORKSPACE, "package.json"));
    return join(dirname(req.resolve("hyperframes/package.json")), "dist", name);
  } catch {
    return null;
  }
}

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".mp4": "video/mp4",
  ".webm": "video/webm",
  ".mov": "video/quicktime",
  ".m4a": "audio/mp4",
  ".mp3": "audio/mpeg",
  ".wav": "audio/wav",
  ".woff2": "font/woff2",
  ".woff": "font/woff",
  ".ttf": "font/ttf",
};

// ---------- project data ----------

export async function loadEdits(projectDir) {
  try {
    const j = JSON.parse(await readFile(join(projectDir, "edit-data", "edits.json"), "utf8"));
    return { items: cleanItems(j.items), originals: j.originals && typeof j.originals === "object" ? j.originals : {} };
  } catch {
    return { items: {}, originals: {} };
  }
}

// Writes the edit list into index.html + edits.json. Returns the saved state.
export async function applyEdits(projectDir, rawItems, prev) {
  const items = cleanItems(rawItems);
  const originals = { ...(prev?.originals || {}) };
  const indexPath = join(projectDir, "index.html");
  const before = await readFile(indexPath, "utf8");
  let src = before;

  // 1) Text changes. Work out every element's new inner HTML from the original source.
  const tree = parse(src);
  const writes = [];
  const sels = new Set([...Object.keys(originals), ...Object.entries(items).filter(([, e]) => typeof e.html === "string").map(([s]) => s)]);
  for (const sel of sels) {
    const node = findBySelector(tree, sel);
    if (!node) continue;
    const current = innerHtml(src, node);
    const e = items[sel];
    if (e && typeof e.html === "string") {
      if (!(sel in originals)) originals[sel] = current;
      if (current !== e.html) writes.push({ node, html: e.html });
    } else if (sel in originals) {
      if (current !== originals[sel]) writes.push({ node, html: originals[sel] });
      delete originals[sel];
    }
  }
  writes.sort((a, b) => b.node.openEnd - a.node.openEnd);
  let lastStart = Infinity;
  for (const w of writes) {
    if (w.node.closeStart > lastStart) continue; // nested inside an element we already rewrote
    src = replaceInner(src, w.node, w.html);
    lastStart = w.node.start;
  }

  // 2) The managed style block, right before </head> (after the project's own styles).
  const s = src.indexOf(MARK_START);
  const e = src.indexOf(MARK_END);
  if (s !== -1 && e !== -1 && e > s) {
    let from = s;
    while (from > 0 && (src[from - 1] === " " || src[from - 1] === "\t")) from--;
    let to = e + MARK_END.length;
    if (src[to] === "\n") to++;
    src = src.slice(0, from) + src.slice(to);
  }
  if (Object.keys(items).length) {
    const head = src.search(/<\/head\s*>/i);
    if (head === -1) throw new Error("index.html has no </head>");
    let at = head;
    while (at > 0 && (src[at - 1] === " " || src[at - 1] === "\t")) at--;
    src = src.slice(0, at) + "    " + managedBlock(items) + "\n" + src.slice(at);
  }

  // 3) Fonts the edits use -> project assets/fonts.
  const fonts = fontFilesFor(items);
  if (fonts.length) {
    const dir = join(projectDir, "assets", "fonts");
    await mkdir(dir, { recursive: true });
    for (const f of fonts) {
      const to = join(dir, f);
      if (!existsSync(to)) await copyFile(join(HERE, "fonts", f), to);
    }
  }

  // 4) Save (atomic writes).
  await mkdir(join(projectDir, "edit-data"), { recursive: true });
  const state = { version: 1, items, originals };
  await atomicWrite(join(projectDir, "edit-data", "edits.json"), JSON.stringify(state, null, 2) + "\n");
  if (src !== before) await atomicWrite(indexPath, src);
  return state;
}

async function atomicWrite(path, text) {
  const tmp = `${path}.tmp-${process.pid}`;
  await writeFile(tmp, text);
  await rename(tmp, path);
}

// ---------- http ----------

function send(res, code, body, type = "text/plain; charset=utf-8") {
  res.writeHead(code, { "content-type": type, "cache-control": "no-store" });
  res.end(body);
}

async function serveFile(req, res, file) {
  let st;
  try {
    st = await stat(file);
    if (!st.isFile()) throw new Error("not a file");
  } catch {
    return send(res, 404, "Not found");
  }
  const type = MIME[extname(file).toLowerCase()] || "application/octet-stream";
  const headers = { "content-type": type, "accept-ranges": "bytes", "cache-control": "no-store" };
  const range = req.headers.range && req.headers.range.match(/^bytes=(\d*)-(\d*)$/);
  if (range) {
    let start = range[1] === "" ? st.size - Number(range[2]) : Number(range[1]);
    let end = range[1] !== "" && range[2] !== "" ? Number(range[2]) : st.size - 1;
    if (range[1] === "") end = st.size - 1;
    start = Math.max(0, start);
    end = Math.min(end, st.size - 1);
    if (start > end) {
      res.writeHead(416, { "content-range": `bytes */${st.size}` });
      return res.end();
    }
    res.writeHead(206, { ...headers, "content-length": end - start + 1, "content-range": `bytes ${start}-${end}/${st.size}` });
    if (req.method === "HEAD") return res.end();
    return createReadStream(file, { start, end }).pipe(res);
  }
  res.writeHead(200, { ...headers, "content-length": st.size });
  if (req.method === "HEAD") return res.end();
  createReadStream(file).pipe(res);
}

function inside(base, rel) {
  const p = normalize(join(base, rel));
  return p === base || p.startsWith(base + sep) ? p : null;
}

function readBody(req, limit = 2_000_000) {
  return new Promise((ok, fail) => {
    let size = 0;
    const chunks = [];
    req.on("data", (c) => {
      size += c.length;
      if (size > limit) {
        fail(new Error("too large"));
        req.destroy();
      } else chunks.push(c);
    });
    req.on("end", () => ok(Buffer.concat(chunks).toString("utf8")));
    req.on("error", fail);
  });
}

export function createEditorServer(projectDir) {
  projectDir = resolve(projectDir);
  let state = null;
  let queue = Promise.resolve();
  let rev = 0;

  return http.createServer(async (req, res) => {
    try {
      const url = new URL(req.url, "http://x");
      const path = decodeURIComponent(url.pathname);

      if (path === "/api/state" && req.method === "GET") {
        state = state || (await loadEdits(projectDir));
        return send(res, 200, JSON.stringify({ project: basename(projectDir), rev, ...state }), MIME[".json"]);
      }
      if (path === "/api/edits" && req.method === "POST") {
        const body = JSON.parse(await readBody(req));
        const job = queue.then(async () => {
          state = state || (await loadEdits(projectDir));
          state = await applyEdits(projectDir, body.items, state);
          rev++;
          return state;
        });
        queue = job.catch(() => {});
        const saved = await job;
        return send(res, 200, JSON.stringify({ ok: true, rev, items: saved.items }), MIME[".json"]);
      }

      if (req.method !== "GET" && req.method !== "HEAD") return send(res, 405, "Method not allowed");

      if (path === "/" || path === "/index.html") return serveFile(req, res, join(HERE, "ui", "index.html"));
      if (path.startsWith("/ui/")) {
        const f = inside(join(HERE, "ui"), path.slice(4));
        return f ? serveFile(req, res, f) : send(res, 404, "Not found");
      }
      if (path === "/lib/edits.mjs") return serveFile(req, res, join(HERE, "lib", "edits.mjs"));
      if (path === "/vendor/player.js" || path === "/vendor/runtime.js") {
        const f = vendorFile(path.endsWith("player.js") ? "hyperframes-player.global.js" : "hyperframe.runtime.iife.js");
        if (!f || !existsSync(f)) return send(res, 500, "hyperframes is not installed — run `npm install` in the workspace root");
        return serveFile(req, res, f);
      }
      if (path.startsWith("/project/")) {
        const rel = path.slice("/project/".length);
        const f = inside(projectDir, rel);
        if (!f) return send(res, 404, "Not found");
        // A font picked a moment ago may not be copied yet: fall back to the bundled copy.
        if (rel.startsWith("assets/fonts/") && !existsSync(f)) {
          const b = inside(join(HERE, "fonts"), rel.slice("assets/fonts/".length));
          if (b) return serveFile(req, res, b);
        }
        return serveFile(req, res, f);
      }
      return send(res, 404, "Not found");
    } catch (err) {
      console.error(err);
      send(res, 500, String(err?.message || err));
    }
  });
}

// ---------- cli ----------

const isMain = process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const args = process.argv.slice(2);
  const dir = args.find((a) => !a.startsWith("--"));
  const portArg = args.indexOf("--port");
  const port = portArg !== -1 ? Number(args[portArg + 1]) : 3010;
  if (!dir || !existsSync(join(dir, "index.html"))) {
    console.error("Usage: node scripts/editor/server.mjs video-projects/<project> [--port 3010] [--apply]");
    process.exit(1);
  }
  if (args.includes("--apply")) {
    const prev = await loadEdits(resolve(dir));
    await applyEdits(resolve(dir), prev.items, prev);
    console.log(`Applied ${Object.keys(prev.items).length} edits to ${join(dir, "index.html")}`);
    process.exit(0);
  }
  createEditorServer(dir).listen(port, "0.0.0.0", () => {
    console.log(`Editor running: http://localhost:${port}/   (project: ${resolve(dir)})`);
  });
}
