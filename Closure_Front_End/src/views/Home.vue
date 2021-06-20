<template>
  <div v-if="$auth.isAuthenticated.value">
    <div dir="rtl">
      <section class="section section-style">
        <div class="columns is-variable is-2">
          <div class="column is-2 is-right is-hidden-mobile is-hidden-touch">
            <navigation @clickcourse="add"></navigation>
          </div>
          <div class="column" v-for="year in years" :key="year">
            <year :year="year" :allcourses="allcourses" 
                  @courseMoved="moveCourse" @courseDeleted="deleteCoruse" />
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
      track: null,
      student: null,
      allcourses: [
        {
          course_id: 1,
          name: "חשבון אינפיניטסימלי 1",
          points: 7,
          year: 1,
          semester: 1,
        },
        {
          course_id: 2,
          name: "מבוא למדעי המחשב",
          points: 7,
          year: 1,
          semester: 1,
        },
        {
          course_id: 3,
          name: "אלגברה ליניארית 1",
          points: 6,
          year: 1,
          semester: 1,
        },
        {
          course_id: 4,
          name: "מתמטיקה דיסקרטית",
          points: 5,
          year: 1,
          semester: 1,
        },
        {
          course_id: 5,
          name: "חשבון אינפיניטסימלי 2",
          points: 7,
          year: 1,
          semester: 2,
        },
        {
          course_id: 6,
          name: "C / C++",
          points: 4,
          year: 1,
          semester: 2,
        },
        {
          course_id: 7,
          name: "אלגברה ליניארית 2",
          points: 6,
          year: 1,
          semester: 2,
        },
        {
          course_id: 8,
          name: "מבני נתונים",
          points: 4,
          year: 1,
          semester: 2,
        },
        {
          course_id: 9,
          name: "אבן פינה קיקיונית כלשהי",
          points: 2,
          year: 1,
          semester: 2,
        },
      ],
    };
  },
  created() {
    if (this.$auth.isAuthenticated.value) {
      this.$auth.getIdTokenClaims().then(console.log, console.error);
      this.$http.get("tracks/?track_number=3010").then(response => {
        this.track = response.data.results[0]
      })
    }
  },
  methods: {
    /**
     * This method adds a new coursebox, by default to the first semester.
     * requires an event (clicking on a course on the drop down menu in the navigation bar
     * and the course itself.
     */
    add(event, course) {
      this.allcourses.push({
        course_id: course.course_id,
        name: course.name,
        points: course.points,
        year: 1,
        semester: 1,
      });
    },

    /** Moves a course to a new year and semester, given by their IDs */
    moveCourse({course, newYear, newSemester}) {
      course.year = newYear
      course.semester = newSemester
    },
    /** Deletes a course from all years */
    deleteCoruse(course) {
      const index = this.allcourses.indexOf(course);
      this.allcourses.splice(index, 1);
    }
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
