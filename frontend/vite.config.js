import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/loginAPI': {
        target: 'https://dev-wwzvhvto6t4diopr.us.auth0.com',
        changeOrigin: true,
        secure: true
      }
    }
  }
})
