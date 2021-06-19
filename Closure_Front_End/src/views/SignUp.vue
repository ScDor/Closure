<template>
  <div>
    <section class="section-style">
      <signup-form></signup-form>
    </section>
  </div>
</template>

<script>
import SignupForm from "../components/SignupForm.vue";

export default {
  name: "Closure()",
  components: { SignupForm },
};
</script>

<style>
.section-style {
  padding: 0.5rem;
}
</style>