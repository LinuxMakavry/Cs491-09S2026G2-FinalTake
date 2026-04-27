import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setupTests.js"],
    css : false,
},
  server: {
    port: 5173,
    proxy: {
  '/api': {
    target: 'http://localhost:5000',
    changeOrigin: true,
  },
  '/auth': {
    target: 'http://localhost:5000',
    changeOrigin: true,
      }
    }
  }
})

/*
SOURCES / TEMPLATES USED:
- Vitest docs: `defineConfig`, `test.environment = jsdom`, `setupFiles`
- Vite React plugin docs: include `@vitejs/plugin-react` in config for JSX handling in tests
*/
