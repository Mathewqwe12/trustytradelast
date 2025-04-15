/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        telegram: {
          primary: '#0088cc',
          secondary: '#0099ff',
          accent: '#00b2ff',
        },
      },
    },
  },
  plugins: [],
} 