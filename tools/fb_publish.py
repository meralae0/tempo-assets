#!/usr/bin/env python3
"""Programmation Facebook (page Brief AI) par l'API Graph — sans Chrome.
Jeton de page permanent : /home/claude/.secrets/fb_page_token (jamais dans le dépôt).
Les vidéos sont récupérées par Facebook depuis une URL publique (raw.githubusercontent.com/...@SHA).

  fb_publish.py reel  <url_mp4> "<légende>" "2026-11-27 13:00"
  fb_publish.py video <url_mp4> "<titre>" "<description>" "2026-11-28 18:00"
  fb_publish.py list            # publications programmées
Heure = heure du Maroc (UTC+0 en novembre ; Africa/Casablanca)."""
import sys, os, json, time, urllib.request, urllib.parse
from datetime import datetime
from zoneinfo import ZoneInfo
PAGE = '1468799139649767'; V = 'v24.0'
TOK = open(os.environ.get('FB_TOKEN_FILE', '/home/claude/.secrets/fb_page_token')).read().strip()

def call(method, url, params=None, headers=None):
    data = urllib.parse.urlencode({**(params or {}), 'access_token': TOK}).encode()
    if method == 'GET': url, data = url + '?' + data.decode(), None
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: return json.load(r)
    except urllib.error.HTTPError as e: sys.exit(f'HTTP {e.code}: {e.read().decode()[:600]}')
def ts(s):
    t = int(datetime.strptime(s, '%Y-%m-%d %H:%M').replace(tzinfo=ZoneInfo('Africa/Casablanca')).timestamp())
    if t < time.time() + 15 * 60: sys.exit('heure trop proche ou passée (min. 15 min, max. 29 jours pour Facebook)')
    return t

def reel(url, caption, when):
    t = ts(when); g = f'https://graph.facebook.com/{V}/{PAGE}/video_reels'
    st = call('POST', g, {'upload_phase': 'start'}); vid = st['video_id']
    req = urllib.request.Request(f'https://rupload.facebook.com/video-upload/{V}/{vid}', data=b'', method='POST',
                                 headers={'Authorization': f'OAuth {TOK}', 'file_url': url})
    with urllib.request.urlopen(req, timeout=300) as r: up = json.load(r)
    if not up.get('success'): sys.exit(f'upload: {up}')
    fin = call('POST', g, {'upload_phase': 'finish', 'video_id': vid, 'video_state': 'SCHEDULED',
                           'scheduled_publish_time': t, 'description': caption})
    print(json.dumps({'reel_video_id': vid, 'finish': fin, 'at': when}))

def video(url, title, desc, when):
    t = ts(when)
    r = call('POST', f'https://graph-video.facebook.com/{V}/{PAGE}/videos',
             {'file_url': url, 'title': title, 'description': desc, 'published': 'false', 'scheduled_publish_time': t})
    print(json.dumps({'video_id': r.get('id'), 'at': when}))

def lst():
    r = call('GET', f'https://graph.facebook.com/{V}/{PAGE}/scheduled_posts', {'fields': 'id,message,scheduled_publish_time', 'limit': 25})
    for p in r.get('data', []):
        print(datetime.fromtimestamp(p['scheduled_publish_time'], ZoneInfo('Africa/Casablanca')).strftime('%Y-%m-%d %H:%M'), p['id'], (p.get('message') or '')[:70].replace('\n', ' '))

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    {'reel': lambda: reel(*a[1:4]), 'video': lambda: video(*a[1:5]), 'list': lst}[a[0]]()
