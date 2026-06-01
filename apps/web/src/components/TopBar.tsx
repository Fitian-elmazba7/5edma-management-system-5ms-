import React from 'react';

interface TopBarProps {
  onMenuClick?: () => void;
  userName?: string;
}

export const TopBar: React.FC<TopBarProps> = ({ onMenuClick, userName = 'User' }) => {
  return (
    <div className="sticky top-0 z-40 backdrop-blur-glass border-b border-gold-primary/20 bg-navy-bg/80">
      <div className="flex justify-between items-center px-6 py-4 max-w-full">
        {/* Logo Section */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-gold-primary rounded-sm flex items-center justify-center text-navy-bg font-bold text-lg">
            ⊕
          </div>
          <span className="text-cream font-display font-medium text-sm">5EDMA</span>
        </div>

        {/* Right Side: User Menu */}
        <div className="flex items-center gap-4">
          <div className="hidden md:block text-cream text-sm">{userName}</div>
          <div className="w-8 h-8 bg-gold-primary/30 border border-gold-primary rounded-full" />
          <button
            onClick={onMenuClick}
            className="md:hidden w-6 h-6 flex flex-col justify-center gap-1.5 text-gold-primary hover:text-gold-accent transition-colors"
            aria-label="Toggle menu"
          >
            <span className="w-full h-0.5 bg-current" />
            <span className="w-full h-0.5 bg-current" />
            <span className="w-full h-0.5 bg-current" />
          </button>
        </div>
      </div>
    </div>
  );
};
