// Aides YouTube Studio (à coller une fois par onglet via javascript_tool), puis :
//   await __up(url, 'nom.mp4')        → dépose la vidéo dans le dialogue d'import (?d=ud)
//   __fill('titre', 'description')    → remplit titre + description (écran Détails)
//   __kids(false)                     → « Non, ce n'est pas une vidéo conçue pour les enfants »
//   __altered(true)                   → contenu modifié/synthétique = Oui
//   await __thumb(url)                → miniature
window.__fileFrom = async (url, name, type) => { const b = await (await fetch(url)).blob(); return new File([b], name, { type: type || b.type || 'video/mp4' }); };
window.__setInput = (inp, file) => { const dt = new DataTransfer(); dt.items.add(file); inp.files = dt.files; inp.dispatchEvent(new Event('change', { bubbles: true })); };
window.__up = async (url, name) => { const f = await __fileFrom(url, name, 'video/mp4'); const inp = document.querySelector('input[name=Filedata]') || document.querySelector('input[type=file]'); __setInput(inp, f); return f.size; };
window.__fill = (title, desc) => {
  const boxes = [...document.querySelectorAll('#textbox[contenteditable=true]')];
  const put = (el, txt) => { el.focus(); document.execCommand('selectAll'); document.execCommand('insertText', false, txt); };
  if (title != null) put(boxes[0], title); if (desc != null) put(boxes[1], desc); return boxes.length;
};
window.__kids = (yes) => { const n = document.querySelector(yes ? 'tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_MFK]' : 'tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]'); n && n.click(); return !!n; };
window.__altered = (yes) => { const n = document.querySelector(yes ? 'tp-yt-paper-radio-button[name=VIDEO_HAS_ALTERED_CONTENT_YES]' : 'tp-yt-paper-radio-button[name=VIDEO_HAS_ALTERED_CONTENT_NO]'); n && n.click(); return !!n; };
window.__thumb = async (url) => { const f = await __fileFrom(url, 'thumb.jpg', 'image/jpeg'); const inp = [...document.querySelectorAll('input[type=file]')].find(i => (i.accept || '').includes('image')); if (!inp) return 'no input'; __setInput(inp, f); return f.size; };
'yt helpers ok';
