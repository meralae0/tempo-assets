# BriefAI #11 caveman — 11 plans 16:9 (FR à l'écran). timing.json : D = durée par plan.
import sys, os, json, re
sys.path.insert(0,'/home/claude/tempo-assets/tools')
from gfx_ai import *
from PIL import Image, ImageDraw, ImageFont
EP='/home/claude/tempo-assets/episodes/briefai-11'; O='/home/claude/b11/seg'; os.makedirs(O,exist_ok=True)
D=json.load(open(EP+'/timing.json'))['D']
def pill(d,xy,txt,col,font,anchor='mm',pad=(22,12),tc=None):
    x,y=xy; b=d.textbbox((x,y),txt,font=font,anchor=anchor)
    d.rounded_rectangle((b[0]-pad[0],b[1]-pad[1],b[2]+pad[0],b[3]+pad[1]),radius=14,fill=col+(255,))
    d.text((x,y),txt,font=font,fill=(tc or BG)+(255,),anchor=anchor)
def fadein(t,a=0,b=0.4): return max(0,min(1,ease((t-a)/(b-a)))) if b>a else 1
def answers(path):
    txt=open(path).read(); parts=re.split(r'=== (Q\d) ===\n',txt); return {parts[i]:parts[i+1].strip() for i in range(1,len(parts),2)}
A=answers(EP+'/A_normal.md'); B=answers(EP+'/B_caveman.md')
TOK={'Q1':(231,66),'Q2':(442,181),'Q3':(373,151),'Q4':(323,161),'Q5':(474,168),'Q6':(396,246)}
QN={'Q1':'Formule Excel','Q2':'Batterie Android','Q3':'Prêt fixe / variable','Q4':'Supprimer un dossier','Q5':'Erreur 404','Q6':'Recette de pâtes'}
def wrap(d,text,font,maxw):
    out=[]
    for para in text.split('\n'):
        line=''
        for w in para.split(' '):
            tst=(line+' '+w).strip()
            if d.textlength(tst,font=font)>maxw and line: out.append(line); line=w
            else: line=tst
        out.append(line)
    return out
def chat(d,box,title,text,col,font,scroll=0,hl=None):
    x0,y0,x1,y1=box; d.rounded_rectangle(box,radius=20,fill=PANEL+(255,),outline=col+(255,),width=3)
    d.text((x0+28,y0+22),title,font=mono(28),fill=col+(255,))
    lines=wrap(d,text.replace('**','').replace('`',''),font,x1-x0-56); lh=font.size+10; y=y0+80-scroll
    for ln in lines:
        if y>y1-lh: break
        if y>=y0+70:
            if hl and hl in ln: d.rectangle((x0+20,y-4,x1-20,y+lh-6),fill=(90,20,30,255))
            d.text((x0+28,y),ln,font=font,fill=WHITE+(255,))
        y+=lh
    return len(lines)*lh
def counter(d,xy,val,col,size=120):
    d.text(xy,f'{val:,}'.replace(',',' '),font=sg(size),fill=col+(255,),anchor='mm')
# 1 résultat d'abord : 2 239 → 973, facture identique
def f1(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im); a=fadein(t,0,1.6)
    d.text((500,250),'CLAUDE NORMAL',font=mono(34),fill=GREY+(255,),anchor='mm'); d.text((1420,250),'CLAUDE + CAVEMAN',font=mono(34),fill=GREY+(255,),anchor='mm')
    counter(d,(500,400),int(2239*a),RED,150); counter(d,(1420,400),int(973*a),GREEN,150)
    d.text((500,510),'tokens de réponse',font=mono(30),fill=GREY+(255,),anchor='mm'); d.text((1420,510),'tokens de réponse  (−57 %)',font=mono(30),fill=GREY+(255,),anchor='mm')
    if t>D[0]*0.6:
        b=fadein(t,D[0]*0.6,D[0]*0.6+0.4)
        d.rounded_rectangle((260,640,1660,900),radius=24,fill=PANEL+(255,),outline=CYAN+(255,),width=3)
        d.text((W/2,700),'Total de la session (facture)',font=mono(32),fill=CYAN+(255,),anchor='mm')
        d.text((W/2,800),'62 591   vs   62 603',font=sg(int(96*b+1)),fill=WHITE+(255,),anchor='mm')
    return im
# 2 le skill + promesse
SK=open(EP+'/caveman-SKILL.md').read().split('---',2)[2].strip()
def f2(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    chat(d,(120,140,1100,980),'skills/caveman/SKILL.md · GitHub (Apache-2.0)',SK,DIM if False else GREY,mono(26),scroll=int(t*14))
    glow_text(im,(1500,330),'caveman',sg(96),WHITE)
    d.text((1500,440),'« parle comme un homme',font=sg(40,500),fill=GREY+(255,),anchor='mm'); d.text((1500,495),'des cavernes »',font=sg(40,500),fill=GREY+(255,),anchor='mm')
    if t>D[1]*0.4: pill(d,(1500,680),'LE CHIFFRE QUI CIRCULE : −65 %',CYAN,sg(40))
    if t>D[1]*0.65: pill(d,(1500,800),'retiré du README le 8 sept. 2026',RED,sg(34),tc=WHITE)
    return im
# 3 six questions
def f3(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    glow_text(im,(W/2,130),'6 questions de tous les jours',sg(64),WHITE)
    for k,q in enumerate(QN):
        if t>0.4+k*D[2]*0.11:
            y=260+k*120; d.rounded_rectangle((420,y-46,1500,y+46),radius=18,fill=PANEL+(255,))
            d.text((470,y),q,font=mono(36),fill=CYAN+(255,),anchor='lm'); d.text((600,y),QN[q],font=sg(48,500),fill=WHITE+(255,),anchor='lm')
    d.text((W/2,1010),'mêmes questions · même Claude · sans / avec le skill',font=mono(30),fill=GREY+(255,),anchor='mm')
    return im
# 4 les deux réponses Q2 côte à côte (style)
def f4(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    pill(d,(W/2,80),'Q2 · batterie Android',WHITE,sg(36))
    chat(d,(60,150,940,1040),'NORMAL · 442 tokens',A['Q2'],RED,sg(28,450),scroll=int(t*22))
    chat(d,(980,150,1860,1040),'CAVEMAN · 181 tokens',B['Q2'],GREEN,sg(28,450))
    return im
# 5 Q1 excel 231 vs 66
def f5(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    pill(d,(W/2,80),'Q1 · formule Excel',WHITE,sg(36))
    chat(d,(60,150,1100,1040),'NORMAL',A['Q1'],RED,sg(28,450))
    chat(d,(1140,150,1860,620),'CAVEMAN',B['Q1'],GREEN,sg(28,450))
    a=fadein(t,0.5,2.0); counter(d,(1500,740),int(231-(231-66)*a),GREEN if a>0.99 else WHITE,110)
    d.text((1500,830),'tokens',font=mono(30),fill=GREY+(255,),anchor='mm')
    if t>D[4]*0.5: pill(d,(1500,940),'−71 % · rien d’important ne manque',GREEN,sg(36))
    return im
# 6 Q6 recette
def f6(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    pill(d,(W/2,80),'Q6 · recette de pâtes',WHITE,sg(36))
    chat(d,(60,150,940,960),'NORMAL · 396 tokens',A['Q6'],RED,sg(28,450))
    chat(d,(980,150,1860,960),'CAVEMAN · 246 tokens',B['Q6'],GREEN,sg(28,450))
    if t>D[5]*0.35: pill(d,(W/2,1025),'seulement −38 % : des quantités, rien à couper',CYAN,sg(40))
    return im
# 7 tableau des 6
def f7(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im); a=fadein(t,0.2,1.8)
    glow_text(im,(W/2,100),'Gain par question',sg(60),WHITE)
    x65=560+int(1100*0.65)
    for k,(q,(na,cv)) in enumerate(TOK.items()):
        y=210+k*118; g=1-cv/na; ok=g>=0.645
        d.text((520,y+30),QN[q],font=sg(36,500),fill=WHITE+(255,),anchor='rm')
        w=int(1100*g*a); d.rounded_rectangle((560,y,560+max(6,w),y+60),radius=10,fill=(GREEN if ok else GREY)+(255,))
        d.text((580+w,y+30),f'−{round(g*100)} %',font=sg(40),fill=WHITE+(255,),anchor='lm')
    d.line((x65,190,x65,920),fill=CYAN+(255,),width=4); d.text((x65,940),'chiffre annoncé −65 %',font=mono(30),fill=CYAN+(255,),anchor='mm')
    if t>D[6]*0.45: pill(d,(W/2,1020),'Total −57 % · −65 % atteint sur 1 question sur 6',WHITE,sg(38))
    return im
# 8 le piège : coût du skill
def f8(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    glow_text(im,(W/2,130),'Le piège',sg(70),RED)
    rows=[('Tokens gagnés sur 6 réponses','−1 266',GREEN,0.25),('Le skill, rechargé à chaque session','+1 158',RED,0.5),('Gain net','≈ −108',CYAN,0.75)]
    for k,(lab,v,col,at) in enumerate(rows):
        if t>D[7]*at-1.5:
            y=330+k*190
            if k==2: d.line((360,y-95,1560,y-95),fill=GREY+(255,),width=3)
            d.text((380,y),lab,font=sg(46,500),fill=WHITE+(255,),anchor='lm'); d.text((1540,y),v,font=sg(80),fill=col+(255,),anchor='rm')
    return im
# 9 compteur session
def f9(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im); a=fadein(t,0,1.8)
    d.text((W/2,170),'Compteur de la session (tout compris)',font=mono(36),fill=GREY+(255,),anchor='mm')
    d.text((560,330),'SANS',font=sg(44),fill=RED+(255,),anchor='mm'); d.text((1360,330),'AVEC CAVEMAN',font=sg(44),fill=GREEN+(255,),anchor='mm')
    counter(d,(560,480),int(62591*a),WHITE,140); counter(d,(1360,480),int(62603*a),WHITE,140)
    if t>D[8]*0.7: glow_text(im,(W/2,760),'= PAREIL',sg(110),CYAN)
    return im
# 10 Q4 : la mise en garde perdue
def f10(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    pill(d,(W/2,80),'Q4 · supprimer « photos_2019 »',WHITE,sg(36))
    hl='Ne mettez jamais d' if t>D[9]*0.35 else None
    chat(d,(60,150,940,1040),'NORMAL',A['Q4'],RED,sg(26,450),hl=hl)
    chat(d,(980,150,1860,900),'CAVEMAN',B['Q4'],GREEN,sg(26,450))
    if t>D[9]*0.55: pill(d,(1420,975),'mise en garde « rm -rf photos_2019 /* » : disparue',RED,sg(30),tc=WHITE)
    return im
# 11 verdict
def f11(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    d.text((W/2,170),'MON VERDICT',font=mono(40),fill=GREY+(255,),anchor='mm')
    pill(d,(W/2,340),'Longues sessions de code → utile',GREEN,sg(54))
    if t>D[10]*0.35: pill(d,(W/2,520),'Quelques questions → ça ne change rien',WHITE,sg(54))
    if t>D[10]*0.65: pill(d,(W/2,700),'Relis toujours les commandes dangereuses',RED,sg(54),tc=WHITE)
    return im
FS=[f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11]
if __name__=='__main__':
    if sys.argv[1:2]==['stills']:
        for k,f in enumerate(FS):
            n=int(D[k]*FPS); f(n-1,n).convert('RGB').save(f'{O}/still{k+1:02d}.jpg',quality=80)
        print('stills ok'); sys.exit()
    only=[int(x) for x in sys.argv[1:]] or range(11)
    for k in only: render(FS[k],D[k],f'{O}/s{k+1:02d}.mp4'); print('ok',k+1,flush=True)
