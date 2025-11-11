/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './templates/*.html',
    './static/src/**/*.{js,ts,jsx,tsx}',
    './templates/registration/login.html',
    "../templates/**/*.html", 
    "../../templates/**/*.html", 
    "./**/*.html", 
    "./**/templates/**/*.html",
    "./**/*.py",
    "./static/js/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
