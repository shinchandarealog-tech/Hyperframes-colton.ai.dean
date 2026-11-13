// node strip_builder.js <tileIndex> <t0> <t1> <step> <name>  -> per-frame PNGs an/s_<name>_NN.png
const { chromium } = require('playwright');
const a = process.argv.slice(2); const [tile, t0, t1, step] = a.slice(0, 4).map(Number); const name = a[4];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1500, height: 1000 } });
  await p.goto('http://localhost:8091/', { waitUntil: 'networkidle' }); await p.waitForTimeout(2000);
  await (await p.$$('.tile'))[tile].click({ position: { x: 20, y: 12 } }); await p.waitForTimeout(200);
  if ((await p.textContent('#play')) === 'Pause') await p.click('#play');
  let i = 0;
  for (let t = t0; t <= t1 + 1e-6; t += step) {
    await p.evaluate(t => { const s = document.getElementById('scrub'); s.value = t; s.dispatchEvent(new Event('input')) }, t);
    await p.waitForTimeout(450); await (await p.$('#stage')).screenshot({ path: `an/s_${name}_${String(i++).padStart(2, '0')}.png` });
  }
  await b.close();
})();
