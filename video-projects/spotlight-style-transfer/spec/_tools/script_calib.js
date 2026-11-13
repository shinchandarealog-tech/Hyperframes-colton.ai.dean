const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
 await p.setContent(`<link href="https://fonts.googleapis.com/css2?family=Italianno&display=block" rel="stylesheet"><canvas id=c></canvas>`); await p.waitForLoadState('networkidle');
 const r = await p.evaluate(async () => { await document.fonts.load("100px Italianno"); const x = document.getElementById('c').getContext('2d'); x.font = "100px Italianno"; const m = x.measureText('competing');
  return { w: m.actualBoundingBoxLeft + m.actualBoundingBoxRight, asc: m.actualBoundingBoxAscent, desc: m.actualBoundingBoxDescent, xh: x.measureText('o').actualBoundingBoxAscent }; });
 console.log(JSON.stringify(r)); await b.close(); })();
