// End-to-end touch test for the reel editor (emulated iPad + Android phone).
// Usage: node scripts/editor/test/touch.test.cjs <project-dir> [outDir]
// Starts the editor on a COPY-safe project (it writes edits.json + index.html!).
const { chromium, devices } = require("playwright");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

const proj = path.resolve(process.argv[2]);
const out = process.argv[3] || proj;
const PORT = 3099;
let failures = 0;
const ok = (c, msg) => { console.log(`${c ? "PASS" : "FAIL"}  ${msg}`); if (!c) failures++; };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function touch(cdp, type, pts) {
  await cdp.send("Input.dispatchTouchEvent", { type, touchPoints: pts.map((p, i) => ({ x: p.x, y: p.y, id: p.id ?? i })) });
}
async function drag(cdp, from, to, steps = 12) {
  await touch(cdp, "touchStart", [from]);
  for (let i = 1; i <= steps; i++) await touch(cdp, "touchMove", [{ x: from.x + ((to.x - from.x) * i) / steps, y: from.y + ((to.y - from.y) * i) / steps }]);
  await touch(cdp, "touchEnd", []);
}
async function tap(cdp, p) { await sleep(450); await touch(cdp, "touchStart", [p]); await touch(cdp, "touchEnd", []); }
async function pinch(cdp, c, d0, d1, steps = 10) {
  const pts = (d) => [{ x: c.x - d / 2, y: c.y, id: 1 }, { x: c.x + d / 2, y: c.y, id: 2 }];
  await touch(cdp, "touchStart", [pts(d0)[0]]);
  await touch(cdp, "touchStart", pts(d0));
  for (let i = 1; i <= steps; i++) await touch(cdp, "touchMove", pts(d0 + ((d1 - d0) * i) / steps));
  await touch(cdp, "touchEnd", []);
}
const saved = () => JSON.parse(fs.readFileSync(path.join(proj, "edit-data/edits.json"), "utf8"));
const html = () => fs.readFileSync(path.join(proj, "index.html"), "utf8");

async function screen(page, frameX, frameY) {
  return page.evaluate(([x, y]) => { const F = window.__editor.frameRect(); return { x: F.ox + F.x + x * F.k, y: F.oy + F.y + y * F.k }; }, [frameX, frameY]);
}
async function settle(page) { await page.evaluate(() => window.__editor.flushNow()); await sleep(300); }

async function run(device, label) {
  // start every device from a clean project
  await fetch(`http://localhost:${PORT}/api/edits`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ items: {} }) });
  const exe = "/opt/pw-browsers/chromium";
  const browser = await chromium.launch(fs.existsSync(exe) && !fs.existsSync(chromium.executablePath()) ? { executablePath: fs.statSync(exe).isDirectory() ? undefined : exe } : {});
  const ctx = await browser.newContext({ ...devices[device] });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  const cdp = await ctx.newCDPSession(page);
  const realTap = page.tap.bind(page);
  page.tap = async (sel) => { await sleep(450); await realTap(sel); await sleep(100); };
  await page.goto(`http://localhost:${PORT}/`);
  await page.waitForFunction(() => document.getElementById("status").textContent.includes("saved"), null, { timeout: 30000 });
  console.log(`\n== ${label} (${device}) ==`);

  // Tap the first caption ("It was never", centre ~ (540, 1072) in frame px)
  await tap(cdp, await screen(page, 540, 1072));
  await sleep(150);
  ok((await page.evaluate(() => window.__editor.selected)) === "#cap-01", "tap selects the caption");
  ok(await page.isVisible("#selbox"), "selection box with handles is shown");
  ok(await page.isVisible("#panel"), "style panel is shown");

  // Drag it up by 200 frame px
  const a = await screen(page, 540, 1072), b = await screen(page, 540, 772);
  await drag(cdp, a, b);
  await settle(page);
  let it = (await page.evaluate(() => window.__editor.items))["#cap-01"];
  ok(it && Math.abs(it.y + 300) < 3 && Math.abs(it.x) < 12, `drag moves it (y=${it && it.y})`);
  ok(saved().items["#cap-01"]?.y === it.y, "move saved to edits.json");
  ok(/html body #cap-01 \{ translate: /.test(html()), "move written into index.html");

  // Snap: drag horizontally a little: x should snap to centre (0 offset)
  const c1 = await screen(page, 540, 772), c2 = await screen(page, 545, 772);
  await drag(cdp, c1, { x: c2.x + 0.5, y: c2.y });
  it = (await page.evaluate(() => window.__editor.items))["#cap-01"];
  ok(Math.abs(it.x) < 0.01, `snaps to the centre line (x=${it.x})`);

  // Pinch to resize
  await pinch(cdp, await screen(page, 540, 772), 100, 200);
  await settle(page);
  it = (await page.evaluate(() => window.__editor.items))["#cap-01"];
  ok(it.scale > 1.6 && it.scale < 2.4, `pinch resizes (scale=${it.scale})`);

  // Rotate handle
  const rot = await page.locator("#selbox .rot").boundingBox();
  const rc = { x: rot.x + rot.width / 2, y: rot.y + rot.height / 2 };
  const ctr = await screen(page, 540, 772 + 0); // approx centre
  await drag(cdp, rc, { x: ctr.x + 150, y: ctr.y - 40 });
  await settle(page);
  it = (await page.evaluate(() => window.__editor.items))["#cap-01"];
  ok(Math.abs(it.rotate) > 20, `rotate handle rotates (rotate=${Math.round(it.rotate)})`);

  // Corner resize
  const br = await page.locator("#selbox .br").boundingBox();
  const s0 = it.scale;
  await drag(cdp, { x: br.x + 14, y: br.y + 14 }, { x: br.x - 40, y: br.y - 10 });
  it = (await page.evaluate(() => window.__editor.items))["#cap-01"];
  ok(it.scale < s0, `corner drag resizes (${s0.toFixed(2)} → ${it.scale.toFixed(2)})`);

  // Undo / redo
  const before = JSON.stringify(await page.evaluate(() => window.__editor.items));
  await page.tap("#undo");
  const afterUndo = JSON.stringify(await page.evaluate(() => window.__editor.items));
  ok(afterUndo !== before, "undo reverts the last change");
  await page.tap("#redo");
  ok(JSON.stringify(await page.evaluate(() => window.__editor.items)) === before, "redo re-applies it");
  // Undo all the way back
  while (await page.evaluate(() => window.__editor.canUndo)) await page.tap("#undo");
  await settle(page);
  ok(Object.keys(saved().items).length === 0 && !html().includes("hf-editor:start"), "undo all → project back to original (file too)");

  // Panel: colour, bold, outline, shadow, opacity, size, font
  await tap(cdp, await screen(page, 540, 1072));
  await page.tap('#p-swatches .swatch[data-c="#ffd60a"]');
  await page.tap("#p-outline");
  await page.tap("#p-size-plus");
  await page.selectOption("#p-font", "Anton");
  await page.locator("#p-opacity").fill("70"); await page.locator("#p-opacity").dispatchEvent("change");
  await settle(page);
  it = saved().items["#cap-01"];
  ok(it.color === "#ffd60a" && it.outline === true && it.fontFamily === "Anton" && it.fontSize === 56 && it.opacity === 0.7, `panel styles saved (${JSON.stringify(it)})`);
  ok(fs.existsSync(path.join(proj, "assets/fonts/anton-latin-400-normal.woff2")), "picked font copied into project assets/fonts");
  const live = await page.evaluate(() => { const d = document.getElementById("player").iframeElement.contentDocument; const cs = d.defaultView.getComputedStyle(d.getElementById("cap-01")); return { c: cs.color, f: cs.fontFamily, s: cs.fontSize }; });
  ok(live.c === "rgb(255, 214, 10)" && live.f.includes("Anton") && live.s === "56px", `preview shows the styles (${JSON.stringify(live)})`);

  // Double-tap to edit text in place
  const p0 = await screen(page, 540, 1072);
  await tap(cdp, p0); await touch(cdp, "touchStart", [p0]); await touch(cdp, "touchEnd", []);
  await sleep(150);
  ok(await page.isVisible("#texted"), "double-tap opens in-place text editing");
  await page.keyboard.press("ControlOrMeta+a");
  await page.keyboard.type("Hello there");
  await page.tap("#p-done");
  await settle(page);
  ok(saved().items["#cap-01"].html === "Hello there" && html().includes('data-track-index="2">Hello there</div>'), "new words saved into index.html");
  await page.tap("#undo"); await settle(page);
  ok(html().includes('data-track-index="2">It was never</div>'), "undo restores the original words in index.html");
  await page.tap("#redo"); await settle(page);

  // Safe zone toggle + red box when outside
  await page.tap("#safe");
  ok(await page.isVisible("#safezone"), "safe zone overlay shows");
  const q = await screen(page, 540, 1072), q2 = await screen(page, 540, 1700);
  await drag(cdp, q, q2);
  await sleep(200);
  ok(await page.evaluate(() => document.getElementById("selbox").classList.contains("bad")), "box turns red outside the safe zone");
  await page.screenshot({ path: path.join(out, `editor-${label}.png`) });

  // Pause while editing: start playback, then tap
  await page.tap("#play"); await sleep(600);
  await tap(cdp, await screen(page, 540, 450));
  await sleep(200);
  ok(await page.evaluate(() => document.getElementById("player").paused), "tapping the preview pauses playback");

  // Hook title selection (no id → path key) and delete
  await page.evaluate(() => document.getElementById("player").seek(0.2)); await sleep(300);
  await tap(cdp, await screen(page, 540, 330));
  await sleep(150);
  const k = await page.evaluate(() => window.__editor.selected);
  ok(k === "#hook > :nth-child(1)", `tap selects the hook title (${k})`);
  await page.tap("#p-delete"); await settle(page);
  ok(saved().items["#hook > :nth-child(1)"]?.deleted === true, "delete saved");
  await tap(cdp, await screen(page, 160, 300)); await sleep(150);
  ok((await page.evaluate(() => window.__editor.selected)) === "#hook > :nth-child(2)", "tap selects a star sticker");
  await page.tap("#undo"); await settle(page);

  ok(errors.length === 0, `no page errors ${errors.join(" | ")}`);
  await browser.close();
}

(async () => {
  const server = spawn("node", [path.join(__dirname, "../server.mjs"), proj, "--port", String(PORT)], { stdio: "inherit" });
  await sleep(800);
  try {
    await run("iPad Pro 11", "ipad");
    await run("Pixel 7", "android");
  } finally {
    server.kill();
  }
  console.log(failures ? `\n${failures} FAILED` : "\nALL PASSED");
  process.exit(failures ? 1 : 0);
})();
