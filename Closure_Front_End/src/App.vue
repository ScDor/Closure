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
import ErrorNotification from './components/ErrorNotification.vue';
export default {
  name: "App",
  components: {ErrorNotification},
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
      this.$http.get(`students/${this.username}`)
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
        returnTo: import.meta.env.VITE_AUTH0_REDIRECT_URI
      });
    },
  },
};
</script>
<style>
@import "bulma/css/bulma-rtl.css";
</style>