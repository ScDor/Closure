import { createApp } from 'vue'
import EmbeddedScrapeStatus from '@/huji-import/EmbeddedScrapeStatus.vue'
import { FRONTEND_ORIGIN } from './course-scrape-communication.js'

const containerId = "vue-container"

const SCRAPE_SCRIPT_MANIFEST_KEY = "src/huji-import/course-scrape-entry.js"

/**
 * Dynamically imports CSS needed for the scrape script by inspecting our frontend's manifest.json
 * This is a hack for using Vite in production mode(rollup) - when using dev mode(esBuild), it seems
 * like the JS code produced by Vite already loads the CSS
 */
function addCssFromManifest(manifest) {
  const cssPaths = new Set()

  const handledImportKeys = new Set();
  const remainingImportKeys = [SCRAPE_SCRIPT_MANIFEST_KEY]

  // traverse over all imports via BFS 
  while (remainingImportKeys.length > 0) {
    const manifestKey = remainingImportKeys.pop()
    if (handledImportKeys.has(manifestKey)) {
      continue;
    }
    console.log(`handling import ${manifestKey}`)
    handledImportKeys.add(manifestKey);
    if ("css" in manifest[manifestKey]) {
      for (const extraCss of Object.values(manifest[manifestKey]["css"])) {
        console.log(`\tfound css ${extraCss}`)
        cssPaths.add(extraCss)
      }
    }

    if ("imports" in manifest[manifestKey]) {
      for (const extraImportKey of Object.values(manifest[manifestKey]["imports"])) {
        if (handledImportKeys.has(extraImportKey)) {
          continue;
        }
        console.log(`\tfound import ${extraImportKey}`)
        remainingImportKeys.push(extraImportKey);
      }
    }
  }

  for (const cssPath of cssPaths) {
    const url = new URL(cssPath, FRONTEND_ORIGIN).toString();
    console.log(`adding CSS ${url}`);
    document
      .getElementsByTagName("head")[0]
      .insertAdjacentHTML(
        "beforeend",
        `<link rel="stylesheet" href="${url}" />`
      );
  }
}

/** Entry point to the bookmarklet, sets up the Vue UI, driving
 *  the rest of the process.
 */
async function setupApp() {
  if (window.vueApp) {
    window.vueApp.unmount()
  }
  const preexisting = document.getElementById(containerId)
  if (preexisting) {
    preexisting.remove()
  }
  if (!import.meta.env.DEV) {
    console.log(`adding CSS dynamically(prod mode)`)
    const manifest_req = await fetch(new URL('manifest.json', FRONTEND_ORIGIN))
    const manifest = await manifest_req.json()
    addCssFromManifest(manifest)
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