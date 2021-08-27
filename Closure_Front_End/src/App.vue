<template>
  <!-- basically a menu, a (soon to be) analytics box, and the years themselves. -->
  <error-notification/>
  <nav class="navbar has-shadow is-dark">
    <div class="navbar-brand">
      <router-link class="navbar-item" to="/"><b>Closure()</b></router-link>
    </div>
    <div class="navbar-start is-hidden-mobile is-hidden-touch">
      <div class="navbar-item">
        <div class="buttons">
          <router-link
            v-if="auth.isAuthenticated.value"
            class="button is-small is-dark"
            to="/data-import"
          >
            <span> 
              <i class="fas fa-upload"></i>
              ייבוא נתונים מהאוניברסיטה
            </span>
          </router-link>
          <!-- Check that the SDK client is not currently loading before accessing is methods -->
          <router-link
            v-if="auth.isAuthenticated.value"
            class="button is-small is-dark"
            to="/settings"
          >
            <span class="icon is-small is-right">
              <i class="fas fa-user-cog"></i>
            </span>
          </router-link>
          <div v-if="!auth.loading.value">
            <button
              class="button is-small is-dark menu-label"
              v-if="!auth.isAuthenticated.value"
              @click="login"
            >
              Log in
            </button>
            <button
              class="button is-small is-dark menu-label"
              v-if="auth.isAuthenticated.value"
              @click="logout"
            >
              Log out
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <router-view />
</template>

<script>
import ErrorNotification from './components/ErrorNotification.vue';

import { toRefs, reactive, onMounted, provide, inject, readonly } from 'vue';
export default {
  name: "App",
  components: {ErrorNotification},
  setup() {
    const state = reactive({
      student: null,
      idClaims: null
    });

    provide("studentAndClaims", readonly(state))
    provide("setStudent", (newStudent) => {
      state.student = newStudent;
    });


    const http = inject("http");
    const auth = inject("auth");


    onMounted(async () => {
      if (auth.isAuthenticated.value) {
        const claims = await auth.getIdTokenClaims();
        const student = (await http.get("student/me")).data;
        window.student = student;
        window.claims = claims;

        state.idClaims = claims;
        state.student = student;

        console.log(`Authenticated, got claims and student profile`)
      }
    });

    const login = () => auth.loginWithRedirect();
    const logout = () => auth.logout({
        returnTo: import.meta.env.VITE_AUTH0_REDIRECT_URI
    });

    return {
      ...toRefs(state), login, logout, auth
    }

  }
};
</script>
<style src="bulma/css/bulma-rtl.css"></style>