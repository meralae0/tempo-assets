# EN5 thumbnail — BIG NUMBER style (green → teal), presenter grin right, real test-grid card
import sys; sys.path.insert(0,'/home/claude/tempo-assets/tools')
from thumb_leap import *
from PIL import Image, ImageDraw, ImageFilter
im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
for y in range(H):
    t=y/H; d.line((0,y,W,y),fill=tuple(int(a+(b-a)*t) for a,b in zip((16,170,110),(6,60,70)))+(255,))
g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse((W*.55,-H*.2,W*1.2,H*1.0),fill=140); g=g.filter(ImageFilter.GaussianBlur(110))
glow=Image.new('RGBA',(W,H),(180,255,120,0)); glow.putalpha(g); im.alpha_composite(glow)
grid=Image.open('/home/claude/b18/v7_last.png').convert('RGB').crop((160,90,1800,930)).resize((560,287))
place(im,card(grid,540,8),(30,390),rot=-3)
place(im,word('42/42',230,fill=WHITE),(30,40),rot=-3)
place(im,word('SAME APP',96,fill=BLACK,box=YEL),(40,270),rot=-3)
host=Image.open('/home/claude/tempo-assets/brand/host_grin.png').convert('RGBA'); host=host.crop(host.getbbox())
h=640; host=outline(host.resize((int(host.width*h/host.height),h),Image.LANCZOS),8); place(im,host,(W-host.width+40,H-h+10))
place(im,sticker('3 AIs · 0 BUGS?',44,col=(225,40,60)),(700,60),rot=3)
sp=sparkle(90); place(im,sp,(640,250),sh=False)
brand(im); im.convert('RGB').save('/home/claude/tempo-assets/pub/b18/b18_thumb.jpg',quality=92); print('ok')
