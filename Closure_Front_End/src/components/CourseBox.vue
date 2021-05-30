<template>
  <div class="course-box">
    <div class="box box-style">
      {{ name }}
    </div>
  </div>
</template>

<script>
export default {
  props: ["name"],
};
</script>

<style>
.box-style {
  padding: 0.25rem;
  box-shadow: 0px 0px 0px 0px;
  font-size: 0.75rem;
}
/* .course-box:hover {
  cursor: grab;
} */
</style>