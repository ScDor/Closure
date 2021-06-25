<template>
  <!-- basically a menu, a (soon to be) analytics box, and the years themselves. -->
  <nav class="navbar has-shadow is-dark">
    <div class="navbar-brand">
      <router-link class="navbar-item" to="/"><b>Closure()</b></router-link>
    </div>
    <div class="navbar-start is-hidden-mobile is-hidden-touch">
      <div class="navbar-item">
        <div class="buttons">
          <!-- Check that the SDK client is not currently loading before accessing is methods -->
          <router-link
            v-if="$auth.isAuthenticated.value"
            class="button is-small is-dark"
            to="/settings"
          >
            <span class="icon is-small is-right">
              <i class="fas fa-user-cog"></i>
            </span>
          </router-link>
          <div v-if="!$auth.loading.value">
            <button
              class="button is-small is-dark menu-label"
              v-if="!$auth.isAuthenticated.value"
              @click="login"
            >
              Log in
            </button>
            <button
              class="button is-small is-dark menu-label"
              v-if="$auth.isAuthenticated.value"
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
import axios from "axios";

export default {
  name: "App",

  data() {
    return {
      username: "",
      student: null,
    };
  },

  created() {
    /** if the user is loged in, then fetching his data from DB, else doing nothing */
    if (this.$auth.isAuthenticated.value) {
      this.$auth
        .getIdTokenClaims()
        .then((response) => (this.username = response.nickname));

      axios
        .get("http://127.0.0.1:8000/api/v1/students/" + this.username, {
          headers: {
            Authorization: "Token 0782d1d5118827d8f32cdeaddde60a8bb53d7625",
          },
        })
        .then((response) => this.student = response);
    }
  },

  methods: {
    // Log the user in
    login() {
      this.$auth.loginWithRedirect();
    },
    // Log the user out
    logout() {
      this.$auth.logout({
        returnTo: process.env.VUE_APP_AUTH0_REDIRECT_URI
      });
    },
  },
};
</script>
