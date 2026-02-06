import React from 'react';
import { Play, Clock, Users, Volume2, MoreHorizontal } from 'lucide-react';

const EpisodeRail = ({ episodes, loading, onPlay, currentTrack, isPlaying }) => {
  if (loading) {
    return (
      <div className="flex gap-4 overflow-x-auto pb-4">
        {[...Array(8)].map((_, i) => (
          <div key={i} className="flex-shrink-0 w-64">
            <div className="bg-gray-800 rounded-lg h-36 animate-pulse" />
            <div className="mt-3 space-y-2">
              <div className="h-4 bg-gray-800 rounded animate-pulse" />
              <div className="h-3 bg-gray-800 rounded w-3/4 animate-pulse" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  const isCurrentlyPlaying = (episode) => {
    return currentTrack?.id === episode.id && isPlaying;
  };

  return (
    <div className="episode-rail">
      {episodes?.map((episode) => (
        <div key={episode.id} className="flex-shrink-0 w-64 group">
          {/* Episode Card */}
          <div className="netflix-card bg-gray-800 rounded-lg overflow-hidden">
            {/* Thumbnail */}
            <div className="relative h-36 bg-gradient-to-br from-[#10B981]/20 to-purple-600/20 flex items-center justify-center">
              {/* Play Button Overlay */}
              <div 
                onClick={() => onPlay(episode)}
                className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
              >
                <div className="w-12 h-12 bg-[#10B981] rounded-full flex items-center justify-center hover:scale-110 transition-transform">
                  {isCurrentlyPlaying(episode) ? (
                    <div className="w-0 h-0 border-l-[12px] border-l-white border-y-[8px] border-y-transparent ml-1" />
                  ) : (
                    <Play className="w-5 h-5 text-white ml-1" />
                  )}
                </div>
              </div>
              
              {/* Now Playing Indicator */}
              {isCurrentlyPlaying(episode) && (
                <div className="absolute top-2 left-2 flex items-center gap-1 bg-[#10B981] px-2 py-1 rounded-full">
                  <Volume2 className="w-3 h-3 text-white" />
                  <span className="text-xs text-white font-medium">NOW PLAYING</span>
                </div>
              )}
              
              {/* Episode Number */}
              <div className="absolute top-2 right-2 bg-black/60 px-2 py-1 rounded">
                <span className="text-xs text-white">EP {episode.turns_count || 0}</span>
              </div>
            </div>
            
            {/* Episode Info */}
            <div className="p-4">
              <h3 className="font-semibold text-white mb-2 line-clamp-2 group-hover:text-[#10B981] transition-colors">
                {episode.topic || 'Untitled Episode'}
              </h3>
              
              <div className="flex items-center gap-4 text-xs text-gray-400">
                <div className="flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  <span>{new Date(episode.created_at).toLocaleDateString()}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Users className="w-3 h-3" />
                  <span>{episode.turns_count || 0} turns</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}
      
      {/* Empty State */}
      {!episodes?.length && !loading && (
        <div className="text-center py-12 col-span-full">
          <div className="text-gray-400 mb-4">No episodes available</div>
          <button className="text-[#10B981] hover:text-[#10B981]/80 text-sm font-medium">
            Create your first episode
          </button>
        </div>
      )}
    </div>
  );
};

export default EpisodeRail;
