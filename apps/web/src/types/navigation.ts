export type NavigationSection = 'dashboard' | 'admin' | 'community' | 'reports' | 'settings' | 'default';

export interface NavigationItem {
  label: string;
  href: string;
  icon?: string;
}

export interface NavigationSectionConfig {
  section: NavigationSection;
  label: string;
  items: NavigationItem[];
}

export interface NavigationContextType {
  currentSection: NavigationSection;
  setCurrentSection: (section: NavigationSection) => void;
  getSectionConfig: (section: NavigationSection) => NavigationSectionConfig;
}
