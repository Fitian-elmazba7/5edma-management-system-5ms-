import React from 'react';

interface CopticButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'success' | 'text';
  children: React.ReactNode;
}

export const CopticButton: React.FC<CopticButtonProps> = ({
  variant = 'primary',
  children,
  className = '',
  ...props
}) => {
  const baseClasses = 'px-6 py-3 rounded-lg font-display font-semibold text-sm transition-all duration-300 active:scale-95 disabled:opacity-50';

  const variantClasses = {
    primary: 'bg-gold-primary text-navy-bg shadow-gold-glow hover:bg-gold-accent hover:shadow-md',
    secondary: 'bg-transparent border-2 border-gold-primary text-gold-primary hover:bg-gold-primary/10 shadow-glass',
    danger: 'bg-red-600 text-white border border-gold-primary/30 hover:bg-red-700 shadow-glass',
    success: 'bg-green-600 text-white border border-gold-primary/30 hover:bg-green-700 shadow-glass',
    text: 'bg-transparent text-gold-primary border-b-2 border-transparent hover:border-b-gold-primary hover:text-gold-accent',
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};
