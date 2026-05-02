/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        premiumBg: '#f9f7f2',
        premiumPrimary: '#4a0e0e',
        premiumAccent: '#b22222',
        premiumDark: '#1a1a1a',
        premiumNeutral: '#e5e1d8',
        premiumText: {
          primary: '#1a1a1a',
          secondary: '#4b4b4b',
          muted: '#8e8e8e',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['"Playfair Display"', 'serif'],
        display: ['"Cormorant Garamond"', 'serif'],
      }
    },
  },
  plugins: [],
}
