import sys; sys.path.insert(0,'/home/claude/tempo-assets/tools')
from thumb_leap import *
from PIL import Image, ImageDraw, ImageFilter
E='/home/claude/tempo-assets/episodes'; T='/home/claude/th'
def bg(c1,c2,rad=True):
    im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H; d.line((0,y,W,y),fill=tuple(int(a+(b-a)*t) for a,b in zip(c1,c2))+(255,))
    if rad:
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse((W*.15,-H*.4,W*1.1,H*.9),fill=90); g=g.filter(ImageFilter.GaussianBlur(120))
        w=Image.new('RGBA',(W,H),(255,255,255,0)); w.putalpha(g); im.alpha_composite(w)
    return im
def face(n,h):
    c=Image.open(f'{T}/cut_{n}.png'); c=c.crop(c.getbbox()); c=c.resize((int(c.width*h/c.height),h),Image.LANCZOS); return outline(c,7)
def shot(p,w,crop=None):
    im=Image.open(p).convert('RGB'); 
    if crop: im=im.crop(crop)
    return card(im,w)
def big(base,txt,sz,xy,fill=WHITE,box=None,rot=0,stroke=12): return place(base,word(txt,sz,fill=fill,box=box,stroke=stroke),xy,rot)
def stamp(base,ok,xy,sz=150):
    col=(40,200,110) if ok else RED; s=Image.new('RGBA',(sz,sz),(0,0,0,0)); d=ImageDraw.Draw(s)
    d.ellipse((4,4,sz-4,sz-4),fill=col+(255,),outline=WHITE+(255,),width=8)
    if ok: d.line([(sz*.27,sz*.52),(sz*.44,sz*.7),(sz*.75,sz*.32)],fill=WHITE+(255,),width=int(sz*.11),joint='curve')
    else:
        d.line([(sz*.3,sz*.3),(sz*.7,sz*.7)],fill=WHITE+(255,),width=int(sz*.11)); d.line([(sz*.7,sz*.3),(sz*.3,sz*.7)],fill=WHITE+(255,),width=int(sz*.11))
    place(base,s,xy)
def save(im,n): brand(im); im.convert('RGB').save(f'{T}/out/{n}.jpg',quality=92); print(n)

# 1 FR prompt maitre — CONCEPT (purple)
im=bg((88,40,200),(30,10,90)); d=ImageDraw.Draw(im)
doc=Image.new('RGBA',(330,420),(0,0,0,0)); dd=ImageDraw.Draw(doc); dd.rounded_rectangle((0,0,329,419),30,fill=(250,250,255,255))
for k in range(9): dd.rounded_rectangle((40,60+k*38,40+[240,200,250,170,230,150,240,190,120][k],80+k*38),8,fill=(150,140,200,255))
dd.rounded_rectangle((40,60+2*38-6,300,86+2*38),8,outline=YEL+(255,),width=6)
place(im,doc,(780,150),rot=-8); arrow(im,(560,560),(800,470),0.3)
big(im,'1 PROMPT',150,(40,90),fill=BLACK,box=YEL); big(im,'=',110,(60,290)); big(im,'1 CHAÎNE',130,(140,270)); big(im,'YOUTUBE',80,(60,450),fill=YEL)
place(im,sticker('JE TE LE DONNE',40,RED),(860,600),rot=-4); save(im,'SlHv7nSQUHk')

# 2 EN prompt — BIG NUMBER (yellow)
im=bg((255,214,0),(255,160,0)); 
big(im,'1',420,(40,60),fill=BLACK,stroke=0); big(im,'PROMPT',120,(330,120),fill=BLACK,stroke=0)
big(im,'WHOLE',110,(330,290),fill=WHITE); big(im,'CHANNEL',110,(330,420),fill=WHITE)
place(im,sticker('FREE PROMPT',46,RED),(880,560),rot=-5); save(im,'pgJx8_P6H48')

# 3 FR Skill Claude — CARD (blue)
im=bg((20,110,255),(10,40,140))
place(im,shot(f'{E}/briefai-03/caps/10_carte_skill.jpg',660,(380,80,1500,700)),(580,150),rot=4)
big(im,'TON',110,(50,90)); big(im,'SKILL',150,(50,220),fill=BLACK,box=YEL); big(im,'CLAUDE',110,(50,420))
place(im,sticker('2 MIN · SANS CODE',42,RED),(640,70),rot=-3); arrow(im,(420,620),(640,560),0.3); save(im,'8Gl7P2NXjKs')

# 4 FR Black Friday — RESULT ZOOM (red/black)
im=bg((200,20,40),(60,0,10)); d=ImageDraw.Draw(im)
tag=Image.new('RGBA',(560,360),(0,0,0,0)); td=ImageDraw.Draw(tag); td.rounded_rectangle((0,0,559,359),30,fill=WHITE+(255,))
td.text((280,110),'−29 %',font=font(150),fill=(20,20,20,255),anchor='mm'); td.line((90,115,470,105),fill=RED+(255,),width=18)
td.text((280,270),'en vrai : −14 %',font=font(70),fill=RED+(255,),anchor='mm')
place(im,tag,(650,170),rot=-5)
big(im,'FAUSSE',140,(40,110),fill=YEL); big(im,'PROMO ?',140,(40,280)); big(im,'BLACK FRIDAY',70,(46,470),fill=BLACK,box=YEL)
save(im,'S8QFCWJyfEA')

# 5 EN bank — BIG NUMBER + face (green)
im=bg((0,170,90),(0,70,40)); place(im,face('wow',640),(780,80))
big(im,'$684',150,(40,90),fill=WHITE); d=ImageDraw.Draw(im); d.line((50,190,420,170),fill=RED+(255,),width=20)
big(im,'$694',190,(40,270),fill=BLACK,box=YEL); big(im,'1 AI GOT IT WRONG',66,(46,520),fill=WHITE)
save(im,'UPkeIM0ZgZs')

# 6 FR Taste — BEFORE/AFTER (white)
im=bg((245,245,248),(215,218,228)); 
place(im,shot(f'{E}/briefai-10/caps/A_desk_hero.jpg',520),(40,200),rot=-3); place(im,shot(f'{E}/briefai-10/caps/B_desk_hero.jpg',520),(680,200),rot=3)
stamp(im,False,(430,420)); stamp(im,True,(1080,420))
big(im,'SANS',90,(120,60),fill=RED); big(im,'AVEC',90,(800,60),fill=(20,160,80)); big(im,'SKILL',90,(470,60),fill=BLACK,box=YEL)
place(im,sticker('2 MIN',44,RED),(150,560)); place(im,sticker('23 MIN',44,(20,150,80)),(800,560)); save(im,'ZYd9aV6DPU8')

# 7 EN lie — VERSUS (3 colors)
im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
for k,c in enumerate([(16,163,127),(217,119,87),(66,133,244)]): d.rectangle((k*W//3,0,(k+1)*W//3,H),fill=c+(255,))
for k,n in enumerate(['CHATGPT','CLAUDE','GEMINI']): big(im,n,64,(k*W//3+40,40))
place(im,face('grin',540),(760,190)); big(im,'WHO',170,(40,180),fill=BLACK,box=YEL,rot=-4); big(im,'LIED?',190,(60,380),fill=WHITE,rot=-4)
place(im,sticker('10 TESTS',46,RED),(560,590),rot=5); save(im,'2sv-E1Qza2E')

# 8 FR caveman — BIG NUMBER (orange)
im=bg((255,120,0),(190,50,0))
big(im,'−57 %',260,(40,60),fill=WHITE); big(im,'DE TOKENS',100,(60,350),fill=BLACK,box=YEL)
big(im,'MÊME FACTURE',90,(60,500),fill=WHITE)
rock=Image.new('RGBA',(300,260),(0,0,0,0)); rd=ImageDraw.Draw(rock); rd.polygon([(30,200),(10,120),(70,40),(170,20),(260,70),(290,170),(220,240),(90,250)],fill=(120,110,100,255),outline=BLACK+(255,),width=8)
rd.text((150,140),'UGH',font=font(70),fill=WHITE+(255,),anchor='mm'); place(im,rock,(900,330),rot=-8)
place(im,sticker('SKILL CAVEMAN',40,(10,10,12)),(880,120),rot=6); save(im,'ZxzbXJ50tGs')

# 9 FR budget — RESULT ZOOM (teal)
im=bg((0,150,160),(0,60,70)); 
cell=Image.new('RGBA',(620,300),(0,0,0,0)); cd=ImageDraw.Draw(cell); cd.rounded_rectangle((0,0,619,299),24,fill=WHITE+(255,))
cd.text((310,110),'=SUMIF(…$D$2:$D$50)',font=font(46),fill=(30,30,30,255),anchor='mm'); cd.text((310,215),'ligne 51 ignorée',font=font(64),fill=RED+(255,),anchor='mm')
cd.ellipse((330,70,600,150),outline=RED+(255,),width=10); place(im,cell,(620,200),rot=-3)
big(im,'LE PIÈGE',130,(40,110),fill=YEL); big(im,'EXCEL',170,(40,280),fill=BLACK,box=WHITE); big(im,'de Claude',80,(50,500))
save(im,'B9wu0kHHNAs')
