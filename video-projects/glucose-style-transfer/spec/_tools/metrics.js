const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+process.cwd()+'/web/blank.html');
const r=await p.evaluate(async()=>{const out={};
for(const [fam,w,st] of [['Outfit',300,'normal'],['DM Serif Display',400,'normal'],['DM Serif Display',400,'italic']]){
 await document.fonts.load(`${st} ${w} 200px '${fam}'`);
 const c=document.createElement('canvas');c.width=600;c.height=400;const x=c.getContext('2d');x.font=`${st} ${w} 200px '${fam}'`;
 const m=k=>x.measureText(k);out[fam+'_'+st]={cap:m('H').actualBoundingBoxAscent/200,xh:m('x').actualBoundingBoxAscent/200,asc:m('b').actualBoundingBoxAscent/200,desc:m('p').actualBoundingBoxDescent/200};}
return out});console.log(JSON.stringify(r));await b.close();})();
