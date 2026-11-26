const { chromium } = require('playwright'); const path=require('path');
const T=[['empty tip','80','', '2'],['tie: $10.70 +15%','10.70','15','1'],['1,000 people','100','0','1000'],['bill 1e2','1e2','0','2'],['tiny bill $0.001','0.001','0','1'],['people 3.0','30','0','3.0'],['tip 0.5%','99.99','0.5','3'],['huge bill','99999999.99','20','7']];
(async()=>{const b=await chromium.launch();
for(const a of ['chatgpt','claude','gemini']){ console.log('== '+a);
 for(const [n,t,tp,p] of T){const pg=await b.newPage(); await pg.goto('file://'+path.resolve('apps/'+a+'.html'));
  await pg.fill('#total',t); await pg.fill('#tip',tp); await pg.fill('#people',p); const t0=Date.now(); await pg.click('#calc'); await pg.waitForTimeout(100);
  const r=(await pg.innerText('#result')).trim().split('\n'); console.log(n.padEnd(20), (Date.now()-t0)+'ms', r.length+' lines', JSON.stringify(r.slice(0,3)), r.length>3?JSON.stringify(r.slice(-1)):''); await pg.close();}}
await b.close();})();
