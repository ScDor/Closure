<template>
  <div>
    <section class="section-style">
      <div class="has-text-centered" v-if="loading">
        <span>טוען נתונים</span>
        <progress class="progress is-small is-primary" max="100">15%</progress>
      </div>

      <div class="has-text-centered" v-if="error">
        <span>חלה שגיאה</span>

        <div class="notification is-danger">
          <p>{{error}}</p>
        </div>
      </div>

      <!-- <span class="is-family-monospace" v-if="!loading">
        ID Claims: {{ idClaims }}
        Student: {{ student }}
      </span> -->

      <div v-if="!loading && !error">
        <user :idClaims="idClaims" :student="student" :saving="saving" @onSave="onSaveHandler"></user>
      </div>
    </section>
  </div>
</template>

<script>
import User from "../components/User.vue";
import { onMounted, reactive, inject, toRefs } from "vue";

export default {
  name: "Closure()",
  components: { User },
  setup() {
    const state = reactive({
      loading: true,
      saving: false,
      error: null,
      idClaims: null,
      student: null
    });

    const http = inject("http");
    const auth = inject("auth")

    onMounted(async () => {
      try {
        const claims = await auth.getIdTokenClaims();
        const student = (await http.get("student/me")).data;
        window.student = student;
        window.claims = claims;

        state.idClaims = claims;
        state.student = student;
      } catch (exception) {
        state.error = exception.toString();
      } finally {
        state.loading = false;
      }
    });

    const onSaveHandler = async (event, newTrack) => {
      try {
        state.saving = true;
        console.log('new track', newTrack)
        // const res = await http.post("student/me", {
        //   ...state.student, newTrack
        // });
        // console.log("post response", res)
      } 
      catch (exception) {
        state.error = exception.toString();
      }
      finally {
        state.saving = false;
      }
    };

    return { ...toRefs(state), onSaveHandler}
  }

};
</script>

<style>
.section-style {
  padding: 0.5rem;
}
</style>