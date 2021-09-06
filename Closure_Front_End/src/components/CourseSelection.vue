<template>
  <vue-multiselect
    :disabled="track == null"
    :modelValue="modelValue"
    @update:modelValue="newVal => $emit('update:modelValue', newVal)"
    placeholder="לא מוגדר קורס"
    :options="options"
    :searchable="true"
    :internal-search="false"
    @search-change="fetchCourses"
    :loading="loading"
    label="name"
    track-by="id"
  >
    <template #noOptions>
        יש להזין שם קורס
    </template>

    <template #noResult>
        לא נמצא מסלול עם השם הנ"ל
    </template>
  </vue-multiselect>
</template>

<script>
import VueMultiselect from "vue-multiselect";
import { reactive, toRefs, inject } from "vue";
export default {
  props: {
    modelValue: {
      type: Object,
    },
    track: {
      type: Object
    },
    year: {
        type: Number,
    }
  },
  emits: ["update:modelValue"],
  components: { VueMultiselect },
  setup(props) {
    const state = reactive({
      loading: false,
      options: [],
    });

    const http = inject("http");
    const fetchCourses = async (query) => {
      state.loading = true;
      const url = `tracks/${props.track?.id}/courses/?limit=6&offset=15&data_year=${props.track?.data_year}&search=${query}`;
      try {
        const response = await http.get(url);
        const results = response.data.results;
        state.options = results;
      } finally {
        state.loading = false;
      }
    };

    return { ...toRefs(state), fetchCourses };
  },
};
</script>

<style>
</style>