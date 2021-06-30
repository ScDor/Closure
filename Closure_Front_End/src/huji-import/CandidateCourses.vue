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
        <th>נקודות זכות</th>
        <th>סמסטר</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="course in courses" :key="course.course_id" 
          :class="{ 'has-background-warning-light': course.ambiguous }">
        <td>{{ course.course_id }}</td>
        <td>{{ course.name }}</td>
        <td>{{ course.points }}</td>
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

  <div class="field is-horizontal" v-if="currentlySavedCoursesCount > 0">
    <div class="field-label">
      <label class="label">בחר/י את אופן ייבוא הקורסים: </label>
    </div>
    <div class="field-body">
      <div class="field is-narrow">
        <div class="control">
          <label class="radio">
            <input type="radio" v-model="importMode" value="combine">
            מיזוג
          </label>
          <label class="radio">
            <input type="radio" v-model="importMode" value="overwrite">
            החלפה
          </label>
        </div>
      </div>
    </div>
  </div>


  <div class="notification is-danger is-light" v-if="importMode === 'overwrite'">
    <strong>אזהרה:</strong>
    <br/>
    אפשרות זו תמחק את 
    {{ currentlySavedCoursesCount }}
    הקורסים ששמורים במערכת הנוכחית.
  </div>
  <button class="button is-success is-large block" :disabled="!canImport" 
          @click="$emit('import', { courses, importMode })">ייבוא</button>
</div>
</template>

<script>
import { courses as currentCourses } from '@/course-store.js'
export default {
  props: {
    courses: Array,
    totalCourseCount: Number
  },
  emits: ['update:courses', 'import'],
  computed: {
    /** For highlighting courses that originally had no semester specified */
    ambiguousCourses() {
      return this.courses.filter(course => course.ambiguous)
    },

    /** The semester must be set for all courses in order to begin the import */
    canImport() {
      return this.courses.every(course => course.semester)
    },

    /** If the user has already inserted courses before beginning import, 
     *  he'll be offered a choice between combining and overriding his courses.
     */
    currentlySavedCoursesCount() {
      return currentCourses.length
    }
  },
  data() { return {
    importMode: 'combine'
  }
  }
};
</script>

<style>
</style>