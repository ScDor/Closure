<template>
  <div id="iframe-div" class="box">
      <span>יבוא קורסים מהאוניברסיטה</span>

      <div class="notification is-danger" v-if="this.status === 'error'">
          שגיאה: {{ errorMessage }}
      </div>

      <a class="button button-is-primary" v-if="!$auth.isAuthenticated.value" @click="authenticate" >אימות</a>

      <a class="button button-is-primary" v-if="status === 'waiting' && $auth.isAuthenticated.value" @click="start">התחלה</a>

      <progress class="progress is-small is-primary" max="100" v-if="status === 'started'">15%</progress>

      <div class="notification is-success" v-if="status === 'success'">
          <span> הצלחה </span>
      </div>

    <div v-for="course in courses.filter(c => c.ambiguous)" :key="course.id">
        <span>{{ course.name }}</span>
    </div>

    <div v-for="notif in notifications" :key="notif.id" class="notification">
        Notification: {{notif.contents }}
    </div>
  </div>
</template>

<script>


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
            if (msg === "started" || msg === "finished") {
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
            this.courses.push(course)
            if (!course.semester) {
                course.ambiguous = true
                await this.tryFillSemesterFromShnaton(course)
            }
        },
        tryFillSemesterFromShnaton: async function(course) {
            try {
                const res = await this.$http(`/courses/${course.course_id}`)
                console.log(`${res.data} `)
            } catch (ex) {
                console.error(`Couldn't get information for course ${course.course_id}: ${ex}`)
            }
        },
        authenticate: async function() {
            this.$auth.loginWithPopup()
        }
    },
    
    data: function() {
        return {
            "status": "waiting",
            "notifications": [],
            "courses": []
        }
    },

}
</script>

<style>
#iframe-div {
    display: flexbox
    flex-
}
</style>