import { defineConfig } from 'vite'
import path from 'path'
import commonConfig from './vite-common.config.js'

const entryFileNameNamingRule = (chunkInfo) => {
  if (chunkInfo.name === "course-scrape-prod") {
    return "course-scrape-prod.js"
  }
  return "[name].[hash].js"
}

// https://vitejs.dev/config/
export default defineConfig({
  ...commonConfig,
  build: {
    manifest: true,
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'index.html'),
        "course-scrape-prod": path.resolve(__dirname, 'src/huji-import/course-scrape-entry.js')
      },
      output: {
        entryFileNames: entryFileNameNamingRule
      }
    }
  }
})
