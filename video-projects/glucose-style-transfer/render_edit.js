// node render_edit.js info | all a b | frames k f1,f2,...   (renders at 1440x2560 = source resolution)
const { chromium } = require('playwright'); const fs = require('fs');
const [, , mode, A, B] = process.argv;
(async () => {
  const br = await chromium.launch(); const pg = await br.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 4 / 3 });
  pg.on('pageerror', e => console.log('PAGE EXC', e.message)); pg.on('console', m => { if (m.type() === 'error') console.log('PAGE ERR', m.text()); });
  await pg.goto('file://' + process.cwd() + '/web/video.html'); await pg.evaluate(() => document.fonts.ready);
  const n = await pg.evaluate(() => SEGN()); const stage = await pg.$('#stage');
  if (mode === 'info') { const all = []; for (let k = 0; k < n; k++) { const m = await pg.evaluate(k => initS(k), k); all.push(m); console.log(k + 1, m.tpl, m.label, 'E0', m.E0, 'N', m.N, 'cam', JSON.stringify(m.cam), 'fit', JSON.stringify(m.fit.map(x => x.final))); }
    fs.writeFileSync('an/edit_info.json', JSON.stringify(all)); }
  else if (mode === 'frames') { const k = +A - 1; const m = await pg.evaluate(k => initS(k), k);
    for (const f of B.split(',').map(Number)) { await pg.evaluate(f => renderT(f), f); await stage.screenshot({ path: `an/ef/S${A}_${String(f).padStart(3, '0')}.jpg`, type: 'jpeg', quality: 90 }); } }
  else if (mode === 'all') { for (let k = +A - 1; k < Math.min(n, +B); k++) { const m = await pg.evaluate(k => initS(k), k); const dir = `vid/S${String(k + 1).padStart(2, '0')}`;
      fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
      for (let f = 0; f < m.N; f++) { await pg.evaluate(f => renderT(f), f); await stage.screenshot({ path: `${dir}/f_${String(f).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 94 }); }
      fs.writeFileSync(`${dir}/meta.json`, JSON.stringify(m)); console.log('rendered', k + 1, m.label, m.N); } }
  await br.close();
})();
