<template>
  <div v-if="$auth.isAuthenticated.value">
    <div dir="rtl">
      <section class="section section-style">
        <div class="columns is-variable is-2">
          <div class="column is-2 is-right is-hidden-mobile is-hidden-touch">
            <navigation
              @clickcourse="add"
              :allcourses="allcourses"
            ></navigation>
          </div>
          <div class="column" v-for="year in years" :key="year">
            <year
              :year="year"
              :allcourses="allcourses"
              @courseMoved="moveCourse"
              @courseDeleted="deleteCoruse"
            />
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

export default {
  name: "Closure()",
  components: { Navigation, Year },

  data() {
    return {
      years: [
        { id: 1, name: "שנה א" },
        { id: 2, name: "שנה ב" },
        { id: 3, name: "שנה ג" },
        { id: 4, name: "שנה ד" },
      ],

      allcourses: [],
      
    };
  },

  created() {
    this.allcourses = this.$route.params.allcourses;

    if (this.$auth.isAuthenticated.value) {
      // this.$auth.getIdTokenClaims().then(console.log, console.error);
      this.$http.get("/student/me").then(function (response) {
        console.log(response);
        // const student = response.data;
        // this.createAllCourses(student);
        // this.getTrack(student);
      });
      // this.createAllCourses(this.student);
      // this.$http.get("tracks/?track_number=3010").then(response => {
      //   this.track = response.data.results[0]
      // })
    }
  },

  methods: {
    getTrack(student) {
      if (student.track_pk == null) {
        this.$http.post();
      }
    },

    /** fetch all student's courses from the DB and store them in allcourses */
    createAllCourses(student) {
      console.log(student);
      for (const course of student.courses) {
        const course_info = course.course;
        this.allcourses.push({
          pk: course.pk,
          course_id: course_info.course_id,
          name: course_info.name,
          semester: this.getSemester(course_info),
          year: course.year_in_studies,
          points: course.course.points,
          type: this.getType(course),
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
      if (course.type == "CHOOSE") return 3;
      return 4;
    },

    /**
     * This method adds a new coursebox, by default to the first semester.
     * requires an event (clicking on a course on the drop down menu in the navigation bar
     * and the course itself.
     */
    add(event, course) {
      this.$http.get("/student/me").then(console.log);
      this.allcourses.push({
        pk: course.pk,
        course_id: course.course_id,
        name: course.name,
        semester: 1,
        year: 1,
        points: course.points,
      });
    },

    /** Moves a course to a new year and semester, given by their IDs */
    moveCourse({ course, newYear, newSemester }) {
      course.year = newYear;
      course.semester = newSemester;
    },

    /** Deletes a course from all years */
    deleteCoruse(course) {
      const index = this.allcourses.indexOf(course);
      this.allcourses.splice(index, 1);
    },
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
