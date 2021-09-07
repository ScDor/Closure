<template>
  <course-plan-settings />
  <h2 class="subtitle is-2">הוספת קורסים</h2>
  <year-selection label="גרסת שנתון" v-model="selectedYear" />
  <div class="field">
    <label class="label">מסלול</label>
    <div class="control">
      <track-selection v-model="selectedTrack" :year="selectedYear" />
    </div>
  </div>

  <div class="field">
    <label class="label">קורס</label>
    <div class="control">
      <course-selection @update:modelValue="course => $emit('clickCourse', course)" :track="selectedTrack"  />
    </div>
  </div>
</template>

<script>
import YearSelection from './YearSelection.vue'
import TrackSelection from './TrackSelection.vue'
import CourseSelection from './CourseSelection.vue'
import CoursePlanSettings from './CoursePlanSettings.vue'
import { reactive, toRefs } from "vue";
export default {
  components: { YearSelection, TrackSelection, CourseSelection, CoursePlanSettings },
  emits: [ "clickCourse"],
  setup() {
    const data = reactive({
      selectedYear: 2022,
      selectedTrack: null
    })

    return { ...toRefs(data) }
  }
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.css"></style>