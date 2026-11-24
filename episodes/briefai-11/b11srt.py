import json,re
T=json.load(open('timing.json')); D=T['D']; S=json.load(open('/home/claude/tempo-assets/episodes/briefai-11/voice/sents.json'))
def chunks(p):
    parts=re.split(r'(?<=[.!?…:])\s+',p); out=[]
    for s in parts:
        while len(s)>84:
            k=s.rfind(', ',0,84); k=k if k>20 else s.rfind(' ',0,80); out.append(s[:k+1].strip()); s=s[k+1:].strip()
        if s: out.append(s)
    return out
def ts(t): h=int(t//3600);m=int(t%3600//60);s=t%60; return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.',',')
def build(l,idx=None,offset=0):
    ent=[];t0=0
    for i in (idx if idx is not None else range(11)):
        a,b=T[l][i]; sp=min(b-a,D[i]-0.3); cs=chunks(S[l][i]); tot=sum(len(c) for c in cs); t=t0
        for c in cs:
            d=sp*len(c)/tot; ent.append((t,t+d,c)); t+=d
        t0+=D[i]
    return ent
def write(ent,f):
    open(f,'w').write('\n'.join(f"{k+1}\n{ts(a)} --> {ts(b)}\n{c}\n" for k,(a,b,c) in enumerate(ent)))
if __name__=='__main__':
    for l in ['fr','en']: write(build(l),f'b11_{l}.srt')
    print(open('b11_fr.srt').read()[:400])
