<template>
  <div v-if="$auth.isAuthenticated.value">
    <div dir="rtl">
      <section class="section section-style">
        <div class="columns is-variable is-2">
          <div class="column is-2 is-right is-hidden-mobile is-hidden-touch">
            <navigation
              :allcourses="courses"
              @clickCourse="addCourse"
            ></navigation>
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
import {
  courses,
  moveCourse,
  deleteCourse,
  addCourse
} from "@/course-store.js";

export default {
  name: "Closure()",
  components: { Navigation, Year },
  data() {
    return {
      years: [
        { id: 1, name: "שנה א" },
        { id: 2, name: "שנה ב" },
        { id: 3, name: "שנה ג" },
        { id: 4, name: "שנה ד" }
      ],
      username: "placehoder",
      student: {
        username: "string",
        track_pk: 28,
        year_in_studies: 1,
        courses: [
          {
            pk: 0,
            year_in_studies: 1,
            semester: "FIRST"
          }
        ]
      },
      courses
    };
  },

  created() {
    if (this.$auth.isAuthenticated.value) {
      this.$auth.getIdTokenClaims().then(console.log, console.error);
      this.$http.get("tracks/?track_number=3010").then(response => {
        this.track = response.data.results[0];
      });
    }
  },
  methods: {
    moveCourse,
    deleteCourse,
    addCourse,
    getUsername() {
      return this.$auth.getIdTokenClaims().then(response => response.nickname);
    },

    /** fetch all student's courses from the DB and store them in allcourses */
    createAllCourses(student) {
      for (const course of student.courses) {
        const course_info = course.course;
        this.allcourses.push({
          pk: course.pk,
          course_id: course_info.course_id,
          name: course_info.name,
          semester: this.getSemester(course_info),
          year: course.year_in_studies,
          points: course.course.points,
          type: this.getType(course)
        });
      }
    },

    getSemester(course) {
      if (course.semester == "FIRST") return 1;
      return 2;
    },

    getType(course) {
      console.log(course);
      if (course.type == "MUST") return 1;
      if (course.type == "CHOOSE_FROM_LIST") return 2;
      return 3;
    }
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
