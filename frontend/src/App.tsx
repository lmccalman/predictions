import React from 'react';
import { RecoilRoot } from 'recoil';

import { Button, Navbar } from 'react-bulma-components';

function App() {
  return (
    <RecoilRoot>
    <div className="App">
      <Navbar color='primary'>
        <Navbar.Brand>
          Predictions 2022
        </Navbar.Brand>
      </Navbar>
      <h1> Predictions 2022 </h1>
      <h2> Website by lachy and Jac </h2>
    </div>
    </RecoilRoot>
  );
}

export default App;
