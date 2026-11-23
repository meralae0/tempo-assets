import sys, os, json, subprocess, math
sys.path.insert(0,'/home/claude/tempo-assets/tools')
from gfx_ai import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter
EP='/home/claude/tempo-assets/episodes/briefai-10'; C=EP+'/caps'; O='/home/claude/b10/seg'; os.makedirs(O,exist_ok=True)
T=json.load(open('/home/claude/b10/timing.json'))
D=T['D']
def inter(sz,w=600):
    f=ImageFont.truetype(os.path.join(BRAND,'Inter.ttf'),sz)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def pill(d,xy,txt,col,font,anchor='mm',pad=(22,12)):
    x,y=xy; b=d.textbbox((x,y),txt,font=font,anchor=anchor)
    d.rounded_rectangle((b[0]-pad[0],b[1]-pad[1],b[2]+pad[0],b[3]+pad[1]),radius=14,fill=col+(255,))
    d.text((x,y),txt,font=font,fill=BG+(255,),anchor=anchor)
def shot(path,width,crop=None):
    im=Image.open(path).convert('RGB')
    if crop: im=im.crop(crop)
    s=width/im.width; return im.resize((width,int(im.height*s)),Image.LANCZOS)
def framed(im,border=(40,44,58)):
    w=Image.new('RGBA',(im.width+6,im.height+6),border+(255,)); w.paste(im,(3,3)); return w
def fadein(t,a=0,b=0.4): return ease((t-a)/(b-a)) if b>a else 1

# 1 split screen
A_h=shot(C+'/A_desk_hero.jpg',880); B_h=shot(C+'/B_desk_hero.jpg',880)
def f1(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    glow_text(im,(W/2,140),'Même demande. Même Claude.',sg(72),WHITE)
    for k,(img,x,lab,tm,col) in enumerate([(A_h,60,'SANS SKILL','2 min 16',RED),(B_h,980,'AVEC TASTE SKILL','23 min',GREEN)]):
        a=fadein(t,0.2+k*0.5,0.7+k*0.5); 
        if a<=0: continue
        fr=framed(img); y=250+int((1-a)*40); im.alpha_composite(fr,(x,y))
        pill(d,(x+440,y+fr.height+60),lab+'  ·  '+tm,col,sg(40))
    return im
# 2 promise
def f2(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    d.text((W/2,330),'Taste Skill · GitHub',font=mono(38),fill=GREY,anchor='mm')
    glow_text(im,(W/2,480),'« Fini les sites qui sentent l’IA »',sg(84),WHITE)
    if t>D[1]*0.45:
        a=fadein(t,D[1]*0.45,D[1]*0.45+0.3); s=int(60+30*(1-a))
        pill(d,(W/2,700),'J’AI VÉRIFIÉ',CYAN,sg(s))
    return im
# 3 request typing
REQ="> Crée la page d'accueil d'un café de quartier\n  à Casablanca : « Café Nour » — café de spécialité,\n  pâtisseries maison, ouvert 7h-20h, quartier Maârif.\n  Une seule page en français._"
def f3(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((180,250,1740,830),radius=24,fill=PANEL+(255,),outline=DIM+(255,),width=2)
    d.text((230,290),'Demande identique pour les deux tests',font=mono(30),fill=GREY)
    k=int(len(REQ)*min(1,t/(D[2]*0.75))); d.multiline_text((230,380),REQ[:k],font=mono(44),fill=WHITE,spacing=26)
    return im
# 4 A hero with callouts
def f4(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im); z=1+0.06*t/D[3]
    img=shot(C+'/A_desk_hero.jpg',int(1500*z)); cx=(img.width-1500)//2; img=img.crop((cx,0,cx+1500,min(img.height,840)))
    im.alpha_composite(framed(img),(60,170)); pill(d,(330,110),'SANS SKILL · 2 min 16',RED,sg(40))
    for k,txt in enumerate(['titre serif + italique doré','photo assombrie','petits badges']):
        if t>D[3]*(0.3+0.12*k): pill(d,(1690,330+k*150),txt,WHITE,sg(30))
    if t>D[3]*0.75: glow_text(im,(W/2,1035),'= le look « IA » qu’on reconnaît en 1 seconde',sg(44),CYAN)
    return im
# 5 fake review + 100%
FULL=Image.open(C+'/A_desk_full.jpg').convert('RGB'); SC=FULL.width/1440
def crop_at(y_css,h=520):
    y=int(y_css*SC/1.5) if False else int(y_css)  # tesseract coords are on full image pixels
    return FULL.crop((0,max(0,y-h//2),FULL.width,max(0,y-h//2)+h))
REV=crop_at(6610,560); PCT=crop_at(2782,560)
def f5(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im); half=t>D[4]*0.62
    src=PCT if half else REV; img=src.resize((1600,int(src.height*1600/src.width)),Image.LANCZOS)
    im.alpha_composite(framed(img),(160,200)); 
    cy=200+img.height//2; r=int(img.height*0.42)
    lt=(t-(D[4]*0.62 if half else 0)); a=fadein(lt,0.3,0.8)
    if a>0: d.ellipse((W/2-int(620*a),cy-r,W/2+int(620*a),cy+r),outline=RED+(255,),width=8)
    pill(d,(W/2,110),'Ce client n’existe pas' if not half else '« 100 % » : chiffre inventé',RED,sg(52))
    if lt>1.2: pill(d,(W/2,cy+r+90),'INVENTÉ PAR CLAUDE',RED,sg(44))
    return im
# 6 B hero
def f6(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im); z=1+0.06*t/D[5]
    img=shot(C+'/B_desk_hero.jpg',int(1500*z)); cx=(img.width-1500)//2; img=img.crop((cx,0,cx+1500,min(img.height,840)))
    im.alpha_composite(framed(img),(210,170)); pill(d,(480,110),'AVEC TASTE SKILL · 23 min',GREEN,sg(40))
    if t>D[5]*0.4: pill(d,(W/2,1035),'titre simple : quoi + où · vraie photo, sans filtre',WHITE,sg(34))
    return im
# 7 checks
CH=[('Ouvre la page dans un vrai navigateur',1),('Relit le texte',1),('Mesure les contrastes',1),('Fait corriger',1),('Reste : 1 contraste sur mobile',0)]
def f7(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    glow_text(im,(W/2,140),'Pourquoi 23 minutes ?',sg(68),WHITE)
    for k,(txt,ok) in enumerate(CH):
        if t>0.6+k*D[6]/7:
            y=290+k*130; col=GREEN if ok else RED
            d.rounded_rectangle((360,y-48,1560,y+48),radius=18,fill=PANEL+(255,))
            d.text((420,y),'✓' if ok else '✗',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',54),fill=col+(255,),anchor='lm'); d.text((500,y),txt,font=sg(46,500),fill=WHITE+(255,),anchor='lm')
    return im
# 8 length comparison
AF=Image.open(C+'/A_desk_full.jpg').convert('RGB'); BF=Image.open(C+'/B_desk_full.jpg').convert('RGB')
s8=780/AF.height; AFs=AF.resize((int(AF.width*s8),780)); BFs=BF.resize((int(BF.width*s8),int(BF.height*s8)))
def f8(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im); a=fadein(t,0,0.8)
    hA=int(780*a); im.alpha_composite(framed(AFs.crop((0,0,AFs.width,max(1,hA)))),(470,160))
    hB=int(BFs.height*a); im.alpha_composite(framed(BFs.crop((0,0,BFs.width,max(1,hB)))),(1250,160))
    d.text((470+AFs.width//2,110),'SANS',font=sg(40),fill=RED+(255,),anchor='mm'); d.text((1250+BFs.width//2,110),'AVEC',font=sg(40),fill=GREEN+(255,),anchor='mm')
    rows=[('7 écrans','3 écrans'),('670 mots','165 mots'),('1 faux avis','0 inventé')]
    for k,(x,y_) in enumerate(rows):
        if t>D[7]*(0.15+0.25*k):
            d.text((420,300+k*130),x,font=sg(54),fill=RED+(255,),anchor='rm'); d.text((1250+BFs.width+60,300+k*130),y_,font=sg(54),fill=GREEN+(255,),anchor='lm')
    return im
# 9 cost bars
def f9(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im); a=fadein(t,0.2,1.5)
    glow_text(im,(W/2,130),'Le prix',sg(70),WHITE)
    for k,(lab,va,vb,ta,tb) in enumerate([('Tokens',75,185,'~75 k','~185 k  (×2,5)'),('Temps',136,1381,'2 min 16','23 min  (×10)')]):
        y=330+k*300; mx=max(va,vb); d.text((200,y-70),lab,font=mono(36),fill=GREY+(255,))
        for j,(v,tx,col) in enumerate([(va,ta,RED),(vb,tb,GREEN)]):
            w_=int(1100*v/mx*a); yy=y+j*95; d.rounded_rectangle((200,yy,200+max(8,w_),yy+70),radius=12,fill=col+(255,))
            d.text((230+max(8,w_),yy+35),tx,font=sg(44),fill=WHITE+(255,),anchor='lm')
    d.text((W/2,1010),'rouge = sans skill · vert = avec Taste Skill',font=mono(30),fill=GREY+(255,),anchor='mm')
    return im
# 10 verdict
def f10(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    d.text((W/2,170),'MON VERDICT',font=mono(40),fill=GREY+(255,),anchor='mm')
    glow_text(im,(W/2,330),'Pas plus jolie d’office.',sg(72),WHITE)
    if t>D[9]*0.25: glow_text(im,(W/2,450),'Plus HONNÊTE.',sg(96),CYAN)
    if t>D[9]*0.5: pill(d,(W/2,640),'Vrai commerce → je le garde',GREEN,sg(46))
    if t>D[9]*0.75: pill(d,(W/2,780),'Maquette rapide → pas besoin',WHITE,sg(46))
    return im
# 11 install
CMD='$ npx skills add https://github.com/Leonxlnx/taste-skill \\\n    --skill "design-taste-frontend"'
def f11(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    glow_text(im,(W/2,180),'L’installer : 1 commande',sg(68),WHITE)
    d.rounded_rectangle((150,330,1770,640),radius=24,fill=PANEL+(255,),outline=DIM+(255,),width=2)
    k=int(len(CMD)*min(1,t/(D[10]*0.5))); d.multiline_text((200,400),CMD[:k],font=mono(40),fill=GREEN+(255,),spacing=30)
    if t>D[10]*0.55: pill(d,(W/2,790),'Node 22+  ·  Chrome  ·  gratuit (licence MIT)',CYAN,sg(44))
    return im
FS=[f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11]
only=[int(x) for x in sys.argv[1:]] or range(11)
for k in only:
    render(FS[k],D[k],f'{O}/s{k+1:02d}.mp4'); print('ok',k+1,flush=True)
