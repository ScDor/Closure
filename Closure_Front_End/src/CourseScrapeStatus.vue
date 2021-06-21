<template>
  <div id="iframe-div" class="box">
      Closure() - HUJI registered courses scraper

      <div class="notification is-danger" v-if="this.status === 'error'">
          Error: {{ errorMessage }}
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
        window.addEventListener("message", this.handleEvent, false);
    },

    unmounted: function() {
        window.removeEventListener("message", this.handleEvent);
    },

    methods: {
        handleEvent: function(event) {
            if (!ALLOWED_MESSAGE_ORIGINS.includes(event.origin)) {
                console.error(`Received window event ${JSON.stringify(event)} from unexpected origin ${event.origin}`);
                return;
            }


            const msg = event.data;
            if (msg.type === "error") {
                console.error(msg);
                this.status = "error";
                this.errorMessage = msg.errorMessage;
            }

            if (msg.type === "gotCourses") {
                console.log(`gotCourses message`);
                this.notifications.push({
                    "id": this.notifications.length,
                    "contents": `Detected ${msg.courses.length} courses`
                })
                this.handleCourses(msg.courses);
            }
        },

        handleCourses: function(courses) {
            // TODO: update the 'Take' resource via API
            console.log(courses)
        }
    },
    
    data: function() {
        return {
            "status": "Initializing",
            "notifications": []
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