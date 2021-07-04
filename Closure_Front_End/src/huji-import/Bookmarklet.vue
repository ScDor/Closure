<template>
  <a :href="url" v-if="dev">
    לפיתוח בלבד - ייבוא נתונים מהאוניברסיטה
  </a>

  <a :href="url" v-if="!dev">
    ייבוא נתונים מהאוניברסיטה
  </a>
</template>

<script>

import scrapeScriptUrl from "./course-scrape-entry.js?url"

export default {
  setup() {
    if (import.meta.env.DEV) {
      const siteURL = import.meta.url
      const scrapeScriptFullURL = new URL(scrapeScriptUrl, siteURL)
      const hmrURL = new URL('/@vite/client', siteURL)
      console.log(`Generating bookmarklet for dev mode, scrape script: ${scrapeScriptFullURL}, hmr: ${hmrURL}`)

      const url = encodeURI(`javascript:(async function() {
        console.log('attaching scrape script and vite HMR client(dev)')
        await import('${hmrURL}')
        const { setupApp } = await import('${scrapeScriptFullURL}')
        setupApp()
      })();`)

      return {
        dev: true, url
      }
    } else {
      // TODO: rename `AUTH0_REDIRECT_URI' to something more informative
      const siteURL = import.meta.env.VITE_AUTH0_REDIRECT_URI
      const scrapeScriptFullURL = new URL("course-scrape-prod.js", siteURL)
      console.log(`Generating bookmarklet for production, scrape script: ${scrapeScriptFullURL}`)

      const url = encodeURI(`javascript:(async function() {
        console.log('attaching scrape script(production)')
        const { setupApp } = await import('${scrapeScriptFullURL}')
        setupApp()
      })();`)
      return {
        dev: false, url
      }
    }
  }
}
</script>

<style>
</style>