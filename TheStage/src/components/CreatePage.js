import React, { useState, useEffect } from 'react';
import axios from 'axios';

function CreatePage({ showPage, viewEpisode }) {
  const [customTopic, setCustomTopic] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generateText, setGenerateText] = useState('🎬 Generate Podcast');
  const [isEssentialTopic, setIsEssentialTopic] = useState(false);

  useEffect(() => {
    // Check for essential topic from sidebar (priority)
    const essentialTopic = sessionStorage.getItem('essentialTopic');
    if (essentialTopic) {
      setCustomTopic(essentialTopic);
      setIsEssentialTopic(true);
      sessionStorage.removeItem('essentialTopic'); // Clear it after using
      return;
    }
    
    // Check for custom topic from URL hash
    const hash = window.location.hash.slice(1);
    if (hash === 'create') {
      const urlParams = new URLSearchParams(window.location.search);
      const topic = urlParams.get('topic');
      if (topic) {
        setCustomTopic(topic);
      }
    }
  }, []);

  const generateNewPodcast = async () => {
    const topic = customTopic.trim();
    
    if (!topic) {
      alert('Please enter a topic for your podcast');
      return;
    }
    
    setIsGenerating(true);
    setGenerateText('⏳ Generating Podcast...');
    
    try {
      // Pass essential flag for Essential Topics
      const response = await axios.post(`/generate?tts=true&topic=${encodeURIComponent(topic)}&essential=${isEssentialTopic}`);
      const episode = response.data;
      
      // Store full episode data in localStorage
      const episodeId = episode.id || Date.now().toString();
      episode.id = episodeId;
      episode.topic = topic; // Ensure the custom topic is saved
      const storedEpisodes = JSON.parse(localStorage.getItem("fullEpisodes") || "{}");
      storedEpisodes[episodeId] = episode;
      localStorage.setItem("fullEpisodes", JSON.stringify(storedEpisodes));
      
      setGenerateText('✅ Podcast Generated!');
      setTimeout(() => {
        // Show the generated episode immediately
        viewEpisode(episode);
        setIsGenerating(false);
        setGenerateText('🎬 Generate Podcast');
        setCustomTopic(''); // Clear the input
        setIsEssentialTopic(false); // Reset essential flag
      }, 1500);
    } catch (error) {
      console.error('Error generating podcast:', error);
      setGenerateText('❌ Error - Try Again');
      setIsGenerating(false);
    }
  };

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
              onClick={() => window.location.hash = '#home'}
            >
              <span>←</span> Back to Library
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="search-section">
        <div className="section-header">
          <h2>🎙️ Create Custom Podcast</h2>
          <p>Generate a podcast on any topic you want to learn about</p>
        </div>
        
        <div style={{ maxWidth: '600px', margin: '0 auto' }}>
          <div style={{ marginTop: '30px' }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '15px', 
              fontWeight: '600', 
              fontSize: '1.2em',
              color: 'inherit'
            }}>
              🎙️ What topic would you like to hear about?
            </label>
            <input 
              type="text"
              value={customTopic}
              onChange={(e) => setCustomTopic(e.target.value)}
              placeholder="e.g., 'The future of renewable energy', 'Ancient Roman history', 'How to invest in stocks'"
              className="search-input"
              style={{
                width: '100%',
                fontSize: '1.1em'
              }}
              onKeyPress={(e) => e.key === 'Enter' && generateNewPodcast()}
              disabled={isGenerating}
            />
            <div style={{ marginTop: '10px', fontSize: '0.9em', opacity: '0.7' }}>
              💡 Be specific! The more detailed your topic, the better the podcast will be.
            </div>
          </div>
          
          <div style={{ marginTop: '40px', textAlign: 'center' }}>
            <button 
              className="cta-button"
              onClick={generateNewPodcast}
              disabled={isGenerating}
              style={{
                fontSize: '1.2em',
                padding: '18px 40px',
                opacity: isGenerating ? 0.7 : 1,
                cursor: isGenerating ? 'not-allowed' : 'pointer'
              }}
            >
              {generateText}
            </button>
            
            {isGenerating && (
              <div style={{ marginTop: '20px' }}>
                <div className="spinner" style={{ 
                  width: '40px', 
                  height: '40px',
                  margin: '0 auto'
                }}></div>
                <p style={{ marginTop: '15px', opacity: '0.8' }}>
                  Generating your AI podcast... This may take a minute.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Info Banner */}
      <div className="info-banner">
        <div className="banner-content">
          <div className="banner-icon">ℹ️</div>
          <div className="banner-text">
            <strong>How it works:</strong> Our AI creates a multi-voice conversation about your topic with 4 different perspectives. Each podcast is unique and educational!
          </div>
        </div>
      </div>
    </div>
  );
}

export default CreatePage;
