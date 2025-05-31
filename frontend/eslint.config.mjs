// frontend/eslint.config.mjs
import nextPlugin from "@next/eslint-plugin-next";
import typescriptEslintParser from "@typescript-eslint/parser";
import typescriptEslintPlugin from "@typescript-eslint/eslint-plugin";
import globals from "globals";

/** @type {import('eslint').Linter.FlatConfig[]} */
const eslintConfig = [
  {
    files: ["**/*.{js,mjs,cjs,ts,tsx}"],
    languageOptions: {
      parser: typescriptEslintParser,
      parserOptions: {
        ecmaFeatures: { jsx: true },
        ecmaVersion: "latest",
        sourceType: "module",
        project: "./tsconfig.json", // Asegúrate que tsconfig.json existe en /app
      },
      globals: {
        ...globals.browser,
        ...globals.node,
        React: "readonly",
        // NO AÑADIR "AudioWorkletGlobalScope" todavía
      }
    },
    plugins: {
      "@next/next": nextPlugin,
      "@typescript-eslint": typescriptEslintPlugin,
      // 'react' es implícitamente manejado por nextPlugin o puedes añadirlo si es necesario
    },
    rules: {
      // Reglas de Next.js (incluye React y core-web-vitals)
      ...nextPlugin.configs.recommended.rules,
      ...nextPlugin.configs["core-web-vitals"].rules,
      // Reglas de TypeScript
      ...typescriptEslintPlugin.configs["eslint-recommended"].rules, // anula eslint base
      ...typescriptEslintPlugin.configs.recommended.rules,
      // Tus personalizaciones (puedes añadir más tarde si esto funciona)
      "react/react-in-jsx-scope": "off", // No necesario con React 17+ y Next.js
      "react/prop-types": "off", // No necesario con TypeScript
      "@typescript-eslint/no-unused-vars": ["warn", { "argsIgnorePattern": "^_" }],
      "@typescript-eslint/no-explicit-any": "warn",
    },
    settings: {
      react: {
        version: "detect",
      },
    },
  }
];

export default eslintConfig;