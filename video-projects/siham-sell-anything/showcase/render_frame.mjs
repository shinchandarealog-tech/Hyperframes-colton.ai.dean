import { createRequire } from 'module';
const { chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright');
import path from 'path'; import { fileURLToPath } from 'url';
const D = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
for (const k of ['bg', 'top']) {
  await p.goto('file://' + path.join(D, 'frame.html') + '#' + k); await p.reload();
  await p.evaluate(() => window.__ready);
  await p.screenshot({ path: path.join(D, `${k}.png`), omitBackground: k === 'top' });
}
await b.close();
