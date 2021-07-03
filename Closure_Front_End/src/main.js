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
  "domain": import.meta.env.VITE_AUTH0_DOMAIN,
  "client_id": import.meta.env.VITE_AUTH0_CLIENT_ID,
  "redirect_uri": import.meta.env.VITE_AUTH0_REDIRECT_URI,
  "cacheLocation": import.meta.env.VITE_AUTH0_CACHE_LOCATION || "localstorage"
}

setupAuth(authConfig, callbackRedirect).then((auth) => {
  app.use(auth).mount('#app')
})