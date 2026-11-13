const { chromium } = require('playwright');
// targets measured on ref (1080x1920): line1 "You're not" cap 432->480 (48px), ink x 407-647; price x-height 608->720 (112), ink x 332-730
const T = { l1: { text: "You're not", metric: 'H', h: 48, w: 240, x0: 407, base: 480 }, big: { text: 'price', metric: 'x', h: 112, w: 398, x0: 332, base: 720 }, on: {text:'on',metric:'x',h:35,w:60,x0:674,base:553} };
const fonts = ['Inter Tight', 'Inter', 'Arimo', 'Archivo', 'Geist', 'Figtree', 'Hanken Grotesk','Schibsted Grotesk','Instrument Sans'];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const fam = fonts.map(f => 'family=' + f.replace(/ /g, '+') + ':wght@300;400;500;600;700').join('&');
  await p.setContent(`<html><head><link href="https://fonts.googleapis.com/css2?${fam}&display=block" rel="stylesheet"></head><body style="margin:0;background:#000"><canvas id=c width=1080 height=1920></canvas></body></html>`);
  await p.waitForLoadState('networkidle'); await p.evaluate(() => document.fonts.ready);
  const out = [];
  for (const f of fonts) for (const [k, t] of Object.entries(T)) for (const wt of (k === 'big' ? [500, 600, 700] : [300, 400, 500])) {
    const r = await p.evaluate(async ([f, t, wt]) => {
      await document.fonts.load(`${wt} 100px '${f}'`);
      const c = document.getElementById('c'), x = c.getContext('2d');
      x.font = `${wt} 100px '${f}'`; const m = x.measureText(t.metric);
      const size = t.h / (m.actualBoundingBoxAscent) * 100;
      x.font = `${wt} ${size}px '${f}'`; x.letterSpacing = '0px';
      const mw = x.measureText(t.text); const ink0 = mw.actualBoundingBoxLeft + mw.actualBoundingBoxRight;
      const ls = (t.w - ink0) / (t.text.length - 1);
      return { size: +size.toFixed(1), ls_em: +(ls / size).toFixed(4) };
    }, [f, t, wt]);
    // render calibrated and grab pixels
    const png = await p.evaluate(async ([f, t, wt, r]) => {
      const c = document.getElementById('c'), x = c.getContext('2d'); x.fillStyle = '#000'; x.fillRect(0, 0, 1080, 1920);
      x.font = `${wt} ${r.size}px '${f}'`; x.letterSpacing = (r.ls_em * r.size) + 'px'; x.fillStyle = '#fff';
      const m = x.measureText(t.text); x.fillText(t.text, t.x0 + m.actualBoundingBoxLeft, t.base); return c.toDataURL('image/png');
    }, [f, t, wt, r]);
    const fn = `an/font/cal_${k}_${f.replace(/ /g, '_')}_${wt}.png`; require('fs').writeFileSync(fn, Buffer.from(png.split(',')[1], 'base64'));
    out.push({ k, f, wt, ...r, fn });
  }
  require('fs').writeFileSync('an/font/calib.json', JSON.stringify(out, null, 1)); await b.close();
})();
