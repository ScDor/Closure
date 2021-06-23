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
      scrape_huji: {
          'entry': 'src/scraper/course-scrape.user.js',
          'chunks': []
          // 'template': 'public/course-scrape.user.html',
          // 'filename': 'course-scrape-user.html'
      }
  },
}