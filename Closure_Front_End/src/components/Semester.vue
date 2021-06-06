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
        v-for="course in filteredCourses"
        :key="course.course_id"
      >
        <course-box
          :course="course"
          class="drag-el"
          draggable="true"
          @dragstart="emitDrag($event, course)"
          @clickclose="$emit('clickclose', $event, course)"
        ></course-box>
      </li>
    </ul>
  </div>
  <semester-summary
    :class="{ space: semester.id == '1' }"
    :courses="filteredCourses"
  ></semester-summary>
</template>

<script>
import CourseBox from "./CourseBox.vue";
import SemesterSummary from "./SemesterSummary.vue";

export default {
  props: ["year", "semester", "allcourses"],

  components: { CourseBox, SemesterSummary },

  emits: ["dragcourse", "dropcourse", "clickclose"],

  computed: {
    filteredCourses() {
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
  min-height: 34vh;
}

.space {
  padding-bottom: 1rem;
}

.list-item-style {
  margin: 0.25rem;
}
</style>