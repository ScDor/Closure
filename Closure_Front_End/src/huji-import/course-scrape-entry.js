import { createApp } from 'vue'
import EmbeddedScrapeStatus from '@/huji-import/EmbeddedScrapeStatus.vue'


const containerId = "vue-container"

/** Entry point to the bookmarklet, sets up the Vue UI, driving
 *  the rest of the process.
 */
export function setupApp() {
  const preexisting = document.getElementById(containerId)
  if (preexisting) {
    preexisting.remove()
  }
  const div = document.createElement("div")
  div.id = containerId
  document.body.prepend(div)
  console.log("setting up ui")
  const app = createApp(EmbeddedScrapeStatus).mount(`#${containerId}`)
  window.app = app
  console.log(`ui is set`)
}