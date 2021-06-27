<template>

<h1 class="title">קורסים לייבוא</h1>
<div class="notification is-danger" v-if="courses.length === 0">
    מתוך
    <strong>{{totalCourseCount}}</strong>
    קורסים שנקלטו מאתר האוניברסיטה, לא אותרו קורסים אשר נתמכים על ידי האתר.
</div>
<div class="box" v-if="courses.length > 0">
<div class="notification is-success">
  אותרו
  <strong>{{courses.length}}</strong>
  קורסים שניתן לייבא
</div>
<div class="notification is-warning" v-if="ambiguousCourses.length > 0">
  עבור
  <strong>{{ambiguousCourses.length}}</strong>
  מהקורסים, יש לבחור ידנית את הסמסטר
</div>
  <table class="table">
    <thead>
      <tr>
        <th>מספר קורס</th>
        <th>שם קורס</th>
        <th>סמסטר</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="course in courses" :key="course.course_id">
        <td>{{ course.course_id }}</td>
        <td>{{ course.name }}</td>
        <td>
            <div class="control">
            <label class="radio">
                <input type="radio" id="one" value="FIRST" v-model="course.semester">
                א'
            </label>
            <label class="radio">
                <input type="radio" id="two" value="SECOND" v-model="course.semester">
                ב'
            </label>
            </div>
        </td>
      </tr>
    </tbody>
  </table>

    <button class="button is-success is-large" :disabled="!canImport" 
            @click="$emit('import', courses)">ייבוא</button>
    <div class="notification is-warning is-light">
      <strong>אזהרה:</strong>
      <br/>
      עם ייבוא הקורסים, כל הקורסים הקודמים ששמורים בדפדפן יימחקו
    </div>
</div>
</template>

<script>
export default {
  props: {
    courses: {
      type: Array
    },
    totalCourseCount: Number
  },
  emits: ['update:courses', 'import'],
  computed: {
    ambiguousCourses() {
      return this.courses.filter(course => course.ambiguous)
    },
    canImport() {
      return this.courses.every(course => course.semester)
    }
  }
};
</script>

<style>
</style>