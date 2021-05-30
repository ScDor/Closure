<template>
  <div
    class="semester half-height drop-zone"
    @drop="emitDrop($event, year, semester)"
    @dragenter.prevent
    @dragover.prevent
  >
    <p class="menu-label has-text-centered">{{ semester.name }}</p>

    <ul class="menu-list">
      <li
        class="list-item-style"
        v-for="course in filterCourses"
        :key="course.id"
      >
        <course-box
          :name="course.name"
          class="drag-el"
          draggable="true"
          @dragstart="emitDrag($event, course)"
        ></course-box>
      </li>
    </ul>
  </div>
</template>

<script>
import CourseBox from "./CourseBox.vue";

export default {
  props: ["year", "semester", "allcourses"],

  components: { CourseBox },

  data() {
    return {};
  },

  computed: {
    filterCourses() {
      return this.allcourses
        .filter(
          (course) =>
            course.year == this.year.id && course.semester == this.semester.id
        )
        .sort((c1, c2) => c1.id - c2.id);
    },
  },

  methods: {
    emitDrag(event, course) {
      this.$emit("dragcourse", event, course);
    },

    emitDrop(event, year, semester) {
      this.$emit("dropcourse", event, year, semester);
    },
  },
};
</script>

<style>
.half-height {
  min-height: 38vh;
}

.list-item-style {
  margin: 0.25rem;
}
</style>