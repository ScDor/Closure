<template>
  <h1 class="title" v-if="courses.length > 0">בעיות</h1>
  <div class="box" v-if="courses.length > 0">
    <div class="notification is-warning">
      זוהו
      <strong>{{ courses.length }}</strong>
      קורסים שאינם נתמכים ולא ישמרו:
    </div>
    <table class="table">
      <thead>
        <tr>
          <th>מספר קורס</th>
          <th>שם קורס</th>
          <th>סיבה לאי-תמיכה</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in courses" :key="course.course_id">
          <td>{{ course.course_id }}</td>
          <td>{{ course.name }}</td>
          <td>
            {{
              course.notInDb
                ? "לא מופיע במסד הנתונים"
                : "קורסי קיץ/שנתי אינו נתמך כעת על ידי האתר"
            }}
          </td>
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