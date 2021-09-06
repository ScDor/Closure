<template>
  <vue-multiselect
    :disabled="year == null"
    :modelValue="modelValue"
    @update:modelValue="newVal => $emit('update:modelValue', newVal)"
    placeholder="לא מוגדר מסלול"
    :options="options"
    :searchable="true"
    :internal-search="false"
    @search-change="fetchTracks"
    :loading="loading"
    label="name"
    track-by="id"
  >
    <template #noOptions>
        יש להזין שם מסלול
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
    const fetchTracks = async (query) => {
      state.loading = true;
      const url = `tracks/?limit=10&data_year=${props.year}&search=${query}`;
      try {
        const response = await http.get(url);
        const results = response.data.results;
        state.options = results;
      } finally {
        state.loading = false;
      }
    };

    return { ...toRefs(state), fetchTracks };
  },
};
</script>

<style>
</style>