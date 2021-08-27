  <!-- we will bind every key movement to the searchCourses method so it will update immediately -->
<template>
  <year-selection label="גרסת שנתון" v-model="selectedYear" />
  <search-bar
    placeholder="חיפוש מסלול"
    :url="`tracks/?limit=6&offset=15&data_year=${selectedYear}&search=`"
    v-model="selectedTrack"
    :resultToString="track => track.name"
  ></search-bar>

  <search-bar
    placeholder="חיפוש קורס"
    :url="`tracks/${selectedTrack?.pk ?? 'null'}/courses/?limit=6&offset=15&data_year=${selectedYear}&search=`"
    @update:modelValue="emitCourseClick"
    :resultToString="course => course.name"
    :clearOnSelect="true"
    :disabled="!selectedTrack"
  ></search-bar>

  
  <ProgressBox :allcourses = "allcourses"/>
</template>

<script>
import YearSelection from './YearSelection.vue'
import SearchBar from "./SearchBar.vue";
import ProgressBox from "./ProgressBox.vue";

export default {
  components: { YearSelection, SearchBar, ProgressBox },
  data() {
    return {
      "selectedYear": 2022,
      "selectedTrack": null
    }
  },
  emits: ["clickCourse"],
  props: ["allcourses"],

  methods: {
    emitCourseClick(course) {
      this.$emit("clickCourse", course);
    },
  },
};
</script>