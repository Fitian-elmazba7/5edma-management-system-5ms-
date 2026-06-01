import React from 'react';

interface GlassCardProps {
  children: React.ReactNode;
  variant?: 'default' | 'stat' | 'with-top-border';
  className?: string;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  variant = 'default',
  className = '',
}) => {
  const baseClasses = 'backdrop-blur-glass border border-gold-primary/20 rounded-lg bg-navy-deep/60 transition-all duration-300 hover:bg-navy-deep/80';

  const variantClasses = {
    default: 'p-6 shadow-glass',
    stat: 'p-4 shadow-md border-t-8 border-t-gold-primary relative',
    'with-top-border': 'p-4 border-t-4 border-t-gold-primary shadow-glass',
  };

  return (
    <div className={`${baseClasses} ${variantClasses[variant]} ${className}`}>
      {children}
    </div>
  );
};
