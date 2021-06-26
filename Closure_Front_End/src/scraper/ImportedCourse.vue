<template>
  <span>{{ course.course_id }} - {{ course.name }}</span>
</template>

<script>
import { API_SEMESTER_TO_PROP_INT, isString } from "@/utils.js";
export default {
  props: {
    course: {
      type: Object,
      validator(value) {
        const cid = "course_id" in value && typeof value.course_id === "number";
        const name = "name" in value && isString(value.name);
        const semester =
          "semester" in value &&
          isString(value.semester) &&
          API_SEMESTER_TO_PROP_INT.has(value.semester);
        return cid && name && semester;
      }
    }
  }
};
</script>

<style>
</style>