import React from 'react';
import { RecoilRoot } from 'recoil';
import { Button } from 'react-bootstrap';

import './App.css';

function App() {
  return (
    <RecoilRoot>
    <div className="App">
      <h1 className="text-3xl font-bold underline"> Predictions 2022 </h1>
      <h2> Website by lachy and Jac </h2>
      <Button />
    </div>
    </RecoilRoot>
  );
}

export default App;
