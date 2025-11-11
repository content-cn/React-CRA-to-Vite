
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { viteCommonjs } from '@originjs/vite-plugin-commonjs';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), viteCommonjs()],
  test: {
    environment: "jsdom",
    globals: true,           
  },
    resolve: {
    alias: {
      // make @ point to /src
      '@': path.resolve(__dirname, 'src'),
    },
  },
})
