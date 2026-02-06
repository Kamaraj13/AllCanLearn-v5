import React from 'react';

function Sidebar({ currentPage, showPage, isBrightMode, soundEnabled, toggleTheme, toggleSound }) {
  return (
    <div className="sidebar">
      <div className="logo" onClick={() => showPage('home')}>
        <img src="/static/assets/logo.jpg" alt="AI Roundtable" />
        <span>AI Podcasts</span>
      </div>
      
      <div className="nav-section">
        <div className="nav-title">Navigation</div>
        <button 
          className={`nav-btn ${currentPage === 'home' ? 'active' : ''}`}
          onClick={() => showPage('home')}
        >
          🎙️ My Podcasts
        </button>
        <button 
          className={`nav-btn ${currentPage === 'create' ? 'active' : ''}`}
          onClick={() => showPage('create')}
        >
          ➕ Create Podcast
        </button>
        <button 
          className="nav-btn" 
          onClick={() => window.location.href = '/quiz'}
          style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', fontWeight: 'bold' }}
        >
          🎮 Take Quiz
        </button>
      </div>
      
      <div className="nav-section">
        <div className="nav-title">Essential Topics</div>
        <button className="nav-btn" onClick={() => quickCreateTopic('Climate Change and Environmental Sustainability')}>
          🌍 Climate Change & Environment
        </button>
        <button className="nav-btn" onClick={() => quickCreateTopic('Artificial Intelligence and the Future of Technology')}>
          🤖 Artificial Intelligence & Tech
        </button>
        <button className="nav-btn" onClick={() => quickCreateTopic('Global Economy and Financial Markets')}>
          💰 Global Economy & Finance
        </button>
        <button className="nav-btn" onClick={() => quickCreateTopic('Mental Health and Wellness in Modern Society')}>
          🧠 Mental Health & Wellness
        </button>
        <button className="nav-btn" onClick={() => quickCreateTopic('Space Exploration and Scientific Discoveries')}>
          🚀 Space Exploration & Science
        </button>
        <button className="nav-btn" onClick={() => quickCreateTopic('Renewable Energy and Sustainable Living')}>
          ⚡ Renewable Energy & Sustainability
        </button>
        <button className="nav-btn" onClick={() => quickCreateTopic('Social Media Impact on Society and Communication')}>
          📱 Social Media & Society
        </button>
        <button className="nav-btn" onClick={() => quickCreateTopic('Global Health and Pandemic Preparedness')}>
          🏥 Global Health & Medicine
        </button>
        <button className="nav-btn" onClick={() => quickCreateTopic('Education Systems and Learning in the Digital Age')}>
          🎓 Education & Digital Learning
        </button>
        <button className="nav-btn" onClick={() => quickCreateTopic('Human Rights and Social Justice Worldwide')}>
          ⚖️ Human Rights & Social Justice
        </button>
      </div>

      <div 
        className={`sound-toggle ${!soundEnabled ? 'disabled' : ''}`}
        onClick={toggleSound}
      >
        <span>Sounds</span>
        <span className="sound-icon">{soundEnabled ? '🔊' : '🔇'}</span>
      </div>

      <div className="theme-toggle" onClick={toggleTheme}>
        <span>Theme</span>
        <span className="theme-icon">{isBrightMode ? '☀️' : '🌙'}</span>
      </div>
    </div>
  );
}

function quickCreateTopic(topic) {
  // This will set the topic in the CreatePage for essential topics
  window.location.hash = '#create';
  // Store the topic in sessionStorage for the CreatePage to pick up
  sessionStorage.setItem('essentialTopic', topic);
}

export default Sidebar;
