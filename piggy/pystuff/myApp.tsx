import React from 'react';
import { BrowserRouter as Router, Routes, Route, HashRouter } from 'react-router-dom';

function ComponentA() {
  return (
    <div>
      <h2>Component A</h2>
      <p>Content for component A.</p>
    </div>
  );
}

function ComponentB() {
  return (
    <div>
      <h2>Component B</h2>
      <p>Content for component B.</p>
    </div>
  );
}


const App = () => {
  return (
    <HashRouter>
      <Routes>
        <Route path="/a" element={<ComponentA />} />
        <Route path="/b" element={<ComponentB />} />
      </Routes>
    </HashRouter>
  );
};
