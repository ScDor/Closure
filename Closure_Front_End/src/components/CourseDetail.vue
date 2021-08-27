<template>

<div class="card">
  <header class="card-header">
    <p class="card-header-title">
        {{ course.course_id}} - 
        {{ course.name }}
    </p>
    <button class="card-header-icon" aria-label="more options">
      <span class="icon">
        <i class="fas fa-angle-down" aria-hidden="true"></i>
      </span>
    </button>
  </header>
  <div class="card-content">
    <div class="content">
    
      <ul>
          <li>
              משנתון:
              <strong>{{ course.data_year}}</strong>
          </li>
          <li>
              סמסטר:
              <strong> {{ courseSemester }}</strong>
          </li>
          <li>
              נ"ז:
              <strong>{{ course.points}}</strong>
          </li>
          <li>
              סוג:
              <strong>{{courseType}}</strong>
          </li>
          <li>
              הערות:
              <p>{{course.comment}}</p>
          </li>

          <li> {{ JSON.stringify({...course, comment: ""}) }} </li>
      </ul>
    </div>
  </div>
  <footer class="card-footer">
    <a href="#" class="card-footer-item">גרור</a>
    <a href="#" class="card-footer-item">מחק</a>
  </footer>
</div>
</template>

<script>
import { MODEL_COURSE_TYPE_TO_STRING, MODEL_SEMESTER_TO_STRING } from '@/utils.js'
export default {
    props: {
        course: Object
    },
    computed: {
        courseType() {
            if (MODEL_COURSE_TYPE_TO_STRING.has(this.course.type)) {
                return MODEL_COURSE_TYPE_TO_STRING.get(this.course.type);
            }
            return "לא מוגדר";
        },
        courseSemester() {
            if (MODEL_SEMESTER_TO_STRING.has(this.course.semester)) {
                return MODEL_SEMESTER_TO_STRING.get(this.course.semester);
            }
            return "לא מוגדר";
        }
    }
}
</script>

<style>

</style>