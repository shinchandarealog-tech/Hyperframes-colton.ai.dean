// node render_tpl.js test | all a b | strip i f0 f1 step
const { chromium } = require('playwright'); const fs = require('fs');
const [, , mode, A, B, Cc, D] = process.argv;
(async () => {
  const br = await chromium.launch(); const pg = await br.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  pg.on('console', m => { if (m.type() === 'error') console.log('PAGE ERR', m.text()); }); pg.on('pageerror', e => console.log('PAGE EXC', e.message));
  await pg.goto('file://' + process.cwd() + '/web/templates.html'); await pg.evaluate(() => document.fonts.ready);
  const n = await pg.evaluate(() => TPLN());
  const stage = await pg.$('#stage');
  const shot = async p => { fs.mkdirSync(require('path').dirname(p), { recursive: true }); await stage.screenshot({ path: p, type: 'jpeg', quality: 92 }); };
  if (mode === 'test') {
    for (let i = 0; i < n; i++) { const m = await pg.evaluate(i => initT(i), i);
      for (const q of [0.15, 0.45, 0.75, 0.97]) { const f = Math.floor(m.N * q); await pg.evaluate(f => renderT(f), f); await shot(`an/test/T${String(i + 1).padStart(2, '0')}_${String(f).padStart(3, '0')}.jpg`); }
      console.log(i + 1, m.name, 'N', m.N, 'fit', JSON.stringify(m.fit)); }
  } else if (mode === 'strip') {
    const i = +A - 1; const m = await pg.evaluate(i => initT(i), i);
    for (let f = +B; f <= Math.min(+Cc, m.N - 1); f += +(D || 1)) { await pg.evaluate(f => renderT(f), f); await shot(`an/strip/T${A}_${String(f).padStart(3, '0')}.jpg`); }
  } else if (mode === 'all') {
    for (let i = +A - 1; i < Math.min(n, +B); i++) { const m = await pg.evaluate(i => initT(i), i); const dir = `tpl/T${String(i + 1).padStart(2, '0')}`;
      fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
      for (let f = 0; f < m.N; f++) { await pg.evaluate(f => renderT(f), f); await shot(`${dir}/f_${String(f).padStart(4, '0')}.jpg`); }
      fs.writeFileSync(`${dir}/meta.json`, JSON.stringify(m)); console.log('rendered', i + 1, m.name, m.N); }
  }
  await br.close();
})();
