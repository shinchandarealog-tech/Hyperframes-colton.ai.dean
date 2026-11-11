const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920}});
p.on('console',m=>console.log('console',m.type(),m.text())); p.on('pageerror',e=>console.log('pageerror',e.message));
await p.goto('http://localhost:8799/index.html'); await p.waitForTimeout(3000);
console.log(await p.evaluate(()=>({tl:!!(window.__timelines&&window.__timelines.main), dur:window.__timelines.main&&window.__timelines.main.duration(), layers:document.querySelectorAll('.beat-layer').length, grp:document.querySelectorAll('.grp').length, glass:document.querySelectorAll('.glass').length})));
await p.evaluate(()=>window.__timelines.main.seek(1.7,false)); await p.waitForTimeout(300);
console.log(await p.evaluate(()=>{const l=document.getElementById('b1-front'); const g=l.querySelector('.grp'); return {op:getComputedStyle(l).opacity, gtop:g&&g.style.top, word:g&&getComputedStyle(g.querySelector('.e span')).opacity}}));
await b.close();})();
