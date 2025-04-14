import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/Home/Home';
import Emotion from './pages/Emotion/Emotion';
import Music from './pages/Music/Music';
import Recent from './pages/Recent/Recent';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/emotion" element={<Emotion />} />
        <Route path="/music" element={<Music />} />
        <Route path="/recent" element={<Recent />} />
      </Routes>
    </Router>
  );
}

export default App
