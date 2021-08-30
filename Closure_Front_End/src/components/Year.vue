<template>
  <div class="notification full-height notification-style">
    <p class="menu-label has-text-centered">
      <b>{{ year.name }}</b>
    </p>

    <!-- each year has only 2 semesters, 
    we still use a loop syntax to render them -->
    
    <semester
      v-for="semester in semesters"
      :key="semester.id"
      :year="year"
      :semester="semester"
    ></semester>
  </div>
</template>

<script>
import Semester from "./Semester.vue";

export default {
  props: ["year" ],
  components: { Semester },

  data() {
    return {
      semesters: [
        { id: "FIRST", name: "סמסטר א" },
        { id: "SECOND", name: "סמסטר ב" },
      ]
    };
  },
};
</script>

<style>
.full-height {
  height: max-content;
  overflow: auto;
}

.notification-style {
  padding-top: 1rem;
  padding-left: 0rem;
  padding-right: 0rem;
  padding-bottom: 0.25rem;
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.1);
}
</style>
