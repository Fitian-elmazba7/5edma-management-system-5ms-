import React, { createContext, useContext, useState } from 'react';
import { NavigationContextType, NavigationSection, NavigationSectionConfig } from '../types/navigation';

const NavigationContext = createContext<NavigationContextType | undefined>(undefined);

const NAVIGATION_CONFIGS: Record<NavigationSection, NavigationSectionConfig> = {
  dashboard: {
    section: 'dashboard',
    label: 'Dashboard',
    items: [
      { label: 'Overview', href: '/dashboard' },
      { label: 'Attendance', href: '/attendance' },
      { label: 'Reports', href: '/reports' },
      { label: 'Settings', href: '/settings' },
    ],
  },
  admin: {
    section: 'admin',
    label: 'Administration',
    items: [
      { label: 'Users', href: '/users' },
      { label: 'Roles & Permissions', href: '/admin' },
      { label: 'Settings', href: '/settings' },
      { label: 'Audit Log', href: '/audit' },
    ],
  },
  community: {
    section: 'community',
    label: 'Community',
    items: [
      { label: 'Members', href: '/members' },
      { label: 'Groups', href: '/groups' },
      { label: 'Events', href: '/events' },
      { label: 'Announcements', href: '/announcements' },
    ],
  },
  reports: {
    section: 'reports',
    label: 'Reports',
    items: [
      { label: 'Analytics', href: '/analytics' },
      { label: 'Exports', href: '/export' },
    ],
  },
  settings: {
    section: 'settings',
    label: 'Settings',
    items: [
      { label: 'Profile', href: '/profile' },
      { label: 'Preferences', href: '/preferences' },
    ],
  },
  default: {
    section: 'default',
    label: 'Home',
    items: [
      { label: 'Dashboard', href: '/dashboard' },
      { label: 'Home', href: '/' },
    ],
  },
};

export const NavigationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentSection, setCurrentSection] = useState<NavigationSection>('dashboard');

  const getSectionConfig = (section: NavigationSection): NavigationSectionConfig => {
    return NAVIGATION_CONFIGS[section] || NAVIGATION_CONFIGS.default;
  };

  const value: NavigationContextType = {
    currentSection,
    setCurrentSection,
    getSectionConfig,
  };

  return (
    <NavigationContext.Provider value={value}>
      {children}
    </NavigationContext.Provider>
  );
};

export const useNavigation = () => {
  const context = useContext(NavigationContext);
  if (!context) {
    throw new Error('useNavigation must be used within a NavigationProvider');
  }
  return context;
};
