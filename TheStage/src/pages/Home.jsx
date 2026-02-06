import React, { useState, useEffect } from 'react';
import { Play, Headphones, Radio, Mic2, Clock, Users } from 'lucide-react';
import { useEpisodes } from '../hooks/useEpisodes';
import { useAudioPlayer } from '../hooks/useAudioPlayer';
import Hero from '../components/features/Hero';
import CharacterCard from '../components/features/CharacterCard';
import EpisodeRail from '../components/features/EpisodeRail';
import AudioPlayer from '../components/features/AudioPlayer';
import Header from '../components/layout/Header';
import Button from '../components/ui/Button';

const Home = () => {
  const { episodes, loading, error } = useEpisodes();
  const { currentTrack, isPlaying, playTrack, pauseTrack, togglePlay } = useAudioPlayer();
  const [selectedCharacter, setSelectedCharacter] = useState(null);

  const characters = [
    {
      id: 'captain',
      name: 'The Captain',
      role: 'Strategic Leadership',
      icon: <Radio className="w-8 h-8" />,
      gradient: 'from-purple-600 to-blue-600',
      description: 'Guides the conversation with strategic insights and direction',
      color: '#8B5CF6'
    },
    {
      id: 'sage',
      name: 'The Sage',
      role: 'Wisdom & Experience',
      icon: <Headphones className="w-8 h-8" />,
      gradient: 'from-emerald-600 to-teal-600',
      description: 'Brings deep knowledge and practical wisdom to discussions',
      color: '#10B981'
    },
    {
      id: 'rebel',
      name: 'The Rebel',
      role: 'Innovation & Challenge',
      icon: <Mic2 className="w-8 h-8" />,
      gradient: 'from-orange-600 to-red-600',
      description: 'Challenges assumptions and brings fresh perspectives',
      color: '#F97316'
    },
    {
      id: 'architect',
      name: 'The Architect',
      role: 'Structure & Logic',
      icon: <Users className="w-8 h-8" />,
      gradient: 'from-cyan-600 to-blue-600',
      description: 'Builds logical frameworks and structured thinking',
      color: '#06B6D4'
    }
  ];

  const recentEpisodes = episodes?.slice(0, 8) || [];
  const essentialEpisodes = episodes?.filter(ep => 
    ep.topic?.includes('Essential') || ep.topic?.includes('Climate') || ep.topic?.includes('AI')
  ).slice(0, 8) || [];

  return (
    <div className="min-h-screen bg-[#121212] text-white">
      <Header />
      
      {/* Hero Section */}
      <Hero />
      
      {/* Character Cards Section */}
      <section className="px-6 py-12 md:px-8 lg:px-12">
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-2">Meet Your AI Learning Team</h2>
          <p className="text-gray-400">Each character brings unique perspectives to every conversation</p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {characters.map((character) => (
            <CharacterCard
              key={character.id}
              character={character}
              isSelected={selectedCharacter === character.id}
              onSelect={() => setSelectedCharacter(character.id)}
            />
          ))}
        </div>
      </section>

      {/* Recent Episodes Rail */}
      <section className="px-6 py-8 md:px-8 lg:px-12">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold mb-2">Recent Episodes</h2>
            <p className="text-gray-400">Latest AI-powered learning conversations</p>
          </div>
          <Button variant="ghost" className="text-[#10B981] hover:text-[#10B981]/80">
            View All
          </Button>
        </div>
        
        <EpisodeRail 
          episodes={recentEpisodes}
          loading={loading}
          onPlay={playTrack}
          currentTrack={currentTrack}
          isPlaying={isPlaying}
        />
      </section>

      {/* Essential Topics Rail */}
      <section className="px-6 py-8 md:px-8 lg:px-12">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold mb-2">Essential Topics</h2>
            <p className="text-gray-400">Deep dives into critical subjects</p>
          </div>
          <Button variant="ghost" className="text-[#10B981] hover:text-[#10B981]/80">
            Explore More
          </Button>
        </div>
        
        <EpisodeRail 
          episodes={essentialEpisodes}
          loading={loading}
          onPlay={playTrack}
          currentTrack={currentTrack}
          isPlaying={isPlaying}
        />
      </section>

      {/* Audio Player */}
      {currentTrack && (
        <AudioPlayer
          track={currentTrack}
          isPlaying={isPlaying}
          onTogglePlay={togglePlay}
          onClose={() => {/* Handle close */}}
        />
      )}
    </div>
  );
};

export default Home;
