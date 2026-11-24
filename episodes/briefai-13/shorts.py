# 2 Shorts 9:16 à partir du long (segments vidéo + audio final)
import subprocess, os, sys
sys.path.insert(0,'/home/claude/tempo-assets/tools')
from gfx_ai import sg, WHITE, RED, GREEN, BG
from PIL import Image, ImageDraw
L='/home/claude/tempo-assets/pub/b13/b13_demo.mp4'; OUT='/home/claude/tempo-assets/pub/b13'
SH={'s1':([(0,10.6),(43.5,62.0),(86.0,95.8)],'ChatGPT told me $684.31.\nThe real answer: $694.35'),
    's2':([(10.6,24.9),(86.0,95.8),(95.8,104.13)],'Same bank statement.\nWhich AI got it right?')}
def bg(hook,name):
    im=Image.new('RGB',(1080,1920),BG); d=ImageDraw.Draw(im)
    f=sg(78); lines=hook.split('\n')
    while max(d.textlength(l,font=f) for l in lines)>1000: f=sg(f.size-4)
    y=300
    for k,l in enumerate(lines):
        d.text((540,y),l,font=f,fill=(RED if (name=='s1' and k==0) else (GREEN if name=='s1' else WHITE)),anchor='mm'); y+=f.size+30
    d.text((540,1600),'BriefAI · real tests, real numbers',font=sg(40,500),fill=(130,140,160),anchor='mm')
    p=f'/home/claude/b13/{name}_bg.png'; im.save(p); return p
for name,(segs,hook) in SH.items():
    parts=[]
    for k,(a,b) in enumerate(segs):
        o=f'/home/claude/b13/{name}_{k}.mp4'
        subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(a),'-to',str(b),'-i',L,'-c:v','libx264','-preset','fast','-crf','18','-c:a','aac','-b:a','192k',o],check=True); parts.append(o)
    lst=f'/home/claude/b13/{name}.txt'; open(lst,'w').write(''.join(f"file '{p}'\n" for p in parts))
    cat=f'/home/claude/b13/{name}_cat.mp4'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',lst,'-c','copy',cat],check=True)
    b=bg(hook,name)
    subprocess.run(['ffmpeg','-loglevel','error','-y','-loop','1','-i',b,'-i',cat,'-filter_complex','[1:v]crop=1520:1080,scale=1080:-2[v];[0:v][v]overlay=0:(H-h)/2+60:shortest=1,format=yuv420p','-map','1:a','-c:v','libx264','-preset','fast','-crf','19','-c:a','copy','-shortest',f'{OUT}/b13_{name}.mp4'],check=True)
    print(name, subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{OUT}/b13_{name}.mp4']).decode().strip())
