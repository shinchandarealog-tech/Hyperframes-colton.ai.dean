// Udaan reel builder — local server.
//   node builder/server.cjs [port]      (run from the project folder; default port 3010)
// Serves the project (with HTTP Range so video scrubbing works), and:
//   GET  /api/project  -> edit-data/beats.json
//   GET  /api/sources  -> available clips + durations
//   POST /api/save     -> writes beats.json (keeps a history copy) + regenerates index.html
const http = require("http");
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const { build } = require("../scripts/build_index.cjs");

const ROOT = path.join(__dirname, "..");
const PORT = +process.argv[2] || 3010;
const BEATS = path.join(ROOT, "edit-data/beats.json");
const HIST = path.join(ROOT, "edit-data/history");
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".cjs": "text/javascript", ".css": "text/css", ".json": "application/json", ".mp4": "video/mp4", ".mp3": "audio/mpeg", ".png": "image/png", ".jpg": "image/jpeg", ".woff2": "font/woff2" };

let SOURCES = null;
function sources() {
  if (SOURCES) return SOURCES;
  SOURCES = [];
  for (const sub of ["assets/clips", "assets/real"]) {
    const d = path.join(ROOT, sub);
    if (!fs.existsSync(d)) continue;
    for (const f of fs.readdirSync(d).filter((f) => f.endsWith(".mp4")).sort()) {
      let dur = 0;
      try { dur = +execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path.join(d, f)]).toString().trim(); } catch (e) {}
      SOURCES.push({ src: `${sub}/${f}`, kind: sub.endsWith("real") ? "real" : "ai", dur: +dur.toFixed(2) });
    }
  }
  return SOURCES;
}

function send(res, code, body, type) { res.writeHead(code, { "Content-Type": type || "application/json", "Cache-Control": "no-store" }); res.end(body); }

function serveFile(req, res, file) {
  fs.stat(file, (err, st) => {
    if (err || !st.isFile()) return send(res, 404, "not found", "text/plain");
    const type = TYPES[path.extname(file)] || "application/octet-stream";
    const range = req.headers.range;
    if (range) {
      const m = /bytes=(\d*)-(\d*)/.exec(range);
      let start = m[1] ? +m[1] : 0, end = m[2] ? +m[2] : st.size - 1;
      if (start >= st.size) { res.writeHead(416, { "Content-Range": `bytes */${st.size}` }); return res.end(); }
      end = Math.min(end, st.size - 1);
      res.writeHead(206, { "Content-Type": type, "Content-Range": `bytes ${start}-${end}/${st.size}`, "Accept-Ranges": "bytes", "Content-Length": end - start + 1, "Cache-Control": "no-store" });
      return fs.createReadStream(file, { start, end }).pipe(res);
    }
    res.writeHead(200, { "Content-Type": type, "Content-Length": st.size, "Accept-Ranges": "bytes", "Cache-Control": "no-store" });
    fs.createReadStream(file).pipe(res);
  });
}

http.createServer((req, res) => {
  const url = decodeURIComponent(req.url.split("?")[0]);
  if (url === "/api/project") return send(res, 200, fs.readFileSync(BEATS));
  if (url === "/api/sources") return send(res, 200, JSON.stringify(sources()));
  if (url === "/api/save" && req.method === "POST") {
    let body = "";
    req.on("data", (c) => { body += c; if (body.length > 5e6) req.destroy(); });
    req.on("end", () => {
      try {
        const P = JSON.parse(body);
        if (!P.meta || !Array.isArray(P.beats) || !P.beats.length) throw new Error("bad project");
        P.beats.sort((a, b) => a.start - b.start);
        fs.mkdirSync(HIST, { recursive: true });
        const stamp = new Date().toISOString().replace(/[:.]/g, "-");
        if (fs.existsSync(BEATS)) fs.copyFileSync(BEATS, path.join(HIST, `beats-${stamp}.json`));
        fs.writeFileSync(BEATS, JSON.stringify(P, null, 1));
        const r = build(ROOT);
        send(res, 200, JSON.stringify({ ok: true, saved: stamp, ...r }));
      } catch (e) { send(res, 400, JSON.stringify({ ok: false, error: String(e.message || e) })); }
    });
    return;
  }
  let rel = url === "/" ? "/builder/index.html" : url;
  const file = path.normalize(path.join(ROOT, rel));
  if (!file.startsWith(ROOT)) return send(res, 403, "forbidden", "text/plain");
  serveFile(req, res, file);
}).listen(PORT, () => console.log(`Udaan reel builder → http://localhost:${PORT}`));
