import React from 'react';
import { RecoilRoot } from 'recoil';

import './App.css';

import { MainPane } from './Main';

function App() {
  return (
    <RecoilRoot>
    <div className="App">
      <MainPane />
    </div>
    </RecoilRoot>
  );
}

export default App;
