import React from 'react';

interface CopticInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const CopticInput: React.FC<CopticInputProps> = ({
  label,
  error,
  className = '',
  ...props
}) => {
  return (
    <div className="flex flex-col gap-2">
      {label && <label className="text-xs font-bold uppercase text-gold-primary">{label}</label>}
      <input
        className={`
          bg-navy-deep/40 border-b-2 border-gold-primary/30 text-cream placeholder:text-text-muted
          focus:bg-navy-deep/60 focus:border-b-gold-primary focus:outline-none
          transition-all duration-300 px-4 py-2
          ${error ? 'border-b-red-500' : ''}
          ${className}
        `}
        {...props}
      />
      {error && <span className="text-xs text-red-500">{error}</span>}
    </div>
  );
};
