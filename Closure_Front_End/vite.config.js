import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import eslint from '@rollup/plugin-eslint'
import path from 'path'

const entryFileNameNamingRule = (chunkInfo) => {
  if (chunkInfo.name === "course-scrape-prod") {
    return "course-scrape-prod.js"
  }
  return "[name].hash-[hash].js"
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), { ...eslint({
    include: '**/*.+(vue|js|jsx|ts|tsx)'
  }), enforce: 'pre', apply: 'build'}],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    port: 8080,
    strictPort: true,
    hmr: {
      protocol: "ws", host: "localhost", port:8080
    }
  },
  build: {
    manifest: true,
    sourcemap: true,
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'index.html'),
        "course-scrape-prod": path.resolve(__dirname, 'src/huji-import/course-scrape-entry.js')
      },
      output: {
        entryFileNames: entryFileNameNamingRule,
        chunkFileNames: "[name].hash-[hash].js",
        assetFileNames: "assets/[name].hash-[hash].[ext]"
      }
    }
  }
})
