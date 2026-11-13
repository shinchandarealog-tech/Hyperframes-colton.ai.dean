const { chromium } = require('playwright');
const sets = {
  script: { text: 'competing', w: 400, fonts: ['Great Vibes','Allura','Parisienne','Pinyon Script','Alex Brush','Italianno','Tangerine','Rouge Script','Mr De Haviland','Petit Formal Script','Herr Von Muellerhoff','Monsieur La Doulaise','Arizonia','Sacramento','Dancing Script','Playball','Yellowtail','Imperial Script','Ephesis','Corinthia','Mea Culpa','Meow Script','Kristi','Bilbo Swash Caps','Euphoria Script','Qwigley','Rochester','Niconne','Pacifico','Lavishly Yours','Ballet','Bad Script','Style Script','Water Brush','Birthstone','Licorice','Hurricane','Cookie'] , wt: 400},
  sans: { text: "You're not", w: 400, fonts: ['Inter','Inter Tight','Roboto','Arimo','Manrope','DM Sans','Figtree','Instrument Sans','Geist','Albert Sans','Archivo','Work Sans','Plus Jakarta Sans','Hanken Grotesk','Schibsted Grotesk','Onest','Public Sans','Poppins','Montserrat'], wt: 400 },
  bold: { text: 'price', w: 700, fonts: ['Inter','Inter Tight','Roboto','Arimo','Manrope','DM Sans','Figtree','Instrument Sans','Geist','Albert Sans','Archivo','Work Sans','Plus Jakarta Sans','Hanken Grotesk','Schibsted Grotesk','Onest','Public Sans','Poppins','Montserrat'], wt: 600 },
};
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 400 } });
  for (const [k, s] of Object.entries(sets)) for (const wt of (k==='bold'?[500,600,700,800]:k==='sans'?[300,400,500]:[400])) {
    const fam = s.fonts.map(f => 'family=' + f.replace(/ /g, '+') + (k==='script'?'':':wght@'+wt)).join('&');
    await p.setContent(`<html><head><link href="https://fonts.googleapis.com/css2?${fam}&display=block" rel="stylesheet"></head><body style="margin:0;background:#000"></body></html>`);
    await p.waitForLoadState('networkidle'); 
    for (const f of s.fonts) {
      await p.evaluate(([f, t, wt, ls]) => { document.body.innerHTML = `<div style="font-family:'${f}';font-weight:${wt};font-size:200px;color:#fff;letter-spacing:${ls};padding:60px;white-space:nowrap;display:inline-block">${t}</div>`; return document.fonts.ready; }, [f, s.text, wt, k==='script'?'0':'-0.06em']);
      await p.screenshot({ path: `an/font/${k}_${wt}_${f.replace(/ /g,'_')}.png` });
    }
  }
  await b.close();
})();
