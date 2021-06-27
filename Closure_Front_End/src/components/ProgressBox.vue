<template>
  <div class="progressbox">
    <br />
    <div class="sub">
      סך הכל:
      <progress class="progress total" v-bind:value="total" max="100">
        15%
      </progress>
    </div>

    <div class="sub">
      חובה:
      <progress class="progress must" v-bind:value="mustValue" max="80">
        15%
      </progress>
    </div>

    <div class="sub">
      חובת בחירה:
      <progress
        class="progress choose_from_list"
        v-bind:value="chooseListValue"
        max="15"
      >
        15%
      </progress>
    </div>

    <div class="sub">
      בחירה:
      <progress class="progress choice" v-bind:value="choiceValue" max="30">
        15%
      </progress>
    </div>
  </div>
</template>
<script>

import { groupBy } from '@/utils.js'


export default {
  props: ["allcourses"],

  computed: {
    total() {
      return this.allcourses.length
    },
    coursesByType() {
      return groupBy(this.allcourses, "type")
    },
    mustValue() {
      return 1 in this.coursesByType ? this.coursesByType[1].length : 0
    },

    chooseListValue() {
      return 2 in this.coursesByType ? this.coursesByType[2].length : 0
    },

    choiceValue() {
      return 3 in this.coursesByType ? this.coursesByType[3].length : 0
    }
  }
};
</script>


<style>
.progress {
  margin-top: 10px;
}

.progressbox {
  font-size: 1rem;
  padding-top: 1rem;
  padding-left: 0.25rem;
  padding-right: 0.25rem;
  padding-bottom: 2rem;
}

.sub {
  padding-top: 0.25rem;
  font-size: 0.75rem;
}

.progress.must::-webkit-progress-value {
  background-color: #bc87d0;
}

.progress.choose_from_list::-webkit-progress-value {
  background-color: #fbaf5d;
}

.progress.choice::-webkit-progress-value {
  background-color: #f06eaa;
}
</style>