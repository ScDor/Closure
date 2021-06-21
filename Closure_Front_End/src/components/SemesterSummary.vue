<template>
  <div class="semester-summary">
    <div class="box semester-summary-style">
      <div class="media">
        <div class="media-content">סה"כ סמסטריאלי</div>

        <div class="media-left">{{ sumPoints }}</div>

        <div class="media-left">נ"ז</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["courses"],

  computed: {
    sumPoints() {
      return this.courses.reduce((partial_sum, c) => partial_sum + c.points, 0);
    },
  },
};
</script>

<style>
.semester-summary-style {
  padding: 0.25rem;
  margin: 0.25rem;
  box-shadow: 0px 0px 0px 0px;
  font-size: 0.75rem;
  background: lightgray;
  color: white;
  margin-bottom: 0rem;
}
.media-content {
  margin-right: 0.3rem;
}
.media-left {
  margin-left: 0.2rem;
  margin-right: 0.5rem;
}
</style>