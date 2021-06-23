<template>
  <div id="iframe-div" class="box container" dir="rtl">
      <h1 class="title is-1 has-text-centered">יבוא קורסים מהאוניברסיטה</h1>

      <div class="notification is-danger" v-if="this.error">
          {{ this.error }}
      </div>

      <div class="has-text-centered">
      <button class="button is-primary is-large" v-if="!$auth.isAuthenticated.value" @click="authenticate">
          <span class="icon">
              <i class="fas fa-lock"></i>
          </span>
          <span>אימות</span>
       </button>


      <button class="button is-primary is-large" v-if="status === 'waiting' && $auth.isAuthenticated.value" @click="start">התחלה</button>
      </div>

      <div v-if="status === 'finishedParsing' && !canSend">
      </div>

      <div class="has-text-centered" v-if="status === 'started'">
        <span>טוען קורסים...</span>
        <progress class="progress is-small is-primary" max="100" v-if="status === 'started'">15%</progress>
      </div>

      <div v-if="status === 'finishedParsing' && this.ambiguousCourses.length > 0">
          <div class="has-text-centered">
          <span> מתוך
                 {{ this.courses.length }}
                 קורסים, נמצאו 
                 {{ this.ambiguousCourses.length}}
                 קורסים שלא ברור מתי הם נעשו. אנא בחר/י לכל אחד מהקורסים הללו את מועד לקיחתו:
          </span>
          <div v-for="course in ambiguousCourses" :key="course.id">
              <span>{{ course.name }}</span>
          </div>
          </div>



          <div class="has-text-centered">
          <button class="button is-primary is-large" :disabled="!canSend"  @click="submit">שמירה</button>
          </div>
      </div>

      <div class="notification is-success" v-if="status === 'success'">
          <span> 
              {{ this.courses.length}}
              קורסים נשמרו בהצלחה
          </span>
      </div>


    <div v-for="notif in notifications" :key="notif.id" class="notification">
        Notification: {{notif.contents }}
    </div>
  </div>
</template>

<script>

import { reactive, ref } from 'vue'

const HUJI_ORIGIN = "https://www.huji.ac.il";

const ALLOWED_MESSAGE_ORIGINS = [HUJI_ORIGIN, `${location.protocol}//${location.host}`]

export default {
    created: function() {
        if (window.parent === window) {
            this.status = "error"
            this.errorMessage = "This page must be ran within HUJI User registration page"
            return;
        }
        window.addEventListener("message", this.handleEvent, false);
    },

    unmounted: function() {
        window.removeEventListener("message", this.handleEvent);
    },
    methods: {
        start: function() {
            window.parent.postMessage("start", HUJI_ORIGIN)
        },
        handleEvent: function(event) {
            if (!ALLOWED_MESSAGE_ORIGINS.includes(event.origin)) {
                console.warn(`Received window event ${JSON.stringify(event)} from unexpected origin ${event.origin}`);
                return;
            }


            const msg = event.data;
            if (msg === "started" || msg === "finishedParsing") {
                this.status = msg
            }
            if (msg.type === "error") {
                console.error(msg);
                this.status = "error";
                this.errorMessage = msg.errorMessage;
            }

            if (msg.type === "gotCourse") {
                this.handleCourse(msg.course)
            }
        },

        handleCourse: async function(course) {

            course.key = this.courses.length
            course.ambiguous = ref(false)
            const rCourse = reactive(course)
            this.courses.push(rCourse)
            if (!rCourse.semester) {
                await this.tryFillSemesterFromShnaton(rCourse)
            }
        },
        tryFillSemesterFromShnaton: async function(course) {
            try {
                const res = await this.$http(`/courses`, {
                    params: {
                        course_id: course.course_id,
                        data_year: course.year
                    }
                })
                const data = res.data
                if (data.count === 0) {
                    console.warn(`Could not get entry for course ${course.course_id} at year ${course.year}`)
                    course.ambiguous = true
                    return
                }
                if (data.count > 1) {
                    console.error(`Got more than 1 course for given course id and year, how?`)
                    console.error(data.results)
                }
                const gottenCourse = data.results[0]
                course.name = gottenCourse.name // `course.name` might be trimmed if it came from the grades website
                course.semester = gottenCourse.semester
                course.ambiguous = course.semester === "EITHER"
                console.log(gottenCourse)
            } catch (error) {
                this.error = `בעיית תקשורת: ${error}`
                course.ambiguous = true
            }
        },
        submit: async function() {

        },
        authenticate: async function() {
            this.$auth.loginWithPopup()
        }
    },
    
    computed: {
        canSend: function() {
            return this.status === "finishedParsing" && this.courses.every(course => course.semester)
        },
        ambiguousCourses: function() {
            return this.courses.filter(course => course.ambiguous)
        }
    },
    data: function() {
        return {
            "status": "waiting",
            "notifications": [],
            "courses": [],
            "error": ""
        }
    },

}
</script>

<style>
#iframe-div {
}
</style>