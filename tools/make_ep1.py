import json
J = json.load(open('/tmp/ep1_sent.json'))
for l in J:
    for k, seg in enumerate(J[l]):
        out = []
        for s in seg:
            if out and out[-1].endswith(':') and len(out[-1]) < 20: out[-1] = out[-1] + ' ' + s
            else: out.append(s)
        J[l][k] = out
B = '../../brand/'; S = 'shots/'
def L(fr, en): return {'fr': fr, 'en': en}
WH = [240, 244, 250]; CY = [0, 212, 255]; VI = [124, 92, 255]; RD = [255, 77, 90]; GR = [130, 140, 160]
segs = [
 dict(id='seg01', title=L('Accroche', 'Hook'), shots=[
   dict(at=0, fn='title', lines=L([["J'ai laissé une IA", WH], ["créer ma chaîne YouTube", CY]], [["I let an AI", WH], ["build my YouTube channel", CY]])),
   dict(at=1, fn='window', shot=S + 'channel.jpg', title='youtube.com/@briefai'),
   dict(at=4, fn='title', lines=L([["méthodes · ratés", WH], ["vues · argent", CY]], [["methods · failures", WH], ["views · money", CY]])),
   dict(at=5, fn='title', lines=L([["JOUR 1", CY]], [["DAY 1", CY]]))]),
 dict(id='seg02', title=L('Le brief', 'The brief'), shots=[
   dict(at=0, fn='terminal', title='brief.txt', lines=L(["# brief pour Claude", "Crée une chaîne d'actualité", "en français et en anglais", "Publie tout en automatique", "Ne me demande que les mots de passe"],
                                                        ["# brief for Claude", "Build a news channel", "in French and English", "Publish everything automatically", "Only ask me for passwords"])),
   dict(at=2, fn='window', shot=B + 'banner.png', title='charte v1 — TempoBrief'),
   dict(at=3, fn='window', shot=S + 'github.jpg', title='github.com · tempo-assets/tools', blur=[[30, 0, 160, 30]]),
   dict(at=3.55, fn='code', path='../../tools/gfx.py', start=30, n=24, title=L('tools/gfx.py — écrit par Claude', 'tools/gfx.py — written by Claude'))]),
 dict(id='seg03', title=L('Le nom', 'The name'), shots=[
   dict(at=0, fn='handles', items=['temponews', 'tempo.news', 'tempoactu', 'tempo.daily', 'tempohq', 'DailyTempo', 'dailybrief', 'dailybrieftv', 'thedailybrief'], ok='tempobrief', title=L('Identifiant YouTube', 'YouTube handle'))]),
 dict(id='seg04', title=L('Le raté', 'The fail'), shots=[
   dict(at=0, fn='window', shot=S + 'trends.jpg', title='trends.google.com'),
   dict(at=1, fn='window', shot=S + 'fail_title.png', title=L('vidéo n°1 — non publiée', 'video #1 — never published'), width=1300),
   dict(at=3, fn='stamp', frame=S + 'fail_drone.png', text=L('HORS SUJET', 'OFF TOPIC'), sub=L("des images de New York pour parler d'une IA", "New York drone shots for an AI story"))]),
 dict(id='seg04b', title=L("L'extrait", 'The clip'), clip=True,
      text=L(["« Lis ce texte comme un présentateur de journal télévisé, voix grave, posée, articulée, rythme soutenu mais naturel, sans emphase excessive. »"],
             ["“Read this as a TV news anchor, deep, calm, articulate, brisk but natural pace, no excessive emphasis.” (in French)"]),
      shots=[dict(at=0, fn='wave', wav='audio/fr/seg04b.wav', quote=L("« Lis ce texte comme un présentateur de journal télévisé… sans emphase excessive. »", "“Read this as a TV news anchor… no excessive emphasis.”"))]),
 dict(id='seg05', title=L('La décision', 'The decision'), shots=[
   dict(at=0, fn='stamp', frame=S + 'fail_title.png', text=L('REFUSÉ', 'REJECTED'), sub=L("rien n'a été publié", 'nothing was published')),
   dict(at=3, fn='title', lines=L([["RÈGLE N°1", CY], ["je valide le sujet", WH]], [["RULE #1", CY], ["I approve the topic", WH]])),
   dict(at=4, fn='title', lines=L([["sport · cinéma · people", WH], ["presque pas d'images libres", RD]], [["sports · movies · celebs", WH], ["almost no free footage", RD]])),
   dict(at=6, fn='rename', old='TempoBrief', avatar=B + 'avatar_briefai.png')]),
 dict(id='seg06', title=L('Bilan', 'Takeaways'), shots=[
   dict(at=0, fn='counters', items=L([["3h30", "de travail", CY], ["6", "programmes\nécrits", VI], ["1", "vidéo\nrefusée", RD], ["0", "vue pour\nl'instant", GR]],
                                    [["3.5h", "of work", CY], ["6", "programs\nwritten", VI], ["1", "video\nrejected", RD], ["0", "views\nso far", GR]])),
   dict(at=3, fn='title', lines=L([["chaque semaine", WH], ["vues · abonnés · coûts · revenus", CY]], [["every week", WH], ["views · subs · costs · revenue", CY]])),
   dict(at=4, fn='window', shot=S + 'channel.jpg', title='youtube.com/@briefai')])]
order = ['seg01', 'seg02', 'seg03', 'seg04', 'seg05', 'seg06']
for s in segs:
    if not s.get('clip'):
        k = order.index(s['id']); s['text'] = {'fr': J['fr'][k], 'en': J['en'][k]}
ep = {'slug': '2026-11-20-ia-jour1', 'gfx': 'gfx_ai', 'date': {'fr': 'JOUR 1', 'en': 'DAY 1'},
      'badge': {'fr': 'EXPÉRIENCE IA · JOUR 1', 'en': 'AI EXPERIMENT · DAY 1'},
      'title': {'fr': "J'ai laissé une IA créer ma chaîne YouTube", 'en': 'I let an AI build my YouTube channel'},
      'footage': {}, 'segments': segs,
      'shorts': [{'id': 's1', 'from': 'seg01', 'to': 'seg02', 'max': 45}, {'id': 's2', 'from': 'seg04', 'to': 'seg05', 'max': 45}, {'id': 's3', 'from': 'seg05', 'to': 'seg06', 'max': 45}]}
json.dump(ep, open('segments.json', 'w'), ensure_ascii=False, indent=1)
print([len(x) for x in J['fr']], [len(x) for x in J['en']])
