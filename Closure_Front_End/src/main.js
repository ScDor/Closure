import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


import { setupAuth } from './auth'

let app = createApp(App).use(router)

function callbackRedirect(appState) {
  router.push(
    appState && appState.targetUrl
      ? appState.targetUrl
      : '/'
  );
}


const authConfig = {
  "domain": process.env.VUE_APP_AUTH0_DOMAIN,
  "client_id": process.env.VUE_APP_AUTH0_CLIENT_ID,
  "redirect_uri": process.env.VUE_APP_AUTH0_REDIRECT_URI,
  "cacheLocation": process.env.VUE_APP_AUTH0_CACHE_LOCATION || "localstorage"
}

setupAuth(authConfig, callbackRedirect).then((auth) => {
  app.use(auth).mount('#app')
})