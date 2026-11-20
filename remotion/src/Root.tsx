import React from 'react';
import {Composition} from 'remotion';
import {Test} from './Test';
import {Tuto} from './Tuto';
import TL from './timeline.json';
export const Root: React.FC = () => (<>
  <Composition id="Test" component={Test} durationInFrames={450} fps={30} width={1920} height={1080} />
  <Composition id="Tuto" component={Tuto} durationInFrames={(TL as any).total} fps={30} width={1920} height={1080} />
</>);
