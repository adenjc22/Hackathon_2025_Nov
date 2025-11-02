/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class', // enable manual dark mode toggling with .dark on <html> or <body>
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          dark: '#1a1a1a',      // dark grey background
          light: '#ebebebff',     // light background (if you add light mode)
          blue: '#00bfff',      // luminous blue accent
        },
      },
    },
  },
  plugins: [],
};
