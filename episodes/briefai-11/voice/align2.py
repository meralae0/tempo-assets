import json,subprocess,re
S=json.load(open('sents.json')); out={}
for l in ['fr','en']:
    f=l+'.wav'
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
    log=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','silencedetect=noise=-38dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
    sil=[(a,b) for a,b in zip(st,en) if a>0.1 and b<dur-0.1]
    lead=0; tail=st[-1] if len(st)>len(en) or (en and abs(en[-1]-dur)<0.05) else dur
    L=[len(s) for s in S[l]]; tot=sum(L); n=len(L)
    est=[tail*sum(L[:i])/tot for i in range(1,n)]
    # DP: assign est[k] to silence j increasing; cost=(mid-est)^2 - bonus*dur
    import math
    M=len(sil); INF=1e18
    C=[[INF]*M for _ in range(n-1)]; P=[[-1]*M for _ in range(n-1)]
    def c(k,j): mid=(sil[j][0]+sil[j][1])/2; return (mid-est[k])**2 - 8*(sil[j][1]-sil[j][0])
    for j in range(M): C[0][j]=c(0,j)
    for k in range(1,n-1):
        best=INF;bj=-1
        for j in range(M):
            if j>0 and C[k-1][j-1]<best: best=C[k-1][j-1]; bj=j-1
            if bj>=0: C[k][j]=best+c(k,j); P[k][j]=bj
    j=min(range(M),key=lambda j:C[n-2][j]); idx=[]
    for k in range(n-2,-1,-1): idx.append(j); j=P[k][j]
    idx=idx[::-1]; starts=[0]+[round(sil[j][1]-0.08,2) for j in idx]
    out[l]={'dur':dur,'starts':starts,'end':tail}
    print(l,round(dur,1),starts); print('  est',[round(e,1) for e in est])
json.dump(out,open('align.json','w'),indent=1)
