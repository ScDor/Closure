<template>
  <div class="card">
    <template v-if="loading">
      טוען את קורס
      {{ course.id }}
      ...
      <progress class="progress is-small is-primary" max="100">15%</progress>
    </template>
    <div v-if="error" class="notification is-danger">
      חלה שגיאה בעת טעינת קורס מספר
      {{ course.id }}:
      {{ error }}
    </div>

    <template v-else-if="courses != null && courses.length === 0 && !loading">
      לא נמצא קורס שמספרו
      {{ course.course_id }}
    </template>

    <template v-else>
      <header class="card-header">
        <p class="card-header-title">
          {{ course.course_id }} -
          {{ course.name }}
        </p>
      </header>
      <div class="card-content">
        <div class="content">
          ניתן ב:

          <div class="field is-grouped is-grouped-multiline">
            <div
              class="control"
              v-for="otherCourse in courses"
              :key="otherCourse.id"
            >
              <a
                class="tags has-addons"
                v-if="otherCourse.is_given_this_year"
                @click="$emit('update:course', otherCourse)"
              >
                <span
                  class="tag is-info"
                  :class="{
                    'is-success': course.id === otherCourse.id,
                    'is-info': course.id !== otherCourse.id,
                  }"
                >
                  {{ renderCourseTag(otherCourse) }}
                </span>
              </a>
            </div>
          </div>

          <ul>
            <li>
              נ"ז:
              <strong>{{ course.points }}</strong>
            </li>
            <li v-if="course.type">
              סוג:
              <strong>{{ renderCourseType(course) }}</strong>
            </li>
            <li v-if="course.comment">
              הערות:
              <p>{{ course.comment }}</p>
            </li>
          </ul>
        </div>
      </div>
      <footer class="card-footer">
        <a href="#" class="card-footer-item">גרור</a>
        <a href="#" class="card-footer-item">מחק</a>
      </footer>
    </template>
  </div>
</template>

<script>
import { reactive, watch, toRefs } from "vue";
import {
  MODEL_COURSE_TYPE_TO_STRING,
  MODEL_SEMESTER_TO_STRING,
} from "@/utils.js";
import { getCoursesForID, getCourseTypes } from "@/services/course-service";

function renderCourseTag(course) {
  return `${course.data_year} - ${MODEL_SEMESTER_TO_STRING.get(
    course.semester
  )}`;
}

function renderCourseType(course) {
  return MODEL_COURSE_TYPE_TO_STRING.get(course.type);
}

export default {
  props: {
    course: {
      type: Object,
      required: true,
    },
    track: {
      type: Object,
      required: false,
    },
  },
  emits: ["update:course"],
  setup(props) {
    const state = reactive({
      loading: false,
      courses: [],
      selectedYear: null,
      error: ""
    });

    watch(
      () => [props.course, props.track],
      async ([course, track]) => {
        state.loading = true;
        try {
          let courses = await getCoursesForID(course.course_id);
          if (track != null) {
            const courseTypes = await getCourseTypes(
              courses.map((c) => c.id),
              track.id
            );
            for (const otherCourse of courses) {
              otherCourse.type = courseTypes.get(otherCourse.id);
            }
          }
          state.courses = courses;
        } catch (ex) {
          state.error = ex;
          throw ex;
        } finally {
          state.loading = false;
        }
      },
      { immediate: true }
    );

    return { ...toRefs(state), renderCourseTag, renderCourseType };
  },
};
</script>

<style>
</style>