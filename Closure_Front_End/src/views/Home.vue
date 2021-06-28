<template>
  <div v-if="$auth.isAuthenticated.value">
    <div dir="rtl">
      <section class="section section-style">
        <div class="columns is-variable is-2">
          <div class="column is-2 is-right is-hidden-mobile is-hidden-touch">
            <navigation @clickcourse="add" :allcourses="allcourses"></navigation>
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
  <error-notification v-if="myData()"
    :errorMessage="showError">
  </error-notification>
    <error-notification v-else
    :errorMessage="'שדdה'">
  </error-notification>

</template>

<script>
import Year from "../components/Year.vue";
import Navigation from "../components/Navigation.vue";
import ErrorNotification from "../components/ErrorNotification.vue";
import Utils from "../Utils.js"

export default {
  name: "Closure()",
  components: { Navigation, Year, ErrorNotification },
  data() {
    return {
      years: [
        { id: 1, name: "שנה א" },
        { id: 2, name: "שנה ב" },
        { id: 3, name: "שנה ג" },
        { id: 4, name: "שנה ד" },
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
            semester: "FIRST",
          },
        ],
      },

      allcourses: [
        {
          pk: 5837,
          course_id: 67315,
          name: "סדנת תכנות בשפות C ו- ++C",
          semester: 1,
          year: 2,
          points: 4,
          type: 1,
        },
        {
          pk: 7208,
          course_id: 80131,
          name: "חשבון אינפיניטסימלי (1)",
          semester: 1,
          year: 1,
          points: 7,
          type: 1,
        },
        {
          pk: 7209,
          course_id: 80132,
          name: "חשבון אינפיניטסימלי (2)",
          semester: 2,
          year: 1,
          points: 7,
          type: 1,
        },
        {
          pk: 7211,
          course_id: 80134,
          name: "אלגברה ליניארית (1)",
          semester: 1,
          year: 1,
          points: 6,
          type: 1,
        },
        {
          pk: 7212,
          course_id: 80135,
          name: "אלגברה ליניארית (2)",
          semester: 2,
          year: 1,
          points: 6,
          type: 1,
        },
        {
          pk: 7220,
          course_id: 80181,
          name: "מתמטיקה דיסקרטית",
          semester: 1,
          year: 1,
          points: 5,
          type: 1,
        },
        {
          pk: 5844,
          course_id: 67392,
          name: "מבוא לקריפטוגרפיה ואבטחת תוכנה",
          semester: 2,
          year: 2,
          points: 4,
          type: 2,
        },
        {
          pk: 5854,
          course_id: 67506,
          name: "מסדי נתונים",
          semester: 1,
          year: 3,
          points: 5,
          type: 2,
        },
        {
          pk: 5888,
          course_id: 67609,
          name: "גרפיקה ממוחשבת",
          semester: 1,
          year: 3,
          points: 5,
          type: 3,
        },
        {
          pk: 5951,
          course_id: 67829,
          name: "עיבוד ספרתי של תמונות",
          semester: "1",
          year: 3,
          points: 4,
          type: 2,
        },
        {
          pk: 5960,
          course_id: 67842,
          name: "מבוא לבינה מלאכותית",
          semester: "2",
          year: 3,
          points: 5,
          type: 2,
        },
      ],
    };
  },

  created() {
    if (this.$auth.isAuthenticated.value) {
      this.$auth.getIdTokenClaims().then(console.log, console.error);
      this.$http.get("tracks/?track_number=3010",
      {validateStatus: Utils.validateStatusCode(status)}
      ).then(response => {
        this.track = response.data.results[0]
      })
      .catch (Utils.popOutStatusCodeError);
    }
  },

  observable:{
    showError: this.$error
  },

   computed: {
    myData() {
      return this.showError
    }
   },

  methods: {
    getUsername() {
      return this.$auth
        .getIdTokenClaims()
        .then((response) => response.nickname);
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
      return 3;
    },

    /**
     * This method adds a new coursebox, by default to the first semester.
     * requires an event (clicking on a course on the drop down menu in the navigation bar
     * and the course itself.
     */
    add(event, course) {
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
.error-notification {
  margin-left: 24vw;
  max-height: 80vh;
}
</style>
