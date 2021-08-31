<template>
  <div class="navbar-item has-dropdown is-hoverable" dir="rtl">
    <a class="navbar-link"> קובץ </a>

    <div class="navbar-dropdown">
      <a class="navbar-item"> טעינה </a>
      <a v-if="!saving" class="navbar-item" :class="{'is-disabled': !canSave}" @click="onSave"> שמירה </a>
      <div class="navbar-item" v-if="saving">
        <button class="navbar-item button is-loading" v-if="saving" disabled>
          שמירה
        </button>
      </div>
      <a class="navbar-item" :class="{'is-disabled': !canSaveAs}" @click="displaySaveAs">
        שמירה בשם
      </a>
      <hr class="navbar-divider" />
      <a class="navbar-item"> שיתוף </a>
    </div>
  </div>
  <div class="modal" :class="{ 'is-active': showSaveAsMenu }">
    <div class="modal-background" @click="closeSaveAsMenu"></div>
    <div class="modal-content">
      <save-as-modal @close="closeSaveAsMenu" />
    </div>
    <button
      class="modal-close is-large"
      aria-label="close"
      @click="closeSaveAsMenu"
    ></button>
  </div>
</template>

<script>
import { computed, ref } from "vue";
import SaveAsModal from "@/components/SaveAsModal.vue";
import { currentCourseplan, isDirty, save } from "@/course-store.js";
export default {
  components: { SaveAsModal },
  setup() {
    const canSave = isDirty;
    const canSaveAs = computed(() => currentCourseplan.value !== null);
    const showSaveAsMenu = ref(false);

    const displaySaveAs = () => {
      showSaveAsMenu.value = true;
    };
    const closeSaveAsMenu = () => (showSaveAsMenu.value = false);

    const saving = ref(false);
    const onSave = async () => {
      if (currentCourseplan == null) {
        displaySaveAs();
      } else {
        saving.value = true;
        try {
          await save();
        } finally {
          saving.value = false;
        }
      }
    };

    return {
      canSave,
      canSaveAs,
      showSaveAsMenu,
      onSave,
      displaySaveAs,
      closeSaveAsMenu,
      saving,
    };
  },
};
</script>

<style scoped>
a.is-disabled {
  pointer-events: none;
  opacity: .65;
}
</style>