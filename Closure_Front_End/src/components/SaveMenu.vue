<template>
  <div class="navbar-item has-dropdown is-hoverable" dir="rtl">
    <a class="navbar-link"> קובץ </a>

    <div class="navbar-dropdown">
      <a class="navbar-item" @click="openLoadMenu"> טעינה </a>
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


  <modal :active="showingSaveAsMenu" @close="closeSaveAsMenu">
      <save-as-modal @close="closeSaveAsMenu" />
  </modal>

  <modal :active="showingLoadMenu" @close="closeLoadMenu">
      <load-modal @close="closeLoadMenu" />
  </modal>
</template>

<script>
import { computed, ref } from "vue";
import Modal from "@/components/Modal.vue";
import SaveAsModal from "@/components/SaveAsModal.vue";
import LoadModal from "@/components/LoadModal.vue";
import { currentCourseplan, isDirty, save } from "@/course-store.js";
export default {
  components: { SaveAsModal, LoadModal, Modal },
  setup() {
    const canSave = isDirty;
    const canSaveAs = computed(() => currentCourseplan.value !== null);
    const showingSaveAsMenu = ref(false);

    const displaySaveAs = () => {
      showingSaveAsMenu.value = true;
    };
    const closeSaveAsMenu = () => (showingSaveAsMenu.value = false);

    const saving = ref(false);
    const onSave = async () => {
      if (currentCourseplan.value === null) {
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

    const showingLoadMenu = ref(false)
    const openLoadMenu = () => showingLoadMenu.value = true;
    const closeLoadMenu = () => (showingLoadMenu.value = false);

    return {
      canSave,
      canSaveAs,
      showingSaveAsMenu,
      onSave,
      displaySaveAs,
      closeSaveAsMenu,
      saving,
      showingLoadMenu, openLoadMenu, closeLoadMenu
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