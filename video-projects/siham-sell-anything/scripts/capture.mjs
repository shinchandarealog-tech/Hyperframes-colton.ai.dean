// Render the GSAP overlay frame by frame in headless Chrome with a transparent background.
import { createRequire } from 'module';
const { chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright');
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const tl = JSON.parse(fs.readFileSync(path.join(ROOT, 'scripts/timeline.json')));
fs.writeFileSync(path.join(ROOT, 'overlay/timeline.js'), 'window.TL=' + JSON.stringify(tl) + ';');
const out = process.argv[2] || path.join(ROOT, 'renders/ovl');
const only = process.argv[3] ? process.argv[3].split(',').map(Number) : null;   // optional list of seconds
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exit(1); });
await page.goto('file://' + path.join(ROOT, 'overlay/index.html'));
await page.waitForFunction(() => window.__ready === true);
await page.evaluate(() => document.fonts.ready);
const N = Math.round(tl.duration * tl.fps);
const frames = only ? only.map(s => Math.round(s * tl.fps)) : [...Array(N).keys()];
const qc = {};
for (const n of frames) {
  await page.evaluate(t => window.__seek(t), n / tl.fps);
  qc[n] = await page.evaluate(() => window.__qc());
  await page.screenshot({ path: path.join(out, `${String(n).padStart(5, '0')}.png`), omitBackground: true });
  if (n % 60 === 0) console.log('frame', n, '/', N);
}
fs.writeFileSync(path.join(out, 'qc.json'), JSON.stringify(qc));
fs.writeFileSync(path.join(ROOT, 'scripts/sfx.json'), JSON.stringify(await page.evaluate(() => window.__sfx), null, 1));
await browser.close();
