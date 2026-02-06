import { useState, useRef, useEffect } from 'react';
import { episodesAPI } from '../services/endpoints';

export const useAudioPlayer = () => {
  const [currentTrack, setCurrentTrack] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [queue, setQueue] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(-1);
  const audioRef = useRef(null);

  const playTrack = (episode) => {
    // Handle both single episode and episode with turns
    const track = {
      id: episode.id,
      title: episode.topic,
      audio_url: episode.audio_files?.[0] || episodesAPI.getAudioUrl(episode.turns?.[0]?.tts),
      speaker: episode.turns?.[0]?.speaker || 'AI Character',
      episode: episode
    };

    setCurrentTrack(track);
    setIsPlaying(true);
    
    // Add to queue if not already there
    if (!queue.find(item => item.id === track.id)) {
      setQueue([...queue, track]);
    }
    
    setCurrentIndex(queue.findIndex(item => item.id === track.id));
  };

  const pauseTrack = () => {
    setIsPlaying(false);
  };

  const togglePlay = () => {
    if (isPlaying) {
      pauseTrack();
    } else if (currentTrack) {
      setIsPlaying(true);
    }
  };

  const playNext = () => {
    if (currentIndex < queue.length - 1) {
      const nextTrack = queue[currentIndex + 1];
      setCurrentTrack(nextTrack);
      setCurrentIndex(currentIndex + 1);
      setIsPlaying(true);
    }
  };

  const playPrevious = () => {
    if (currentIndex > 0) {
      const prevTrack = queue[currentIndex - 1];
      setCurrentTrack(prevTrack);
      setCurrentIndex(currentIndex - 1);
      setIsPlaying(true);
    }
  };

  const setVolume = (volume) => {
    if (audioRef.current) {
      audioRef.current.volume = volume;
    }
  };

  const seekTo = (percentage) => {
    if (audioRef.current && audioRef.current.duration) {
      const time = (percentage / 100) * audioRef.current.duration;
      audioRef.current.currentTime = time;
    }
  };

  // Handle audio element events
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleEnded = () => {
      // Auto-play next track if available
      if (currentIndex < queue.length - 1) {
        playNext();
      } else {
        setIsPlaying(false);
      }
    };

    const handleLoadedMetadata = () => {
      if (isPlaying) {
        audio.play().catch(console.error);
      }
    };

    audio.addEventListener('ended', handleEnded);
    audio.addEventListener('loadedmetadata', handleLoadedMetadata);

    return () => {
      audio.removeEventListener('ended', handleEnded);
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
    };
  }, [currentTrack, isPlaying, currentIndex, queue]);

  // Play/pause when isPlaying changes
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio || !currentTrack) return;

    if (isPlaying) {
      audio.play().catch(console.error);
    } else {
      audio.pause();
    }
  }, [isPlaying, currentTrack]);

  return {
    currentTrack,
    isPlaying,
    queue,
    currentIndex,
    playTrack,
    pauseTrack,
    togglePlay,
    playNext,
    playPrevious,
    setVolume,
    seekTo,
    audioRef
  };
};
