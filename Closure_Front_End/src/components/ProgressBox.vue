<template>
  <div class="progressbox">
    <br />
    <div class="sub">
      סך הכל:
      <progress class="progress total" v-bind:value="sum(allcourses,1)+sum(allcourses,2)+sum(allcourses,3)" max="100">
        15%
      </progress>
    </div>

    <div class="sub">
      חובה:
      <progress class="progress must" v-bind:value="sum(allcourses,1)" max="80">
        15%
      </progress>
    </div>

    <div class="sub">
      חובת בחירה:
      <progress
        class="progress choose_from_list"
        v-bind:value="sum(allcourses,2)"
        max="15"
      >
        15%
      </progress>
    </div>

    <div class="sub">
      בחירה:
      <progress class="progress choice" v-bind:value="sum(allcourses,3)" max="30">
        15%
      </progress>
    </div>
  </div>
</template>
<script>
export default {
  props: ["allcourses"],

  data() {
    return {
      total: 50,
      mandatory: 30,
      mand_choice: 20,
      choice: 15
    };
  },

  methods: {
    groupBy: function (xs, key) {
      return xs.reduce(function (rv, x) {
        (rv[x[key]] = rv[x[key]] || []).push(x);
        return rv;
      }, {});
    },
    sum: function(allcourses, index){
      var courses = this.groupBy(this.allcourses, "type")[index];
      var sum = 0;
      for (var i = 0; i<courses.length; i++)
      {
        sum += courses[i]["points"];
      }
      console.log(sum);
      return sum;
      
    }
  },
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