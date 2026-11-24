import json,subprocess,sys,os
sys.path.append("/home/claude/tempo-assets/tools"); from gfx_ai import sg,mono,background,glow_text,WHITE,CYAN,RED,BG
from PIL import Image,ImageDraw
from b12srt import build,write
T=json.load(open('timing.json')); D=T['D']
SH={'s1':([0,7,8,9],'J\'ajoute 50 € de courses…\nle budget de Claude\nne bouge pas','Claude + vrai fichier Excel · test réel',RED),
    's2':([0,3,4],'49 lignes de relevé,\nClaude calcule de tête :\njuste au centime ?','3 essais · vérifié par programme',CYAN)}
def run(a): subprocess.run(a,check=True)
for k,(idx,hook,sub,col) in SH.items():
    bg=Image.new('RGBA',(1080,1920),BG+(255,)); g=background().resize((1080*2,1920)).crop((540,0,1620,1920)); bg.alpha_composite(g)
    d=ImageDraw.Draw(bg); fz=92
    while fz>50 and max(d.textlength(l,font=sg(fz)) for l in hook.split('\n'))>1000: fz-=4
    d.multiline_text((540,330),hook,font=sg(fz),fill=col+(255,),anchor='mm',align='center',spacing=14)
    d.text((540,560),sub,font=mono(34),fill=(200,206,220,255),anchor='mm')
    d.text((540,1830),'BriefAI · Je teste pour toi',font=mono(32),fill=(130,140,160,255),anchor='mm')
    bg.convert('RGB').save(f'{k}_bg.png')
    open(f'{k}.txt','w').write(''.join(f"file 'seg/s{i+1:02d}.mp4'\n" for i in idx))
    run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',f'{k}.txt','-c','copy',f'{k}_v.mp4'])
    open(f'{k}_a.txt','w').write(''.join(f"file 'aud/fr{i:02d}.wav'\n" for i in idx))
    run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',f'{k}_a.txt','-c','copy',f'{k}_a.wav'])
    write(build('fr',idx),f'{k}.srt'); tot=sum(D[i] for i in idx)
    style="FontName=Space Grotesk,FontSize=11,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=62,MarginL=30,MarginR=30"
    run(['ffmpeg','-y','-v','error','-loop','1','-i',f'{k}_bg.png','-i',f'{k}_v.mp4','-i',f'{k}_a.wav','-stream_loop','-1','-i','/home/claude/tempo-assets/episodes/briefai-01/music.mp3',
      '-filter_complex',f"[1:v]scale=1080:608[v1];[0:v][v1]overlay=0:700:shortest=1,subtitles={k}.srt:fontsdir=/home/claude/tempo-assets/brand:force_style='{style}',format=yuv420p[v];[3:a]volume=0.07[m];[2:a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.8,loudnorm=I=-14:TP=-2[a]",
      '-map','[v]','-map','[a]','-t',f'{tot:.2f}','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k',f'out_{k}.mp4'])
    print(k,tot)
