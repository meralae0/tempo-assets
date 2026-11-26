# EN6 thumbnail — SHOCK style, purple background, host_wow right, real Gemini still as card
import sys; sys.path.insert(0,'/home/claude/tempo-assets/tools')
from thumb_leap import *
from PIL import Image, ImageDraw, ImageFilter
EP='/home/claude/tempo-assets/episodes/briefai-20'
im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
for y in range(H):
    t=y/H; d.line((0,y,W,y),fill=tuple(int(a+(b-a)*t) for a,b in zip((120,50,220),(40,10,90)))+(255,))
g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse((-200,200,700,1000),fill=110); g=g.filter(ImageFilter.GaussianBlur(120))
glow=Image.new('RGBA',(W,H),(255,200,80,0)); glow.putalpha(g); im.alpha_composite(glow)
shot=Image.open(EP+'/img/s6.png').convert('RGB')
c=card(shot,600,8); place(im,c,(40,250),rot=-4)
place(im,sticker('100% AI · $0',40,col=(40,200,110)),(60,560),rot=-3)
place(im,word('1 SENTENCE',120,fill=BLACK,box=YEL),(30,24),rot=-2)
place(im,word('→ CARTOON',96),(70,160))
host=Image.open('/home/claude/tempo-assets/brand/host_wow.png').convert('RGBA'); host=host.crop(host.getbbox())
h=640; host=outline(host.resize((int(host.width*h/host.height),h),Image.LANCZOS),8); place(im,host,(W-host.width+30,H-h+10))
place(im,sticker('AI REFUSED 3×',44),(700,40),rot=4)
arrow(im,(760,150),(560,330),bend=0.3)
brand(im); im.convert('RGB').save('/home/claude/tempo-assets/pub/b20/b20_thumb.jpg',quality=92); print('ok')
