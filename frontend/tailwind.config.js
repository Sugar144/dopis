/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        // Colores de marca Dopis. El dueño (Jaime) pidió limitarse a beige + rojo
        // por ahora. Los tonos marrón/azul que aparecen en el PDF de marca se
        // ignoran salvo variaciones suaves de apoyo (borde, texto secundario).
        brand: {
          beige: '#f4f4e6', // beige extraído del PDF de marca
          red: '#ce412e', // rojo corporativo extraído del PDF de marca
          'red-dark': '#a8331f', // rojo más oscuro para hover/estados
          background: '#fbf9f0', // beige muy claro de fondo
          card: '#fffdf7', // tarjetas beige casi blanco
          text: '#2b241d', // texto oscuro legible
          'text-soft': '#6b6155', // texto secundario
          border: '#e8e0cd', // bordes suaves
        },
      },
    },
  },
  plugins: [],
}
