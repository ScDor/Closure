<template>
  <div class="box" dir="rtl">
    <h1 class="title">שמירת תכנית לימודים</h1>
    <div class="field">
      <label class="label">שם תכנית</label>
      <div class="control">
        <input
          class="input"
          type="text"
          placeholder="שם התכנית"
          v-model="name"
        />
      </div>
    </div>

    <div class="field">
      <div class="control">
        <label class="checkbox">
          <input
            type="checkbox"
            v-model="publicize"
            :disabled="saving || savedPlan"
          />
          ציבורי
        </label>
      </div>
    </div>

    <copyable-link
      v-if="savedPlan"
      routeName="Course Plan"
      :routeParams="{ plan_id: savedPlan.id }"
      label="כתובת"
    />

    <div class="field is-grouped">
      <div class="control">
        <button
          class="button is-link"
          :class="{ 'is-loading': saving, 'is-success': savedPlan }"
          @click="onSubmit"
          :disabled="!canSave || saving"
        >
          <span v-if="savedPlan">
            <i class="fas fa-check" />
            סיום
          </span>
          <span v-else>שמירה</span>
        </button>
      </div>
      <div class="control" v-if="!savedPlan">
        <button class="button is-link is-light" @click="$emit('close')">
          ביטול
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, computed, toRefs } from "vue";
import { saveAs } from "@/course-store.js";
import CopyableLink from "@/components/CopyableLink.vue";
import router from "@/router";

export default {
  components: { CopyableLink },
  emits: ["close"],
  setup(_props, { emit }) {
    const state = reactive({
      name: "",
      publicize: false,
      saving: false,
      savedPlan: null,
    });

    const onSubmit = async () => {
      if (state.savedPlan !== null) {
        emit("close");
        return;
      }
      state.saving = true;
      try {
        state.savedPlan = await saveAs({
          name: state.name,
          publicize: state.publicize,
        });
        router.push({
          name: "Course Plan",
          params: { plan_id: state.savedPlan.id },
        });
      } finally {
        state.saving = false;
      }
    };

    const canSave = computed(() => state.name.length > 0);
    return {
      ...toRefs(state),
      canSave,
      onSubmit,
    };
  },
};
</script>

<style>
</style>