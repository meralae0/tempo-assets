import json,subprocess,re,os,wave,numpy as np,sys
sys.path.insert(0,'../../tools')
TR=json.load(open('transcript.json')); S=json.load(open('script.json'))
def sil(wav):
    out=subprocess.run(['ffmpeg','-i',wav,'-af','silencedetect=n=-40dB:d=0.15','-f','null','-'],capture_output=True,text=True).stderr
    return list(zip(map(float,re.findall(r'silence_start: ([\d.]+)',out)),map(float,re.findall(r'silence_end: ([\d.]+)',out))))
def rd(p):
    w=wave.open(p);a=np.frombuffer(w.readframes(w.getnframes()),np.int16);return a
def wr(p,a):
    w=wave.open(p,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(a.astype(np.int16).tobytes());w.close()
SR=24000
# fix doubled "deux"
a=rd('raw/fr_A.wav'); a=np.concatenate([a[:int(104.82*SR)],a[int(105.58*SR):]]); wr('raw/fr_A_fix.wav',a)
TR['fr_A']=[[s-(0.76 if s>105 else 0),e-(0.76 if e>105 else 0),t] for s,e,t in TR['fr_A']]
del TR['fr_A'][28]  # "2, 2." merged: re-insert as start of next
TR['fr_A'][28][0]=104.46; TR['fr_A'][28][2]='Deux : '+TR['fr_A'][28][2]
starts={'fr_A':[0,3,7,12,18,21,28,30],'fr_B':[0,3,5,8],'en_A':[0,5,9,15,22,25,32,35],'en_B':[0,4,6,11]}
ids={'fr':['seg01','seg02','seg03','seg04','seg05','seg06','seg07','seg08','seg10','seg11','seg12','seg13']}
ids['en']=ids['fr']
os.makedirs('audio/fr',exist_ok=True);os.makedirs('audio/en',exist_ok=True)
for lang in ['fr','en']:
    k=0
    for part in 'AB':
        key=f'{lang}_{part}'; src='raw/fr_A_fix.wav' if key=='fr_A' else f'raw/{key}.wav'
        a=rd(src); D=len(a)/SR; ss=sil(src); tr=TR[key]; st=starts[key]
        cuts=[0.0]
        for i in st[1:]:
            mid=(tr[i-1][1]+tr[i][0])/2
            s,e=min(ss,key=lambda x:abs((x[0]+x[1])/2-mid))
            cuts.append((s+e)/2)
        cuts.append(D)
        for j in range(len(st)):
            sid=ids[lang][k]; k+=1
            seg=a[int(cuts[j]*SR):int(cuts[j+1]*SR)]; wr(f'audio/{lang}/raw_{sid}.wav',seg)
            subprocess.run(['python3','../../tools/tighten.py',f'audio/{lang}/raw_{sid}.wav',f'audio/{lang}/{sid}.wav','0.42','0.35'],check=True)
            print(lang,sid,round(cuts[j],2),round(cuts[j+1]-cuts[j],2), [t[2][:25] for t in tr if cuts[j]<=t[0]<cuts[j+1]][:1])
json.dump(TR,open('transcript_fixed.json','w'),ensure_ascii=False)
