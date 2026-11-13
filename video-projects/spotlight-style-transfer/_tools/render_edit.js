// Render the edit's graphics as two transparent 1080x1920 layers per frame (card = behind the speaker, gfx = in front)
// and dump the graphic events for sound design.  node _tools/render_edit.js <config.json> <outdir>
const { chromium } = require('playwright');
const fs = require('fs');
const [cfgPath, out] = process.argv.slice(2);
const FPS = 24, N = 216;
(async () => {
  fs.mkdirSync(`${out}/card`, { recursive: true }); fs.mkdirSync(`${out}/gfx`, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 2100 }, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8091/', { waitUntil: 'networkidle' }); await p.waitForTimeout(2000);
  await p.addStyleTag({ content: `.stage{width:1080px!important;height:1920px!important;max-width:none!important;background:transparent!important;border-radius:0!important;outline:none!important}
    .monitor{position:static!important}.desk{display:block!important}#rack,#insp,header,.transport,.scrub,.mode,.checks{display:none!important}
    html,body{background:transparent!important;padding:0!important}#bg,#fg,#guides,#refImg{display:none!important}` });
  const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
  await p.evaluate(c => { window.RENDER = true; window.__rb.load(c) }, cfg);
  const ev = await p.evaluate(() => window.__rb.events());
  fs.writeFileSync(`${out}/events.json`, JSON.stringify(ev, null, 1));
  const st = await p.$('#stage');
  for (let f = 0; f < N; f++) {
    await p.evaluate(t => window.__rb.frame(t), f / FPS);
    await p.evaluate(() => { document.getElementById('gfx').style.visibility = 'hidden'; document.getElementById('cardSvg').style.visibility = 'visible' });
    await st.screenshot({ path: `${out}/card/c_${String(f + 1).padStart(4, '0')}.png`, omitBackground: true });
    await p.evaluate(() => { document.getElementById('gfx').style.visibility = 'visible'; document.getElementById('cardSvg').style.visibility = 'hidden' });
    await st.screenshot({ path: `${out}/gfx/g_${String(f + 1).padStart(4, '0')}.png`, omitBackground: true });
  }
  console.log('frames', N, 'events', ev.length, 'errors', JSON.stringify(errs)); await b.close();
})();
