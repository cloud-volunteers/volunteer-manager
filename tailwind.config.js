/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./static/*.css",
    "./templates/*.html",
    "./scripts/*.js"
  ],
  theme: {
    extend: {
      content: {
        'adjustments': 'url("./static/icons/24/outline/adjustments-vertical.svg")'
      }
    },
  },
  plugins: [],
}
