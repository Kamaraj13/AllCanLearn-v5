import React from 'react';
import { Play, Users, Clock, Volume2 } from 'lucide-react';

const CharacterCard = ({ character, isSelected, onSelect }) => {
  return (
    <div
      onClick={onSelect}
      className={`
        relative overflow-hidden rounded-xl cursor-pointer transition-all duration-300
        hover:scale-105 hover:shadow-2xl hover:shadow-[#10B981]/20
        ${isSelected ? 'ring-2 ring-[#10B981]' : ''}
      `}
    >
      {/* Card Background */}
      <div className={`h-48 bg-gradient-to-br ${character.gradient} p-6 flex flex-col justify-between`}>
        
        {/* Icon */}
        <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center">
          {character.icon}
        </div>
        
        {/* Content */}
        <div className="space-y-2">
          <h3 className="text-xl font-bold text-white">{character.name}</h3>
          <p className="text-sm text-white/80 font-medium">{character.role}</p>
        </div>
      </div>
      
      {/* Hover Overlay */}
      <div className="absolute inset-0 bg-black/60 opacity-0 hover:opacity-100 transition-opacity duration-300 p-6 flex flex-col justify-center">
        <p className="text-sm text-white/90 mb-4">{character.description}</p>
        <div className="flex items-center gap-2 text-white">
          <Play className="w-4 h-4" />
          <span className="text-sm font-medium">View Episodes</span>
        </div>
      </div>
      
      {/* Selection Indicator */}
      {isSelected && (
        <div className="absolute top-3 right-3 w-3 h-3 bg-[#10B981] rounded-full animate-pulse" />
      )}
    </div>
  );
};

export default CharacterCard;
