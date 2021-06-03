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
          <navigation @clickcourse="add"></navigation>
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
          course_id: 1,
          name: "חשבון אינפיניטסימלי 1",
          year: 1,
          semester: 1,
        },
        {
          course_id: 2,
          name: "מבוא למדעי המחשב",
          year: 1,
          semester: 1,
        },
        {
          course_id: 3,
          name: "אלגברה ליניארית 1",
          year: 1,
          semester: 1,
        },
        {
          course_id: 4,
          name: "מתמטיקה דיסקרטית",
          year: 1,
          semester: 1,
        },
        {
          course_id: 5,
          name: "חשבון אינפיניטסימלי 2",
          year: 1,
          semester: 2,
        },
        {
          course_id: 6,
          name: "C / C++",
          year: 1,
          semester: 2,
        },
        {
          course_id: 7,
          name: "אלגברה ליניארית 2",
          year: 1,
          semester: 2,
        },
        {
          course_id: 8,
          name: "מבני נתונים",
          year: 1,
          semester: 2,
        },
        {
          course_id: 9,
          name: "אבן פינה קיקיונית כלשהי",
          year: 1,
          semester: 2,
        },
      ],
    };
  },


  methods: {
    add(event, course) {
      console.log(course);
      this.allcourses.push({
        id: course.course_id,
        name: course.name,
        
        year: 1,
        semester: 1,
      });
      console.log(this.allcourses);
    },
  },
};
</script>

<style>
.section-style {
  padding: 0.5rem;
}
</style>
