<template>
  <div class="card content">
    <header class="card-header">
      <p class="card-header-title">
        <bold>[{{ plan.id }}]</bold>&nbsp;
        {{ plan.name }}
      </p>
    </header>

    <div class="card-content">
      <div v-if="!plan.track">לא מוגדר מסלול</div>
      <div v-if="plan.track">מסלול: {{ plan.track_name }}</div>

      <div class="level">
        <div class="level-left">
          שינוי אחרון:
          {{ new Date(plan.modified_at).toLocaleString() }}
        </div>
        <div class="level-right">
          נוצר ב:
          {{ new Date(plan.created_at).toLocaleString() }}
        </div>
      </div>

      <div class="field is-grouped">
        <p class="control">
          <button
            class="button is-link"
            :class="{ 'is-loading': loading }"
            :disabled="deleting || loading"
            @click="onLoadPlan"
          >
            טעינה
          </button>
        </p>
        <p class="control">
          <button
            class="button is-danger"
            :class="{ 'is-loading': deleting }"
            :disabled="deleting || loading"
            @click="onDeleteClick"
          >
            מחיקה
          </button>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { deletePlan, loadPlan } from "@/course-store.js";
export default {
  props: {
    plan: Object,
  },
  emits: ["deletedPlan", "loadedPlan"],
  setup(props, { emit }) {
    const deleting = ref(false);
    const loading = ref(false);
    const onDeleteClick = async () => {
      deleting.value = true;
      try {
        await deletePlan(props.plan);
        emit("deletedPlan", props.plan);
      } finally {
        deleting.value = false;
      }
    };

    const onLoadPlan = async () => {
      loading.value = true
      try {
        const fullPlan = await loadPlan(props.plan.id)
        emit("loadedPlan", fullPlan);
      } finally {
        loading.value = false;
      }
    };

    return {
      onDeleteClick,
      deleting,
      onLoadPlan,
      loading
    };
  },
};
</script>

<style>
</style>