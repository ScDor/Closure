<template>
  <div id="iframe-div" class="container" dir="rtl">
    <h1 class="title is-1 has-text-centered">יבוא קורסים מהאוניברסיטה</h1>

    <div class="notification is-danger" v-if="this.error">
      {{ this.error }}
    </div>

    <instructions />

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

    <div v-if="status === 'finishedParsing' && !canSend"></div>

    <div class="has-text-centered" v-if="status === 'started'">
      <span>טוען קורסים...</span>
      <progress
        class="progress is-small is-primary"
        max="100"
        v-if="status === 'started'"
        >15%</progress
      >
    </div>

    <div
      v-if="status === 'finishedParsing' && this.ambiguousCourses.length > 0"
    >
      <div class="has-text-centered">
        <span>
          מתוך
          {{ this.courses.length }}
          קורסים, נמצאו
          {{ this.ambiguousCourses.length }}
          קורסים שלא ברור מתי הם נעשו. אנא בחר/י לכל אחד מהקורסים הללו את מועד
          לקיחתו:
        </span>
        <div v-for="course in ambiguousCourses" :key="course.id">
          <span>{{ course.name }}</span>
        </div>
      </div>

      <div class="has-text-centered">
        <button
          class="button is-primary is-large"
          :disabled="!canSend"
          @click="save"
        >
          שמירה
        </button>
      </div>
    </div>

    <div class="notification is-success" v-if="status === 'success'">
      <span>
        {{ this.courses.length }}
        קורסים נשמרו בהצלחה
      </span>
    </div>

    <div v-for="notif in notifications" :key="notif.id" class="notification">
      Notification: {{ notif.contents }}
    </div>
  </div>
</template>

<script>
import { reactive, ref } from "vue";
import { addCourses } from "@/course-store.js";
import Instructions from "./Instructions.vue";

const HUJI_ORIGIN = "https://www.huji.ac.il";

const ALLOWED_MESSAGE_ORIGINS = [
  HUJI_ORIGIN,
  `${location.protocol}//${location.host}`
];

const SEMESTER_TO_INT = {
  FIRST: 1,
  SECOND: 2
};

export default {
  components: { Instructions },
  created() {
    window.addEventListener("message", this.handleEvent);
  },

  unmounted() {
    window.removeEventListener("message", this.handleEvent);
  },
  methods: {
    openUni: function() {
      const winRef = window.open(
        "https://www.huji.ac.il/dataj/controller/!92DE8E041B23BAFFCA1BFB95B571EBC3/stu/STU-STUZIYUNIM?winsub=yes&safa=H"
      );
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
      course.key = this.courses.length;
      course.ambiguous = ref(false);
      const rCourse = reactive(course);
      this.courses.push(rCourse);
      if (!rCourse.semester) {
        await this.tryFillSemesterFromShnaton(rCourse);
      }
    },
    tryFillSemesterFromShnaton: async function(course) {
      try {
        const res = await this.$http(`/courses`, {
          params: {
            course_id: course.course_id,
            data_year: course.year
          }
        });
        const data = res.data;
        if (data.count === 0) {
          console.error(
            `Could not get entry for course ${course.course_id} - ${course.name} at year ${course.year}`
          );
          course.ambiguous = true;
          return;
        }
        if (data.count > 1) {
          console.error(
            `Got more than 1 course for given course id and year, how?`
          );
          console.error(data.results);
        }
        const gottenCourse = data.results[0];
        course.name = gottenCourse.name; // `course.name` might be trimmed if it came from the grades website
        course.semester = gottenCourse.semester;
        course.ambiguous = course.semester === "EITHER";
        console.log(gottenCourse);
      } catch (error) {
        this.error = `בעיית תקשורת: ${error}`;
        course.ambiguous = true;
      }
    },
    authenticate: async function() {
      await this.$auth.loginWithPopup();
    },
    save() {
      const firstYear = Math.min(...this.courses.map(course => course.year));
      const courses = this.courses.map(course => {
        return {
          ...course,
          year: course.year - firstYear + 1,
          semester: SEMESTER_TO_INT[course.semester]
        };
      });
      addCourses(courses);
      this.$router.push("/");
    }
  },

  computed: {
    canSend() {
      // return this.status === "finishedParsing" && this.courses.every(course => course.semester)
      return true;
    },
    ambiguousCourses() {
      return this.courses.filter(course => course.ambiguous);
    }
  },
  data() {
    return {
      status: "notHooked",
      notifications: [],
      courses: [],
      error: "",
      ref: null
    };
  }
};
</script>

<style>
#iframe-div {
}
</style>