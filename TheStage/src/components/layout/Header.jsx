import React from 'react';
import { Menu, X, Radio, Search, User } from 'lucide-react';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  const navigation = [
    { name: 'Home', href: '#', current: true },
    { name: 'Explore', href: '#explore', current: false },
    { name: 'Create', href: '#create', current: false },
    { name: 'Library', href: '#library', current: false },
  ];

  return (
    <header className="sticky top-0 z-40 bg-[#121212]/80 backdrop-blur-lg border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo */}
          <div className="flex items-center">
            <div className="flex items-center gap-2">
              <Radio className="w-8 h-8 text-[#10B981]" />
              <span className="text-xl font-bold text-white">AllCanLearn</span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <a
                key={item.name}
                href={item.href}
                className={`
                  text-sm font-medium transition-colors
                  ${item.current 
                    ? 'text-[#10B981]' 
                    : 'text-gray-300 hover:text-white'
                  }
                `}
              >
                {item.name}
              </a>
            ))}
          </nav>

          {/* Search & User */}
          <div className="hidden md:flex items-center gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search episodes..."
                className="w-64 pl-10 pr-4 py-2 bg-[#181818] border border-gray-700 rounded-full text-sm text-white placeholder-gray-400 focus:outline-none focus:border-[#10B981] focus:ring-1 focus:ring-[#10B981]"
              />
            </div>
            
            <button className="w-10 h-10 bg-[#181818] border border-gray-700 rounded-full flex items-center justify-center hover:bg-[#282828] transition-colors">
              <User className="w-5 h-5 text-gray-400" />
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="w-10 h-10 bg-[#181818] border border-gray-700 rounded-full flex items-center justify-center hover:bg-[#282828] transition-colors"
            >
              {isMenuOpen ? (
                <X className="w-5 h-5 text-gray-400" />
              ) : (
                <Menu className="w-5 h-5 text-gray-400" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className="md:hidden bg-[#181818] border-t border-gray-800">
          <div className="px-4 py-4 space-y-3">
            {navigation.map((item) => (
              <a
                key={item.name}
                href={item.href}
                className={`
                  block px-3 py-2 rounded-md text-base font-medium transition-colors
                  ${item.current 
                    ? 'bg-[#10B981]/10 text-[#10B981] border border-[#10B981]/30' 
                    : 'text-gray-300 hover:bg-[#282828] hover:text-white'
                  }
                `}
                onClick={() => setIsMenuOpen(false)}
              >
                {item.name}
              </a>
            ))}
            
            {/* Mobile Search */}
            <div className="pt-4 border-t border-gray-700">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search episodes..."
                  className="w-full pl-10 pr-4 py-2 bg-[#121212] border border-gray-700 rounded-full text-sm text-white placeholder-gray-400 focus:outline-none focus:border-[#10B981] focus:ring-1 focus:ring-[#10B981]"
                />
              </div>
            </div>
            
            {/* Mobile User */}
            <div className="pt-2 border-t border-gray-700">
              <button className="w-full flex items-center gap-3 px-3 py-2 bg-[#121212] border border-gray-700 rounded-full text-gray-300 hover:bg-[#282818] hover:text-white transition-colors">
                <User className="w-5 h-5" />
                <span>Account</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
