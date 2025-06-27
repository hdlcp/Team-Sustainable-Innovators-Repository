// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#4CAF50",   // Vert
        accent: "#FFD700",    // Jaune
        light: "#F3F4F6",     // Gris clair
      },
    },
  },
  plugins: [],
}
