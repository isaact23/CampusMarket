// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: './build',
    emptyOutDir: true
  },
  server: {
    host: '0.0.0.0',
    port: 443,
    proxy: {
      '/api': {
        target: 'http://backend:8080'
      }
    }
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
  }
})