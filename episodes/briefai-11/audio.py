import json,subprocess,os
T=json.load(open('timing.json')); D=T['D']; V='/home/claude/tempo-assets/episodes/briefai-11/voice'
MUS='/home/claude/tempo-assets/episodes/briefai-01/music.mp3'; os.makedirs('aud',exist_ok=True)
def run(a): subprocess.run(a,check=True)
for l in ['fr','en']:
    parts=[]
    for i,(a,b) in enumerate(T[l]):
        seg=b-a; tgt=D[i]-0.3; f=f'aud/{l}{i:02d}.wav'
        tempo=max(1.0,seg/tgt)
        af=f"atrim={a}:{b},asetpts=N/SR/TB" + (f",atempo={tempo:.4f}" if tempo>1.001 else "") + f",apad=whole_dur={D[i]}"
        run(['ffmpeg','-y','-v','error','-i',f'{V}/{l}.wav','-af',af,'-ar','48000','-ac','1',f]); parts.append(f)
    open(f'aud/{l}.txt','w').write(''.join(f"file '{os.path.basename(p)}'\n" for p in parts))
    run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',f'aud/{l}.txt','-c','copy',f'aud/{l}_voice.wav'])
    tot=sum(D)
    run(['ffmpeg','-y','-v','error','-i',f'aud/{l}_voice.wav','-stream_loop','-1','-i',MUS,'-filter_complex',
         f"[1:a]volume=0.07,atrim=0:{tot},afade=t=out:st={tot-2}:d=2[m];[0:a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.8,loudnorm=I=-14:TP=-2[o]",
         '-map','[o]','-ar','48000','-ac','2',f'aud/{l}_mix.wav'])
    print(l,'ok')
