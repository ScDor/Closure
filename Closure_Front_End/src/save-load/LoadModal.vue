<template>
  <div class="box" dir="rtl">
    <h1 class="title">טעינת תכנית לימודים</h1>

    <div v-if="coursePlans">
      <loadable-course-plan
        :plan="plan"
        v-for="plan in shownCoursePlans"
        :key="plan.id"
        @deletedPlan="handleDeletedPlan"
        @loadingPlan="handleLoadingPlan"
      />

      <div v-if="shownCoursePlans.length === 0">אין תכניות שמורות</div>
    </div>

    <div v-if="isValidating">
      טוען ...
      <progress class="progress is-small is-primary" max="100">15%</progress>
    </div>

    <div class="control">
      <button class="button is-link is-light" @click="$emit('close')">
        ביטול
      </button>
    </div>
  </div>
</template>

<script>
import { inject, computed, ref } from "vue";
import LoadableCoursePlan from "@/save-load/LoadableCoursePlan.vue";
import useSWRV from "swrv";

export default {
  components: { LoadableCoursePlan },
  emits: ["close"],
  setup(_props, { emit }) {
    console.log("LoadModal setup()");
    const http = inject("http");
    const fetcher = (key) => http.get(key).then((res) => res.data.course_plans);
    const {
      data: coursePlans,
      mutate,
      isValidating,
      error,
    } = useSWRV("/student/me/", fetcher);

    // used to hide deleted courses from the UI until the data is revalidated
    const deletedIds = ref(new Set());

    const shownCoursePlans = computed(() =>
      coursePlans.value.filter((plan) => !deletedIds.value.has(plan.id))
    );

    const handleDeletedPlan = async (deletedPlan) => {
      deletedIds.value.add(deletedPlan.id);
      await mutate();
      deletedIds.value.delete(deletedPlan.id);
    };

    const handleLoadingPlan = () => {
      emit("close");
    };

    return {
      coursePlans,
      shownCoursePlans,
      handleDeletedPlan,
      isValidating,
      error,
      handleLoadingPlan,
      deletedIds,
    };
  },
};
</script>

<style>
</style>