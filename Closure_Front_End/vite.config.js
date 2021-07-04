import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import eslint from '@rollup/plugin-eslint';
import path from 'path'


/** This function is used to determine the file-name of the production assets entry-points.
 *
 *  By default, every asset except `index.html` is concatenated with a hash, which is useful for caching.
 *  However, for the scrape script, we would like to have a constant path which we can reference when
 *  generating the bookmarklet URL at build-time.
 *
 *  @type {(chunkInfo: import('rollup').PreRenderedChunk) => string }
**/
const entryFileNameNamingRule = (chunkInfo) => {
  if (chunkInfo.name === "course-scrape-prod") {
    return "course-scrape-prod.js"
  }
  return "[name].[hash].js"
}


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), { ...eslint({
    include: '**/*.+(vue|js|jsx|ts|tsx)'
  }), enforce: 'pre', apply: 'build'}],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, '/src')
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
