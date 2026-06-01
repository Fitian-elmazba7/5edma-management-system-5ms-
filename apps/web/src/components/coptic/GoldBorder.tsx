import React from 'react';

interface GoldBorderProps {
  position?: 'top' | 'left' | 'bottom' | 'all';
  children: React.ReactNode;
  className?: string;
}

export const GoldBorder: React.FC<GoldBorderProps> = ({
  position = 'top',
  children,
  className = '',
}) => {
  const positionClasses = {
    top: 'border-t-4 border-t-gold-primary',
    left: 'border-l-4 border-l-gold-primary',
    bottom: 'border-b-4 border-b-gold-primary',
    all: 'border-4 border-gold-primary',
  };

  return (
    <div className={`${positionClasses[position]} ${className}`}>
      {children}
    </div>
  );
};
