import React from 'react';
import {AbsoluteFill, Sequence, Img, OffthreadVideo, useCurrentFrame, useVideoConfig, spring, interpolate, Easing, staticFile} from 'remotion';
import TL from './tl8.json';

const C = {bg: '#07080d', cyan: '#00d4ff', violet: '#7c5cff', white: '#f0f4fa', grey: '#8a93a8', green: '#28dc8c', red: '#ff4d5a', panel: 'rgba(22,25,38,0.72)'};
const COL: Record<string, string> = {c: C.cyan, w: C.white, r: C.red, g: C.green, v: C.violet};
const fonts = `@font-face{font-family:SG;src:url(${staticFile('SpaceGrotesk.ttf')});font-weight:300 700}
@font-face{font-family:JB;src:url(${staticFile('JetBrainsMono.ttf')});font-weight:100 800}`;
const IW = 1568;
const ease = Easing.bezier(0.65, 0, 0.35, 1);

const Bg: React.FC = () => {
  const f = useCurrentFrame();
  const x = Math.sin(f / 120) * 140, y = Math.cos(f / 150) * 90;
  return <AbsoluteFill style={{background: C.bg}}>
    <AbsoluteFill style={{background: `radial-gradient(1000px 650px at ${760 + x}px ${430 + y}px, rgba(124,92,255,0.30), transparent 70%)`}} />
    <AbsoluteFill style={{background: `radial-gradient(800px 560px at ${1320 - x}px ${760 - y}px, rgba(0,212,255,0.16), transparent 70%)`}} />
    <AbsoluteFill style={{backgroundImage: 'linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)', backgroundSize: '64px 64px', maskImage: 'radial-gradient(circle at 50% 45%, black 30%, transparent 80%)'}} />
  </AbsoluteFill>;
};

// ---------- fenêtre navigateur avec caméra ----------
const VW = 1600, VH = 720; // zone visible
// position du vrai curseur dans chaque capture (effacé de l'image, redessiné ici pour qu'il n'y ait qu'une seule flèche)
const BAKED: Record<string, number[]> = {};
type Rect = number[];
const camFor = (r: Rect | undefined, IH: number = 705) => {
  if (!r) return {s: VW / IW, tx: 0, ty: IH * VW / IW > VH ? 0 : (VH - IH * VW / IW) / 2};
  const [x, y, w, h] = r; const s = Math.min(VW / w, VH / h, 3.3); const sMin = VW / IW; const sc = Math.max(s, sMin);
  const cx = x + w / 2, cy = y + h / 2;
  let tx = VW / 2 - cx * sc, ty = VH / 2 - cy * sc;
  tx = Math.min(0, Math.max(VW - IW * sc, tx)); ty = Math.min(Math.max(0, (VH - IH * sc) / 2), Math.max(VH - IH * sc, ty));
  return {s: sc, tx, ty};
};

const Cursor: React.FC<{x: number; y: number}> = ({x, y}) => (
  <svg style={{position: 'absolute', left: x - 6, top: y - 4, filter: 'drop-shadow(0 6px 10px rgba(0,0,0,0.55))'}} width="40" height="48" viewBox="0 0 40 48"><path d="M4 2 L4 38 L14 29 L21 45 L28 42 L21 27 L35 27 Z" fill="#fff" stroke="#07080d" strokeWidth="2.5" /></svg>
);

const Shot: React.FC<{d: any}> = ({d}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const D = d.dur;
  const enter = d.cont ? 1 : spring({frame: f, fps, config: {damping: 22, mass: 0.8}});
  const camIn = interpolate(f, d.scroll ? [6, D - 4] : [0, Math.min(26, D * 0.35)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
  const IH = d.ih || 751; const a = camFor(d.cam0, IH), b = camFor(d.cam, IH), c2 = d.cam2 ? camFor(d.cam2, IH) : null;
  const drift = c2 ? interpolate(f, [Math.min(26, D - 2), D], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease}) : 0;
  const lerp = (p: number, q: number, t: number) => p + (q - p) * t;
  let s = lerp(a.s, b.s, camIn), tx = lerp(a.tx, b.tx, camIn), ty = lerp(a.ty, b.ty, camIn);
  if (c2) { s = lerp(s, c2.s, drift); tx = lerp(tx, c2.tx, drift); ty = lerp(ty, c2.ty, drift); }
  const P = (x: number, y: number) => [tx + x * s, ty + y * s];
  // curseur
  let cur: number[] | null = null; let clickT = -1;
  const bk = BAKED[d.img];
  // raw = capture d'origine avec son vrai curseur (aucune flèche ajoutée) : plan sans déplacement, ou clic à l'endroit où était déjà le curseur
  const raw = false;
  const path = d.cursor && !raw ? [bk || d.cursor[0], d.cursor[1]] : null;
  if (path) {
    const t0 = Math.min(18, Math.floor(D * 0.25)), t1 = Math.max(t0 + 4, Math.min(D - 12, 46));
    const m = interpolate(f, [t0, t1], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
    const [x0, y0] = path[0], [x1, y1] = path[1];
    cur = P(lerp(x0, x1, m), lerp(y0, y1, m)); if (d.click) clickT = t1 + 2;
  }
  let ripple: number[] | null = cur;
  if (raw && d.click && d.cursor) { clickT = Math.min(30, D - 18); ripple = P(bk ? bk[0] - 2 : d.cursor[1][0], bk ? bk[1] - 2 : d.cursor[1][1]); }
  const ck = clickT > 0 ? interpolate(f, [clickT, clickT + 16], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
  const hl = d.hl ? spring({frame: f - 22, fps, config: {damping: 15}}) : 0;
  const lab = d.label ? spring({frame: f - 34, fps, config: {damping: 14}}) : 0;
  const typeReveal = d.typing ? interpolate(f, [8, Math.max(20, D - 20)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 1;
  const out = d.contNext ? 1 : interpolate(f, [D - 6, D], [1, 0.0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const urlP = d.urlHl ? spring({frame: f - 20, fps, config: {damping: 14}}) : 0;
  const hp = d.hl ? (() => { const [x, y, w, h] = d.hl; const [px, py] = P(x, y); return [px, py, w * s, h * s]; })() : null;
  return <AbsoluteFill>
    <div style={{position: 'absolute', left: (1920 - VW) / 2, top: 168, width: VW, height: VH + 46, borderRadius: 20, overflow: 'hidden', background: '#1a1a1a', border: '1px solid rgba(255,255,255,0.10)', boxShadow: '0 50px 140px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.08)', transform: `translateY(${(1 - enter) * 40}px) scale(${0.97 + 0.03 * enter})`, opacity: Math.min(enter, out + 0.0001)}}>
      <div style={{height: 46, display: 'flex', alignItems: 'center', gap: 10, padding: '0 20px', background: '#232325', borderBottom: '1px solid rgba(255,255,255,0.06)'}}>
        {['#ff5f57', '#febc2e', '#28c840'].map(c => <div key={c} style={{width: 13, height: 13, borderRadius: 7, background: c}} />)}
        <div style={{marginLeft: 22, flex: 1, maxWidth: 520, height: 28, borderRadius: 8, background: d.urlHl ? 'rgba(0,212,255,0.18)' : '#161618', border: d.urlHl ? `2px solid ${C.cyan}` : 'none', boxShadow: d.urlHl ? `0 0 ${10 + 14 * urlP}px ${C.cyan}` : 'none', display: 'flex', alignItems: 'center', padding: '0 14px', fontFamily: 'SG', fontSize: 17, color: d.urlHl ? C.white : C.grey}}>🔒&nbsp; {d.url || 'claude.ai'}</div>
        {d.urlHl && <div style={{marginLeft: 16, fontFamily: 'SG', fontWeight: 700, fontSize: 20, color: '#07080d', background: C.cyan, padding: '3px 14px', borderRadius: 8, opacity: urlP}}>{d.urlHl}</div>}
      </div>
      <div style={{position: 'relative', width: VW, height: VH, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: tx, top: ty, width: IW * s, height: IH * s}}>
          <Img src={staticFile('caps8/' + d.img)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'top'}} />
          {d.typing && <div style={{position: 'absolute', left: 528 * s, top: 290 * s, width: (1045 - 528) * s, height: 85 * s, background: '#303030', transformOrigin: 'right', transform: `scaleX(${1 - typeReveal})`, marginLeft: 0, right: 0}} />}
          {([] as any[]).map((r: Rect, i: number) => <div key={i} style={{position: 'absolute', left: r[0] * s, top: r[1] * s, width: r[2] * s, height: r[3] * s, backdropFilter: 'blur(9px)', background: 'rgba(30,30,30,0.35)', borderRadius: 6}} />)}
        </div>
        {hp && <div style={{position: 'absolute', left: hp[0] - 8, top: hp[1] - 6, width: hp[2] + 16, height: hp[3] + 12, borderRadius: 12, border: `3px solid ${C.cyan}`, boxShadow: `0 0 0 ${9999 * 0}px rgba(0,0,0,0), 0 0 40px rgba(0,212,255,0.45)`, background: 'rgba(0,212,255,0.06)', opacity: hl, transform: `scale(${0.96 + 0.04 * hl})`}} />}
        {hp && d.label && <div style={{position: 'absolute', left: Math.min(VW - 560, Math.max(20, hp[0])), top: hp[1] - 76 > 8 ? hp[1] - 76 : hp[1] + hp[3] + 18, opacity: lab, transform: `translateY(${(1 - lab) * 12}px)`, fontFamily: 'SG', fontWeight: 700, fontSize: 30, color: '#07080d', background: C.cyan, padding: '10px 20px', borderRadius: 12, boxShadow: '0 12px 40px rgba(0,212,255,0.45)', whiteSpace: 'nowrap'}}>{d.label}</div>}
        {ripple && ck > 0 && ck < 1 && <div style={{position: 'absolute', left: ripple[0] - 50 * ck, top: ripple[1] - 50 * ck, width: 100 * ck, height: 100 * ck, borderRadius: '50%', border: `4px solid rgba(0,212,255,${1 - ck})`}} />}
        {cur && <>
          {false && <div style={{position: 'absolute', left: cur[0] - 50 * ck, top: cur[1] - 50 * ck, width: 100 * ck, height: 100 * ck, borderRadius: '50%', border: `4px solid rgba(0,212,255,${1 - ck})`}} />}
          <Cursor x={cur[0]} y={cur[1]} />
        </>}
      </div>
    </div>
  </AbsoluteFill>;
};

const Title: React.FC<{d: any}> = ({d}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const out = interpolate(f, [d.dur - 8, d.dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity: out}}>
    {d.lines.map(([t, c]: string[], i: number) => { const s = spring({frame: f - i * 6, fps, config: {damping: 16}});
      return <div key={i} style={{fontFamily: 'SG', fontWeight: 700, fontSize: i === 0 ? 120 : 76, letterSpacing: -2, color: COL[c] || C.white, opacity: s, transform: `translateY(${(1 - s) * 40}px)`, textShadow: `0 0 50px ${COL[c] || C.white}55`}}>{t}</div>; })}
  </AbsoluteFill>;
};

const Concept: React.FC<{d: any}> = ({d}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const a = spring({frame: f, fps, config: {damping: 18}}); const b = spring({frame: f - 40, fps, config: {damping: 16}}); const c = spring({frame: f - 90, fps, config: {damping: 16}});
  const card = (x: number, title: string, lines: string[], col: string, s: number) => <div style={{position: 'absolute', boxSizing: 'border-box', left: x, top: 330, width: 520, height: 400, borderRadius: 24, background: C.panel, border: `1px solid ${col}66`, boxShadow: `0 30px 90px rgba(0,0,0,0.5), 0 0 60px ${col}22`, padding: 34, opacity: s, transform: `translateY(${(1 - s) * 50}px)`}}>
    <div style={{fontFamily: 'JB', fontSize: 24, color: col, marginBottom: 20}}>{title}</div>
    {lines.map((l, i) => <div key={i} style={{fontFamily: 'SG', fontSize: 34, color: C.white, margin: '14px 0'}}>{l}</div>)}
  </div>;
  return <AbsoluteFill>
    <div style={{position: 'absolute', top: 150, width: '100%', textAlign: 'center', fontFamily: 'SG', fontWeight: 700, fontSize: 80, color: C.white, opacity: a}}>Un Skill = une fiche que Claude garde</div>
    {card(240, 'SKILL · scénariste YouTube', ['① accroche 5 s', '② étapes + bouton exact', '③ 2 erreurs', '④ temps et coût'], C.cyan, a)}
    <svg style={{position: 'absolute', left: 776, top: 500, opacity: b}} width="370" height="60" viewBox="0 0 370 60">
      <defs><linearGradient id="ag" gradientUnits="userSpaceOnUse" x1="10" y1="0" x2="340" y2="0"><stop offset="0" stopColor={C.cyan} /><stop offset="1" stopColor={C.violet} /></linearGradient></defs>
      <line x1="10" y1="30" x2={10 + 320 * b} y2="30" stroke="url(#ag)" strokeWidth="6" strokeLinecap="round" />
      <path d={`M ${330 * b - 6} 12 L ${330 * b + 18} 30 L ${330 * b - 6} 48`} fill="none" stroke={C.violet} strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
    {card(1160, 'TA DEMANDE', ['« Écris le script', 'd\'une vidéo… »', '', '→ Claude ouvre la fiche'], C.violet, c)}
  </AbsoluteFill>;
};

const Summary: React.FC<{d: any}> = ({d}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const items = [['30 s', 'pour vérifier', C.cyan], ['0 €', 'gratuit', C.green], ['−14 %', 'la vraie remise', C.violet]];
  return <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', flexDirection: 'row', gap: 40}}>
    {items.map(([v, l, c], i) => { const s = spring({frame: f - i * 8, fps, config: {damping: 15}});
      return <div key={i} style={{width: 420, height: 380, borderRadius: 26, background: C.panel, border: `2px solid ${c}`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: s, transform: `translateY(${(1 - s) * 50}px)`, boxShadow: `0 0 70px ${c}33`}}>
        <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 130, color: c}}>{v}</div>
        <div style={{fontFamily: 'JB', fontSize: 32, color: C.grey}}>{l}</div></div>; })}
  </AbsoluteFill>;
};

const Gift: React.FC<{d: any}> = ({d}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 18}});
  const lines = ["C'est une vraie promo ?", '[nom du produit] à [prix] : [lien]', '', "Cherche l'historique du prix", "et le prix chez d'autres vendeurs.", '', 'Réponds en 3 lignes :', 'vraie promo, fausse promo ou attendre ?', 'Donne tes sources.'];
  return <AbsoluteFill>
    <div style={{position: 'absolute', top: 110, width: '100%', textAlign: 'center', fontFamily: 'SG', fontWeight: 700, fontSize: 64, color: C.white, opacity: s}}>🎁 Gratuit dans la description</div>
    <div style={{position: 'absolute', left: 260, top: 230, width: 1400, height: 640, borderRadius: 22, background: C.panel, border: '1px solid rgba(255,255,255,0.1)', boxShadow: '0 40px 120px rgba(0,0,0,0.55)', overflow: 'hidden', opacity: s, transform: `perspective(1800px) rotateX(${(1 - s) * 12}deg)`}}>
      <div style={{height: 56, display: 'flex', alignItems: 'center', gap: 10, padding: '0 22px', background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid rgba(255,255,255,0.07)'}}>
        {['#ff5f57', '#febc2e', '#28c840'].map(c => <div key={c} style={{width: 14, height: 14, borderRadius: 7, background: c}} />)}
        <div style={{fontFamily: 'JB', fontSize: 20, color: C.grey, marginLeft: 16}}>la question exacte · à copier</div></div>
      <div style={{padding: '26px 40px', fontFamily: 'JB', fontSize: 30, lineHeight: '52px'}}>
        {lines.map((l, i) => { const v = interpolate(f, [8 + i * 4, 14 + i * 4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return <div key={i} style={{opacity: v, color: l.startsWith('[') ? C.cyan : l.startsWith('Réponds') ? C.violet : C.white}}><span style={{color: 'rgba(255,255,255,0.2)', marginRight: 24}}>{String(i + 1).padStart(2, ' ')}</span>{l}</div>; })}
      </div></div>
  </AbsoluteFill>;
};

const End: React.FC<{d: any}> = ({d}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 16}}); const b = spring({frame: f - 18, fps, config: {damping: 14}});
  return <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
    <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 84, color: C.white, opacity: s, transform: `translateY(${(1 - s) * 30}px)`, textAlign: 'center', maxWidth: 1500}}>Et toi, tu partirais où<br /><span style={{color: C.cyan}}>avec 500 € ?</span></div>
    <div style={{marginTop: 50, display: 'flex', alignItems: 'center', gap: 24, opacity: b}}>
      <Img src={staticFile('avatar_briefai.png')} style={{width: 90, height: 90}} />
      <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 34, color: C.grey}}>dis-le en commentaire 💬</div>
    </div>
  </AbsoluteFill>;
};



const Clip: React.FC<{d: any}> = ({d}) => {
  const f = useCurrentFrame(); const D = d.dur;
  const op = Math.min(interpolate(f, [0, 10], [0, 1], {extrapolateRight: 'clamp'}), interpolate(f, [D - 10, D], [1, 0], {extrapolateLeft: 'clamp'}));
  const z = interpolate(f, [0, D], [1.04, 1.12]);
  return <AbsoluteFill style={{opacity: op}}>
    <AbsoluteFill style={{transform: `scale(${z})`}}><OffthreadVideo src={staticFile('mcr/' + d.src)} startFrom={d.start || 0} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} /></AbsoluteFill>
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(7,8,13,0.25), transparent 30%, transparent 65%, rgba(7,8,13,0.7))'}} />
    {d.tag && <div style={{position: 'absolute', left: 70, bottom: 60, fontFamily: 'SG', fontWeight: 700, fontSize: 30, color: C.white, letterSpacing: 2, textShadow: '0 4px 20px rgba(0,0,0,0.6)'}}>📍 {d.tag}</div>}
  </AbsoluteFill>;
};

const Chapter: React.FC<{d: any}> = ({d}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 16}}); const out = interpolate(f, [d.dur - 8, d.dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity: out}}>
    <div style={{fontFamily: 'JB', fontSize: 34, letterSpacing: 6, color: C.cyan, opacity: s}}>VOYAGE {d.n} / 3</div>
    <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 110, color: C.white, opacity: s, transform: `translateY(${(1 - s) * 40}px)`, marginTop: 10}}>{d.who}</div>
    <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 64, color: C.green, opacity: s, marginTop: 6}}>{d.budget}</div>
    <div style={{fontFamily: 'SG', fontSize: 34, color: C.grey, opacity: s, marginTop: 24}}>{d.method}</div>
  </AbsoluteFill>;
};
const StepBadge: React.FC<{n: number; title: string; total: number}> = ({n, title, total}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 16}});
  return <div style={{position: 'absolute', top: 54, left: 160, display: 'flex', alignItems: 'center', gap: 22, opacity: s, transform: `translateX(${(1 - s) * -40}px)`}}>
    <div style={{fontFamily: 'JB', fontSize: 26, letterSpacing: 4, color: C.cyan, padding: '10px 20px', border: `2px solid ${C.cyan}`, borderRadius: 999, background: 'rgba(0,212,255,0.08)', boxShadow: '0 0 30px rgba(0,212,255,0.25)'}}>ÉTAPE {n} / {total}</div>
    <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 40, color: C.white}}>{title}</div>
    <div style={{display: 'flex', gap: 8, marginLeft: 10}}>{Array.from({length: total}).map((_, i) => <div key={i} style={{width: 40, height: 6, borderRadius: 3, background: i < n ? C.cyan : 'rgba(255,255,255,0.15)'}} />)}</div>
  </div>;
};

export const Trip8: React.FC = () => {
  const shots: any[] = (TL as any).shots;
  // regrouper les badges par étape (continu sur toute l'étape)
  const stepRuns: {from: number; dur: number; n: number; title: string}[] = [];
  shots.forEach(s => { if (!s.step) return; const last = stepRuns[stepRuns.length - 1];
    if (last && last.n === s.step) last.dur = s.from + s.dur - last.from; else stepRuns.push({from: s.from, dur: s.dur, n: s.step, title: s.stepTitle}); });
  return <AbsoluteFill style={{overflow: 'hidden'}}>
    <style>{fonts}</style>
    <Bg />
    {shots.map((d, i) => <Sequence key={i} from={d.from} durationInFrames={Math.max(1, d.dur)}>
      {d.kind === 'shot' ? <Shot d={d} /> : d.kind === 'clip' ? <Clip d={d} /> : d.kind === 'chapter' ? <Chapter d={d} /> : d.kind === 'title' ? <Title d={d} /> : d.kind === 'concept' ? <Concept d={d} /> : d.kind === 'summary' ? <Summary d={d} /> : d.kind === 'gift' ? <Gift d={d} /> : <End d={d} />}
    </Sequence>)}
    {stepRuns.map((r, i) => <Sequence key={'b' + i} from={r.from} durationInFrames={r.dur}><StepBadge n={r.n} title={r.title} total={3} /></Sequence>)}
  </AbsoluteFill>;
};
