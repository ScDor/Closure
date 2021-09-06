<template>
  <div>
    <section class="section-style">

      <div class="has-text-centered" v-if="!student">
        <h2 class="subtitle">טוען נתונים...</h2>
        <progress class="progress is-primary max=100" >15%</progress>
      </div>

      <div v-if="idClaims && showDebug">
        <span>ID Claims:</span><br/>
        <span class="is-family-monospace">{{ idClaims }}</span>
      </div>

      <div v-if="student && showDebug">
        <span>Student Object:</span><br/>
        <span class="is-family-monospace">{{ student }}</span>
      </div>
      
      <div v-if="student">
        <user :idClaims="idClaims" :student="student" />
      </div>
    </section>
  </div>
</template>

<script>
import User from "../components/User.vue";
import { inject, toRefs } from "vue";

export default {
  name: "Closure()",
  components: { User },
  setup() {
    const showDebug = false
    const { student, idClaims } = toRefs(inject("studentAndClaims"))

    return { idClaims, student, showDebug }
  }

};
</script>

<style>
.section-style {
  padding: 0.5rem;
}
</style>