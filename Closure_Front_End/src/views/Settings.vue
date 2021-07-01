<template>
  <div dir="rtl">
    <div class="has-text-centered">
      <div class="section section-style">
        <label class="menu-label"><b>הגדרות</b></label>
        <user></user>
      </div>
    </div>
  </div>
</template>

<script>
import User from "../components/User.vue";

export default {
  name: "Closure()",
  components: { User },

  data() {
    return {};
  },

  created() {},
};
</script>

<style>
.section-style {
  padding: 0.5rem;
}
</style>