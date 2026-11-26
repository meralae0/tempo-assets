const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch();
for(const a of ['chatgpt','claude','gemini']){
 const pg=await b.newPage({viewport:{width:390,height:780},deviceScaleFactor:2});
 await pg.goto('file://'+path.resolve('apps/'+a+'.html'));
 await pg.fill('#total','10'); await pg.fill('#tip','0'); await pg.fill('#people','3'); await pg.click('#calc'); await pg.waitForTimeout(200);
 await pg.screenshot({path:`caps/app_${a}_phone.png`});
 await pg.fill('#total','4.35'); await pg.fill('#people','1'); await pg.click('#calc'); await pg.waitForTimeout(150); await pg.screenshot({path:`caps/app_${a}_435.png`});
 await pg.fill('#total','80'); await pg.fill('#tip',''); await pg.fill('#people','2'); await pg.click('#calc'); await pg.waitForTimeout(150); await pg.screenshot({path:`caps/app_${a}_emptytip.png`});
 await pg.close();}
await b.close();})();
