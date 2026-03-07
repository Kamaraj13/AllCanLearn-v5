import React, { useState, useEffect } from 'react';
import axios from 'axios';

function HomePage({ viewEpisode }) {
  const [episodes, setEpisodes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadEpisodes();
    const interval = setInterval(loadEpisodes, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadEpisodes = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/episodes');
      let episodesData = response.data.episodes || [];
      
      const threeDaysAgo = Date.now() - (3 * 24 * 60 * 60 * 1000);
      episodesData = episodesData.filter(ep => {
        const episodeTime = parseInt(ep.id);
        return episodeTime > threeDaysAgo;
      });
      
      episodesData.sort((a, b) => parseInt(b.id) - parseInt(a.id));
      setEpisodes(episodesData);
    } catch (error) {
      console.error('Error loading episodes:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTimeRemaining = (episode) => {
    if (episode.is_essential || episode.topic?.includes('Essential') || !episode.id) {
      return '📚 Permanent';
    }
    
    const episodeTime = parseInt(episode.id);
    const threeDaysAgo = Date.now() - (3 * 24 * 60 * 60 * 1000);
    const expiryTime = episodeTime + (3 * 24 * 60 * 60 * 1000);
    const timeRemaining = expiryTime - Date.now();
    
    if (timeRemaining <= 0) return '🔄 Refresh Needed';
    
    const hours = Math.floor(timeRemaining / (1000 * 60 * 60));
    const days = Math.floor(hours / 24);
    const remainingHours = hours % 24;
    
    if (days > 0) {
      return `${days}d ${remainingHours}h left`;
    } else {
      return `${hours}h left`;
    }
  };

  const filteredEpisodes = episodes.filter(ep => 
    ep.topic.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="netflix-container">
        <div className="loading-screen">
          <div className="spinner"></div>
          <h2>Loading Your Library...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="netflix-container">
      {/* Header */}
      <div className="netflix-header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo">🎙️ AllCanLearn</div>
            <div className="tagline">AI-Powered Learning</div>
          </div>
          <div className="header-actions">
            <button 
              className="create-btn"
              onClick={() => window.location.hash = '#create'}
            >
              <span>➕</span> Create Podcast
            </button>
            <button 
              className="create-btn"
              onClick={() => window.location.href = '/quiz'}
              style={{ marginLeft: '10px', background: 'linear-gradient(45deg, #34d399, #fbbf24)' }}
            >
              <span>🎮</span> Take Quiz
            </button>
          </div>
        </div>
      </div>

      {/* Quick Topics Section */}
      <div className="search-section">
        <div className="section-header">
          <h2>🚀 Quick Start Topics</h2>
          <p>Popular learning topics</p>
        </div>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '30px' }}>
          {[
            '🌍 Climate Change',
            '🤖 Artificial Intelligence', 
            '💰 Global Economy',
            '🧠 Mental Health',
            '🚀 Space Exploration',
            '⚡ Renewable Energy',
            '📱 Social Media',
            '🏥 Global Health'
          ].map((topic, index) => (
            <button
              key={index}
              className="create-btn"
              onClick={() => {
                window.location.hash = '#create';
                sessionStorage.setItem('essentialTopic', topic.replace(/[🌍🤖💰🧠🚀⚡📱🏥]\s*/g, ''));
              }}
              style={{ 
                fontSize: '0.9em', 
                padding: '8px 16px',
                background: 'linear-gradient(45deg, #38bdf8, #34d399)'
              }}
            >
              {topic}
            </button>
          ))}
        </div>
      </div>

      {/* Search Bar */}
      <div className="search-section">
        <div className="search-container">
          <input
            type="text"
            className="search-input"
            placeholder="🔍 Search your podcasts..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* Content */}
      {filteredEpisodes.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🎙️</div>
          <h2>No Podcasts Found</h2>
          <p>
            {searchTerm 
              ? `No results for "${searchTerm}"` 
              : "Create your first podcast on any topic you want to learn about!"
            }
          </p>
          {!searchTerm && (
            <button 
              className="cta-button"
              onClick={() => window.location.hash = '#create'}
            >
              <span>🚀</span> Create Your First Podcast
            </button>
          )}
        </div>
      ) : (
        <div className="content-section">
          <div className="section-header">
            <h2>Your Podcast Library</h2>
            <p>{filteredEpisodes.length} episodes</p>
          </div>
          
          <div className="episodes-grid">
            {filteredEpisodes.map(ep => (
              <div 
                key={ep.id} 
                className="episode-card spotify-card"
                onClick={() => viewEpisode(ep)}
              >
                {/* Card Background */}
                <div className="card-background">
                  <div className="gradient-overlay"></div>
                  <div className="play-button-overlay">
                    <div className="play-button">▶</div>
                  </div>
                </div>
                
                {/* Card Content */}
                <div className="card-content">
                  <div className="episode-header">
                    <div className="episode-type">
                      {ep.is_essential ? '📚 Essential' : '🎙️ Custom'}
                    </div>
                    <div className={`episode-status ${getTimeRemaining(ep) === '🔄 Refresh Needed' ? 'expired' : 'active'}`}>
                      {getTimeRemaining(ep)}
                    </div>
                  </div>
                  
                  <h3 className="episode-title">{ep.topic}</h3>
                  
                  <div className="episode-meta">
                    <div className="meta-item">
                      <span className="meta-icon">📅</span>
                      <span>{new Date(ep.timestamp || ep.created_at).toLocaleDateString()}</span>
                    </div>
                    <div className="meta-item">
                      <span className="meta-icon">💬</span>
                      <span>{ep.turns?.length || ep.turns_count || 0} turns</span>
                    </div>
                    {ep.audio_files && ep.audio_files.length > 0 && (
                      <div className="meta-item">
                        <span className="meta-icon">🎵</span>
                        <span>{ep.audio_files.length} audio files</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Info Banner */}
      <div className="info-banner">
        <div className="banner-content">
          <div className="banner-icon">ℹ️</div>
          <div className="banner-text">
            <strong>Storage Info:</strong> Essential Topics are permanent • Custom podcasts refresh every 3 days • Audio files auto-cleanup every 3 hours
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
