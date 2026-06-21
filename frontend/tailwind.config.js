/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0f172a", // slate-900
        card: "rgba(30, 41, 59, 0.7)", // slate-800 with opacity for glass
        cardborder: "rgba(148, 163, 184, 0.1)",
        primary: "#3b82f6", // blue-500
        secondary: "#8b5cf6", // violet-500
        accent: "#10b981", // emerald-500
        danger: "#ef4444", // red-500
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
