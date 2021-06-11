<template>
<<<<<<< HEAD
  <search-bar
    :placeholder="'חפש מסלול'"
    :url="'http://127.0.0.1:8000/api/v1/tracks/?limit=6&offset=15&search='"
    @clicksuggestion="emitTrackClick"
  ></search-bar>
  
  <search-bar
    :placeholder="'חפש קורס'"
    :url="'http://127.0.0.1:8000/api/v1/courses/?limit=6&offset=15&search='"
    @clicksuggestion="emitCourseClick"
  ></search-bar>
=======
  <p class="menu-label">ניווט</p>


  <!-- we will bind every key movement to the searchCourses method so it will update immediately -->
  
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
>>>>>>> 5620cb40eb36a01157f969530b506e157d430407
</template>

<script>
import SearchBar from "./SearchBar.vue";

export default {
  components: { SearchBar },
  emits: ["clickcourse"],

  methods: {
<<<<<<< HEAD
    emitCourseClick(event, course) {
      this.$emit("clickcourse", event, course);
    },

    emitTrackClick(event, track) {
      this.$emit("clicktrack", event, track);
    },
  },
};
</script>
=======
  
    /**
    * this method uses the axios package to access our local database, and search
    * courses according to the given query.
    * notice that the drop down menu is hidden unless there are actual restults for the search.
    * more on the implementation of the search on the backend part of the project.
    */
    
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

    /**
    * once a course is clicked, we need to transfer it's information up the component tree
    * so the app could create a new coursebox for it
    */
    
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
>>>>>>> 5620cb40eb36a01157f969530b506e157d430407
