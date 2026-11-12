// Calibrate text: for each item, fit font-size to the measured ink height, letter-spacing to the ink width,
// and CSS left/top so the rendered ink lands on the measured ink box. Prints JSON.
const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{
const [itemsPath, fontsDir, outPath] = process.argv.slice(2);
const items = JSON.parse(fs.readFileSync(itemsPath,'utf8'));
const f64 = n => fs.readFileSync(path.join(fontsDir,n)).toString('base64');
const css = `@font-face{font-family:'Inter';src:url(data:font/woff2;base64,${f64('Inter-var-latin.woff2')}) format('woff2');font-weight:100 900;}
@font-face{font-family:'Bebas Neue';src:url(data:font/woff2;base64,${f64('BebasNeue-latin.woff2')}) format('woff2');}
html,body{margin:0;background:transparent} span{position:absolute;left:100px;top:100px;line-height:1;white-space:pre;color:#000;font-optical-sizing:auto;font-kerning:normal}`;
const b = await chromium.launch(); const pg = await b.newPage({viewport:{width:1600,height:600}});
await pg.setContent(`<style>${css}</style><span id=s></span>`); await pg.evaluate(()=>document.fonts.ready);
// decode PNG alpha with sharp-free approach: use the browser itself to compute ink bbox from a canvas
async function ink(it,size,lsEm){
  return await pg.evaluate(async ([t,fam,wt,size,ls])=>{
    const c=document.createElement('canvas');c.width=1600;c.height=700;const x=c.getContext('2d');
    x.font=`${wt} ${size}px '${fam}'`; x.letterSpacing=(ls*size)+'px'; x.fontKerning='normal'; x.textBaseline='alphabetic';
    x.fillStyle='#000'; x.fillText(t,100,400);
    const d=x.getImageData(0,0,1600,700).data; let x0=1e9,y0=1e9,x1=-1,y1=-1;
    for(let yy=0;yy<700;yy++)for(let xx=0;xx<1600;xx++){if(d[(yy*1600+xx)*4+3]>110){if(xx<x0)x0=xx;if(xx>x1)x1=xx;if(yy<y0)y0=yy;if(yy>y1)y1=yy;}}
    // DOM metrics for converting baseline -> CSS top with line-height:1
    const s=document.getElementById('s');s.textContent=t;s.style.fontFamily=`'${fam}'`;s.style.fontWeight=wt;s.style.fontSize=size+'px';s.style.letterSpacing=(ls*size)+'px';
    const m=x.measureText(t); const r=s.getBoundingClientRect();
    // baseline position inside a line-height:1 box: half-leading model
    const asc=m.fontBoundingBoxAscent, desc=m.fontBoundingBoxDescent; const top_to_base=(size-(asc+desc))/2+asc;
    return {x0:x0-100,x1:x1+1-100,y0:y0-400,y1:y1+1-400,top_to_base,h:r.height};
  },[it.t,it.fam,it.wt,size,lsEm]);
}
const out={};
for(const it of items){
  const [tx0,ty0,tx1,ty1]=it.ink; let size=it.size0, ls=it.ls, m;
  for(let i=0;i<4;i++){
    m=await ink(it,size,ls);
    const H=m.y1-m.y0, TH=ty1-ty0; if(!it.sizeFrom) size=size*TH/H;
    m=await ink(it,size,ls);
    if(it.fitw!==false && it.t.length>1){ const W=m.x1-m.x0, TW=tx1-tx0; ls=ls+(TW-W)/((it.t.length-1)*size); }
  }
  if(it.sizeFrom){ size=out[it.sizeFrom].size; ls=out[it.sizeFrom].lsEm; }
  m=await ink(it,size,ls);
  const left=tx0-m.x0, base=(it.fith==='bottom'||true)? ty1 - m.y1 : 0;  // baseline y in frame = ty1 - (ink bottom below baseline)
  const top=base - m.top_to_base;
  out[it.id]={t:it.t,fam:it.fam,wt:it.wt,size:+size.toFixed(2),lsEm:+ls.toFixed(4),left:+left.toFixed(1),top:+top.toFixed(1),baseline:+base.toFixed(1),
    inkW:m.x1-m.x0,targetW:tx1-tx0,inkH:m.y1-m.y0,targetH:ty1-ty0};
}
fs.writeFileSync(outPath,JSON.stringify(out,null,1)); console.log(JSON.stringify(out,null,0).replace(/},/g,'},\n'));
await b.close();
})();
