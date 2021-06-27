  <!-- we will bind every key movement to the searchCourses method so it will update immediately -->
<template>
  <search-bar
    :placeholder="'חפש מסלול'"
    :url="'tracks/?limit=6&offset=15&search='"
    @clicksuggestion="emitTrackClick"
  ></search-bar>

  <search-bar
    :placeholder="'חפש קורס'"
    :url="'courses/?limit=6&offset=15&search='"
    @clicksuggestion="emitCourseClick"
  ></search-bar>

  
  <ProgressBox :allcourses = "allcourses"/>
</template>

<script>
import SearchBar from "./SearchBar.vue";
import ProgressBox from "./ProgressBox.vue";

export default {
  components: { SearchBar, ProgressBox },
  emits: ["clickcourse"],
  props: ["allcourses"],

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