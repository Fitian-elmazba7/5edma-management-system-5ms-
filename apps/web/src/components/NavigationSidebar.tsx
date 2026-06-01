import React from 'react';
import { useNavigation } from '../context/NavigationContext';

interface NavigationSidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export const NavigationSidebar: React.FC<NavigationSidebarProps> = ({ isOpen = true, onClose }) => {
  const { currentSection, getSectionConfig } = useNavigation();
  const config = getSectionConfig(currentSection);

  return (
    <>
      {/* Mobile Overlay */}
      {!isOpen && (
        <div className="fixed inset-0 bg-black/50 z-30 md:hidden" onClick={onClose} />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed md:sticky top-0 left-0 z-40 h-screen w-48 bg-navy-deep/60 backdrop-blur-glass
          border-r border-gold-primary/15 overflow-y-auto transition-all duration-300
          ${!isOpen ? '-translate-x-full md:translate-x-0' : 'translate-x-0'}
          md:translate-x-0 md:top-16
        `}
      >
        <div className="p-4 flex flex-col gap-2">
          {/* Section Label */}
          <div className="px-4 py-2 text-xs font-bold uppercase text-gold-accent">
            {config.label}
          </div>

          {/* Navigation Items */}
          {config.items.map((item) => (
            <a
              key={item.href}
              href={item.href}
              onClick={onClose}
              className="px-4 py-3 rounded-lg text-sm text-cream hover:bg-navy-light/30 hover:text-gold-primary transition-all duration-200 border-l-4 border-l-transparent hover:border-l-gold-primary hover:bg-gold-primary/5"
            >
              {item.label}
            </a>
          ))}
        </div>
      </aside>
    </>
  );
};
