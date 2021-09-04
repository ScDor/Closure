<template>
  <div class="card content">
    <header class="card-header">
      <p class="card-header-title">
        <strong>[{{ plan.id }}]</strong>&nbsp;
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
          <router-link
            class="button is-info"
            :to="{ name: 'Course Plan', params: { plan_id: plan.id } }"
            :disabled="deleting || undefined"
            @click="onLoadPlan"
          >
            טעינה
          </router-link>
        </p>
        <p class="control">
          <button
            class="button is-danger"
            :class="{ 'is-loading': deleting }"
            :disabled="deleting"
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
import router from "@/router";
import { deletePlan } from "@/course-store.js";
export default {
  props: {
    plan: Object,
  },
  emits: ["deletedPlan", "loadingPlan"],
  setup(props, { emit }) {
    const deleting = ref(false);
    const onDeleteClick = async () => {
      deleting.value = true;
      try {
        const { deletedOwnPlan } = await deletePlan(props.plan);
        emit("deletedPlan", props.plan);
        if (deletedOwnPlan) {
          router.push({
            name: "Course Plan",
            params: { plan_id: "unsaved" },
          });
        }
      } finally {
        deleting.value = false;
      }
    };

    const onLoadPlan = async () => {
      emit("loadingPlan");
    };

    return {
      onDeleteClick,
      deleting,
      onLoadPlan,
    };
  },
};
</script>

<style>
.field a.button[disabled] {
  pointer-events: none;
}
</style>