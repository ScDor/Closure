import createAuth0Client from '@auth0/auth0-spa-js'
import { computed, reactive, watchEffect } from 'vue'
import axios from 'axios'

// status codes
const badRequestStatusCode = 400;
const unauthorizedStatusCode = 401;
const notFoundErrorStatusCode = 404;
const serverErrorStatusCode = 500;


let client
const state = reactive({
  loading: true,
  isAuthenticated: false,
  user: {},
  popupOpen: false,
  error: null,
})

const errorState = reactive({
    errorMessage: "",
})

async function loginWithPopup() {
    state.popupOpen = true

    try {
        await client.loginWithPopup(0)
    } catch (e) {
        console.error(e)
    } finally {
        state.popupOpen = false
    }

    state.user = await client.getUser()
    state.isAuthenticated = true
}

async function handleRedirectCallback() {
    state.loading = true

    try {
        await client.handleRedirectCallback()
        state.user = await client.getUser()
        state.isAuthenticated = true
    } catch (e) {
        state.error = e
    } finally {
        state.loading = false
    }
}

function loginWithRedirect(o) {
  return client.loginWithRedirect(o)
}

function getIdTokenClaims(o) {
  return client.getIdTokenClaims(o)
}

function getTokenSilently(o) {
  return client.getTokenSilently(o)
}

function getTokenWithPopup(o) {
  return client.getTokenWithPopup(o)
}

function logout(o) {
  return client.logout(o)
}

function setErrorMessage(message) {
    errorState.errorMessage = message;
}

function errorHandler(error) {
  const statusCode = error.response ? error.response.status : null;
      if (statusCode === badRequestStatusCode){
        setErrorMessage("סטטוס 400: הבקשה שנשלחה איננה חוקית")
      }
      else if (statusCode === unauthorizedStatusCode){
        setErrorMessage("סטטוס 401: למשתמש אין הרשאות לבצע את הבקשה")
      }
      else if (statusCode === notFoundErrorStatusCode){
        setErrorMessage("סטטוס 404: ה- API המבוקש לא קיים")
      }
      else if (statusCode === serverErrorStatusCode){
        setErrorMessage("סטטוס 500: התרחשה תקלה בצד השרת בעת ביצוע הבקשה")
      }
      else if (statusCode < 200 || statusCode >= 300){
        setErrorMessage("התרחשה תקלה בעת ביצוע הבקשה")
      }
}

const authPlugin = {
  isAuthenticated: computed(() => state.isAuthenticated),
  loading: computed(() => state.loading),
  user: computed(() => state.user),
  getIdTokenClaims,
  getTokenSilently,
  getTokenWithPopup,
  handleRedirectCallback,
  loginWithRedirect,
  loginWithPopup,
  logout,
}

export const routeGuard = (to, from, next) => {
  const {isAuthenticated, loading, loginWithRedirect} = authPlugin

  const verify = () => {
      // If the user is authenticated, continue with the route
      if (isAuthenticated.value) {
          return next()
      }

      // Otherwise, log in
      loginWithRedirect({appState: {targetUrl: to.fullPath}})
  }

  // If loading has already finished, check our auth state using `fn()`
  if (!loading.value) {
      return verify()
  }

  // Watch for the loading property to change before we check isAuthenticated
  watchEffect(() => {
      if (loading.value === false) {
          return verify()
      }
  })
}

export const setupAuth = async (options, callbackRedirect) => {
  client = await createAuth0Client({
      ...options,
  });


  let http = axios.create({
      baseURL: import.meta.env.VITE_API_URL
  });

  http.interceptors.response.use((response) => response,
      function (error){
      errorHandler(error);
      return Promise.reject(error);
  });
  window.closureAxios = http;


  watchEffect(async () => {
      if (state.isAuthenticated) {
          const idTokenClaims = await client.getIdTokenClaims();
          if (!idTokenClaims) {
              console.error(`Client is authenticated but couldn't get ID token claims`)
              return;
          }
          const idToken = idTokenClaims.__raw;
          console.log(`Client is authenticated`)
          http.defaults.headers.common["Authorization"] = `Bearer ${idToken}`
      } else {
          console.log(`Client is not authenticated`)
          delete http.defaults.headers.common["Authorization"]
      }
  });

  try {
      // If the user is returning to the app after authentication


      if (
          window.location.search.includes('code=') &&
          window.location.search.includes('state=')
      ) {
          // handle the redirect and retrieve tokens
          const {appState} = await client.handleRedirectCallback()

          // Notify subscribers that the redirect callback has happened, passing the appState
          // (useful for retrieving any pre-authentication state)
          callbackRedirect(appState)
      }
  } catch (e) {
      state.error = e
  } finally {
      // Initialize our internal authentication state
      state.isAuthenticated = await client.isAuthenticated()
      state.user = await client.getUser()
      state.loading = false
  }

  return {
    install: (app) => {
      app.config.globalProperties.$auth = authPlugin
      app.config.globalProperties.$http = http
      app.provide("auth", authPlugin)
      app.provide("http", http)
      app.provide("errorState", errorState);
      app.provide("setErrorMessage", setErrorMessage);
    }
  }
}
