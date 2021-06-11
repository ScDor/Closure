<template>
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
</template>

<script>
import SearchBar from "./SearchBar.vue";

export default {
  components: { SearchBar },
  emits: ["clickcourse"],

  methods: {
    emitCourseClick(event, course) {
      this.$emit("clickcourse", event, course);
    },

    emitTrackClick(event, track) {
      this.$emit("clicktrack", event, track);
    },
  },
};
</script>