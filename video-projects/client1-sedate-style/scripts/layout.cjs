// Lay text out by the reference's anchors: size/tracking per role, anchor = ink centre x or ink left x, plus baseline.
// Prints left/top (CSS, line-height:1) and the resulting ink box. items: [{id,text,fam,wt,size,ls,anchor:'center'|'left',x,base}]
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [itemsPath, fontsDir, outPath] = process.argv.slice(2);
  const items = JSON.parse(fs.readFileSync(itemsPath, 'utf8'));
  const f64 = n => fs.readFileSync(path.join(fontsDir, n)).toString('base64');
  const css = `@font-face{font-family:'Inter';src:url(data:font/woff2;base64,${f64('Inter-var-latin.woff2')}) format('woff2');font-weight:100 900;}
  @font-face{font-family:'Bebas Neue';src:url(data:font/woff2;base64,${f64('BebasNeue-latin.woff2')}) format('woff2');}`;
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.setContent(`<style>${css}</style><span style="font-family:'Inter'">a</span><span style="font-family:'Bebas Neue'">a</span>`);
  await pg.evaluate(async () => { for (const w of [300,400,500,600,700]) await document.fonts.load(`${w} 50px 'Inter'`); await document.fonts.load("50px 'Bebas Neue'"); await document.fonts.ready; });
  const out = {};
  for (const it of items) {
    const m = await pg.evaluate(([t, fam, wt, size, ls]) => {
      const c = document.createElement('canvas'); c.width = 2600; c.height = 900; const x = c.getContext('2d');
      x.font = `${wt} ${size}px '${fam}'`; x.letterSpacing = (ls * size) + 'px'; x.fontKerning = 'normal'; x.textBaseline = 'alphabetic';
      x.fillText(t, 100, 500); const d = x.getImageData(0, 0, 2600, 900).data; let x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1;
      for (let yy = 0; yy < 900; yy++) for (let xx = 0; xx < 2600; xx++) if (d[(yy * 2600 + xx) * 4 + 3] > 110) { if (xx < x0) x0 = xx; if (xx > x1) x1 = xx; if (yy < y0) y0 = yy; if (yy > y1) y1 = yy; }
      const mm = x.measureText(t); const asc = mm.fontBoundingBoxAscent, desc = mm.fontBoundingBoxDescent;
      return { x0: x0 - 100, x1: x1 + 1 - 100, y0: y0 - 500, y1: y1 + 1 - 500, t2b: (size - (asc + desc)) / 2 + asc, adv: mm.width };
    }, [it.text, it.fam, it.wt, it.size, it.ls]);
    const inkW = m.x1 - m.x0; const inkX0 = it.anchor === 'center' ? it.x - inkW / 2 : it.x;
    const left = inkX0 - m.x0, top = it.base - m.t2b;
    out[it.id] = { left: +left.toFixed(2), top: +top.toFixed(2), ink: [+inkX0.toFixed(1), +(it.base + m.y0).toFixed(1), +(inkX0 + inkW).toFixed(1), +(it.base + m.y1).toFixed(1)], size: it.size, ls: it.ls };
  }
  fs.writeFileSync(outPath, JSON.stringify(out, null, 1)); console.log(JSON.stringify(out));
  await b.close();
})();
