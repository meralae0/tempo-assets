// node test_app.js apps/x.html -> JSON results
const { chromium } = require('playwright');
const path = require('path');
const CASES = [
 {id:1, name:'$100, 15% tip, 2 people', total:'100', tip:'15', people:'2', want:['57.50','57.50']},
 {id:2, name:'$10, no tip, 3 people (cents)', total:'10', tip:'0', people:'3', want:['3.34','3.33','3.33']},
 {id:3, name:'$19.99, 20% tip, 3 people', total:'19.99', tip:'20', people:'3', want:['8.00','8.00','7.99']},
 {id:4, name:'5 cents, 7 people', total:'0.05', tip:'0', people:'7', want:['0.01','0.01','0.01','0.01','0.01','0.00','0.00']},
 {id:5, name:'$33.33, 15% tip, 1 person', total:'33.33', tip:'15', people:'1', want:['38.33']},
 {id:6, name:'$1,234.56, 12.5% tip, 6 people', total:'1234.56', tip:'12.5', people:'6', want:['231.48','231.48','231.48','231.48','231.48','231.48']},
 {id:7, name:'defaults: $80 only', total:'80', want:['46.00','46.00']},
 {id:13, name:'$4.35, no tip, 1 person (float trap)', total:'4.35', tip:'0', people:'1', want:['4.35']},
 {id:14, name:'10 cents, 3 people', total:'0.1', tip:'0', people:'3', want:['0.04','0.03','0.03']},
 {id:8, name:'empty bill', total:'', tip:'15', people:'2', invalid:true},
 {id:9, name:'negative bill', total:'-20', tip:'15', people:'2', invalid:true},
 {id:10, name:'2.5 people', total:'50', tip:'15', people:'2.5', invalid:true},
 {id:11, name:'0 people', total:'50', tip:'15', people:'0', invalid:true},
 {id:12, name:'negative tip', total:'50', tip:'-5', people:'2', invalid:true},
];
(async () => {
  const file = path.resolve(process.argv[2]);
  const b = await chromium.launch(); const out = {file, cases:[], errors:[]};
  for (const c of CASES) {
    const p = await b.newPage(); const errs=[];
    p.on('pageerror', e=>errs.push(String(e))); p.on('dialog', d=>{errs.push('dialog:'+d.message()); d.dismiss();});
    await p.goto('file://'+file);
    let got='', pass=false, note='';
    try {
      const ids = ['#total','#tip','#people','#calc','#result'];
      for (const s of ids) if (!(await p.$(s))) throw new Error('missing '+s);
      if (c.total!==undefined) await p.fill('#total', c.total);
      if (c.tip!==undefined) await p.fill('#tip', c.tip);
      if (c.people!==undefined) await p.fill('#people', c.people);
      await p.click('#calc'); await p.waitForTimeout(150);
      got = (await p.innerText('#result')).trim();
      const lines = [...got.matchAll(/Person\s+(\d+):\s*\$([\d,]+\.\d{2})/g)].map(m=>m[2].replace(/,/g,''));
      if (c.invalid) { pass = /Invalid input/.test(got) && lines.length===0; }
      else { pass = JSON.stringify(lines)===JSON.stringify(c.want); if(!pass) note='got '+JSON.stringify(lines); }
    } catch(e) { note = String(e.message||e); }
    out.cases.push({id:c.id, name:c.name, pass, got:got.slice(0,300), note, errs});
    await p.close();
  }
  out.score = out.cases.filter(x=>x.pass).length;
  console.log(JSON.stringify(out, null, 1)); await b.close();
})();
