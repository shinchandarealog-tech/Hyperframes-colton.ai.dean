#!/usr/bin/env node
// Search the creator's Google Drive audio library (catalog.json) and download single files on demand.
// The full library (~6,000 SFX + ~400 music tracks) lives in Drive, not in git; only this index is committed.
//
//   node assets/library/fetch.mjs search <words...> [--kind music|sfx] [--folder <text>] [--limit N]
//   node assets/library/fetch.mjs folders [--kind music|sfx]
//   node assets/library/fetch.mjs get <id> [--to <dir>] [--name <file>]
//
// Example (from a project folder):
//   node ../../assets/library/fetch.mjs search riser --kind sfx
//   node ../../assets/library/fetch.mjs get 1AbC... --to assets
//
// Downloads use curl (respects HTTPS_PROXY). Files are saved under a kebab-case name.

import { readFileSync, mkdirSync, existsSync, statSync } from "node:fs";
import { dirname, join, extname, basename } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const here = dirname(fileURLToPath(import.meta.url));
const { files } = JSON.parse(readFileSync(join(here, "catalog.json"), "utf8"));

const argv = process.argv.slice(2);
const cmd = argv.shift();
const opt = (k, d) => { const i = argv.indexOf(`--${k}`); if (i < 0) return d; const v = argv[i + 1]; argv.splice(i, 2); return v; };
const fmt = (s) => (s == null ? "   ?  " : `${s.toFixed(1).padStart(5)}s`);
const slug = (n) => basename(n, extname(n)).replace(/([a-z])([A-Z])/g, "$1-$2").replace(/[^a-zA-Z0-9]+/g, "-").replace(/^-|-$/g, "").toLowerCase() + extname(n).toLowerCase();

if (cmd === "search") {
  const kind = opt("kind"), folder = opt("folder")?.toLowerCase(), limit = Number(opt("limit", 40));
  const words = argv.map((w) => w.toLowerCase());
  const hits = files.filter((f) => {
    if (kind && f.kind !== kind) return false;
    if (folder && !f.folder.toLowerCase().includes(folder)) return false;
    const hay = `${f.folder}/${f.name}`.toLowerCase();
    return words.every((w) => hay.includes(w));
  });
  for (const f of hits.slice(0, limit))
    console.log(`${f.id}  ${fmt(f.dur)}  ${f.kind.padEnd(5)}  ${f.folder}/${f.name}${f.kit ? `  [already local: assets/${f.kit}]` : ""}`);
  console.log(`\n${hits.length} match(es)${hits.length > limit ? `, showing ${limit} (use --limit)` : ""}`);
} else if (cmd === "folders") {
  const kind = opt("kind"); const counts = {};
  for (const f of files) if (!kind || f.kind === kind) counts[f.folder] = (counts[f.folder] || 0) + 1;
  for (const [k, v] of Object.entries(counts).sort()) console.log(`${String(v).padStart(5)}  ${k}`);
} else if (cmd === "get") {
  const id = argv[0];
  const f = files.find((x) => x.id === id);
  if (!f) { console.error(`No catalog entry with id ${id}`); process.exit(1); }
  if (f.kit) console.error(`Note: already in the repo at assets/${f.kit}`);
  const dir = opt("to", "assets"); const name = opt("name", slug(f.name));
  mkdirSync(dir, { recursive: true });
  const out = join(dir, name);
  if (existsSync(out)) { console.log(`exists: ${out}`); process.exit(0); }
  const url = `https://drive.usercontent.google.com/download?id=${encodeURIComponent(id)}&export=download&confirm=t`;
  const r = spawnSync("curl", ["-fsSL", "--retry", "3", "-o", out, url], { stdio: "inherit" });
  if (r.status !== 0 || !existsSync(out) || statSync(out).size === 0) { console.error("Download failed (is the Drive folder still shared 'Anyone with the link'?)"); process.exit(1); }
  console.log(`saved: ${out}  (${f.folder}/${f.name})`);
} else {
  console.log(readFileSync(fileURLToPath(import.meta.url), "utf8").split("\n").slice(1, 12).map((l) => l.replace(/^\/\/ ?/, "")).join("\n"));
}
