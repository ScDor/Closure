<template>
  <h2 class="subtitle is-2">הוספת קורסים</h2>
  <year-selection label="גרסת שנתון" v-model="selectedYear" />
  <div class="field">
    <label class="label">מסלול</label>
    <div class="control" dir="rtl">
      <multiselect
        placeholder="חיפוש מסלול"
        v-model="selectedTrack"
        searchable
        :delay="0"
        :minChars="1"
        :resolveOnLoad="false"
        :options="fetchTracks"
      />
    </div>
  </div>

  <div class="field">
    <label class="label">קורס</label>
    <div class="control" dir="rtl">
      <multiselect
        placeholder="חיפוש קורס"
        searchable
        @update:modelValue="selectCourse"
        :disabled="!selectedTrack"
        :delay="0"
        :minChars="1"
        :resolveOnLoad="false"
        :options="fetchCourses"
      />
    </div>
  </div>
</template>

<script>
import YearSelection from './YearSelection.vue'
import Multiselect from '@vueform/multiselect';
import { fetchDjangoListIntoSelectOptions } from '@/utils.js';

export default {
  components: { YearSelection, Multiselect },
  data() {
    return {
      "selectedYear": 2022,
      "selectedTrack": null,
      "value": null
    }
  },
  props: ["allcourses"],
  inject: ["http", "selectCourse"],
  methods: {
    emitCourseClick(course) {
      this.$emit("clickCourse", course);
    },
    async fetchTracks(query) {
      const url = `tracks/?limit=6&offset=15&data_year=${this.selectedYear}&search=${query}`;
      return await fetchDjangoListIntoSelectOptions(this.http, url, track => track.name);
    },
    async fetchCourses(query) {
      const url = `tracks/${this.selectedTrack?.pk ?? 'null'}/courses/?limit=6&offset=15&data_year=${this.selectedYear}&search=${query}`;
      return await fetchDjangoListIntoSelectOptions(this.http, url, course => course.name);
    },
  }
};
</script>
<style src="@vueform/multiselect/themes/default.css"></style>