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
    <div className="page active">
      <div className="header">
        <h1>Create Custom Podcast</h1>
        <p>Generate a podcast on any topic you want to learn about</p>
      </div>
      
      <div style={{ maxWidth: '600px' }}>
        <div style={{ marginTop: '20px' }}>
          <label style={{ display: 'block', marginBottom: '10px', fontWeight: '600', fontSize: '1.1em' }}>
            🎙️ What topic would you like to hear about?
          </label>
          <input 
            type="text"
            value={customTopic}
            onChange={(e) => setCustomTopic(e.target.value)}
            placeholder="e.g., 'The future of renewable energy', 'Ancient Roman history', 'How to invest in stocks'"
            style={{
              width: '100%',
              padding: '14px 20px',
              background: 'rgba(26, 31, 58, 0.7)',
              backdropFilter: 'blur(20px)',
              border: '2px solid rgba(14, 165, 233, 0.3)',
              color: 'inherit',
              fontSize: '1em',
              borderRadius: '14px',
              cursor: 'text',
              fontWeight: '600',
              transition: 'all 0.3s'
            }}
            onKeyPress={(e) => e.key === 'Enter' && generateNewPodcast()}
          />
          <div style={{ marginTop: '8px', fontSize: '0.9em', opacity: '0.7' }}>
            💡 Be specific! The more detailed your topic, the better the podcast will be.
          </div>
        </div>
        
        <div style={{ marginTop: '30px' }}>
          <button 
            className="btn" 
            onClick={generateNewPodcast}
            disabled={isGenerating || !customTopic.trim()}
          >
            <span>{generateText}</span>
          </button>
        </div>
        
        <div style={{ marginTop: '20px', padding: '20px', background: 'rgba(14, 165, 233, 0.1)', borderRadius: '12px', border: '1px solid rgba(14, 165, 233, 0.3)' }}>
          <h4 style={{ marginBottom: '10px', color: '#0ea5e9' }}>📋 How it works:</h4>
          <ul style={{ margin: 0, paddingLeft: '20px', lineHeight: '1.6' }}>
            <li>Enter any topic you're interested in learning about</li>
            <li>AI will generate a discussion with multiple expert perspectives</li>
            <li>Your podcast will be saved for 3 days</li>
            <li>Listen as many times as you want during that period</li>
            <li>Episodes are automatically deleted after 3 days to save space</li>
          </ul>
        </div>

        <div style={{ marginTop: '20px', padding: '20px', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '12px', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
          <h4 style={{ marginBottom: '10px', color: '#10b981' }}>💡 Pro Tips:</h4>
          <ul style={{ margin: 0, paddingLeft: '20px', lineHeight: '1.6' }}>
            <li><strong>Be specific:</strong> Instead of "science", try "quantum computing applications"</li>
            <li><strong>Add context:</strong> "How blockchain is changing supply chain management"</li>
            <li><strong>Ask questions:</strong> "Why do we dream and what do dreams mean?"</li>
            <li><strong>Compare topics:</strong> "Traditional vs. online education pros and cons"</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default CreatePage;
