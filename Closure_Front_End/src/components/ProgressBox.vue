<template>
  <div class="progressbox">
    <br />
    <div class="sub">
      סך הכל:
      <progress
        class="progress total"
        v-bind:value="sum(1) + sum(2) + sum(3)"
        max="100"
      >
        15%
      </progress>
    </div>

    <div class="sub">
      חובה:
      <progress class="progress must" v-bind:value="sum(1)" max="80">
        15%
      </progress>
    </div>

    <div class="sub">
      חובת בחירה:
      <progress
        class="progress choose_from_list"
        v-bind:value="sum(2)"
        max="15"
      >
        15%
      </progress>
    </div>

    <div class="sub">
      בחירה:
      <progress class="progress choice" v-bind:value="sum(3)" max="30">
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
      choice: 15,
    };
  },

  methods: {
    /**
     * a helper method for grouping courses.
     * will be mostly used to group by type
     */
    groupBy: function (xs, key) {
      return xs.reduce(function (rv, x) {
        (rv[x[key]] = rv[x[key]] || []).push(x);
        return rv;
      }, {});
    },
    /**
     * sums up the total points for a given course type
     */
    sum: function (type) {
      var courses = this.groupBy(this.allcourses, "type");
      // first we need to check if we have a course from this type
      if (type in courses) {
        // if so, we will sum up the points from that course group,
        var sum = 0;
        for (var i = 0; i < courses[type].length; i++) {
          sum += courses[type][i]["points"];
        }
        return sum;
      } else {
        // otherwise we will return 0.
        return 0;
      }
    },
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