<template>
  <div v-if="$auth.isAuthenticated.value">
    <div dir="rtl">
      <section class="section section-style">
        <div class="columns is-variable is-2">
          <div class="column is-2 is-right is-hidden-mobile is-hidden-touch">
            <navigation
              :allcourses="courses"
            />
            <CourseDetail :course="selectedCourse" v-if="selectedCourse" />
            <ProgressBox :allcourses="courses" />
          </div>
          <div class="column" v-for="year in years" :key="year">
            <year :year="year" />
          </div>
        </div>
      </section>
    </div>
  </div>
  <div v-else>
    <transition name="landing" appear>
      <img class="fit image-box" src="../assets/logo.png" />
    </transition>
  </div>
</template>

<script>
import Year from "../components/Year.vue";
import Navigation from "../components/Navigation.vue";
import CourseDetail from '../components/CourseDetail.vue';
import ProgressBox from "../components/ProgressBox.vue";
import {
  courses,
  moveCourse,
  deleteCourse,
  addCourse
} from "@/course-store.js";

export default {
  name: "Closure()",
  components: { Year, Navigation, CourseDetail, ProgressBox },
  data() {
    return {
      years: [
        { id: 1, name: "שנה א" },
        { id: 2, name: "שנה ב" },
        { id: 3, name: "שנה ג" },
        { id: 4, name: "שנה ד" }
      ],
      courses,
      selectedCourse: null
    };
  },
  methods: {
    moveCourse,
    deleteCourse,
    addCourse,
  },
  provide() {
    return {
      selectCourse: (course) => {
        this.selectedCourse = course;
      }
    };
  }
};
</script>

<style>
.section-style {
  padding: 0.5rem;
}
.image-box {
  margin-left: 24vw;
  max-height: 80vh;
}
.landing-enter-from {
  opacity: 0;
  transform: scale(0.6);
}
.landing-enter-to {
  opacity: 1;
  transform: scale(1);
}
.landing-enter-active {
  transition: all 0.7s ease;
}
</style>
