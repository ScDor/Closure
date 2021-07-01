<template>
  <!-- basically a menu, a (soon to be) analytics box, and the years themselves. -->
  <nav class="navbar has-shadow is-dark">
    <div class="navbar-brand">
      <router-link class="navbar-item" name="Home" to="/"
        ><b>Closure()</b></router-link
      >
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
  data() {
    return {
      track: null,
      allcourses: [
        {
          pk: 5837,
          course_id: 67315,
          name: "סדנת תכנות בשפות C ו- ++C",
          semester: 1,
          year: 2,
          points: 4,
          type: 1,
        },
        {
          pk: 7208,
          course_id: 80131,
          name: "חשבון אינפיניטסימלי (1)",
          semester: 1,
          year: 1,
          points: 7,
          type: 1,
        },
        {
          pk: 7209,
          course_id: 80132,
          name: "חשבון אינפיניטסימלי (2)",
          semester: 2,
          year: 1,
          points: 7,
          type: 1,
        },
        {
          pk: 7211,
          course_id: 80134,
          name: "אלגברה ליניארית (1)",
          semester: 1,
          year: 1,
          points: 6,
          type: 1,
        },
        {
          pk: 7212,
          course_id: 80135,
          name: "אלגברה ליניארית (2)",
          semester: 2,
          year: 1,
          points: 6,
          type: 1,
        },
        {
          pk: 7220,
          course_id: 80181,
          name: "מתמטיקה דיסקרטית",
          semester: 1,
          year: 1,
          points: 5,
          type: 1,
        },
        {
          pk: 5844,
          course_id: 67392,
          name: "מבוא לקריפטוגרפיה ואבטחת תוכנה",
          semester: 2,
          year: 2,
          points: 4,
          type: 2,
        },
        {
          pk: 5854,
          course_id: 67506,
          name: "מסדי נתונים",
          semester: 1,
          year: 3,
          points: 5,
          type: 2,
        },
        {
          pk: 5888,
          course_id: 67609,
          name: "גרפיקה ממוחשבת",
          semester: 1,
          year: 3,
          points: 5,
          type: 3,
        },
        {
          pk: 5951,
          course_id: 67829,
          name: "עיבוד ספרתי של תמונות",
          semester: "1",
          year: 3,
          points: 4,
          type: 2,
        },
        {
          pk: 5960,
          course_id: 67842,
          name: "מבוא לבינה מלאכותית",
          semester: "2",
          year: 3,
          points: 5,
          type: 2,
        },
      ],
    };
  },

  created() {
    /** if the user is loged in, then fetching his data from DB, else doing nothing */
  },

  methods: {
    // Log the user in
    login() {
      this.$auth.loginWithRedirect();
    },
    // Log the user out
    logout() {
      this.$auth.logout({
        returnTo: process.env.VUE_APP_AUTH0_REDIRECT_URI,
      });
    },
  },
};
</script>

<style>
.app {
  font-size: 0.75rem;
}
</style>