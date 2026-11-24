import json,subprocess,re,sys
S=json.load(open('sents.json'))
out={}
for l in ['fr','en']:
    f=l+'.wav'
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
    log=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','silencedetect=noise=-38dB:d=0.3','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]
    en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
    sil=list(zip(st,en))
    lead=en[0] if st and st[0]<0.05 else 0
    tail=st[-1] if en and abs(en[-1]-dur)<0.05 else dur
    L=[len(s) for s in S[l]]; tot=sum(L); cum=0; starts=[lead]
    used=set()
    for i in range(1,len(L)):
        cum+=L[i-1]; t=lead+(tail-lead)*cum/tot
        # nearest silence midpoint, prefer longer
        best=min([s for s in sil if s not in used and s[0]>starts[-1]+0.5],key=lambda s:abs((s[0]+s[1])/2-t)-0.6*(s[1]-s[0]))
        used.add(best); starts.append(round(best[1]-0.08,2))
    out[l]={'dur':dur,'starts':starts,'end':tail}
    print(l,round(dur,1),starts)
json.dump(out,open('align.json','w'),indent=1)
