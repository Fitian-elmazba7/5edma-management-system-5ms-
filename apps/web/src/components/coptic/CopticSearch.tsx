import React from 'react';

interface CopticSearchProps extends React.InputHTMLAttributes<HTMLInputElement> {
  onSearch?: (value: string) => void;
}

export const CopticSearch: React.FC<CopticSearchProps> = ({
  onSearch,
  className = '',
  ...props
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onSearch?.(e.target.value);
  };

  return (
    <div className="relative">
      <input
        type="text"
        className={`
          w-full bg-navy-deep/40 border-b-2 border-gold-primary/30 text-cream placeholder:text-text-muted
          focus:bg-navy-deep/60 focus:border-b-gold-primary focus:outline-none
          transition-all duration-300 px-4 py-2 pl-10
          ${className}
        `}
        onChange={handleChange}
        {...props}
      />
      <svg
        className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gold-primary"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>
  );
};
