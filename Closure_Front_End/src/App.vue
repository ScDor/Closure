<template>
  <nav class="navbar has-shadow is-dark">
    <div class="navbar-brand">
      <div class="navbar-item"><b>Closure()</b></div>
    </div>
  </nav>

  <div dir="rtl">
    <section class="section section-style">
      <div class="columns is-variable is-2">
        <!-- navigation -->
        <div class="column is-2 is-right is-hidden-mobile is-hidden-touch">
          <navigation></navigation>
        </div>
        <!-- all years -->
        <div class="column" v-for="year in years" :key="year">
          <year :year="year" :allcourses="allcourses"></year>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import Year from "./components/Year.vue";
import Navigation from "./components/Navigation.vue";

export default {
  name: "Closure()",

  components: { Navigation, Year },

  data() {
    return {
      years: [
        { id: 1, name: "שנה א" },
        { id: 2, name: "שנה ב" },
        { id: 3, name: "שנה ג" },
        { id: 4, name: "שנה ד" },
      ],

      allcourses: [
        {
          id: 1,
          name: "קורס 1",
          year: 1,
          semester: 2,
        },
        {
          id: 2,
          name: "קורס 2",
          year: 1,
          semester: 1,
        },
        {
          id: 3,
          name: "קורס 3",
          year: 1,
          semester: 1,
        },
        {
          id: 4,
          name: "קורס 4",
          year: 2,
          semester: 1,
        },
      ],
    };
  },
};
</script>

<style>
.section-style {
  padding: 0.5rem;
}
</style>
