// Text calibration in Chromium (same engine as the renderer).
// ink mode : fit font-size to the measured ink height, letter-spacing to the ink width, position to the ink box.
// fix mode : size given; left = ink-left (or after previous word + a space), top from the measured baseline.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [itemsPath, fontsDir, outPath] = process.argv.slice(2);
  const items = JSON.parse(fs.readFileSync(itemsPath, 'utf8'));
  const f64 = n => fs.readFileSync(path.join(fontsDir, n)).toString('base64');
  const css = `@font-face{font-family:'Inter';src:url(data:font/woff2;base64,${f64('Inter-var-latin.woff2')}) format('woff2');font-weight:100 900;}
  @font-face{font-family:'Bebas Neue';src:url(data:font/woff2;base64,${f64('BebasNeue-latin.woff2')}) format('woff2');}`;
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 400, height: 300 } });
  await pg.setContent(`<style>${css}</style><span style="font-family:'Inter'">a</span><span style="font-family:'Bebas Neue'">a</span>`);
  await pg.evaluate(async () => { await document.fonts.load("400 50px 'Inter'"); await document.fonts.load("600 50px 'Inter'"); await document.fonts.load("50px 'Bebas Neue'"); await document.fonts.ready; });
  const ink = (t, fam, wt, size, ls) => pg.evaluate(([t, fam, wt, size, ls]) => {
    const c = document.createElement('canvas'); c.width = 2400; c.height = 900; const x = c.getContext('2d');
    x.font = `${wt} ${size}px '${fam}'`; x.letterSpacing = (ls * size) + 'px'; x.fontKerning = 'normal'; x.textBaseline = 'alphabetic';
    x.fillStyle = '#000'; x.fillText(t, 100, 500);
    const d = x.getImageData(0, 0, 2400, 900).data; let x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1;
    for (let yy = 0; yy < 900; yy++) for (let xx = 0; xx < 2400; xx++) if (d[(yy * 2400 + xx) * 4 + 3] > 110) { if (xx < x0) x0 = xx; if (xx > x1) x1 = xx; if (yy < y0) y0 = yy; if (yy > y1) y1 = yy; }
    const m = x.measureText(t); const sp = x.measureText(t + ' ').width - m.width;
    const asc = m.fontBoundingBoxAscent, desc = m.fontBoundingBoxDescent;
    return { x0: x0 - 100, x1: x1 + 1 - 100, y0: y0 - 500, y1: y1 + 1 - 500, top_to_base: (size - (asc + desc)) / 2 + asc, adv: m.width, sp };
  }, [t, fam, wt, size, ls]);
  const out = {};
  for (const it of items) {
    let size, ls = it.ls, m, left, base;
    if (it.ink) {
      const [tx0, ty0, tx1, ty1] = it.ink; size = it.size0 || 80;
      for (let i = 0; i < 5; i++) {
        m = await ink(it.text, it.fam, it.wt, size, ls); size = size * (ty1 - ty0) / (m.y1 - m.y0);
        m = await ink(it.text, it.fam, it.wt, size, ls);
        const n = [...it.text].length; if (n > 1) ls = ls + ((tx1 - tx0) - (m.x1 - m.x0)) / ((n - 1) * size);
      }
      m = await ink(it.text, it.fam, it.wt, size, ls); left = tx0 - m.x0; base = ty1 - m.y1;
      // words without descenders: ink bottom == baseline; with descenders correct via font metrics at that size
      if (/[gjpqy,;]/.test(it.text)) { const ref = await ink(it.text.replace(/[gjpqy,;]/g, 'x'), it.fam, it.wt, size, ls); base = ty1 - m.y1; }
    } else {
      const [sz, x0, b0] = it.fix; size = sz; m = await ink(it.text, it.fam, it.wt, size, ls); base = b0;
      if (typeof x0 === 'string' && x0.startsWith('after:')) { const p = out[x0.slice(6)]; left = p.left + p.adv + p.sp; }
      else left = x0 - m.x0;
    }
    out[it.id] = { size: +size.toFixed(2), lsEm: +ls.toFixed(4), left: +left.toFixed(2), top: +(base - m.top_to_base).toFixed(2), base: +base.toFixed(1),
      adv: m.adv, sp: m.sp, inkW: m.x1 - m.x0, inkH: m.y1 - m.y0 };
  }
  fs.writeFileSync(outPath, JSON.stringify(out, null, 1)); console.log('calibrated', Object.keys(out).length);
  await b.close();
})();
