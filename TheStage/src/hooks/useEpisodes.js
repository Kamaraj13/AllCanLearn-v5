import { useState, useEffect } from 'react';
import { episodesAPI } from '../services/endpoints';

export const useEpisodes = () => {
  const [episodes, setEpisodes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchEpisodes = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await episodesAPI.getAll();
      setEpisodes(data);
    } catch (err) {
      console.error('Failed to fetch episodes:', err);
      setError(err.message || 'Failed to load episodes');
    } finally {
      setLoading(false);
    }
  };

  const generateEpisode = async (topic, options = {}) => {
    try {
      const newEpisode = await episodesAPI.generate(topic, options);
      // Refresh episodes list after generation
      await fetchEpisodes();
      return newEpisode;
    } catch (err) {
      console.error('Failed to generate episode:', err);
      throw err;
    }
  };

  useEffect(() => {
    fetchEpisodes();
  }, []);

  return {
    episodes,
    loading,
    error,
    refetch: fetchEpisodes,
    generate: generateEpisode
  };
};
