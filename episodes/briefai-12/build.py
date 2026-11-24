# BriefAI #12 budget — 11 plans 16:9 (FR à l'écran). timing.json : D = durée par plan.
import sys, os, json, csv
sys.path.insert(0,'/home/claude/tempo-assets/tools')
from gfx_ai import *
from PIL import Image, ImageDraw
EP='/home/claude/tempo-assets/episodes/briefai-12'; O='/home/claude/b12/seg'; os.makedirs(O,exist_ok=True)
D=json.load(open(EP+'/timing.json'))['D']
def pill(d,xy,txt,col,font,anchor='mm',pad=(22,12),tc=None):
    x,y=xy; b=d.textbbox((x,y),txt,font=font,anchor=anchor)
    d.rounded_rectangle((b[0]-pad[0],b[1]-pad[1],b[2]+pad[0],b[3]+pad[1]),radius=14,fill=col+(255,))
    d.text((x,y),txt,font=font,fill=(tc or BG)+(255,),anchor=anchor)
def fadein(t,a=0,b=0.4): return max(0,min(1,ease((t-a)/(b-a)))) if b>a else 1
def eur(v): s=f'{abs(v):,.2f}'.replace(',',' ').replace('.',','); return ('−' if v<0 else '')+s+' €'
ROWS=[r for r in csv.DictReader(open(EP+'/releve-octobre.csv'),delimiter=';')]
CAT={"SUPERMARCHE":"Courses","EPICERIE":"Courses","BOULANGERIE":"Courses","ESSENCE":"Transport","BUS":"Transport","RESTAURANT":"Restos & cafés","CAFE":"Restos & cafés","CINEMA":"Loisirs","PHARMACIE":"Santé","MUTUELLE":"Revenus","VETEMENTS":"Loisirs","LIVRES":"Loisirs","LOYER":"Logement","ELECTRICITE":"Logement","ASSURANCE":"Logement","MOBILE":"Abonnements","INTERNET":"Abonnements","STREAMING":"Abonnements","MUSIQUE":"Abonnements","SPORT":"Abonnements","EPARGNE":"Épargne","DAB":"Retraits","SALAIRE":"Revenus"}
for r in ROWS:
    r['v']=float(r['montant'].replace(',','.')); r['c']=next(v for k,v in CAT.items() if k in r['libelle'])
A1=open(EP+'/A1_reponse.md').read()
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
def chat(d,box,title,text,col,font,scroll=0):
    x0,y0,x1,y1=box; d.rounded_rectangle(box,radius=20,fill=PANEL+(255,),outline=col+(255,),width=3)
    d.text((x0+28,y0+22),title,font=mono(28),fill=col+(255,))
    lh=font.size+10; y=y0+80-scroll
    for ln in wrap(d,text,font,x1-x0-56):
        if y>y1-lh: break
        if y>=y0+70: d.text((x0+28,y),ln,font=font,fill=WHITE+(255,))
        y+=lh
def sheet(d,box,rows,start=1,hl_row=None,col_w=(150,420,190,230),head=('Date','Libellé','Montant','Catégorie'),fs=24,letters=True):
    """Feuille de calcul : rows = liste de tuples ; start = n° de la 1re ligne de données."""
    x0,y0,x1,y1=box; rh=fs+18
    d.rectangle(box,fill=(250,250,252,255))
    xs=[x0+60]; [xs.append(xs[-1]+w) for w in col_w]
    if letters:
        d.rectangle((x0,y0,x1,y0+rh),fill=(232,234,240,255))
        for k,L in enumerate('ABCD'[:len(col_w)]): d.text(((xs[k]+xs[k+1])/2,y0+rh/2),L,font=mono(fs-4),fill=(90,96,110,255),anchor='mm')
    y=y0+rh
    allr=[head]+rows
    for i,r in enumerate(allr):
        n=start-1+i
        if y+rh>y1: break
        bg=(255,236,150,255) if (hl_row is not None and n==hl_row) else ((222,230,245,255) if i==0 else None)
        if bg: d.rectangle((x0+60,y,x1,y+rh),fill=bg)
        d.rectangle((x0,y,x0+60,y+rh),fill=(232,234,240,255)); d.text((x0+30,y+rh/2),str(n if i else start-1),font=mono(fs-6),fill=(90,96,110,255),anchor='mm')
        for k,v in enumerate(r):
            colr=(20,24,32,255)
            if isinstance(v,str) and v.startswith('−'): colr=(200,40,50,255)
            al='rm' if k==2 else 'lm'; xx=xs[k+1]-12 if k==2 else xs[k]+10
            d.text((xx,y+rh/2),str(v),font=(sg(fs,700) if i==0 else sg(fs,450)),fill=colr,anchor=al)
        d.line((x0,y+rh,x1,y+rh),fill=(215,218,226,255),width=1)
        y+=rh
    for xx in xs: d.line((xx,y0,xx,y),fill=(215,218,226,255),width=1)
def rowfmt(r): return (r['date'][8:10]+'/10',r['libelle'][:26],eur(r['v']),r['c'])
TOT=[('Logement',862.60),('Courses',429.44),('Épargne',200.00),('Transport',162.54),('Restos & cafés',154.29),('Abonnements',102.36),('Loisirs',73.06),('Retraits',60.00),('Santé',34.00)]
def timer(d,xy,sec,col=CYAN):
    d.rounded_rectangle((xy[0]-130,xy[1]-50,xy[0]+130,xy[1]+50),radius=24,fill=PANEL+(255,),outline=col+(255,),width=3)
    d.text(xy,f'{sec:4.1f} s'.replace('.',','),font=sg(52),fill=col+(255,),anchor='mm')
# 1 résultat d'abord
def f1(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im); a=fadein(t,0,1.6)
    glow_text(im,(W/2,110),'49 lignes de relevé → budget',sg(62),WHITE)
    timer(d,(W/2,240),34*a)
    for k,(lab,v,col) in enumerate([('Entrées',2492.30,GREEN),('Sorties',2078.29,RED),('Solde',414.01,CYAN)]):
        x=380+k*580; d.text((x,400),lab,font=mono(34),fill=GREY+(255,),anchor='mm')
        d.text((x,500),('+' if k==2 else '')+eur(v*a),font=sg(76),fill=col+(255,),anchor='mm')
    if t>D[0]*0.35: pill(d,(W/2,650),'juste au centime',GREEN,sg(44))
    if t>D[0]*0.7: pill(d,(W/2,800),'… mais son fichier Excel cachait un piège',RED,sg(44),tc=WHITE)
    return im
# 2 le relevé
def f2(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    glow_text(im,(1520,170),'Relevé d’octobre',sg(56),WHITE)
    d.text((1520,250),'49 opérations · données fictives',font=mono(28),fill=GREY+(255,),anchor='mm')
    off=min(len(ROWS)-20,int(t*2.2))
    rows=[(r['date'][8:10]+'/10',r['libelle'][:26],eur(r['v'])) for r in ROWS[off:off+22]]
    sheet(d,(60,60,1020,1040),rows,start=2+off,col_w=(130,500,240),head=('Date','Libellé','Montant'),fs=24)
    if t>D[1]*0.55:
        for k,q in enumerate(['total par catégorie','entrées','sorties','solde']): pill(d,(1520,420+k*110),q,CYAN,sg(40))
    return im
# 3 à la main + vérification
def f3(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    glow_text(im,(W/2,100),'À la main',sg(62),WHITE)
    pill(d,(560,240),'49 lignes à classer',WHITE,sg(44)); pill(d,(1360,240),'1 formule par catégorie',WHITE,sg(44))
    if t>D[2]*0.45:
        d.text((W/2,370),'Ma vérification (calcul par programme, au centime)',font=mono(30),fill=CYAN+(255,),anchor='mm')
        for k,(c,v) in enumerate(TOT):
            if t>D[2]*0.45+k*0.25:
                x=420+(k%3)*540; y=470+(k//3)*150
                d.rounded_rectangle((x-240,y-55,x+240,y+55),radius=16,fill=PANEL+(255,))
                d.text((x-215,y),c,font=sg(34,500),fill=GREY+(255,),anchor='lm'); d.text((x+215,y),eur(v),font=sg(40),fill=WHITE+(255,),anchor='rm')
    return im
# 4 essai 1 : conversation
def f4(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    pill(d,(530,80),'Essai 1 · Claude dans la conversation, sans tableur',WHITE,sg(32))
    chat(d,(60,140,1040,1040),'CLAUDE',A1,CYAN,sg(28,450),scroll=int(max(0,t-1)*48))
    timer(d,(1460,200),min(34,t*34/max(1,D[3]*0.4)))
    a=fadein(t,D[3]*0.4,D[3]*0.4+1)
    for k,(lab,v,col) in enumerate([('Entrées','2 492,30 €',GREEN),('Sorties','2 078,29 €',RED),('Solde','+414,01 €',CYAN)]):
        if a>0:
            y=380+k*200; d.text((1460,y),lab,font=mono(34),fill=GREY+(255,),anchor='mm'); d.text((1460,y+70),v,font=sg(int(70*a)+1),fill=col+(255,),anchor='mm')
    return im
# 5 3 essais, 0 erreur
def f5(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    glow_text(im,(W/2,110),'Comparé à ma vérification',sg(60),WHITE)
    runs=[('Essai 1 · Claude','33,5 s'),('Essai 2 · Claude','25,9 s'),('Essai 3 · petit modèle (Haiku)','22,8 s')]
    for k,(lab,s) in enumerate(runs):
        if t>0.3+k*D[4]*0.18:
            y=290+k*180; d.rounded_rectangle((240,y-65,1680,y+65),radius=20,fill=PANEL+(255,))
            d.text((290,y),lab,font=sg(44,500),fill=WHITE+(255,),anchor='lm'); d.text((1180,y),s,font=mono(40),fill=GREY+(255,),anchor='mm')
            d.text((1600,y),'0 erreur',font=sg(46),fill=GREEN+(255,),anchor='rm')
    if t>D[4]*0.7: pill(d,(W/2,900),'Entrées, sorties, solde, totaux par catégorie : justes au centime',GREEN,sg(38))
    return im
# 6 essai 2 : vrai Excel
BUD=[('Logement','862,60 €','=-SOMME.SI(Relevé!$D$2:$D$50;A4;…)'),('Courses','429,44 €','=-SOMME.SI(Relevé!$D$2:$D$50;A5;…)'),('Transport','162,54 €','…'),('Restos & cafés','154,29 €','…'),('Abonnements','102,36 €','…'),('Loisirs & shopping','73,06 €','…'),('Santé','34,00 €','…'),('Retraits espèces','60,00 €','…'),('Total dépenses','1 878,29 €','=SOMME(B4:B11)'),('Épargne','200,00 €','…'),('Total des entrées','2 492,30 €','=SOMME.SI(…;">0")'),('Total des sorties','2 078,29 €','=-SOMME.SI(…;"<0")'),('Solde du mois','414,01 €','=B17-B18'),('Contrôle','414,01 €','=SOMME(Relevé!C2:C50)')]
def budsheet(d,box,hl=None,fs=26,courses='429,44 €'):
    rows=[(a,(courses if a=='Courses' else b),'') for a,b,c in BUD]
    sheet(d,box,rows,start=4,col_w=(380,260,0),head=('Catégorie','Montant',''),fs=fs,hl_row=hl)
def f6(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    pill(d,(530,80),'Essai 2 · « fais-moi un vrai fichier Excel »',WHITE,sg(32))
    budsheet(d,(60,140,820,1040))
    timer(d,(1400,210),min(51,t*51/max(1,D[5]*0.5)))
    for k,s in enumerate(['feuille Relevé + colonne Catégorie','feuille Budget en SOMME.SI','graphique des dépenses']):
        if t>D[5]*0.3+k*0.6: pill(d,(1400,400+k*130),s,GREEN,sg(36))
    return im
# 7 ligne de contrôle
def f7(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    budsheet(d,(60,80,1100,1040),hl=17 if t>D[6]*0.3 else None,fs=28)
    if t>D[6]*0.3: pill(d,(1480,520),'ligne de contrôle = 414,01 €',GREEN,sg(40))
    if t>D[6]*0.6: pill(d,(1480,660),'mêmes totaux · propre',WHITE,sg(40))
    return im
# 8 ajout d'une dépense de novembre
def f8(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    rows=[rowfmt(r) for r in ROWS[-6:]]
    add=t>D[7]*0.25
    if add: rows.append(('01/11','CB SUPERMARCHE DU CENTRE','−50,00 €','Courses'))
    sheet(d,(40,120,1000,600),rows,start=45,hl_row=51 if add else None,col_w=(110,420,170,200),fs=24)
    d.text((520,80),'Relevé : j’ajoute une ligne',font=mono(30),fill=GREY+(255,),anchor='mm')
    budsheet(d,(1060,120,1880,700),fs=24)
    d.text((1470,80),'Budget',font=mono(30),fill=GREY+(255,),anchor='mm')
    if t>D[7]*0.55: pill(d,(W/2,820),'Courses : 429,44 € → 429,44 €   ·   le budget ne bouge pas',RED,sg(40),tc=WHITE)
    return im
# 9 la formule figée
def f9(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    glow_text(im,(W/2,140),'La formule écrite par Claude',sg(58),WHITE)
    f='=-SOMME.SI(Relevé!$D$2:$D$50 ; A5 ; Relevé!$C$2:$C$50)'
    d.rounded_rectangle((120,300,1800,440),radius=20,fill=(250,250,252,255))
    d.text((W/2,370),f,font=mono(46),fill=(20,24,32,255),anchor='mm')
    if t>D[8]*0.25:
        bb=d.textbbox((W/2,370),f,font=mono(46),anchor='mm'); pre=d.textlength('=-SOMME.SI(Relevé!$D$2:',font=mono(46)); w=d.textlength('$D$50',font=mono(46))
        x=bb[0]+pre; d.rectangle((x-6,330,x+w+6,410),outline=RED+(255,),width=6)
    if t>D[8]*0.45: pill(d,(W/2,580),'s’arrête à la ligne 50',RED,sg(52),tc=WHITE)
    if t>D[8]*0.65: d.text((W/2,740),'ligne 51 et suivantes : ignorées, sans message d’erreur',font=sg(44,500),fill=WHITE+(255,),anchor='mm')
    return im
# 10 la correction
def f10(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    glow_text(im,(W/2,130),'La correction : une phrase en plus',sg(58),GREEN)
    d.rounded_rectangle((180,240,1740,520),radius=24,fill=PANEL+(255,),outline=GREEN+(255,),width=3)
    for k,l in enumerate(['« Utilise des colonnes entières ou un tableau Excel,','pour que les lignes ajoutées plus tard soient comptées. »']):
        d.text((W/2,330+k*90),l,font=sg(46,500),fill=WHITE+(255,),anchor='mm')
    if t>D[9]*0.5:
        d.text((W/2,650),'=-SOMME.SI(Relevé!D:D ; A5 ; Relevé!C:C)',font=mono(48),fill=GREEN+(255,),anchor='mm')
        d.text((W/2,750),'→ la ligne de novembre est comptée : Courses 479,44 €',font=sg(40,500),fill=GREY+(255,),anchor='mm')
    return im
# 11 verdict
def f11(i,n):
    t=i/FPS; im=background(); d=ImageDraw.Draw(im)
    glow_text(im,(W/2,150),'Verdict',sg(80),WHITE)
    pill(d,(W/2,380),'Calculs : 0 erreur sur 3 essais',GREEN,sg(54))
    if t>D[10]*0.4: pill(d,(W/2,560),'Fichier : relis les plages des formules',RED,sg(54),tc=WHITE)
    if t>D[10]*0.65: d.text((W/2,740),'avant de le réutiliser le mois suivant',font=sg(44,500),fill=GREY+(255,),anchor='mm')
    return im
FS=[f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11]
if __name__=='__main__':
    if sys.argv[1:2]==['stills']:
        for k,f in enumerate(FS):
            n=int(D[k]*FPS); f(n-1,n).convert('RGB').save(f'{O}/still{k+1:02d}.jpg',quality=80)
        print('stills ok'); sys.exit()
    only=[int(x) for x in sys.argv[1:]] or range(11)
    for k in only: render(FS[k],D[k],f'{O}/s{k+1:02d}.mp4'); print('ok',k+1,flush=True)
