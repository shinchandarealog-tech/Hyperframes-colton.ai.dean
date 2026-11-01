// Scan every frame for jumps: mean abs luma diff between consecutive frames (160x90 gray).
// Flags spikes that are big in absolute terms AND large vs their neighbours (a smooth
// fast move ramps; a jump spikes alone). Planned flash/push windows are labelled.
// usage: node scripts/jumpscan.mjs renders/blurred.mp4
import { execFileSync } from "node:child_process";
const file = process.argv[2];
const W = 160, H = 90, N = W * H;
const raw = execFileSync("ffmpeg", ["-v", "error", "-i", file, "-vf", `scale=${W}:${H},format=gray`, "-f", "rawvideo", "-"], { maxBuffer: 1 << 30 });
const frames = raw.length / N;
const d = [0];
for (let f = 1; f < frames; f++) {
  let s = 0;
  for (let i = 0; i < N; i++) s += Math.abs(raw[f * N + i] - raw[(f - 1) * N + i]);
  d.push(s / N);
}
const PLANNED = [[1.75, 2.3, "push through icon"], [4.0, 4.5, "flash"], [6.95, 7.95, "tunnel push"], [9.5, 9.9, "flash"], [10.45, 11.1, "glow→logo"]];
const label = (t) => (PLANNED.find(([a, b]) => t >= a && t <= b) || [, , ""])[2];
const flags = [];
for (let f = 1; f < frames; f++) {
  const nb = Math.max(d[f - 1] ?? 0, d[f + 1] ?? 0);
  if (d[f] > 6 && d[f] > 2.2 * nb) flags.push(f);
}
console.log(`${frames} frames · mean diff ${(d.reduce((a, b) => a + b, 0) / frames).toFixed(2)} · max ${Math.max(...d).toFixed(2)} @ frame ${d.indexOf(Math.max(...d))}`);
const top = [...d.keys()].sort((a, b) => d[b] - d[a]).slice(0, 12);
console.log("largest frame-to-frame changes:");
for (const f of top.sort((a, b) => a - b)) console.log(`  f${String(f).padStart(3)} t=${(f / 30).toFixed(2)}s diff=${d[f].toFixed(2)}  ${label(f / 30) || "(unplanned)"}`);
console.log(flags.length ? `ISOLATED SPIKES (possible jumps): ${flags.map((f) => `f${f}@${(f / 30).toFixed(2)}s ${label(f / 30) || "UNPLANNED"}`).join(", ")}` : "no isolated spikes — no jumps detected");
