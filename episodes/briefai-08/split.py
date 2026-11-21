import sys, json, wave, numpy as np
sys.path.insert(0, '../../tools'); import assemble as A
seg = {s['id']: s for s in json.load(open('segments.json'))['segments']}
G = [['seg01','seg02','seg03'],['seg04','seg05','seg06','seg07'],['seg08','seg09','seg10']]
for l in ['fr','en']:
    for gi, g in enumerate(G):
        src = f'raw/{l}_c{gi+1}.wav'; w = wave.open(src); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16); w.close()
        sents = []; owner = []
        for sid in g:
            for t in seg[sid]['text'][l]: sents.append(t); owner.append(sid)
        st = A._sentence_times_dp(src, sents)
        cuts = [0]
        for i in range(1, len(sents)):
            if owner[i] != owner[i-1]: cuts.append(int((st[i-1][1] + st[i][0]) / 2 * sr))
        cuts.append(len(a))
        for k, sid in enumerate(g):
            o = wave.open(f'raw/{l}_{sid}.wav', 'wb'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(a[cuts[k]:cuts[k+1]].tobytes()); o.close()
            print(l, sid, round((cuts[k+1]-cuts[k])/sr, 1))
