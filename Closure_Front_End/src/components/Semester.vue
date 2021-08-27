<template>
  <div
    class="semester half-height drop-zone"
    @drop="onDrop($event, year, semester)"
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
          @click="selectCourse(course)"
          @dragstart="startDrag($event, course)"
          @clickclose="deleteCourse(course)"
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
import { courses, moveCourse, deleteCourse} from '@/course-store.js'

export default {
  props: ["year", "semester" ],
  inject: [ "selectCourse"],
  components: { CourseBox, SemesterSummary },
  data() {
    return {
      courses
    }
  },

  computed: {
    filteredCourses() {
      return this.courses
        .filter(
          (course) =>
            course.year == this.year.id && course.semester == this.semester.id
        )
        .sort((c1, c2) => c1.type - c2.type);
    },
  },

  methods: {
    startDrag(event, course) {
      event.dataTransfer.dropEffect = "move";
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("id", course.course_id);
    },


    onDrop(event, year, semester) {
      const courseid = event.dataTransfer.getData("id");
      const course = this.courses.find(
        (course) => course.course_id == courseid
      );
      moveCourse({course, newYear: year.id, newSemester: semester.id})
    },
    deleteCourse
  },
};
</script>

<style>
.half-height {
  min-height: 36vh;
}

.space {
  padding-bottom: 1rem;
}

.list-item-style {
  margin: 0.25rem;
}
</style>