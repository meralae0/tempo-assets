import sys, json, shutil
sys.path.insert(0, '../../tools'); import assemble as A
ep = json.load(open('segments.json')); align = {}
for seg in ep['segments']:
    sid = seg['id']; src = f'audio/en/t_{sid}.wav'; shutil.copy(src, f'audio/en/{sid}.wav')
    st = A._sentence_times_dp(src, seg['text']['en']); align[f'en_{sid}'] = [round(s, 3) for s, e, t in st]
json.dump(align, open('align.json', 'w'), indent=1); print('ok', len(align))
