/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "*.html",
    "scripts/*.js"
  ],
  theme: {
    extend: {
      content: {
        'adjustments': 'url("src/24/outline/adjustments-vertical.svg")'
      }
    },
  },
  plugins: [],
}
