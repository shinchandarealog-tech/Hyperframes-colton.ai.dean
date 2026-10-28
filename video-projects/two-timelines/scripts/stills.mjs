// Render the QA stills listed in the brief into out/stills/.
import { execSync } from "node:child_process";
import { mkdirSync } from "node:fs";

const frames = (process.argv[2] ?? "30,100,200,300,420,500,600,670,800,880").split(",").map(Number);
mkdirSync("out/stills", { recursive: true });
for (const f of frames) {
  execSync(`npx remotion still TwoTimelines out/stills/frame-${String(f).padStart(3, "0")}.png --frame=${f} --log=error`, {
    stdio: "inherit",
  });
}
