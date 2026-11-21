import json, wave
FPS = 30
al = json.load(open('align.json')); ep = json.load(open('segments.json'))
def dur(p): w = wave.open(p); return w.getnframes() / w.getframerate()
# Plans : (seg, at, spec)   coordonnées dans l'image 1568x705
S = lambda img, **k: dict(kind='shot', img=img, **k)
T = lambda lines, **k: dict(kind='title', lines=lines, **k)
plan = {
 'seg01': [(0, S('13_test_tape.jpg', cam=[480, 280, 620, 130], blur=[[600, 240, 340, 55]], cursor=[[780, 330], [1033, 368]], click=True)),
           (2, S('14_chargeant_competence.jpg', cam=[470, 60, 640, 120], hl=[480, 128, 220, 30], label='Le Skill se charge tout seul')),
           (2.45, S('16_resultat_script.jpg', cam=[470, 290, 600, 330], cam2=[470, 330, 600, 300])),
           (3, T([['2 minutes', 'c'], ['0 code · 0 fichier', 'w']]))],
 'seg02': [(0, dict(kind='concept'))],
 'seg03': [(0, S('02_capacites.jpg', cam=[360, 20, 850, 670], cursor=[[700, 500], [440, 276]], click=True)),
           (2, S('02_capacites.jpg', cam=[540, 255, 660, 125], hl=[548, 265, 640, 112], label='Créer et modifier des fichiers : activé'))],
 'seg04': [(0, S('03_plugins_skills.jpg', cam=[380, 20, 820, 200], cursor=[[700, 160], [1041, 83]], click=True)),
           (1, S('04_menu_ajouter.jpg', cam=[880, 60, 330, 190], cursor=[[1041, 83], [1136, 83]], click=True)),
           (1.5, S('06_menu_creer_avec_claude.jpg', cam=[880, 60, 330, 190], hl=[936, 181, 230, 23], cursor=[[1136, 90], [1014, 192]], click=True)),
           (2, S('07_creer_prefill.jpg', cam=[500, 230, 570, 190], hl=[518, 304, 532, 34], label='Phrase déjà écrite'))],
 'seg05': [(0, S('07_creer_prefill.jpg', cam=[500, 230, 570, 190])),
           (1, S('08_demande_tapee.jpg', cam=[510, 270, 550, 150], typing=True)),
           (4, S('08_demande_tapee.jpg', cam=[500, 230, 570, 200], cursor=[[800, 360], [1033, 390]], click=True)),
           (4.6, S('09_proposition_en_cours.jpg', cam=[470, 60, 640, 180]))],
 'seg06': [(0, S('10_carte_skill.jpg', cam=[470, 225, 630, 200], blur=[[493, 306, 340, 15]], hl=[485, 236, 598, 172])),
           (1, S('11_contenu.jpg', cam=[470, 320, 630, 300], blur=[[493, 306, 340, 15]], cursor=[[700, 300], [519, 340]], click=True)),
           (2, S('11_contenu.jpg', cam=[800, 560, 330, 90], blur=[[493, 306, 340, 15]], cursor=[[900, 560], [1035, 613]], click=True)),
           (2.5, S('12_enregistre.jpg', cam=[470, 225, 630, 90], hl=[485, 262, 598, 30], label='Enregistré', blur=[[700, 507, 115, 16]])),
           (3, S('19_skill_dans_liste.jpg', cam=[380, 120, 560, 90], hl=[388, 155, 205, 35], label='Nouveau'))],
 'seg07': [(0, S('13_test_tape.jpg', cam=[480, 230, 620, 180], blur=[[600, 240, 340, 55]])),
           (1, S('13_test_tape.jpg', cam=[500, 290, 580, 110], hl=[518, 306, 532, 30], blur=[[600, 240, 340, 55]])),
           (3, S('14_chargeant_competence.jpg', cam=[470, 60, 640, 120], hl=[480, 128, 220, 30], label='Chargeant une compétence')),
           (4, S('17_resultat_etapes.jpg', cam=[470, 30, 600, 370], cam2=[470, 250, 600, 380]))],
 'seg08': [(0, T([['2 erreurs', 'r'], ['fréquentes', 'w']])),
           (1, T([['1 · le Skill', 'w'], ['ne se déclenche pas', 'r']])),
           (2, S('10_carte_skill.jpg', cam=[470, 260, 630, 80], hl=[488, 293, 580, 30], label='La description décide de tout', blur=[[493, 306, 340, 15]])),
           (4, T([['2 · enregistrer', 'w'], ['sans relire', 'r']])),
           (5, S('11_contenu.jpg', cam=[470, 330, 630, 280], hl=[488, 335, 70, 14], label='Ouvre toujours « Contenu »', blur=[[493, 306, 340, 15]]))],
 'seg09': [(0, dict(kind='summary')),
           (1, dict(kind='gift')),
           (2, S('05_import_vide.jpg', cam=[380, 20, 800, 120], hl=[985, 88, 100, 18], label='.md accepté')),
           (3, T([['Prochaine vidéo', 'c'], ['les vrais chiffres', 'w']])),
           (4, dict(kind='end'))]}
steps = {'seg03': 1, 'seg04': 2, 'seg05': 3, 'seg06': 4, 'seg07': 5}
titles = {'seg03': 'Vérifie l\'option', 'seg04': 'Créer avec Claude', 'seg05': 'Décris ton Skill', 'seg06': 'Relis et enregistre', 'seg07': 'Teste-le'}
out = []; t0 = 0.0; segsout = []
for seg in ep['segments']:
    sid = seg['id']; D = dur(f'audio/fr/{sid}.wav'); st = al[f'fr_{sid}']
    def at(a):
        k = int(a); f = a - k; s0 = st[k]; s1 = st[k + 1] if k + 1 < len(st) else D; return s0 + f * (s1 - s0)
    items = plan[sid]; starts = [0.0 if i == 0 else at(a) for i, (a, _) in enumerate(items)] + [D]
    for i, (a, spec) in enumerate(items):
        d = dict(spec); d['from'] = round((t0 + starts[i]) * FPS); d['dur'] = round((starts[i + 1] - starts[i]) * FPS)
        if sid in steps: d['step'] = steps[sid]; d['stepTitle'] = titles[sid]
        out.append(d)
    segsout.append([sid, round(t0, 2)]); t0 += D
END = 6.0
out[-1]['dur'] += round(END * FPS)
total = round((t0 + END) * FPS)
json.dump({'shots': out, 'total': total, 'segs': segsout}, open('../../remotion/src/timeline.json', 'w'), ensure_ascii=False, indent=1)
print('total', total / FPS, 's', len(out), 'plans')
