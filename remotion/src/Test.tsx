import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, spring, interpolate, Easing, staticFile} from 'remotion';

const C = {bg: '#07080d', cyan: '#00d4ff', violet: '#7c5cff', white: '#f0f4fa', grey: '#8a93a8', green: '#28dc8c', panel: 'rgba(22,25,38,0.72)'};
const fonts = `@font-face{font-family:SG;src:url(${staticFile('SpaceGrotesk.ttf')});font-weight:300 700}
@font-face{font-family:JB;src:url(${staticFile('JetBrainsMono.ttf')});font-weight:100 800}`;

const Bg: React.FC = () => {
  const f = useCurrentFrame();
  const x = Math.sin(f / 90) * 120, y = Math.cos(f / 110) * 80;
  return <AbsoluteFill style={{background: C.bg}}>
    <AbsoluteFill style={{background: `radial-gradient(900px 600px at ${760 + x}px ${420 + y}px, rgba(124,92,255,0.35), transparent 70%)`}} />
    <AbsoluteFill style={{background: `radial-gradient(700px 500px at ${1300 - x}px ${720 - y}px, rgba(0,212,255,0.18), transparent 70%)`}} />
    <AbsoluteFill style={{backgroundImage: 'linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)', backgroundSize: '64px 64px', maskImage: 'radial-gradient(circle at 50% 45%, black 30%, transparent 80%)'}} />
  </AbsoluteFill>;
};

const StepBadge: React.FC<{n: number; total: number}> = ({n, total}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 16}});
  return <div style={{position: 'absolute', top: 60, left: 80, transform: `translateX(${(1 - s) * -60}px)`, opacity: s, display: 'flex', alignItems: 'center', gap: 18}}>
    <div style={{fontFamily: 'JB', fontSize: 26, letterSpacing: 4, color: C.cyan, padding: '10px 20px', border: `2px solid ${C.cyan}`, borderRadius: 999, background: 'rgba(0,212,255,0.08)', boxShadow: '0 0 30px rgba(0,212,255,0.25)'}}>ÉTAPE {n} / {total}</div>
    <div style={{display: 'flex', gap: 8}}>{Array.from({length: total}).map((_, i) => <div key={i} style={{width: 34, height: 6, borderRadius: 3, background: i < n ? C.cyan : 'rgba(255,255,255,0.15)'}} />)}</div>
  </div>;
};

const Title: React.FC = () => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const a = spring({frame: f - 6, fps, config: {damping: 18}}); const b = spring({frame: f - 16, fps, config: {damping: 18}});
  const out = interpolate(f, [100, 118], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity: out}}>
    <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 104, color: C.white, transform: `translateY(${(1 - a) * 40}px)`, opacity: a, letterSpacing: -2}}>Écris ton fichier <span style={{background: `linear-gradient(90deg, ${C.cyan}, ${C.violet})`, WebkitBackgroundClip: 'text', color: 'transparent'}}>SKILL.md</span></div>
    <div style={{fontFamily: 'SG', fontWeight: 400, fontSize: 40, color: C.grey, marginTop: 20, transform: `translateY(${(1 - b) * 30}px)`, opacity: b}}>3 blocs : un nom, une description, des instructions</div>
  </AbsoluteFill>;
};

const lines: [string, string][] = [
  ['---', C.grey], ['name: scenariste-youtube', C.cyan],
  ['description: Écrit le script d\'une vidéo YouTube tuto', C.white], ['  au format de ma chaîne. À utiliser dès que', C.white], ['  je demande un script ou une voix off.', C.white],
  ['---', C.grey], ['', C.white], ['# Scénariste YouTube', C.violet], ['1. [ACCROCHE] le résultat en 5 secondes', C.white], ['2. [ÉTAPES] le bouton exact à cliquer', C.white], ['3. [ERREURS] 2 erreurs et la solution', C.white],
];

const Editor: React.FC = () => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const enter = spring({frame: f, fps, config: {damping: 20, mass: 0.9}});
  const zoom = interpolate(f, [120, 160], [1, 1.32], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  const zx = interpolate(f, [120, 160], [0, 230], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  const zy = interpolate(f, [120, 160], [0, 90], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  const chars = Math.floor(interpolate(f, [10, 105], [0, lines.reduce((s, l) => s + l[0].length + 1, 0)], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  let left = chars;
  const hl = spring({frame: f - 150, fps, config: {damping: 14}});
  const call = spring({frame: f - 168, fps, config: {damping: 12}});
  const cx = interpolate(f, [128, 158], [1500, 900], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  const cy = interpolate(f, [128, 158], [900, 380], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  return <AbsoluteFill style={{transform: `scale(${zoom})`, transformOrigin: '760px 360px'}}>
    <div style={{position: 'absolute', left: 260, top: 170, width: 1400, height: 740, borderRadius: 22, background: C.panel, border: '1px solid rgba(255,255,255,0.10)', backdropFilter: 'blur(18px)', boxShadow: '0 40px 120px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.08)', transform: `perspective(1800px) rotateX(${(1 - enter) * 14}deg) translateY(${(1 - enter) * 80}px)`, opacity: enter, overflow: 'hidden'}}>
      <div style={{height: 58, display: 'flex', alignItems: 'center', gap: 10, padding: '0 22px', borderBottom: '1px solid rgba(255,255,255,0.07)', background: 'rgba(255,255,255,0.03)'}}>
        {['#ff5f57', '#febc2e', '#28c840'].map(c => <div key={c} style={{width: 14, height: 14, borderRadius: 7, background: c}} />)}
        <div style={{fontFamily: 'JB', fontSize: 20, color: C.grey, marginLeft: 18}}>scenariste-youtube / SKILL.md</div>
      </div>
      <div style={{padding: '30px 40px', fontFamily: 'JB', fontSize: 31, lineHeight: '50px'}}>
        {lines.map(([t, col], i) => { const n = Math.max(0, Math.min(t.length, left)); left -= t.length + 1;
          const isDesc = i >= 2 && i <= 4;
          return <div key={i} style={{display: 'flex', position: 'relative'}}>
            <span style={{width: 50, color: 'rgba(255,255,255,0.2)'}}>{i + 1}</span>
            {isDesc && <div style={{position: 'absolute', left: 40, right: -10, top: 0, bottom: 0, background: `rgba(0,212,255,${0.13 * hl})`, borderLeft: `4px solid rgba(0,212,255,${hl})`}} />}
            <span style={{color: col, position: 'relative'}}>{t.slice(0, n)}{n < t.length && n > 0 && f % 20 < 10 ? '▌' : ''}</span>
          </div>; })}
      </div>
    </div>
    <div style={{position: 'absolute', left: 700, top: 545, transform: `scale(${call})`, transformOrigin: 'left top', opacity: call, fontFamily: 'SG', fontWeight: 700, fontSize: 30, color: '#07080d', background: C.cyan, padding: '14px 24px', borderRadius: 14, boxShadow: '0 12px 40px rgba(0,212,255,0.45)'}}>≤ 200 caractères · c'est ce que Claude lit</div>
    <svg style={{position: 'absolute', left: cx, top: cy, filter: 'drop-shadow(0 6px 10px rgba(0,0,0,0.5))'}} width="40" height="48" viewBox="0 0 40 48"><path d="M4 2 L4 38 L14 29 L21 45 L28 42 L21 27 L35 27 Z" fill="#fff" stroke="#07080d" strokeWidth="2.5" /></svg>
  </AbsoluteFill>;
};

const Breadcrumb: React.FC = () => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const items = ['Personnaliser', 'Skills', '+ Créer un skill', 'Importer un skill'];
  const toast = spring({frame: f - 78, fps, config: {damping: 13}});
  return <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
    <div style={{display: 'flex', alignItems: 'center', gap: 22}}>
      {items.map((t, i) => { const s = spring({frame: f - i * 14, fps, config: {damping: 15}}); const last = i === items.length - 1;
        const click = interpolate(f - (i * 14 + 10), [0, 12], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return <React.Fragment key={t}>
          <div style={{position: 'relative', fontFamily: 'SG', fontWeight: 600, fontSize: 40, color: last ? '#07080d' : C.white, background: last ? C.cyan : 'rgba(255,255,255,0.06)', border: `1px solid ${last ? C.cyan : 'rgba(255,255,255,0.14)'}`, padding: '20px 32px', borderRadius: 18, transform: `translateY(${(1 - s) * 30}px) scale(${0.9 + 0.1 * s})`, opacity: s, boxShadow: last ? '0 16px 50px rgba(0,212,255,0.35)' : '0 10px 30px rgba(0,0,0,0.35)'}}>
            {t}
            <div style={{position: 'absolute', left: '50%', top: '50%', width: 160 * click, height: 160 * click, marginLeft: -80 * click, marginTop: -80 * click, borderRadius: '50%', border: `3px solid rgba(0,212,255,${1 - click})`}} />
          </div>
          {i < items.length - 1 && <div style={{fontFamily: 'SG', fontSize: 40, color: C.grey, opacity: s}}>›</div>}
        </React.Fragment>; })}
    </div>
    <div style={{position: 'absolute', bottom: 170, opacity: toast, transform: `translateY(${(1 - toast) * 40}px)`, display: 'flex', alignItems: 'center', gap: 16, fontFamily: 'SG', fontWeight: 600, fontSize: 34, color: C.white, background: 'rgba(40,220,140,0.12)', border: `1px solid ${C.green}`, padding: '18px 30px', borderRadius: 16}}>
      <div style={{width: 40, height: 40, borderRadius: 20, background: C.green, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#07080d', fontSize: 26, fontWeight: 800}}>✓</div>
      Skill importé : scenariste-youtube
    </div>
  </AbsoluteFill>;
};

export const Test: React.FC = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{overflow: 'hidden'}}>
    <style>{fonts}</style>
    <Bg />
    <Sequence from={0} durationInFrames={120}><Title /></Sequence>
    <Sequence from={105} durationInFrames={225}><Editor /></Sequence>
    <Sequence from={330} durationInFrames={120}><Breadcrumb /></Sequence>
    <StepBadge n={f < 330 ? 3 : 5} total={8} />
  </AbsoluteFill>;
};
