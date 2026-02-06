import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

function DetailPage({ episode, showPage }) {
  const [fullEpisode, setFullEpisode] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTrackIndex, setCurrentTrackIndex] = useState(0);
  const [audioUrls, setAudioUrls] = useState([]);
  const audioRef = useRef(null);

  useEffect(() => {
    if (episode) {
      loadFullEpisode(episode.id);
    }
  }, [episode]);

  const loadFullEpisode = async (episodeId) => {
    try {
      setLoading(true);
      
      // First check localStorage for newly generated episodes
      const storedEpisodes = JSON.parse(localStorage.getItem("fullEpisodes") || "{}");
      let episodeData = storedEpisodes[episodeId];
      
      // If not in localStorage, fetch from server
      if (!episodeData) {
        const response = await axios.get(`/api/episodes/${episodeId}`);
        episodeData = response.data;
      }
      
      setFullEpisode(episodeData);
      
      // Extract audio URLs and consolidate them
      const urls = [];
      if (episodeData.turns && Array.isArray(episodeData.turns)) {
        episodeData.turns.forEach(turn => {
          if (turn.tts) {
            urls.push({
              url: turn.tts.startsWith('/') ? turn.tts : `/tts_output/${turn.tts}`,
              speaker: turn.speaker,
              message: turn.message
            });
          }
        });
      } else if (episodeData.audio_files && Array.isArray(episodeData.audio_files)) {
        episodeData.audio_files.forEach((audioFile, idx) => {
          urls.push({
            url: audioFile.startsWith('/') ? audioFile : `/tts_output/${audioFile}`,
            speaker: `Audio Part ${idx + 1}`,
            message: 'Audio segment'
          });
        });
      }
      setAudioUrls(urls);
    } catch (error) {
      console.error('Error loading episode:', error);
    } finally {
      setLoading(false);
    }
  };

  const downloadEpisode = (episodeId) => {
    axios.get('/api/episodes')
      .then(response => {
        const ep = response.data.episodes.find(e => e.id === episodeId);
        if (!ep) { 
          alert('Episode not found'); 
          return; 
        }
        
        const blob = new Blob([JSON.stringify(ep, null, 2)], {type: 'application/json'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'episode-' + ep.topic.replace(/[^a-z0-9]/gi, '-').toLowerCase() + '.json';
        a.click();
        URL.revokeObjectURL(url);
      });
  };

  const handlePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleAudioEnded = () => {
    // Auto-play next track
    if (currentTrackIndex < audioUrls.length - 1) {
      setCurrentTrackIndex(currentTrackIndex + 1);
      setTimeout(() => {
        if (audioRef.current) {
          audioRef.current.play();
        }
      }, 100);
    } else {
      // End of playlist
      setIsPlaying(false);
      setCurrentTrackIndex(0);
    }
  };

  const handleTrackSelect = (index) => {
    setCurrentTrackIndex(index);
    setIsPlaying(true);
    setTimeout(() => {
      if (audioRef.current) {
        audioRef.current.play();
      }
    }, 100);
  };

  if (loading || !fullEpisode) {
    return (
      <div className="page active">
        <button className="btn" onClick={() => showPage('home')} style={{ marginBottom: '20px' }}>
          ← Back
        </button>
        <div className="loading">Loading episode...</div>
      </div>
    );
  }

  // Check if we have full episode data (with turns) or metadata (with audio_files)
  const hasFullData = fullEpisode.turns && Array.isArray(fullEpisode.turns) && fullEpisode.turns.length > 0;

  return (
    <div className="page active">
      <button className="btn" onClick={() => showPage('home')} style={{ marginBottom: '20px' }}>
        ← Back
      </button>
      
      <div id="detail-content">
        <div className="header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
          <div>
            <h1>{fullEpisode.topic}</h1>
            <p>{fullEpisode.timestamp ? new Date(parseInt(fullEpisode.id)).toLocaleString() : "Just now"}</p>
          </div>
          <button 
            onClick={() => downloadEpisode(fullEpisode.id)} 
            className="download-btn" 
            style={{ 
              padding: '10px 20px',
              background: 'linear-gradient(135deg, #0ea5e9, #10b981)',
              color: 'white',
              border: 'none',
              borderRadius: '14px',
              cursor: 'pointer',
              fontWeight: '600',
              fontSize: '0.9em',
              transition: 'all 0.3s',
              boxShadow: '0 8px 24px rgba(14, 165, 233, 0.3)',
              whiteSpace: 'nowrap'
            }}
          >
            📥 Download
          </button>
        </div>

        {/* Consolidated Audio Player */}
        {audioUrls.length > 0 && (
          <div className="card" style={{ marginBottom: '30px' }}>
            <h3>🎵 Podcast Player</h3>
            <p>Continuous playback - {audioUrls.length} segments</p>
            
            {/* Main Audio Player */}
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '15px', 
              margin: '20px 0',
              padding: '20px',
              background: 'rgba(255,255,255,0.08)',
              borderRadius: '12px'
            }}>
              <button 
                onClick={handlePlayPause}
                style={{
                  width: '60px',
                  height: '60px',
                  borderRadius: '50%',
                  border: 'none',
                  background: 'linear-gradient(135deg, #0ea5e9, #10b981)',
                  color: 'white',
                  fontSize: '24px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '0 8px 24px rgba(14, 165, 233, 0.3)'
                }}
              >
                {isPlaying ? '⏸️' : '▶️'}
              </button>
              
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: '600', marginBottom: '5px' }}>
                  {audioUrls[currentTrackIndex]?.speaker || 'Unknown'}
                </div>
                <div style={{ fontSize: '0.9em', opacity: 0.8 }}>
                  Track {currentTrackIndex + 1} of {audioUrls.length}
                </div>
              </div>
            </div>

            {/* Hidden Audio Element */}
            <audio 
              ref={audioRef}
              src={audioUrls[currentTrackIndex]?.url || ''}
              onEnded={handleAudioEnded}
              preload="auto"
            />

            {/* Track List */}
            <div style={{ marginTop: '20px' }}>
              <h4 style={{ marginBottom: '10px' }}>📋 Conversation Tracks</h4>
              {audioUrls.length > 0 ? (
                audioUrls.map((track, index) => (
                  <div 
                    key={index}
                    className={`track-item ${currentTrackIndex === index ? 'active' : ''}`}
                    onClick={() => handleTrackSelect(index)}
                  >
                    <div className="track-info">
                      <div className="track-speaker">{track.speaker}</div>
                      <div className="track-message">{track.message}</div>
                    </div>
                  </div>
                ))
              ) : (
                <p>No tracks available.</p>
              )}
            </div>
          </div>
        )}

        {/* Original Content Display */}
        {fullEpisode.turns && Array.isArray(fullEpisode.turns) && fullEpisode.turns.length > 0 ? (
          fullEpisode.turns.map((turn, idx) => (
            <div key={idx} className="card">
              <h3>Turn {idx + 1}</h3>
              <div style={{ margin: '16px 0', padding: '16px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                <strong>{turn.speaker}:</strong>
                <p>{turn.message}</p>
              </div>
            </div>
          ))
        ) : (
          <div className="card">
            <h3>📝 Episode Content</h3>
            <p>This episode contains {fullEpisode.turns_count || 0} conversation turns.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default DetailPage;
