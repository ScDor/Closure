<template>
  <div class="container" dir="rtl">
    <h1 class="title is-1 has-text-centered">ייבוא קורסים מהאוניברסיטה</h1>

    <div class="section">
      <instructions />
    </div>

    <div class="notification is-danger" v-if="this.error">
      {{ this.error }}
    </div>

    <div class="has-text-centered">
      <div class="container">
        <span>{{ status }}</span>
      </div>

      <button
        class="button is-primary is-large"
        v-if="status === 'notHooked'"
        @click="openUni"
      >
        <span class="icon">
          <i class="fas fa-university"></i>
        </span>
        <span>פתח מידע אישי</span>
      </button>
    </div>

    <div class="has-text-centered" v-if="status === 'started'">
      <span>טוען קורסים...</span>
      <progress
        class="progress is-small is-primary"
        max="100"
        v-if="status === 'started'"
        >15%</progress
      >
    </div>

    <div class="section" v-if="status === 'finishedParsing'">
      <imported-courses-grid :parsedCourses="courses" @import="onImportCourses" />
    </div>

  </div>
</template>

<script>
import { addCourses } from "@/course-store.js";
import Instructions from "./Instructions.vue";
import { default as INITIAL_COURSES } from "./example-parsed-courses.js";
import ImportedCoursesGrid from "./ImportedCoursesGrid.vue";
import { API_SEMESTER_TO_PROP_INT } from "@/utils.js";

const HUJI_ORIGIN = "https://www.huji.ac.il";

const ALLOWED_MESSAGE_ORIGINS = [
  HUJI_ORIGIN,
  `${location.protocol}//${location.host}`
];



const USE_TEST_COURSES = false

export default {
  components: { Instructions, ImportedCoursesGrid },
  created() {
    window.addEventListener("message", this.handleEvent);
  },

  unmounted() {
    window.removeEventListener("message", this.handleEvent);
  },
  methods: {
    openUni: function() {
      const winRef = window.open("https://www.huji.ac.il/dataj/controller/stu");
      if (!winRef) {
        this.error = `חלה שגיאה בפתיחת האתר, אם יש לך חוסם חלונות קופצים או פרסומות, אנא בטל/י אותו.`;
        return;
      }
    },
    handleEvent: function(event) {
      if (!ALLOWED_MESSAGE_ORIGINS.includes(event.origin)) {
        console.warn(
          `Received window event ${JSON.stringify(
            event
          )} from unexpected origin ${event.origin}`
        );
        return;
      }

      const msg = event.data;
      if (msg.type === "tryHook") {
        this.status = msg.type;
        console.log(`Got hook attempt from HUJI at level ${msg.level}`);
        event.source.postMessage("hooked", HUJI_ORIGIN);
        console.log(`responded with hooked message.`);
        this.status = "hooked";
        this.ref = event.source;
      }
      if (msg === "started" || msg === "finishedParsing") {
        this.status = msg;
      }
      if (msg.type === "error") {
        console.error(msg);
        this.error = msg.errorMessage;
      }

      if (msg.type === "gotCourse") {
        this.handleCourse(msg.course);
      }
    },

    handleCourse: async function(course) {
      this.courses.push({ ...course, key: this.courses.length });
    },
    onImportCourses(courses) {
      const firstYear = Math.min(...courses.map(course => course.year));
      const coursesForDisplay = courses.map(course => {
        return {
          ...course,
          year: course.year - firstYear + 1,
          semester: API_SEMESTER_TO_PROP_INT.get(course.semester)
        };
      });
      addCourses(coursesForDisplay);
      this.$router.push("/");
    }
  },
  data() {
    const data = {
      status: "notHooked",
      courses: [],
      error: "",
      ref: null
    };
    if (USE_TEST_COURSES) {
      data.status = "finishedParsing"
      data.courses = INITIAL_COURSES
    }
    return data
  }
};
</script>

<style>
</style>