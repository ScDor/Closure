<template>
  <p class="menu-label">ניווט</p>

  <div class="control has-icons-right">
    <input
      class="input is-dark"
      type="course"
      placeholder="חפש קורס"
      v-model="query"
      @keyup="searchCourses"
      @keydown="showSearch"
    />

    <span class="icon is-small is-right is-size-7">
      <i class="fas fa-search"></i>
    </span>
  </div>

  <div class="dropdown is-active" :class="{ hide: hide }">
    <div class="dropdown-menu">
      <div class="dropdown-content">
        <li
          class="dropdown-item"
          v-for="course in suggestions"
          :key="course"
          @click="emitClick($event, course)"
        >
          {{ course.name }}
        </li>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";

export default {
  emits: ["clickcourse"],

  data() {
    return {
      hide: true,
      query: "",
      suggestions: [],
    };
  },

  methods: {
    searchCourses() {
      axios
        .get(
          "http://127.0.0.1:8000/api/v1/courses/?limit=6&offset=15&search=" +
            this.query,
          {
            headers: {
              Authorization: "Token 425fa39de10f02351c7043d0dbe34a4b31be7a27",
            },
          }
        )
        .then((response) => (this.suggestions = response.data.results))
        .then((this.hide = !this.suggestions.length || this.query == ""));
    },

    emitClick(event, course) {
      this.hide = true;
      this.query = "";
      this.$emit("clickcourse", event, course);
    },
  },
};
</script>


<style>
.input {
  min-width: 15.5vw;
  padding: 0.25rem;
  margin-right: 0.2rem;
  font-size: 0.75rem;
}

.span {
  font-size: 0.75rem;
}

.dropdown-menu {
  min-width: 15.5vw;
  margin-right: 0.2rem;
}

.dropdown-content {
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
}

.hide {
  display: none;
}

.dropdown-item {
  font-size: 0.75rem;
}

.dropdown-item:hover {
  background: #efefef;
  cursor: pointer;
}
</style>