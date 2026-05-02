/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        premium: {
          bg: '#f9f7f2', // Warm Ivory / Cream
          panel: '#ffffff',
          dark: '#1a1a1a', // Near Black
          burgundy: '#4a0e0e', // Deep Wine
          maroon: '#800000',
          accent: '#b22222', // Muted Red
          border: '#e5e1d8',
          text: {
            primary: '#1a1a1a',
            secondary: '#4b4b4b',
            muted: '#8e8e8e',
          }
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['"Playfair Display"', 'serif'],
        display: ['"Cormorant Garamond"', 'serif'],
      },
      letterSpacing: {
        widest: '.2em',
      }
    },
  },
  plugins: [],
}
