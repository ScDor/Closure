<template>
  <div>
    <section class="section-style">
      <user :username="name"></user>
    </section>
  </div>
</template>

<script>
import User from "../components/User.vue";

export default {
  name: "Closure()",
  components: { User },
  data() {
    return {
      username: "",
      name: "placeholder",
    };
  },
  created() {
    if (this.$auth.isAuthenticated.value) {
      this.$auth.getIdTokenClaims().then((response) => this.name = response.nickname);

    //   this.username = this.$auth
    //     .getIdTokenClaims()
    //     .then((response) => JSON.json(response));
    //   this.name = this.$auth
    //     .getIdTokenClaims()
    //     .then((response) => response.name);
    //   console.log(this.username);

      /**get username */
      //   axios
      //     .get("http://127.0.0.1:8000/api/v1/tracks/?track_number=3010", {
      //       headers: {
      //         Authorization: "Token 425fa39de10f02351c7043d0dbe34a4b31be7a27",
      //       },
      //     })
      //     .then((response) => (this.track = response.data.results[0]));
    }
  },
};
</script>

<style>
.section-style {
  padding: 0.5rem;
}
</style>