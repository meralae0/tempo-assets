// Captures pages A (sans skill) / B (avec skill). Fonts Google + photos externes servies en local (proxy bloque).
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const F='/tmp/claude-0/x/fonts/node_modules/';const IMG='/tmp/claude-0/x/runB/out/assets/img/';
const photos=['photo-m187311853-2400.webp','photo-m28989985-1200.webp','photo-m147143898-1200.webp'];
const fontCss=`@font-face{font-family:'Fraunces';src:url(https://local.font/fraunces.woff2) format('woff2');font-weight:100 900}
@font-face{font-family:'Nunito';src:url(https://local.font/nunito.woff2) format('woff2');font-weight:200 1000}
${[400,500,600].map(w=>`@font-face{font-family:'Inter';src:url(https://local.font/inter${w}.woff2) format('woff2');font-weight:${w}}`).join('\n')}`;
const fontFiles={'fraunces.woff2':F+'@fontsource-variable/fraunces/files/fraunces-latin-wght-normal.woff2','nunito.woff2':F+'@fontsource-variable/nunito/files/nunito-latin-wght-normal.woff2',
'inter400.woff2':F+'@fontsource/inter/files/inter-latin-400-normal.woff2','inter500.woff2':F+'@fontsource/inter/files/inter-latin-500-normal.woff2','inter600.woff2':F+'@fontsource/inter/files/inter-latin-600-normal.woff2'};
const OUT=__dirname+'/caps/';
(async()=>{const b=await chromium.launch();
for(const [k,url] of [['A','file:///home/claude/tempo-assets/docs/briefai-10-taste/sans-skill/index.html'],['B','file:///home/claude/tempo-assets/docs/briefai-10-taste/avec-skill/index.html']]){
 for(const [vp,w,h] of [['desk',1440,900],['mob',390,844]]){
  const ctx=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:vp=='mob'?2:1.5,recordVideo:vp=='desk'?{dir:OUT+'vid_'+k,size:{width:1440,height:900}}:undefined});
  let n=0;const map={};
  await ctx.route(/fonts\.googleapis\.com/,r=>r.fulfill({contentType:'text/css',body:fontCss}));
  await ctx.route(/local\.font/,r=>r.fulfill({contentType:'font/woff2',body:fs.readFileSync(fontFiles[r.request().url().split('/').pop()])}));
  await ctx.route(/unsplash\.com/,r=>{const u=r.request().url().split('?')[0];if(!(u in map))map[u]=photos[(n++)%3];r.fulfill({contentType:'image/webp',body:fs.readFileSync(IMG+map[u])})});
  await ctx.route(/openstreetmap\.org\/export/,r=>r.fulfill({contentType:'text/html',body:'<body style="margin:0;background:#e8e4da;font:14px sans-serif;display:grid;place-items:center;height:100vh;color:#777">carte OpenStreetMap</body>'}));
  const p=await ctx.newPage();await p.goto(url,{waitUntil:'networkidle'}).catch(()=>{});await p.waitForTimeout(2500);
  await p.screenshot({path:`${OUT}${k}_${vp}_hero.png`});
  // scroll lent pour déclencher les animations
  const H=await p.evaluate(()=>document.documentElement.scrollHeight);
  for(let y=0;y<H;y+=vp=="desk"?14:40){await p.evaluate(v=>scrollTo(0,v),y);await p.waitForTimeout(vp=="desk"?16:5);}
  await p.waitForTimeout(800);await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(800);
  await p.screenshot({path:`${OUT}${k}_${vp}_full.png`,fullPage:true});
  console.log(k,vp,'height',H);
  await ctx.close();}
}
await b.close();})();
