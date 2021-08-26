import { defineConfig } from 'vite'
import path from 'path'

import commonConfig from './vite-common.config.js'

// https://vitejs.dev/config/
export default defineConfig({
  ...commonConfig,
  build: {
    emptyOutDir: false,
    lib: {
      entry: path.resolve(__dirname, 'src/huji-import/course-scrape-entry.js'),
      name: 'course-scrape-prod',
      fileName: 'course-scrape-prod'
    },
  }
})
