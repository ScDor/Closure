<template>
  <p class="subtitle is-3">הגדרות תכנית לימודים</p>
  <div class="field">
    <year-selection label="שנת תחילת לימודים" v-model="selectedYear" />
  </div>
  <div class="field">
    <label class="label">מסלול לימודים</label>
    <div class="control" dir="rtl">
      <multiselect
        placeholder="חיפוש מסלול"
        class="is-loading"
        v-model="selectedTrack"
        searchable
        :delay="0"
        :minChars="1"
        :resolveOnLoad="false"
        :options="fetchTracks"
      />
    </div>
  </div>

</template>

<script>
import YearSelection from "./YearSelection.vue";
import Multiselect from "@vueform/multiselect";
import { fetchDjangoListIntoSelectOptions } from "@/utils.js";
import { currentTrack, setTrack } from "@/course-store.js";
import { reactive, toRefs, inject, computed } from "vue";

export default {
  components: { YearSelection, Multiselect },
  setup() {
    console.log("setup tracksettings");
    const state = reactive({
      selectedYear: 2022,
      saving: false,
    });

    const http = inject("http");
    const fetchTracks = async (query) => {
      const url = `tracks/?limit=10&data_year=${state.selectedYear}&search=${query}`;
      return await fetchDjangoListIntoSelectOptions(
        http,
        url,
        (track) => track.name
      );
    };

    const selectedTrack = computed({
      get() { return currentTrack },
      set(newVal) { setTrack(newVal) }
    })

    return { ...toRefs(state), selectedTrack, fetchTracks };
  },
};
</script>

<style src="@vueform/multiselect/themes/default.css">
</style>