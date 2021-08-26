module.exports = {
  presets: ['@babel/preset-env'],
  plugins: ['babel-plugin-transform-vite-meta-env'],
  env: {
    test: {
      plugins: ['@babel/plugin-transform-runtime']
    }
  }
}