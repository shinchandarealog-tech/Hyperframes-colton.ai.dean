const {chromium}=require('playwright');const fs=require('fs');
const S=JSON.parse(fs.readFileSync('spec/_tools/samples.json'));
const C={sans:[['Jost',300],['Jost',400],['Urbanist',300],['Urbanist',400],['Outfit',300],['Outfit',200],['Josefin Sans',300],['Montserrat',300],['Poppins',300],['Questrial',400],['Lexend',300],['Raleway',300],['Plus Jakarta Sans',300]],
 serif:[['Playfair Display',700],['Playfair Display',800],['Playfair Display',900],['DM Serif Display',400],['Bodoni Moda',700],['Bodoni Moda',800],['Gloock',400],['Abril Fatface',400],['Libre Caslon Display',400],['Prata',400]]};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2400,height:400}});
await p.goto('file://'+process.cwd()+'/web/blank.html');
fs.mkdirSync('an/fc',{recursive:true});
for(const [n,s] of Object.entries(S)){const kind=n.split('_')[0];const ital=/sugars/.test(n);
 for(const [fam,w] of C[kind]){
  await p.evaluate(([fam,w,t,ital])=>{document.body.innerHTML=`<span id=t style="font-family:'${fam}';font-weight:${w};font-style:${ital?'italic':'normal'};font-size:200px;color:#fff;white-space:pre;display:inline-block;padding:20px">${t}</span>`},[fam,w,s.text,ital]);
  await p.evaluate(async([fam,w,ital])=>{await document.fonts.load(`${ital?'italic ':''}${w} 200px '${fam}'`);await document.fonts.ready},[fam,w,ital]);
  await p.locator('#t').screenshot({path:`an/fc/${n}__${fam.replace(/ /g,'_')}_${w}.png`});
 }}
await b.close();})();
