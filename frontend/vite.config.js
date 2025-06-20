import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'node:path'
import url from 'node:url'

const _dirname = path.dirname(url.fileURLToPath(import.meta.url))
// https://vite.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "@shared": resolve(_dirname, "./shared"),
    }
  },
  plugins: [vue()],
})
