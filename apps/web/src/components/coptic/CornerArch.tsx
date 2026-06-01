import React from 'react';

interface CornerArchProps {
  size?: 'sm' | 'md' | 'lg';
  color?: string;
  className?: string;
}

export const CornerArch: React.FC<CornerArchProps> = ({
  size = 'md',
  color = 'var(--color-gold-primary)',
  className = '',
}) => {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <svg
      className={`${sizeClasses[size]} ${className}`}
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="1.5"
    >
      <path d="M3 3 Q3 12 12 12" />
    </svg>
  );
};
