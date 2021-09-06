<template>
  <div class="box box-style">
    <div class="media">
      <course-color-circle :courseType="course.type" />

      <div class="media-content">
        {{ course.name }}
      </div>

      <div class="media-left">
        {{ course.points }}
      </div>

      <div class="media-left" @click="$emit('clickclose', $event, course)">
        <span class="icon is-small is-left is-size-7">
          <i class="fas fa-times-circle"></i>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import CourseColorCircle from './CourseColorCircle.vue'

export default {
  props: {
    course: {
      type: Object, required: true
    }
  },
  emits: ['clickclose'],
  components: { CourseColorCircle },
};
</script>

<style scoped>
.box-style {
  padding: 0.25rem;
  box-shadow: 0px 0px 0px 0px;
  font-size: 0.75rem;
}

.box:hover {
  box-shadow: 1px 1px 1px 0px rgb(231, 231, 231);
}

.media-left .icon {
  opacity: 30%;
}

.fa-times-circle:hover {
  cursor: pointer;
}
</style>