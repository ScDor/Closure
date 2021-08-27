<template>
  <div>
    <section class="section-style">

      <div class="has-text-centered" v-if="!student">
        <h2 class="subtitle">טוען נתונים...</h2>
        <progress class="progress is-primary max=100" >15%</progress>
      </div>
      <div class="has-text-centered" v-if="error">
        <span>חלה שגיאה</span>

        <div class="notification is-danger">
          <p>{{error}}</p>
        </div>
      </div>

      <div v-if="idClaims">
        <span>ID Claims:</span><br/>
        <span class="is-family-monospace">{{ idClaims }}</span>
      </div>

      <div v-if="student">
        <span>Student Object:</span><br/>
        <span class="is-family-monospace">{{ student }}</span>
      </div>
      
      <div v-if="!error && student">
        <user :idClaims="idClaims" :student="student" :saving="saving" @onSave="onSaveHandler"></user>
      </div>
    </section>
  </div>
</template>

<script>
import User from "../components/User.vue";
import { reactive, inject, toRefs } from "vue";

export default {
  name: "Closure()",
  components: { User },
  setup() {
    const state = reactive({
      saving: false,
      error: null,
    });

    const http = inject("http");

    const { student, idClaims } = toRefs(inject("studentAndClaims"))
    const setStudent = inject("setStudent");

    const onSaveHandler = async (event, newTrack) => {
      try {
        state.saving = true;
        console.log('new track', newTrack)
        const response = await http.post("student/me/", {
          "courses": [],
          "track_pk": newTrack.pk
        });
        setStudent(response.data);
      } 
      catch (exception) {
        state.error = exception.toString();
      }
      finally {
        state.saving = false;
      }
    };

    return { ...toRefs(state), idClaims, student, onSaveHandler}
  }

};
</script>

<style>
.section-style {
  padding: 0.5rem;
}
</style>