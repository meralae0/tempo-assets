const {encode}=require('/tmp/claude-0/tok/node_modules/gpt-tokenizer/cjs/encoding/o200k_base.js');
const fs=require('fs');
const split=f=>fs.readFileSync(f,'utf8').split(/^=== (Q\d) ===\s*$/m).slice(1);
const pairs=f=>{const s=split(f),o={};for(let i=0;i<s.length;i+=2)o[s[i]]=s[i+1].trim();return o};
const A=pairs(process.argv[2]),B=pairs(process.argv[3]);let ta=0,tb=0;
for(const q of Object.keys(A)){const a=encode(A[q]).length,b=encode(B[q]||'').length;ta+=a;tb+=b;console.log(q,a,b,Math.round((1-b/a)*100)+'%')}
console.log('TOTAL',ta,tb,Math.round((1-tb/ta)*100)+'%');
