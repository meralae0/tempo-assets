import json,subprocess,re,os,wave,numpy as np
TR=json.load(open('raw/transcript.json'));SR=24000
def sil(wav):
    out=subprocess.run(['ffmpeg','-i',wav,'-af','silencedetect=n=-40dB:d=0.15','-f','null','-'],capture_output=True,text=True).stderr
    return list(zip(map(float,re.findall(r'silence_start: ([\d.]+)',out)),map(float,re.findall(r'silence_end: ([\d.]+)',out))))
def rd(p):w=wave.open(p);return np.frombuffer(w.readframes(w.getnframes()),np.int16)
def wr(p,a):
    w=wave.open(p,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(a.astype(np.int16).tobytes());w.close()
starts={'fr_A':[0,3,8,15,23],'fr_B':[0,7,11,15],'en_A':[0,4,9,17,27],'en_B':[0,8,12,16]}
ids=['seg01','seg02','seg03','seg04','seg05','seg06','seg07','seg08','seg09']
for l in ['fr','en']:
    os.makedirs(f'audio/{l}',exist_ok=True);k=0
    for part in 'AB':
        key=f'{l}_{part}';src=f'raw/{key}.wav';a=rd(src);D=len(a)/SR;ss=sil(src);tr=TR[key]['sentences']
        cuts=[0.0]
        for i in starts[key][1:]:
            mid=(tr[i-1]['end']+tr[i]['start'])/2
            s,e=min(ss,key=lambda x:abs((x[0]+x[1])/2-mid));cuts.append((s+e)/2)
        if key=='en_B': cuts[3]=47.4
        cuts.append(D)
        for j in range(len(starts[key])):
            sid=ids[k];k+=1;wr(f'audio/{l}/raw_{sid}.wav',a[int(cuts[j]*SR):int(cuts[j+1]*SR)])
            subprocess.run(['python3','../../tools/tighten.py',f'audio/{l}/raw_{sid}.wav',f'audio/{l}/t_{sid}.wav','0.42','0.35'],check=True,capture_output=True)
# pad to common length
for sid in ids:
    A={l:rd(f'audio/{l}/t_{sid}.wav') for l in ['fr','en']};n=max(len(x) for x in A.values())
    for l in A: wr(f'audio/{l}/{sid}.wav',np.concatenate([A[l],np.zeros(n-len(A[l]),np.int16)]))
    print(sid,{l:round(len(A[l])/SR,2) for l in A},'->',round(n/SR,2))
