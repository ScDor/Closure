import vue from '@vitejs/plugin-vue'
import eslint from '@rollup/plugin-eslint'
import path from 'path'

/** @type{import('vite').UserConfigExport} */
const commonConfig = {
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
}

export default commonConfig
