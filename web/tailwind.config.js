/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Calm, neutral palette — the polished Figma comes later.
        ink: "#1f2933",
        calm: "#3b6ea5",
        mist: "#f5f7fa",
      },
    },
  },
  plugins: [],
};
