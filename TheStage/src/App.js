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
    <div className={`app ${isBrightMode ? 'bright-mode' : ''}`}>
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

      {/* Sidebar */}
      <Sidebar 
        currentPage={currentPage}
        showPage={showPage}
        isBrightMode={isBrightMode}
        soundEnabled={soundEnabled}
        toggleTheme={toggleTheme}
        toggleSound={toggleSound}
      />

      {/* Main Content */}
      <div className="content">
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
      </div>

      {/* Chat Panel */}
      <ChatPanel soundEnabled={soundEnabled} />
    </div>
  );
}

export default App;
