/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "*.html",
    "./templates/*.html",
    "./scripts/*.js"
  ],
  theme: {
    extend: {
      content: {
        'adjustments': 'url("icons/24/outline/adjustments-vertical.svg")'
      },
      backgroundImage: {
        'gradient-dark': 'radial-gradient(ellipse at top, rgb(71 85 105), transparent), radial-gradient(ellipse at bottom, rgb(100 116 139), transparent)'
      }
    },
  },
  plugins: [],
}
