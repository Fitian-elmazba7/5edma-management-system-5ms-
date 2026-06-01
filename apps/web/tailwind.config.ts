import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        gold: {
          primary: 'var(--color-gold-primary)',
          accent: 'var(--color-gold-accent)',
        },
        navy: {
          deep: 'var(--color-navy-deep)',
          light: 'var(--color-navy-light)',
          bg: 'var(--color-navy-bg)',
        },
        cream: 'var(--color-cream)',
        text: {
          primary: 'var(--color-text-primary)',
          muted: 'var(--color-text-muted)',
        },
      },
      spacing: {
        xs: 'var(--spacing-xs)',
        sm: 'var(--spacing-sm)',
        md: 'var(--spacing-md)',
        lg: 'var(--spacing-lg)',
        xl: 'var(--spacing-xl)',
        xxl: 'var(--spacing-xxl)',
      },
      fontFamily: {
        display: "var(--font-family-heading)",
        body: "var(--font-family-body)",
      },
      boxShadow: {
        glass: 'var(--glass-effect-shadow)',
        'gold-glow': 'var(--gold-glow-shadow)',
      },
      backdropBlur: {
        glass: 'var(--glass-effect-backdrop)',
      },
      animation: {
        fadeIn: 'fadeIn 0.6s ease-in-out',
        slideInUp: 'slideInUp 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideInUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
};

export default config;
