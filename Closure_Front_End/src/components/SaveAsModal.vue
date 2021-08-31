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
          <input type="checkbox" v-model="publicize" />
          ציבורי
        </label>
      </div>
    </div>

    <div class="field is-grouped">
      <div class="control">
        <button
          class="button is-link"
          :class="{ 'is-loading': saving }"
          @click="onSubmit"
          :disabled="!canSave || saving"
        >
          שמירה
        </button>
      </div>
      <div class="control">
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
export default {
  emits: ["close"],
  setup(_props, { emit }) {
    const state = reactive({
      name: "",
      publicize: false,
      saving: false,
    });

    const onSubmit = async () => {
      state.saving = true;
      try {
        await saveAs({ name: state.name, publicize: state.publicize });
        emit("close");
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