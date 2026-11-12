const {chromium}=require('playwright');const fs=require('fs');
const S=JSON.parse(fs.readFileSync('spec/_tools/samples.json'));
const C={sans:[['Urbanist',300],['Urbanist',400],['Urbanist',500],['Outfit',300],['Outfit',400]],serif:[['DM Serif Display',400],['Playfair Display',700]]};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2400,height:400}});
await p.goto('file://'+process.cwd()+'/web/blank.html');fs.rmSync('an/ft',{recursive:true,force:true});fs.mkdirSync('an/ft',{recursive:true});
for(const [n,s] of Object.entries(S)){const kind=n.split('_')[0];const ital=/sugars/.test(n);
 for(const [fam,w] of C[kind]) for(const ls of [0,-0.02,-0.04,-0.06,-0.08]){
  await p.evaluate(async([fam,w,t,ital,ls])=>{document.body.innerHTML=`<span id=t style="font-family:'${fam}';font-weight:${w};font-style:${ital?'italic':'normal'};font-size:200px;letter-spacing:${ls}em;color:#fff;white-space:pre;display:inline-block;padding:20px 60px">${t}</span>`;await document.fonts.load(`${ital?'italic ':''}${w} 200px '${fam}'`);await document.fonts.ready},[fam,w,s.text,ital,ls]);
  await p.locator('#t').screenshot({path:`an/ft/${n}__${fam.replace(/ /g,'_')}_${w}_${ls}.png`});
 }}
await b.close();})();
