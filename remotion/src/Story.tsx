import React from 'react';
import {AbsoluteFill, Sequence, Img, useCurrentFrame, useVideoConfig, spring, interpolate, Easing, staticFile, random} from 'remotion';
import TL from './tl4.json';

const C = {bg: '#07080d', cyan: '#00d4ff', violet: '#7c5cff', white: '#f0f4fa', grey: '#8a93a8', green: '#28dc8c', red: '#ff4d5a', amber: '#ffb547', panel: 'rgba(22,25,38,0.78)'};
const fonts = `@font-face{font-family:SG;src:url(${staticFile('SpaceGrotesk.ttf')});font-weight:300 700}
@font-face{font-family:JB;src:url(${staticFile('JetBrainsMono.ttf')});font-weight:100 800}
@font-face{font-family:PF;src:url(${staticFile('PlayfairDisplay.ttf')});font-weight:400 900;font-style:normal italic}`;
const ease = Easing.bezier(0.65, 0, 0.35, 1);
const cl = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

type Seg = {id: string; from: number; dur: number; st: number[]};
const Ctx = React.createContext<Seg>({id: '', from: 0, dur: 1, st: [0]});
const useS = () => {
  const s = React.useContext(Ctx); const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const at = (k: number) => s.st[Math.min(k, s.st.length - 1)] ?? 0;
  const sp = (k: number, d = 0, damping = 16) => spring({frame: f - at(k) - d, fps, config: {damping}});
  const lin = (a: number, b: number) => interpolate(f, [a, Math.max(a + 1, b)], [0, 1], {...cl, easing: ease});
  return {f, fps, s, at, sp, lin, D: s.dur};
};

const Bg: React.FC = () => {
  const f = useCurrentFrame();
  const x = Math.sin(f / 140) * 160, y = Math.cos(f / 170) * 100;
  return <AbsoluteFill style={{background: C.bg}}>
    <AbsoluteFill style={{background: `radial-gradient(1100px 700px at ${760 + x}px ${420 + y}px, rgba(124,92,255,0.26), transparent 70%)`}} />
    <AbsoluteFill style={{background: `radial-gradient(900px 600px at ${1300 - x}px ${780 - y}px, rgba(0,212,255,0.14), transparent 70%)`}} />
    <AbsoluteFill style={{backgroundImage: 'linear-gradient(rgba(255,255,255,0.028) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.028) 1px, transparent 1px)', backgroundSize: '64px 64px', maskImage: 'radial-gradient(circle at 50% 45%, black 30%, transparent 80%)'}} />
  </AbsoluteFill>;
};

const T: React.FC<{s: number; size?: number; color?: string; font?: string; style?: React.CSSProperties; children: React.ReactNode}> = ({s, size = 72, color = C.white, font = 'SG', style, children}) =>
  <div style={{fontFamily: font, fontWeight: 700, fontSize: size, color, opacity: s, transform: `translateY(${(1 - s) * 30}px)`, letterSpacing: font === 'SG' ? -1 : 0, ...style}}>{children}</div>;

const Panel: React.FC<{s: number; x: number; y: number; w: number; h: number; col?: string; children?: React.ReactNode; style?: React.CSSProperties}> = ({s, x, y, w, h, col = C.cyan, children, style}) =>
  <div style={{position: 'absolute', left: x, top: y, width: w, height: h, boxSizing: 'border-box', borderRadius: 22, background: C.panel, border: `1px solid ${col}55`, boxShadow: `0 30px 90px rgba(0,0,0,0.5), 0 0 50px ${col}1f`, opacity: s, transform: `translateY(${(1 - s) * 40}px) scale(${0.96 + 0.04 * s})`, padding: 30, ...style}}>{children}</div>;

const Label: React.FC<{children: React.ReactNode; col?: string}> = ({children, col = C.cyan}) =>
  <div style={{fontFamily: 'JB', fontSize: 24, letterSpacing: 3, color: col, textTransform: 'uppercase', marginBottom: 14}}>{children}</div>;

const Count: React.FC<{to: number; p: number; dec?: number; suffix?: string}> = ({to, p, dec = 0, suffix = ''}) => {
  const v = to * p; const txt = dec ? v.toFixed(dec).replace('.', ',') : Math.round(v).toLocaleString('fr-FR').replace(/ | /g, ' ');
  return <>{txt}{suffix}</>;
};

// grille de points (agents)
const Dots: React.FC<{n: number; cols: number; x: number; y: number; gap: number; r: number; on: (i: number) => number; col?: (i: number) => string}> = ({n, cols, x, y, gap, r, on, col}) => {
  const items = [];
  for (let i = 0; i < n; i++) {
    const o = on(i); const cx = x + (i % cols) * gap, cy = y + Math.floor(i / cols) * gap; const c = col ? col(i) : C.cyan;
    items.push(<circle key={i} cx={cx} cy={cy} r={r * (0.4 + 0.6 * o)} fill={c} opacity={0.12 + 0.88 * o} />);
  }
  return <>{items}</>;
};

// ---------------- scènes ----------------
const S01: React.FC = () => {
  const {f, sp, at} = useS();
  const lines: [string, string][] = [['1 000 IA', C.cyan], ['1 objectif : le théorème le plus célèbre des maths', C.white], ['0 humain pour les diriger', C.white], ['< 30 heures', C.green], ['Comment ?', C.violet]];
  const k = lines.reduce((acc, _, i) => (f >= at(i) ? i : acc), 0);
  return <AbsoluteFill>
    <svg width={1920} height={1080} style={{position: 'absolute'}}>
      <Dots n={1000} cols={50} x={372} y={312} gap={24} r={7} on={(i) => interpolate(f, [random('d' + i) * 50, random('d' + i) * 50 + 8], [0, 1], cl)} col={(i) => (k >= 3 ? (random('g' + i) < 0.9 ? C.green : C.cyan) : random('v' + i) < 0.15 ? C.violet : C.cyan)} />
    </svg>
    <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 50%, rgba(7,8,13,0.92) 0%, rgba(7,8,13,0.55) 45%, rgba(7,8,13,0.1) 80%)'}} />
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', textAlign: 'center'}}>
      {lines.map(([t, c], i) => i === k && <T key={i} s={sp(i)} size={i === 0 ? 220 : i === 3 ? 170 : 84} color={c} style={{maxWidth: 1500, textShadow: `0 0 60px ${c}66`}}>{t}</T>)}
    </AbsoluteFill>
  </AbsoluteFill>;
};

const S02: React.FC = () => {
  const {sp, f, at} = useS();
  const a = sp(0), b = sp(1), c = sp(2);
  const bar = interpolate(f, [at(2) + 5, at(2) + 45], [0, 1], {...cl, easing: ease});
  return <AbsoluteFill>
    <div style={{position: 'absolute', top: 120, width: '100%', textAlign: 'center', opacity: a, transform: `scale(${0.9 + 0.1 * a})`}}>
      <div style={{fontFamily: 'PF', fontStyle: 'italic', fontSize: 150, color: C.white}}>a<sup style={{fontSize: 80}}>n</sup> + b<sup style={{fontSize: 80}}>n</sup> <span style={{color: C.red}}>≠</span> c<sup style={{fontSize: 80}}>n</sup></div>
      <div style={{fontFamily: 'JB', fontSize: 40, color: C.cyan, marginTop: 6}}>pour tout n &gt; 2</div>
    </div>
    <Panel s={b} x={250} y={560} w={640} h={330} col={C.amber}>
      <Label col={C.amber}>1637 · Pierre de Fermat</Label>
      <div style={{fontFamily: 'PF', fontStyle: 'italic', fontSize: 44, lineHeight: '62px', color: '#f3e6c8'}}>« J'en ai une preuve merveilleuse… mais la marge est trop petite. »</div>
    </Panel>
    <Panel s={c} x={1030} y={560} w={640} h={330} col={C.cyan}>
      <Label>1995 · Andrew Wiles</Label>
      <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 110, color: C.white}}>129 <span style={{fontSize: 50, color: C.grey}}>pages</span></div>
      <div style={{fontFamily: 'SG', fontSize: 34, color: C.grey}}>des mois pour la vérifier</div>
    </Panel>
    <div style={{position: 'absolute', left: 250, top: 935, width: 1420 * bar, height: 6, borderRadius: 3, background: `linear-gradient(90deg, ${C.amber}, ${C.cyan})`, opacity: c}} />
    <div style={{position: 'absolute', left: 0, top: 960, width: '100%', textAlign: 'center', fontFamily: 'JB', fontSize: 30, color: C.grey, opacity: bar}}>358 ans plus tard</div>
  </AbsoluteFill>;
};

const LEAN = ['theorem step_017 (E : EllipticCurve ℚ) :', '  E.IsModular := by', '  apply modularity_lifting', '  · exact residual_irreducible E', '  · simp [frobenius_trace]', 'lemma step_018 : ...', '  := by omega', 'theorem goal : ∀ n > 2, ¬ ∃ a b c, ...'];
const S03: React.FC = () => {
  const {f, sp, at, lin} = useS();
  const a = sp(0), b = sp(1), c = sp(2);
  const p = lin(at(1), at(1) + 50);
  return <AbsoluteFill>
    <Panel s={a} x={160} y={160} w={900} h={720} col={C.violet} style={{padding: 0, overflow: 'hidden'}}>
      <div style={{height: 52, display: 'flex', alignItems: 'center', gap: 10, padding: '0 22px', borderBottom: '1px solid rgba(255,255,255,0.08)'}}>
        {['#ff5f57', '#febc2e', '#28c840'].map((c) => <div key={c} style={{width: 13, height: 13, borderRadius: 7, background: c}} />)}
        <div style={{fontFamily: 'JB', fontSize: 20, color: C.grey, marginLeft: 14}}>Fermat.lean · illustration</div>
      </div>
      <div style={{height: 668, overflow: 'hidden'}}><div style={{padding: '20px 28px', fontFamily: 'JB', fontSize: 25, lineHeight: '46px', transform: `translateY(${-((f * 1.4) % 368)}px)`}}>
        {[...LEAN, ...LEAN, ...LEAN].map((l, i) => <div key={i} style={{color: l.startsWith('theorem') || l.startsWith('lemma') ? C.violet : l.includes('by') ? C.cyan : C.white, whiteSpace: 'pre'}}>{l} <span style={{color: C.green}}>{i % 3 === 0 ? ' ✓' : ''}</span></div>)}
      </div></div>
    </Panel>
    <div style={{position: 'absolute', left: 1140, top: 190, display: 'flex', flexDirection: 'column', gap: 26}}>
      {[[<>des dizaines</>, "d'agents Claude", C.cyan], [<><Count to={11} p={p} /></>, 'jours', C.violet], [<><Count to={13} p={p} /> M</>, 'lignes vérifiées', C.green]].map(([v, l, c], i) => {
        const s = sp(1, i * 6);
        return <div key={i} style={{opacity: s, transform: `translateX(${(1 - s) * 40}px)`}}>
          <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 92, color: c as string, lineHeight: '96px'}}>{v}</div>
          <div style={{fontFamily: 'JB', fontSize: 28, color: C.grey}}>{l}</div></div>;
      })}
    </div>
    <div style={{position: 'absolute', left: 1150, top: 820, fontFamily: 'SG', fontWeight: 700, fontSize: 52, color: C.bg, background: C.green, padding: '10px 30px', borderRadius: 14, opacity: c, transform: `rotate(-4deg) scale(${0.6 + 0.4 * c})`, boxShadow: '0 16px 50px rgba(40,220,140,0.4)'}}>UNE PREMIÈRE · sept. 2026</div>
  </AbsoluteFill>;
};

const S04: React.FC = () => {
  const {f, sp, at} = useS();
  const a = sp(0), b = sp(1), c = sp(2), d = sp(3);
  return <AbsoluteFill>
    <div style={{position: 'absolute', top: 70, width: '100%', textAlign: 'center'}}><T s={a} size={64}>9 novembre · <span style={{color: C.cyan}}>1 000 agents</span> Claude Fable 5.2</T></div>
    <svg width={1920} height={1080} style={{position: 'absolute'}}>
      <line x1={960} y1={300} x2={960} y2={360} stroke={C.violet} strokeWidth={4} opacity={b} />
      <Dots n={999} cols={54} x={430} y={400} gap={20} r={6} on={(i) => interpolate(f, [at(1) + random('h' + i) * 40, at(1) + random('h' + i) * 40 + 6], [0, 1], cl)} />
    </svg>
    <div style={{position: 'absolute', left: 860, top: 190, width: 200, height: 110, borderRadius: 20, background: `linear-gradient(135deg, ${C.violet}, #4b33c9)`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: b, transform: `scale(${0.7 + 0.3 * b})`, boxShadow: '0 0 60px rgba(124,92,255,0.6)'}}>
      <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 40, color: C.white}}>1 chef</div></div>
    <div style={{position: 'absolute', left: 1545, top: 420, fontFamily: 'SG', fontWeight: 700, fontSize: 56, color: C.cyan, opacity: b}}>999<br /><span style={{fontSize: 30, color: C.grey}}>aides</span></div>
    <div style={{position: 'absolute', bottom: 70, width: '100%', display: 'flex', justifyContent: 'center', gap: 40}}>
      {[['✕ messagerie', C.red, c], ['✕ internet', C.red, c], ['✓ Git', C.green, d], ['✓ base de données partagée', C.green, d]].map(([t, col, s], i) =>
        <div key={i} style={{fontFamily: 'SG', fontWeight: 700, fontSize: 36, color: col as string, padding: '14px 28px', borderRadius: 14, border: `2px solid ${col}`, background: `${col}14`, opacity: s as number, transform: `translateY(${(1 - (s as number)) * 30}px)`}}>{t}</div>)}
    </div>
  </AbsoluteFill>;
};

const S05: React.FC = () => {
  const {f, sp, at} = useS();
  const tabs = ['ordres', 'qui fait quoi', 'notes', 'tâches', 'terminé'];
  const b = sp(1);
  const crew = (i: number) => [C.cyan, C.violet, C.green, C.amber][Math.floor(i / 15)];
  return <AbsoluteFill>
    <div style={{position: 'absolute', top: 80, width: '100%', textAlign: 'center'}}><T s={sp(0)} size={58}>10 minutes · <span style={{color: C.cyan}}>5 tableaux</span> partagés</T></div>
    <div style={{position: 'absolute', top: 200, width: '100%', display: 'flex', justifyContent: 'center', gap: 26}}>
      {tabs.map((t, i) => { const s = sp(0, 8 + i * 7); return <div key={i} style={{width: 300, height: 190, boxSizing: 'border-box', borderRadius: 18, background: C.panel, border: `1px solid ${C.cyan}44`, opacity: s, transform: `translateY(${(1 - s) * 40}px)`, overflow: 'hidden'}}>
        <div style={{fontFamily: 'JB', fontSize: 24, color: C.cyan, padding: '14px 18px', borderBottom: `1px solid ${C.cyan}33`}}>{t}</div>
        {[0, 1, 2, 3].map((r) => <div key={r} style={{margin: '14px 18px 0', height: 10, borderRadius: 5, background: 'rgba(255,255,255,0.12)', width: `${40 + random(t + r) * 55}%`}} />)}
      </div>; })}
    </div>
    <div style={{position: 'absolute', top: 470, width: '100%', textAlign: 'center'}}><T s={b} size={46} color={C.grey}>le but → <span style={{color: C.white}}>60 étapes</span> → des équipes</T></div>
    <div style={{position: 'absolute', left: 360, top: 570, display: 'grid', gridTemplateColumns: 'repeat(15, 64px)', gap: 14}}>
      {Array.from({length: 60}).map((_, i) => { const s = spring({frame: f - at(1) - 10 - i, fps: 30, config: {damping: 14}}); const g = interpolate(f, [at(1) + 80, at(1) + 110], [0, 1], cl);
        return <div key={i} style={{width: 64, height: 64, borderRadius: 12, background: g > 0 ? `${crew(i)}${Math.round(40 + 160 * g).toString(16).padStart(2, '0')}` : 'rgba(255,255,255,0.1)', border: `2px solid ${g > 0.5 ? crew(i) : 'rgba(255,255,255,0.2)'}`, opacity: s, transform: `scale(${s})`}} />; })}
    </div>
  </AbsoluteFill>;
};

const S06: React.FC = () => {
  const {f, sp, at} = useS();
  const red = (i: number) => i >= 13; // 47 « impossibles »
  const st = (i: number) => {
    if (i < 3) return f >= at(1) ? 'ok' : 'idle';
    if (i < 13) return f >= at(3) + (i - 3) * 4 ? 'ok' : f >= at(2) ? 'hot' : 'idle';
    if (f >= at(4) + (i % 20) * 3 && random('late' + i) < 0.55) return 'ok';
    return f >= at(0) + (i - 13) ? 'no' : 'idle';
  };
  const col = {ok: C.green, hot: C.amber, no: C.red, idle: 'rgba(255,255,255,0.18)'} as Record<string, string>;
  return <AbsoluteFill>
    <div style={{position: 'absolute', top: 70, width: '100%', textAlign: 'center'}}><T s={sp(0)} size={62}><span style={{color: C.red}}>47 / 60</span> jugées « impossibles »</T></div>
    <div style={{position: 'absolute', left: 360, top: 230, display: 'grid', gridTemplateColumns: 'repeat(15, 64px)', gap: 14}}>
      {Array.from({length: 60}).map((_, i) => { const s = st(i); const pulse = s === 'hot' ? 0.5 + 0.5 * Math.sin(f / 4 + i) : 0;
        return <div key={i} style={{width: 64, height: 64, borderRadius: 12, background: `${col[s]}${s === 'idle' ? '' : '33'}`, border: `2px solid ${col[s]}`, boxShadow: s === 'hot' ? `0 0 ${20 + 20 * pulse}px ${C.amber}` : s === 'ok' ? `0 0 18px ${C.green}66` : 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'SG', fontWeight: 700, fontSize: 30, color: col[s]}}>{s === 'ok' ? '✓' : s === 'no' ? '✕' : ''}</div>; })}
    </div>
    <div style={{position: 'absolute', bottom: 90, width: '100%', display: 'flex', justifyContent: 'center', gap: 50}}>
      {[['3 déjà prouvées', C.green, sp(1)], ['tout le monde sur les 10 autres', C.amber, sp(2)], ['70 min → 10 / 10 ✓', C.green, sp(3)], ['puis des « impossibles » tombent', C.cyan, sp(4)]].map(([t, c, s], i) =>
        <div key={i} style={{fontFamily: 'SG', fontWeight: 700, fontSize: 32, color: c as string, opacity: s as number, transform: `translateY(${(1 - (s as number)) * 20}px)`}}>{t}</div>)}
    </div>
  </AbsoluteFill>;
};

const S07: React.FC = () => {
  const {f, sp, at, D} = useS();
  const prog = interpolate(f, [at(2) - 40, at(2)], [0.45, 0.6], cl);
  const stopped = f >= at(2) && f < at(3) + 10;
  const tree = interpolate(f, [at(5), D - 10], [0, 1], {...cl, easing: Easing.out(Easing.cubic)});
  const nodes: React.ReactNode[] = [];
  if (f >= at(5)) {
    let id = 0;
    for (let lv = 0; lv < 10; lv++) {
      const n = Math.min(2 ** lv, 160); const y = 470 + lv * 52; const vis = interpolate(tree, [lv / 10, (lv + 1) / 10], [0, 1], cl);
      for (let k = 0; k < n; k++) { id++; const x = 960 + (k - (n - 1) / 2) * Math.min(150, 1500 / n);
        nodes.push(<circle key={id} cx={x} cy={y} r={lv < 3 ? 10 : 5} fill={lv < 2 ? C.violet : C.cyan} opacity={vis * (0.5 + 0.5 * random('t' + id))} />); }
    }
  }
  return <AbsoluteFill>
    <div style={{position: 'absolute', top: 60, width: '100%', textAlign: 'center'}}><T s={sp(0)} size={70}>Le mur : <span style={{color: C.amber}}>Langlands–Tunnell</span></T></div>
    {f < at(5) && <>
      <Panel s={sp(1)} x={460} y={200} w={1000} h={170} col={C.amber}>
        <Label col={C.amber}>estimation du capitaine</Label>
        <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 60, color: C.white, whiteSpace: 'nowrap'}}>≈ 1 000 000 lignes · <span style={{color: C.red}}>&lt; 1 %</span></div>
      </Panel>
      <div style={{position: 'absolute', left: 260, top: 470, width: 1400, opacity: sp(2)}}>
        <div style={{display: 'flex', justifyContent: 'space-between', fontFamily: 'JB', fontSize: 24, color: C.grey}}><span>0 h</span><span>30 h</span></div>
        <div style={{height: 18, borderRadius: 9, background: 'rgba(255,255,255,0.1)', marginTop: 10, overflow: 'hidden'}}>
          <div style={{width: `${prog * 100}%`, height: '100%', background: stopped ? C.red : `linear-gradient(90deg, ${C.cyan}, ${C.violet})`}} /></div>
        <div style={{position: 'absolute', left: 1400 * 0.6 - 90, top: 70, fontFamily: 'SG', fontWeight: 700, fontSize: 40, color: f >= at(3) ? C.green : C.red}}>{f >= at(3) ? '↻ relancé' : '■ heure 18 : arrêt'}</div>
      </div>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {f >= at(4) && Array.from({length: 300}).map((_, i) => { const p = interpolate(f, [at(4) + random('w' + i) * 30, at(4) + 30 + random('w' + i) * 30], [0, 1], {...cl, easing: ease});
          const x0 = 200 + random('x' + i) * 1520, y0 = 1000 + random('y' + i) * 60; const x1 = 760 + random('a' + i) * 400, y1 = 260 + random('b' + i) * 90;
          return <circle key={i} cx={x0 + (x1 - x0) * p} cy={y0 + (y1 - y0) * p} r={4} fill={C.cyan} opacity={0.8 * (1 - p * 0.6)} />; })}
      </svg>
      <div style={{position: 'absolute', bottom: 90, width: '100%', textAlign: 'center'}}><T s={sp(4)} size={50} color={C.cyan}>≈ 750 aides envoyés sur le mur</T></div>
    </>}
    {f >= at(5) && <>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>{nodes}</svg>
      <div style={{position: 'absolute', left: 140, top: 230}}><T s={sp(5)} size={130} color={C.cyan}><Count to={2418} p={tree} /></T><T s={sp(5, 6)} size={36} color={C.grey}>tâches · 10 niveaux</T></div>
    </>}
  </AbsoluteFill>;
};

const S08: React.FC = () => {
  const {f, sp, at} = useS();
  const p = interpolate(f, [0, at(1) + 20], [0, 1], {...cl, easing: ease});
  const W = 1400, X = 260;
  return <AbsoluteFill>
    <div style={{position: 'absolute', left: X, top: 200, width: W}}>
      <div style={{height: 14, borderRadius: 7, background: 'rgba(255,255,255,0.1)'}}><div style={{width: `${p * 28.7 / 30 * 100}%`, height: '100%', borderRadius: 7, background: `linear-gradient(90deg, ${C.cyan}, ${C.violet})`}} /></div>
      <div style={{display: 'flex', justifyContent: 'space-between', fontFamily: 'JB', fontSize: 24, color: C.grey, marginTop: 10}}><span>0 h</span><span>18 h</span><span>30 h</span></div>
      {[[28.4, 'Langlands–Tunnell ✓', 0, -150], [28.7, 'FERMAT ✓', 1, 40]].map(([h, t, k, dy]) => { const s = sp(k as number);
        return <div key={t as string} style={{position: 'absolute', left: W * (h as number) / 30, top: dy as number, transform: `translateX(-100%) scale(${0.8 + 0.2 * s})`, transformOrigin: 'right', opacity: s, textAlign: 'right', whiteSpace: 'nowrap'}}>
          <div style={{fontFamily: 'JB', fontSize: 28, color: C.grey}}>heure {String(h).replace('.', ',')}</div>
          <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: k ? 84 : 48, color: C.green, textShadow: k ? '0 0 50px rgba(40,220,140,0.6)' : 'none'}}>{t}</div></div>; })}
    </div>
    <div style={{position: 'absolute', left: X, top: 560, width: W, opacity: sp(2)}}>
      {[['septembre', 264, '11 jours', 1, C.violet], ['novembre', 28.7, '< 30 h', 1 / 7, C.cyan]].map(([m, h, lab, len, c], i) => { const g = interpolate(f, [at(2) + i * 10, at(2) + 40 + i * 10], [0, 1], {...cl, easing: ease});
        return <div key={i} style={{display: 'flex', alignItems: 'center', gap: 24, marginBottom: 34}}>
          <div style={{width: 200, fontFamily: 'JB', fontSize: 30, color: C.grey}}>{m}</div>
          <div style={{flex: 1}}>
            <div style={{height: 40, width: `${(h as number) / 264 * 100 * g}%`, minWidth: 8, borderRadius: 10, background: c as string, display: 'flex', alignItems: 'center'}} />
            <div style={{height: 12, marginTop: 8, width: `${(len as number) * 100 * g}%`, borderRadius: 6, background: `${c}66`}} />
          </div>
          <div style={{width: 200, fontFamily: 'SG', fontWeight: 700, fontSize: 44, color: c as string}}>{lab}</div></div>; })}
      <div style={{fontFamily: 'JB', fontSize: 24, color: C.grey}}>barre épaisse : durée · barre fine : longueur de la preuve (≈ 1/7)</div>
    </div>
  </AbsoluteFill>;
};

const CMDS = ['lake build Fermat.Modularity', 'git push origin helper-417', 'psql -c "UPDATE subtasks …"', 'lean --run step_042.lean', 'git push origin helper-088', 'psql -c "INSERT INTO notes …"'];
const S09: React.FC = () => {
  const {f, sp, at, lin} = useS();
  const c = lin(at(3), at(3) + 45);
  return <AbsoluteFill>
    <div style={{position: 'absolute', top: 70, width: '100%', textAlign: 'center'}}><T s={sp(0)} size={66}>Et la sécurité ?</T></div>
    <div style={{position: 'absolute', left: 170, top: 210, display: 'grid', gridTemplateColumns: 'repeat(10, 64px)', gap: 12, opacity: sp(1)}}>
      {Array.from({length: 60}).map((_, i) => <div key={i} style={{width: 64, height: 64, borderRadius: 10, border: `2px solid ${C.cyan}66`, background: 'rgba(0,212,255,0.05)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <div style={{width: 14, height: 14, borderRadius: 7, background: C.cyan, opacity: 0.5 + 0.5 * Math.sin(f / 9 + i)}} /></div>)}
      <div style={{gridColumn: '1 / span 10', fontFamily: 'JB', fontSize: 26, color: C.grey, marginTop: 10}}>1 agent = 1 machine isolée · <span style={{color: C.red}}>✕ internet</span></div>
    </div>
    <Panel s={sp(2)} x={1000} y={210} w={760} h={420} col={C.green}>
      <Label col={C.green}>surveillant automatique</Label>
      {CMDS.map((cmd, i) => { const y = ((f * 1.6 + i * 60) % 360); return <div key={i} style={{position: 'absolute', left: 30, top: 80 + y, fontFamily: 'JB', fontSize: 24, color: C.white, opacity: 0.85}}><span style={{color: C.green}}>✓ </span>{cmd}</div>; })}
      <div style={{position: 'absolute', left: 0, right: 0, top: 80 + ((f * 3) % 330), height: 3, background: `linear-gradient(90deg, transparent, ${C.green}, transparent)`}} />
    </Panel>
    <div style={{position: 'absolute', left: 1000, top: 680, opacity: sp(3)}}>
      <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 92, color: C.white}}>+<Count to={1000000} p={c} /></div>
      <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 46, color: C.green}}>actions vérifiées · 0 bloquée</div>
    </div>
  </AbsoluteFill>;
};

const S10: React.FC = () => {
  const {sp} = useS();
  return <AbsoluteFill style={{alignItems: 'center'}}>
    <div style={{position: 'absolute', top: 90, width: '100%', textAlign: 'center'}}><T s={sp(0)} size={80} color={C.amber}>⚠ Attention</T></div>
    <div style={{position: 'absolute', top: 290, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 50}}>
      <Panel s={sp(1)} x={0} y={0} w={680} h={330} col={C.red} style={{position: 'relative'}}>
        <Label col={C.red}>trouver la preuve</Label>
        <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 64, color: C.white}}>✕ pas l'IA</div>
        <div style={{fontFamily: 'SG', fontSize: 38, color: C.grey, marginTop: 14}}>Andrew Wiles, 1995</div>
      </Panel>
      <Panel s={sp(2)} x={0} y={0} w={680} h={330} col={C.green} style={{position: 'relative'}}>
        <Label col={C.green}>la réécrire pour l'ordinateur</Label>
        <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 64, color: C.white}}>✓ l'IA</div>
        <div style={{fontFamily: 'SG', fontSize: 38, color: C.grey, marginTop: 14}}>vérifiée étape par étape</div>
      </Panel>
    </div>
    <div style={{position: 'absolute', top: 720, width: '100%', textAlign: 'center'}}><T s={sp(3)} size={52} color={C.grey}>Anthropic : « <span style={{color: C.white}}>une expérience jouet</span> »</T></div>
  </AbsoluteFill>;
};

const S11: React.FC = () => {
  const {f, sp, at} = useS();
  const split = interpolate(f, [at(2), at(2) + 40], [0, 1], {...cl, easing: ease});
  const split2 = interpolate(f, [at(3) + 50, at(3) + 90], [0, 1], {...cl, easing: ease});
  const Box: React.FC<{x: number; y: number; w: number; t: string; c: string; o: number}> = ({x, y, w, t, c, o}) =>
    <div style={{position: 'absolute', left: x, top: y, width: w, height: 70, boxSizing: 'border-box', borderRadius: 14, border: `2px solid ${c}`, background: `${c}1a`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'SG', fontWeight: 700, fontSize: 28, color: c, opacity: o, transform: `scale(${0.8 + 0.2 * o})`}}>{t}</div>;
  return <AbsoluteFill>
    <div style={{position: 'absolute', top: 60, width: '100%', textAlign: 'center'}}><T s={sp(0)} size={60}>Même 1 000 IA <span style={{color: C.amber}}>abandonnent trop tôt</span></T></div>
    <div style={{position: 'absolute', top: 150, width: '100%', textAlign: 'center'}}><T s={sp(1)} size={40} color={C.grey}>la solution marche aussi avec une seule</T></div>
    <Box x={710} y={250} w={500} t="ta grosse tâche" c={C.violet} o={sp(2)} />
    {[0, 1, 2].map((i) => <Box key={i} x={300 + i * 460} y={380} w={400} t={['étape 1', 'étape 2', 'étape 3'][i]} c={C.cyan} o={split} />)}
    {[0, 1, 2].map((i) => <Box key={'b' + i} x={760 + i * 140 - 60} y={510} w={120} t={`3.${i + 1}`} c={C.green} o={split2} />)}
    <Panel s={sp(3)} x={260} y={640} w={1400} h={190} col={C.amber}>
      <div style={{fontFamily: 'SG', fontSize: 36, color: C.grey}}>L'IA : <span style={{color: C.red}}>« C'est impossible. »</span></div>
      <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 40, color: C.white, marginTop: 18}}>Toi : « Découpe en 3 sous-tâches plus petites et continue. »</div>
    </Panel>
    <div style={{position: 'absolute', bottom: 70, width: '100%', textAlign: 'center'}}><T s={sp(4)} size={38} color={C.cyan}>Sources ↓ dans la description</T></div>
  </AbsoluteFill>;
};

const End: React.FC = () => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 16}}); const b = spring({frame: f - 14, fps, config: {damping: 14}});
  return <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
    <Img src={staticFile('avatar_briefai.png')} style={{width: 200, height: 200, opacity: s, transform: `scale(${0.8 + 0.2 * s})`}} />
    <div style={{fontFamily: 'SG', fontWeight: 700, fontSize: 96, color: C.white, marginTop: 20, opacity: s}}>Brief<span style={{color: C.cyan}}>AI</span></div>
    <div style={{marginTop: 30, fontFamily: 'SG', fontWeight: 700, fontSize: 40, color: '#07080d', background: C.cyan, padding: '18px 44px', borderRadius: 16, opacity: b, transform: `scale(${0.9 + 0.1 * b})`, boxShadow: '0 16px 50px rgba(0,212,255,0.4)'}}>S'abonner</div>
  </AbsoluteFill>;
};

const SCENES: Record<string, React.FC> = {seg01: S01, seg02: S02, seg03: S03, seg04: S04, seg05: S05, seg06: S06, seg07: S07, seg08: S08, seg09: S09, seg10: S10, seg11: S11};

const Fade: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 8, dur - 8, dur], [0, 1, 1, 0], cl);
  return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};

const Chip: React.FC<{t: string}> = ({t}) => {
  const f = useCurrentFrame(); const s = spring({frame: f, fps: 30, config: {damping: 18}});
  return <div style={{position: 'absolute', right: 50, bottom: 40, fontFamily: 'JB', fontSize: 20, color: C.grey, opacity: 0.8 * s}}>source : Anthropic · {t}</div>;
};

export const Story: React.FC = () => {
  const segs = (TL as any).segs as Seg[];
  return <AbsoluteFill style={{overflow: 'hidden'}}>
    <style>{fonts}</style>
    <Bg />
    {segs.map((s) => { const Sc = SCENES[s.id]; return <Sequence key={s.id} from={s.from} durationInFrames={s.dur}>
      <Ctx.Provider value={s}><Fade dur={s.dur}><Sc />{['seg03'].includes(s.id) && <Chip t="anthropic.com · 4 sept. 2026" />}{['seg04', 'seg05', 'seg06', 'seg07', 'seg08', 'seg09', 'seg10'].includes(s.id) && <Chip t="claude.dev · 9 nov. 2026" />}</Fade></Ctx.Provider>
    </Sequence>; })}
    <Sequence from={(TL as any).endFrom} durationInFrames={(TL as any).total - (TL as any).endFrom}><End /></Sequence>
  </AbsoluteFill>;
};
