/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#020617', // Slate 950
        card: '#0f172a', // Slate 900
        border: 'rgba(51, 65, 85, 0.5)',
        primary: {
          DEFAULT: '#3b82f6', // Blue 500
          hover: '#2563eb', // Blue 600
        },
        success: '#22c55e',
        warning: '#f59e0b',
        danger: '#ef4444',
      },
      fontFamily: {
        mono: ['Fira Code', 'monospace'],
        sans: ['Fira Sans', 'sans-serif'],
      },
      animation: {
        pulse: 'pulse var(--duration) ease-out infinite',
      },
      keyframes: {
        pulse: {
          '0%': { boxShadow: '0 0 0 0 var(--pulse-color)' },
          '70%': { boxShadow: '0 0 0 var(--pulse-distance) var(--pulse-color-fade)' },
          '100%': { boxShadow: '0 0 0 0 var(--pulse-color-fade)' },
        }
      }
    },
  },
  plugins: [],
}
