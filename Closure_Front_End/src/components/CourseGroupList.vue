<template>
  <div class="dropdown is-dark is-active">
    <div class="dropdown-trigger">
      <button class="button" aria-haspopup="true" aria-controls="dropdown-menu">
        <!-- icon -->
        <span class="icon is-small is-right is-size-7">
          <i class="fas fa-circle" :class="type"></i>
        </span>

        <span>{{ type }}</span>

        <span class="icon is-small">
          <i class="fas fa-angle-down" aria-hidden="true"></i>
        </span>
      </button>
    </div>
    <div class="dropdown-menu" :class="{ hidden: hidden }">
      <div class="dropdown-content">
        <li
          class="dropdown-item"
          v-for="sugg in getCourses"
          :key="sugg"
          @click="emitClick($event, sugg)"
        >
          {{ sugg.name }}
        </li>
      </div>
    </div>
  </div>
</template>

<script>
// import axios from "axios";

export default {
  props: ["type", "url"],
  emits: ["clicksuggestion"],

  data() {
    return {
      hidden: false,
      suggestions: [],
    };
  },

  methods: {
    /** get all courses in this course group */
    getCourses() {
      //   axios
      //     .get(this.url + this.query, {
      //       headers: {
      //         Authorization: "Token 0782d1d5118827d8f32cdeaddde60a8bb53d7625",
      //       },
      //     })
      //     .then((response) => (this.suggestions = response.data.results));
      return [1];
    },

    emitClick(event, sugg) {
      this.hide = true;
      this.$emit("clicksuggestion", event, sugg);
    },
  },
};
</script>

<style>
.hidden {
    display: none;
}
</style>