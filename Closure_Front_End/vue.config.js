/**
 * @type {import('@vue/cli-service').ProjectOptions}
 */
module.exports = {  
  publicPath: process.env.PUBLIC_PATH,
  pages: {
      index: {
          'entry': 'src/main.js',
          'template': 'public/index.html',
          'filename': 'index.html'
      },
      scrape_iframe: {
          'entry': 'src/course-scrape-iframe.js',
          'template': 'public/course-scrape-iframe.html',
          'filename': 'course-scrape-iframe.html'
      }
  }
}
