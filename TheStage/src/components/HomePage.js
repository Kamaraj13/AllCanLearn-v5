import React, { useState, useEffect } from 'react';
import axios from 'axios';

function HomePage({ viewEpisode }) {
  const [episodes, setEpisodes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadEpisodes();
    // Set up auto-refresh every 30 seconds to check for expired episodes
    const interval = setInterval(loadEpisodes, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadEpisodes = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/episodes');
      let episodesData = response.data.episodes || [];
      
      // Filter out episodes older than 3 days
      const threeDaysAgo = Date.now() - (3 * 24 * 60 * 60 * 1000);
      episodesData = episodesData.filter(ep => {
        const episodeTime = parseInt(ep.id);
        return episodeTime > threeDaysAgo;
      });
      
      // Sort by newest first
      episodesData.sort((a, b) => parseInt(b.id) - parseInt(a.id));
      
      setEpisodes(episodesData);
    } catch (error) {
      console.error('Error loading episodes:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTimeRemaining = (episode) => {
    // Don't show expiry for Essential Topics or if it's not a custom podcast
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

  if (loading) {
    return (
      <div className="page active">
        <div className="header">
          <h1>Your Podcasts</h1>
          <p>Your custom AI-generated podcasts (saved for 3 days)</p>
        </div>
        <div className="loading">Loading your podcasts...</div>
      </div>
    );
  }

  return (
    <div className="page active">
      <div className="header">
        <h1>Your Podcasts</h1>
        <p>Your AI-generated podcasts • Essential Topics are permanent • Custom topics auto-refresh</p>
      </div>
      
      {episodes.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '60px 20px' }}>
          <div style={{ fontSize: '4em', marginBottom: '20px' }}>🎙️</div>
          <h2 style={{ marginBottom: '16px', color: '#0ea5e9' }}>No Podcasts Yet</h2>
          <p style={{ marginBottom: '30px', opacity: '0.8' }}>
            Create your first custom podcast on any topic you want to learn about!
          </p>
          <button 
            className="btn"
            onClick={() => window.location.hash = '#create'}
          >
            ➕ Create Your First Podcast
          </button>
        </div>
      ) : (
        <div>
          <div style={{ marginBottom: '20px', padding: '15px', background: 'rgba(14, 165, 233, 0.1)', borderRadius: '12px', border: '1px solid rgba(14, 165, 233, 0.3)' }}>
            <p style={{ margin: 0, fontSize: '0.9em' }}>
              📅 <strong>Storage Info:</strong> Essential Topics are permanent • Custom podcasts refresh every 3 days • Audio files auto-cleanup every 3 hours
            </p>
          </div>
          
          <div className="episodes-grid">
            {episodes.map(ep => (
              <div 
                key={ep.id} 
                className="card episode-card" 
                onClick={() => viewEpisode(ep)}
              >
                <div className="episode-icon">🎙️</div>
                <div className="episode-title">{ep.topic}</div>
                <div className="episode-meta">
                  <span>🕒 {new Date(ep.timestamp || ep.created_at).toLocaleDateString()}</span>
                  <span>💬 {ep.turns?.length || ep.turns_count || 0} turns</span>
                  <span style={{ 
                    color: getTimeRemaining(ep) === '🔄 Refresh Needed' ? '#ef4444' : '#10b981',
                    fontWeight: '600'
                  }}>
                    ⏰ {getTimeRemaining(ep)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default HomePage;
