<template>
  <h1 class="title" v-if="courses.length > 0">בעיות</h1>
  <div class="box" v-if="courses.length > 0">
    <div class="notification is-warning">
      זוהו
      <strong>{{ courses.length }}</strong>
      קורסים שלא קיימים במסד הנתונים ולכן לא ייובאו:
    </div>
    <table class="table">
      <thead>
        <tr>
          <th>מספר קורס</th>
          <th>שם קורס</th>
          <th>נקודות זכות</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in courses" :key="course.course_id">
          <td>{{ course.course_id }}</td>
          <td>{{ course.name }}</td>
          <td>{{ course.points }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    courses: {
      type: Array
    }
  }
};
</script>

<style>
</style>