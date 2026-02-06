import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, SkipBack, SkipForward, Volume2, Maximize2, Minimize2 } from 'lucide-react';

const AudioPlayer = ({ track, isPlaying, onTogglePlay, onClose }) => {
  const [volume, setVolume] = useState(0.7);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isMinimized, setIsMinimized] = useState(false);
  const audioRef = useRef(null);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio || !track) return;

    const updateProgress = () => {
      setProgress((audio.currentTime / audio.duration) * 100 || 0);
    };

    const updateDuration = () => {
      setDuration(audio.duration || 0);
    };

    audio.addEventListener('timeupdate', updateProgress);
    audio.addEventListener('loadedmetadata', updateDuration);

    return () => {
      audio.removeEventListener('timeupdate', updateProgress);
      audio.removeEventListener('loadedmetadata', updateDuration);
    };
  }, [track]);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.play();
    } else {
      audio.pause();
    }
  }, [isPlaying]);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;
    audio.volume = volume;
  }, [volume]);

  const handleProgressChange = (e) => {
    const audio = audioRef.current;
    const newProgress = e.target.value;
    setProgress(newProgress);
    if (audio && duration) {
      audio.currentTime = (newProgress / 100) * duration;
    }
  };

  const handleVolumeChange = (e) => {
    setVolume(e.target.value);
  };

  const formatTime = (seconds) => {
    if (!seconds || isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!track) return null;

  return (
    <>
      {/* Hidden Audio Element */}
      <audio
        ref={audioRef}
        src={track.audio_url || `/tts_output/${track.tts}`}
        onEnded={() => {/* Handle track end */}}
      />
      
      {/* Audio Player */}
      <div className={`
        fixed bottom-0 left-0 right-0 bg-[#181818] border-t border-gray-800 z-50
        transition-all duration-300
        ${isMinimized ? 'h-16' : 'h-24'}
      `}>
        <div className="max-w-7xl mx-auto h-full px-4 flex items-center gap-4">
          
          {/* Track Info */}
          <div className="flex items-center gap-4 min-w-0 flex-1">
            <div className="w-12 h-12 bg-gradient-to-br from-[#10B981] to-purple-600 rounded flex items-center justify-center flex-shrink-0">
              <Volume2 className="w-6 h-6 text-white" />
            </div>
            
            {!isMinimized && (
              <div className="min-w-0">
                <h4 className="font-medium text-white truncate">
                  {track.topic || 'Unknown Episode'}
                </h4>
                <p className="text-sm text-gray-400 truncate">
                  {track.speaker || 'AI Character'}
                </p>
              </div>
            )}
          </div>
          
          {/* Controls */}
          <div className="flex items-center gap-4">
            <button className="text-gray-400 hover:text-white transition-colors">
              <SkipBack className="w-5 h-5" />
            </button>
            
            <button
              onClick={onTogglePlay}
              className="w-10 h-10 bg-[#10B981] rounded-full flex items-center justify-center hover:scale-110 transition-transform"
            >
              {isPlaying ? (
                <Pause className="w-5 h-5 text-white" />
              ) : (
                <Play className="w-5 h-5 text-white ml-1" />
              )}
            </button>
            
            <button className="text-gray-400 hover:text-white transition-colors">
              <SkipForward className="w-5 h-5" />
            </button>
          </div>
          
          {/* Progress Bar */}
          {!isMinimized && (
            <div className="flex items-center gap-3 flex-1 max-w-md">
              <span className="text-xs text-gray-400">
                {formatTime((progress / 100) * duration)}
              </span>
              
              <div className="flex-1 h-1 bg-gray-700 rounded-full overflow-hidden">
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={progress}
                  onChange={handleProgressChange}
                  className="w-full h-1 bg-transparent appearance-none cursor-pointer slider"
                  style={{
                    background: `linear-gradient(to right, #10B981 0%, #10B981 ${progress}%, #374151 ${progress}%, #374151 100%)`
                  }}
                />
              </div>
              
              <span className="text-xs text-gray-400">
                {formatTime(duration)}
              </span>
            </div>
          )}
          
          {/* Volume & Minimize */}
          <div className="flex items-center gap-3">
            {!isMinimized && (
              <div className="flex items-center gap-2">
                <Volume2 className="w-4 h-4 text-gray-400" />
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={volume}
                  onChange={handleVolumeChange}
                  className="w-20 h-1 bg-gray-700 rounded-full appearance-none cursor-pointer"
                />
              </div>
            )}
            
            <button
              onClick={() => setIsMinimized(!isMinimized)}
              className="text-gray-400 hover:text-white transition-colors"
            >
              {isMinimized ? (
                <Maximize2 className="w-4 h-4" />
              ) : (
                <Minimize2 className="w-4 h-4" />
              )}
            </button>
          </div>
        </div>
      </div>
      
      {/* Custom Styles */}
      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          width: 12px;
          height: 12px;
          background: #10B981;
          border-radius: 50%;
          cursor: pointer;
        }
        
        .slider::-moz-range-thumb {
          width: 12px;
          height: 12px;
          background: #10B981;
          border-radius: 50%;
          cursor: pointer;
          border: none;
        }
      `}</style>
    </>
  );
};

export default AudioPlayer;
