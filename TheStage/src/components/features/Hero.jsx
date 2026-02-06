import React from 'react';
import { Play, Radio, Sparkles } from 'lucide-react';
import Button from '../ui/Button';

const Hero = () => {
  return (
    <section className="relative px-6 py-16 md:px-8 lg:px-12 overflow-hidden">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-[#10B981]/20 via-transparent to-purple-600/20" />
      
      {/* Content */}
      <div className="relative max-w-7xl mx-auto">
        <div className="text-center mb-12">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-[#10B981]/10 border border-[#10B981]/30 rounded-full mb-6">
            <Radio className="w-4 h-4 text-[#10B981]" />
            <span className="text-sm text-[#10B981] font-medium">Now Streaming</span>
          </div>
          
          {/* Main Title */}
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-white via-[#10B981] to-purple-400 bg-clip-text text-transparent">
            AllCanLearn Radio
          </h1>
          
          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Your AI Learning Station - Where conversations become knowledge
          </p>
          
          {/* Description */}
          <p className="text-gray-400 mb-12 max-w-2xl mx-auto">
            Experience dynamic AI-powered discussions featuring strategic leaders, wisdom keepers, 
            innovators, and architects exploring topics that matter to your growth.
          </p>
          
          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button 
              size="lg" 
              className="bg-[#10B981] hover:bg-[#10B981]/90 text-white font-semibold px-8 py-4 flex items-center gap-2"
            >
              <Play className="w-5 h-5" />
              Start Listening
            </Button>
            
            <Button 
              variant="outline" 
              size="lg"
              className="border-gray-600 text-white hover:bg-white/10 font-semibold px-8 py-4 flex items-center gap-2"
            >
              <Sparkles className="w-5 h-5" />
              Create Episode
            </Button>
          </div>
        </div>
        
        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16">
          <div className="text-center">
            <div className="text-3xl font-bold text-[#10B981] mb-2">1000+</div>
            <div className="text-gray-400 text-sm">AI Episodes</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-400 mb-2">4</div>
            <div className="text-gray-400 text-sm">AI Characters</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-orange-400 mb-2">24/7</div>
            <div className="text-gray-400 text-sm">Learning Stream</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-cyan-400 mb-2">∞</div>
            <div className="text-gray-400 text-sm">Topics</div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
