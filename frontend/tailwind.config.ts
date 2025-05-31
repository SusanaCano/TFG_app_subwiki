// tailwind.config.js

import type { Config } from "tailwindcss";
import { fontFamily } from 'tailwindcss/defaultTheme';

const config: Config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}", 
  ],
  theme: {
    extend: {
      // Fuentes personalizadas (Geist)
      fontFamily: {
        // Sobrescribe la fuente sans-serif por defecto de Tailwind
        sans: ['var(--font-geist-sans)', ...fontFamily.sans],
        // Sobrescribe la fuente monoespaciada por defecto de Tailwind
        mono: ['var(--font-geist-mono)', ...fontFamily.mono],
      },
      // Colores personalizados usando variables CSS (como ya tienes)
      colors: {
        // Estos nombres 'background' y 'foreground' son buenos y descriptivos.
        // Ahora puedes usarlos en tus clases de Tailwind: bg-background, text-foreground
        background: "var(--background)", // Mapea a --background definido en tu CSS
        foreground: "var(--foreground)", // Mapea a --foreground definido en tu CSS

        // Ejemplo de añadir más colores personalizados si los necesitas:
        // primary: {
        //   DEFAULT: 'var(--primary-color)',
        //   hover: 'var(--primary-color-hover)',
        // },
        // accent: 'var(--accent-color)',
      },
      // Puedes extender otras propiedades aquí si es necesario
      // مثلاً: spacing, borderRadius, keyframes para animaciones, etc.
      // keyframes: {
      //   fadeIn: {
      //     '0%': { opacity: '0' },
      //     '100%': { opacity: '1' },
      //   },
      // },
      // animation: {
      //   fadeIn: 'fadeIn 1s ease-in-out',
      // },
    },
  },
  plugins: [
    // Aquí puedes añadir plugins de Tailwind si los usas, por ejemplo:
    // require('@tailwindcss/typography'),
    // require('@tailwindcss/forms'),
    // require('tailwindcss-animate'), // Para animaciones complejas
  ],
};


export default config;