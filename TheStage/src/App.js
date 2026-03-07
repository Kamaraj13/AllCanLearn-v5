import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import HomePage from './components/HomePage';
import CreatePage from './components/CreatePage';
import DetailPage from './components/DetailPage';
import ChatPanel from './components/ChatPanel';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [currentEpisode, setCurrentEpisode] = useState(null);
  const [isBrightMode, setIsBrightMode] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(true);

  useEffect(() => {
    // Load saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'bright') {
      setIsBrightMode(true);
      document.body.classList.add('bright-mode');
    }

    // Load sound preference
    const soundPref = localStorage.getItem('soundEnabled');
    if (soundPref === 'false') {
      setSoundEnabled(false);
    }
  }, []);

  const toggleTheme = () => {
    setIsBrightMode(!isBrightMode);
    if (!isBrightMode) {
      document.body.classList.add('bright-mode');
      localStorage.setItem('theme', 'bright');
    } else {
      document.body.classList.remove('bright-mode');
      localStorage.setItem('theme', 'dark');
    }
  };

  const toggleSound = () => {
    setSoundEnabled(!soundEnabled);
    localStorage.setItem('soundEnabled', !soundEnabled);
  };

  const showPage = (page) => {
    setCurrentPage(page);
  };

  const viewEpisode = (episode) => {
    setCurrentEpisode(episode);
    setCurrentPage('detail');
  };

  return (
    <div className={`netflix-container ${isBrightMode ? 'bright-mode' : ''}`}>
      {/* Animated Background */}
      <div className="slideshow-background">
        {[...Array(44)].map((_, i) => (
          <img 
            key={i} 
            src={`/static/assets/bg-frame-${(i % 4) + 1}.jpg`} 
            alt="Background"
            onError={(e) => {
              // Fallback for missing images
              e.target.style.display = 'none';
            }}
          />
        ))}
      </div>

      {/* Main Content */}
      {currentPage === 'home' && (
        <HomePage viewEpisode={viewEpisode} />
      )}
      {currentPage === 'create' && (
        <CreatePage 
          showPage={showPage}
          viewEpisode={viewEpisode}
        />
      )}
      {currentPage === 'detail' && (
        <DetailPage 
          episode={currentEpisode}
          showPage={showPage}
        />
      )}

      {/* Chat Panel - Floating */}
      <ChatPanel soundEnabled={soundEnabled} />

      {/* Theme Toggle - Fixed Position */}
      <div 
        className="theme-toggle" 
        onClick={toggleTheme}
        style={{
          position: 'fixed',
          bottom: '20px',
          left: '20px',
          background: 'rgba(26, 31, 58, 0.7)',
          backdropFilter: 'blur(20px)',
          border: '2px solid rgba(255, 255, 255, 0.15)',
          borderRadius: '12px',
          padding: '14px',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          fontWeight: '600',
          transition: 'all 0.3s',
          zIndex: 1000
        }}
      >
        <span>Theme</span>
        <span className="theme-icon">{isBrightMode ? '☀️' : '🌙'}</span>
      </div>
    </div>
  );
}

export default App;
