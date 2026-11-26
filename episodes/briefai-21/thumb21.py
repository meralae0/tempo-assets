# EN9 thumbnail — VERSUS style, 3 colored columns (blue / orange / teal), no presenter (faceless video)
import sys; sys.path.insert(0,'/home/claude/tempo-assets/tools')
from thumb_leap import *
from PIL import Image, ImageDraw
im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
cols=[(30,90,220),(255,120,40),(0,160,150)]
for k,c in enumerate(cols): d.polygon([(k*427-40,0),((k+1)*427+40,0),((k+1)*427-40,H),(k*427-120,H)],fill=c+(255,))
shots=['veo','pixverse','hailuo']; labs=['VEO','PIXVERSE','HAILUO']
for k,n in enumerate(shots):
    sh=Image.open(f'/home/claude/b21/th_{n}.png').convert('RGB'); c=card(sh,380,7)
    place(im,c,(24+k*420,300),rot=[-4,2,-3][k])
    place(im,word(labs[k],44),(80+k*420,560),rot=0)
place(im,word('5 FREE AI VIDEO',96,fill=BLACK,box=YEL),(40,30),rot=-2)
place(im,word('TOOLS · 1 WINNER',78),(80,160))
place(im,sticker('0 CREDITS?!',40),(940,40),rot=6)
brand(im); im.convert('RGB').save('/home/claude/tempo-assets/pub/b21/b21_thumb.jpg',quality=92); print('ok')
