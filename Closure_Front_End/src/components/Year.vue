<template>
  <div class="notification full-height notification-style">
    <p class="menu-label has-text-centered">
      <b>{{ year.name }}</b>
    </p>

    <!-- each year has only 2 semesters, 
    we still use a loop syntax to render them -->
    
    <semester
      v-for="semester in semesters"
      :key="semester.id"
      :year="year"
      :semester="semester"
      :allcourses="allcourses"
      @dragcourse="startDrag"
      @dropcourse="onDrop"
      @clickclose="onClick"
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
      event.dataTransfer.dropEffect = "move";
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("id", course.course_id);
    };

     /** 
    * this method handles transferring courses from semester to semester   */
    
    const onDrop = (event, year, semester) => {
      const courseid = event.dataTransfer.getData("id");
      const course = props.allcourses.find(
        (course) => course.course_id == courseid
      );
      course.year = year.id;
      course.semester = semester.id;
    };

    /** 
    * this method removes a certain course once it's X button is clicked
    */
    
    const onClick = (event, toRemove) => {
      const index = props.allcourses.indexOf(toRemove);
      props.allcourses.splice(index, 1);
    };

    return {
      startDrag,
      onDrop,
      onClick,
    };
  },
};
</script>

<style>
.full-height {
  height: max-content;
  overflow: auto;
}

.notification-style {
  padding-top: 1rem;
  padding-left: 0rem;
  padding-right: 0rem;
  padding-bottom: 0.25rem;
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.1);
}
</style>
