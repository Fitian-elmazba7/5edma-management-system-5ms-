/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'glass-bg': '#020408',
        'glass-surface': 'rgba(8, 14, 26, 0.7)',
        'glass-border': 'rgba(59, 130, 246, 0.2)',
        'glass-primary': '#2563eb',
        'glass-primary-dark': '#1d4ed8',
        'glass-text': '#e2e8f0',
        'glass-muted': '#94a3b8',
      },
      backgroundImage: {
        'glass-gradient': 'linear-gradient(135deg, #1e40af, #3b82f6, #6366f1)',
      },
      backdropBlur: {
        'glass': '16px',
      },
    },
  },
  plugins: [],
}
