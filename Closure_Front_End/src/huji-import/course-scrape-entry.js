import { createApp } from 'vue'
import EmbeddedScrapeStatus from '@/huji-import/EmbeddedScrapeStatus.vue'
const containerId = "vue-container"

/** Entry point to the bookmarklet, sets up the Vue UI, driving
 *  the rest of the process.
 */
function setupApp() {
  if (window.vueApp) {
    window.vueApp.unmount()
  }
  const preexisting = document.getElementById(containerId)
  if (preexisting) {
    preexisting.remove()
  }
  console.log("setting up ui")
  const div = document.createElement("div")
  div.id = containerId
  document.body.prepend(div)
  window.vueApp = createApp(EmbeddedScrapeStatus)
  window.vueApp.mount(`#${containerId}`)
  console.log(`ui is set`)
}

setupApp()