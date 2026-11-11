// Assembles the publishable Artifact page (builder/artifact.html template + engine + current edit).
//   node scripts/build_artifact.cjs <outDir>   → <outDir>/index.html  (proxies go in <outDir>/assets/)
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const dir = path.join(__dirname, ".."), out = process.argv[2];
const D = require(path.join(dir, "builder/designs.js"));
const P = JSON.parse(fs.readFileSync(path.join(dir, "edit-data/beats.json"), "utf8"));
const sources = [];
for (const sub of ["assets/clips", "assets/real"]) for (const f of fs.readdirSync(path.join(dir, sub)).filter((f) => f.endsWith(".mp4")).sort()) {
  const dur = +execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path.join(dir, sub, f)]).toString().trim();
  sources.push({ src: `${sub}/${f}`, kind: sub.endsWith("real") ? "real" : "ai", dur: +dur.toFixed(2) });
}
const engineCss = D.css("").replace(/@font-face\{[^}]*\}\n?/g, "");
const designsJs = fs.readFileSync(path.join(dir, "builder/designs.js"), "utf8");
let html = fs.readFileSync(path.join(dir, "builder/artifact.html"), "utf8");
const put = (k, v) => { if (!html.includes(k)) throw new Error("missing " + k); html = html.split(k).join(v); };
put("/*__ENGINE_CSS__*/", engineCss);
put("/*__DESIGNS_JS__*/", designsJs.replace(/<\/script/gi, "<\\/script"));
put("/*__PROJECT__*/null", JSON.stringify(P));
put("/*__SOURCES__*/[]", JSON.stringify(sources));
fs.writeFileSync(path.join(out, "index.html"), html);
console.log("artifact page written", (html.length / 1024).toFixed(0) + " KB", sources.length, "sources");
