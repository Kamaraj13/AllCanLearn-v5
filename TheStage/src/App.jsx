import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import CreatePage from './components/CreatePage';
import './styles/globals.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-[#121212]">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/create" element={<CreatePage showPage={true} />} />
          <Route path="/explore" element={<div className="text-white p-8">Explore Page - Coming Soon</div>} />
          <Route path="/library" element={<div className="text-white p-8">Library Page - Coming Soon</div>} />
          <Route path="/episode/:id" element={<div className="text-white p-8">Episode Detail - Coming Soon</div>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
