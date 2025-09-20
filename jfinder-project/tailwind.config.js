module.exports = {
  content: ["./static/**/*.{html,js,css}", "./templates/**/*.{html,js,css}"],
  theme: {
    extend: {},
  },
  plugins: [
    require("./static/css/daisyui.js"), // your custom plugin
  ],
};