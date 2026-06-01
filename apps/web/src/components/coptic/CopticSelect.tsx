import React from 'react';

interface CopticSelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: { value: string; label: string }[];
  error?: string;
}

export const CopticSelect: React.FC<CopticSelectProps> = ({
  label,
  options,
  error,
  className = '',
  ...props
}) => {
  return (
    <div className="flex flex-col gap-2">
      {label && <label className="text-xs font-bold uppercase text-gold-primary">{label}</label>}
      <select
        className={`
          bg-navy-deep/40 border-b-2 border-gold-primary/30 text-cream
          focus:bg-navy-deep/60 focus:border-b-gold-primary focus:outline-none
          transition-all duration-300 px-4 py-2 rounded-none
          appearance-none cursor-pointer
          ${error ? 'border-b-red-500' : ''}
          ${className}
        `}
        {...props}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value} className="bg-navy-deep text-cream">
            {option.label}
          </option>
        ))}
      </select>
      {error && <span className="text-xs text-red-500">{error}</span>}
    </div>
  );
};
