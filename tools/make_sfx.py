# Effets sonores maison (libres de droits) : whoosh, pop, click, ding, riser, typing
import numpy as np, wave, os
SR=48000; O=os.path.join(os.path.dirname(__file__),'sfx')
def save(n,x):
    x=np.clip(x/ (np.abs(x).max()+1e-9)*0.8,-1,1); s=(x*32767).astype(np.int16)
    with wave.open(f'{O}/{n}.wav','w') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.repeat(s,2).tobytes())
t=lambda d: np.linspace(0,d,int(SR*d),False)
rng=np.random.default_rng(7)
# whoosh : bruit filtré balayé
d=0.45; n=rng.standard_normal(int(SR*d)); env=np.sin(np.pi*np.linspace(0,1,len(n)))**2
f=np.linspace(300,3000,len(n)); ph=np.cumsum(f)/SR; w=n*env*(0.5+0.5*np.sin(2*np.pi*ph*0.02))
k=np.ones(40)/40; save('whoosh',np.convolve(w,k,'same'))
# pop : sinus descendant court
tt=t(0.12); save('pop',np.sin(2*np.pi*(900-5000*tt)*tt)*np.exp(-tt*40))
# click : impulsion
tt=t(0.03); save('click',rng.standard_normal(len(tt))*np.exp(-tt*300))
# ding : 2 partiels
tt=t(0.9); save('ding',(np.sin(2*np.pi*1320*tt)+0.5*np.sin(2*np.pi*1980*tt))*np.exp(-tt*5))
# error buzz
tt=t(0.35); save('buzz',np.sign(np.sin(2*np.pi*140*tt))*np.exp(-tt*6)*0.6)
# riser
tt=t(1.2); save('riser',rng.standard_normal(len(tt))*np.linspace(0,1,len(tt))**2*0.6+np.sin(2*np.pi*(200+600*tt)*tt)*np.linspace(0,1,len(tt))*0.4)
print(sorted(os.listdir(O)))
