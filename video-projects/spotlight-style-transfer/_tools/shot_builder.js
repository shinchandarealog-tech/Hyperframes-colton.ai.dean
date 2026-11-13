// Screenshot every design in the builder at rest (end of its beat) + collect console errors.
const { chromium } = require('playwright');
const OUT = process.argv[2] || 'an';
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage({ viewport: { width: 1500, height: 1000 } });
  const errs = []; p.on('console', m => { if (m.type() === 'error') errs.push(m.text()) }); p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8091/', { waitUntil: 'networkidle' }); await p.waitForTimeout(2500);
  await p.screenshot({ path: `${OUT}/builder_full.png` });
  const n = (await p.$$('.tile')).length;
  for (let i = 0; i < n; i++) {
    const tiles = await p.$$('.tile');
    await tiles[i].click({ position: { x: 20, y: 12 } }); await p.waitForTimeout(200);
    if ((await p.textContent('#play')) === 'Pause') await p.click('#play');
    const ends = await p.evaluate(() => [...document.querySelectorAll('.beat-h span')].map(s => s.textContent));
    const bi = Math.floor(i / 3); const [a, e] = ends[bi].replace(' s', '').split('–').map(Number);
    const t = Math.max(a + 0.05, e - 0.06);
    await p.evaluate(t => { const s = document.getElementById('scrub'); s.value = t; s.dispatchEvent(new Event('input')) }, t);
    await p.waitForTimeout(800);
    await (await p.$('#stage')).screenshot({ path: `${OUT}/st_${bi}_${i % 3}.png` });
  }
  console.log('errors', JSON.stringify(errs)); await b.close();
})();
