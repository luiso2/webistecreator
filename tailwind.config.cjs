/** @type {import('tailwindcss').Config} */
module.exports = {
  // Todos los demos usan el mismo CSS compartido. Al analizar sus HTML se incluyen solo
  // las utilidades usadas realmente, sin ejecutar el compilador de Tailwind en cada visita.
  content: [
    './output/*/index.html',
    './templates/**/*.html',
  ],
  theme: { extend: {} },
  plugins: [],
};
