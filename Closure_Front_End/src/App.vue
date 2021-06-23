<template>
  <!-- basically a menu, a (soon to be) analytics box, and the years themselves. -->
  <nav class="navbar has-shadow is-dark" v-if="!$route.meta.hideNavbar">
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
export default {
  name: "App",

  methods: {
    // Log the user in
    login() {
      this.$auth.loginWithRedirect();
    },
    // Log the user out
    logout() {
      this.$auth.logout({
        returnTo: window.location.origin,
      });
    },
  },
};
</script>
