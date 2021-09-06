<template>
  <p class="subtitle is-3">הגדרות תכנית לימודים</p>
  <div class="field">
    <year-selection label="שנת תחילת לימודים" v-model="selectedYear" />
  </div>
  <div class="field">
    <label class="label">מסלול לימודים</label>
    <div class="control">
      <track-selection v-model="selectedTrack" :year="selectedYear" />
    </div>
  </div>
</template>

<script>
import YearSelection from "./YearSelection.vue";
import TrackSelection from "./TrackSelection.vue";
import { currentTrack, setTrack } from "@/course-store.js";
import { reactive, toRefs, computed, watch } from "vue";

export default {
  components: { YearSelection, TrackSelection },
  setup() {
    console.log("setup tracksettings");
    const state = reactive({
      selectedYear: currentTrack.value?.data_year,
      loading: false,
      saving: false,
    });

    const selectedTrack = computed({
      get() {
        return currentTrack.value;
      },
      set(newVal) {
        setTrack(newVal);
      },
    });

    watch(
      () => state.selectedYear,
      (newYear, oldYear) => {
        if (newYear !== oldYear) {
          selectedTrack.value = null;
        }
      }
    );

    return { ...toRefs(state), selectedTrack };
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.css">
</style>