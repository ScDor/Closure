<template>
  <div class="notification full-height notification-style">
    <p class="menu-label has-text-centered">
      <b>{{ year.name }}</b>
    </p>

    <semester
      v-for="semester in semesters"
      :key="semester.id"
      :year="year"
      :semester="semester"
      :allcourses="allcourses"
      @dragcourse="startDrag"
      @dropcourse="onDrop"
    ></semester>
  </div>
</template>

<script>
import Semester from "./Semester.vue";

export default {
  props: ["year", "allcourses"],

  components: { Semester },

  data() {
    return {
      semesters: [
        { id: 1, name: "סמסטר א" },
        { id: 2, name: "סמסטר ב" },
      ],
    };
  },

  setup(props) {
    const startDrag = (event, course) => {
      console.log(event);
      console.log(course);
      event.dataTransfer.dropEffect = "move";
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("id", course.id);
    };

    const onDrop = (event, year, semester) => {
      const courseid = event.dataTransfer.getData("id");
      const course = props.allcourses.find((course) => course.id == courseid);
      course.year = year.id;
      course.semester = semester.id;
    };

    return {
      startDrag,
      onDrop,
    };
  },
};
</script>

<style>
.full-height {
  min-height: 88vh;
}

.notification-style {
  padding-top: 1rem;
  padding-left: 0rem;
  padding-right: 0rem;
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.1);
}
</style>