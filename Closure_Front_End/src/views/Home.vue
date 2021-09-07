<template>
  <div v-if="auth.isAuthenticated.value">
    <div dir="rtl">
      <section class="section section-style">
        <div class="notification is-danger" v-if="error">
          חלה שגיאה בהסקת סוגי קורסים:
          <p> {{ error }}</p>
        </div>


        <template v-if="loading">
          מחשב סוגי קורסים בהתאם למסלול הנחבר
          ...
          <progress class="progress is-small is-primary" max="100">15%</progress>
        </template>

        <div class="columns is-variable is-2">
          <div class="column is-2 is-right is-hidden-mobile is-hidden-touch">
            <navigation />
            <course-detail v-model:course="selectedCourse" v-if="selectedCourse" :track="currentTrack" />
            <progress-box :allcourses="courses" />
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
import { ref, inject, provide } from "vue";
import Year from "../components/Year.vue";
import Navigation from "../components/Navigation.vue";
import CourseDetail from "../components/CourseDetail.vue";
import ProgressBox from "../components/ProgressBox.vue";
import { courses, currentTrack } from "@/course-store.js";
import { syncCourseTypesToTrack } from "@/hooks"
const years = [
  { id: 1, name: "שנה א" },
  { id: 2, name: "שנה ב" },
  { id: 3, name: "שנה ג" },
  { id: 4, name: "שנה ד" },
];

export default {
  name: "Closure()",
  components: { Year, Navigation, CourseDetail, ProgressBox },
  setup() {
    const selectedCourse = ref(null);
    provide("selectCourse", (course) => (selectedCourse.value = course));
    const auth = inject("auth");

    const { error, loading } = syncCourseTypesToTrack(courses, currentTrack)

    return {
      years,
      selectedCourse,
      courses,
      auth,
      currentTrack,
      error,
      loading
    };
  },
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
