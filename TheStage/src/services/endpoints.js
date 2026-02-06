import api from './api';

export const episodesAPI = {
  // Get all episodes
  getAll: async () => {
    const response = await api.get('/api/episodes');
    return response.data.episodes || [];
  },

  // Get specific episode by ID
  getById: async (episodeId) => {
    const response = await api.get(`/api/episodes/${episodeId}`);
    return response.data;
  },

  // Generate new episode
  generate: async (topic, options = {}) => {
    const payload = {
      topic,
      tts: options.tts !== false, // Default to true
      essential: options.essential || false,
    };
    
    const response = await api.post('/generate', payload);
    return response.data;
  },

  // Get episode audio file URL
  getAudioUrl: (filename) => {
    return `${api.defaults.baseURL}/tts_output/${filename}`;
  },

  // Download episode JSON
  downloadEpisode: async (episodeId) => {
    const response = await api.get('/api/episodes');
    const episode = response.data.episodes.find(ep => ep.id === episodeId);
    
    if (!episode) {
      throw new Error('Episode not found');
    }
    
    const blob = new Blob([JSON.stringify(episode, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `episode-${episode.topic.replace(/[^a-z0-9]/gi, '-').toLowerCase()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }
};

export const charactersAPI = {
  // Get character information
  getAll: () => [
    {
      id: 'captain',
      name: 'The Captain',
      role: 'Strategic Leadership',
      description: 'Guides conversations with strategic insights and direction',
      gradient: 'from-purple-600 to-blue-600',
      color: '#8B5CF6'
    },
    {
      id: 'sage',
      name: 'The Sage',
      role: 'Wisdom & Experience',
      description: 'Brings deep knowledge and practical wisdom to discussions',
      gradient: 'from-emerald-600 to-teal-600',
      color: '#10B981'
    },
    {
      id: 'rebel',
      name: 'The Rebel',
      role: 'Innovation & Challenge',
      description: 'Challenges assumptions and brings fresh perspectives',
      gradient: 'from-orange-600 to-red-600',
      color: '#F97316'
    },
    {
      id: 'architect',
      name: 'The Architect',
      role: 'Structure & Logic',
      description: 'Builds logical frameworks and structured thinking',
      gradient: 'from-cyan-600 to-blue-600',
      color: '#06B6D4'
    }
  ]
};

// Essential topics for quick generation
export const essentialTopics = [
  "Climate Change and Environmental Sustainability",
  "Artificial Intelligence and the Future of Technology",
  "Global Economy and Financial Markets",
  "Mental Health and Wellness in Modern Society",
  "Space Exploration and Scientific Discoveries",
  "Renewable Energy and Sustainable Living",
  "Social Media Impact on Society and Communication",
  "Global Health and Pandemic Preparedness",
  "Education Systems and Learning in the Digital Age",
  "Human Rights and Social Justice Worldwide"
];

export default {
  episodes: episodesAPI,
  characters: charactersAPI,
  essentialTopics
};
