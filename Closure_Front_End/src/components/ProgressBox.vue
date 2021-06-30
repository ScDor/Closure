<template>
  <div class="progressbox">
    <br />

    <div class="sub">
      סך הכל:&ensp; {{ allPoints() }}/{{ 100 }}
      <progress
        class="progress total"
        v-bind:value="allPoints()"
        max="100"
      ></progress>
    </div>

    <div class="sub">
      חובה:&ensp; {{pointsByType(MUST_TYPE)}}/{{80}}
      <progress
        class="progress must"
        v-bind:value="pointsByType(MUST_TYPE)"
        max="80"
      ></progress>
    </div>

    <div class="sub">
       חובת בחירה:&ensp; {{pointsByType(MUST_CHOOSE_LIST_TYPE)}}/{{15}}
      <progress
        class="progress choose_from_list"
        v-bind:value="pointsByType(CHOOSE_LIST_TYPE)"
        max="15"
      ></progress>
    </div>

    <div class="sub">
     בחירה:&ensp; {{pointsByType(CHOICE_TYPE)}}/{{30}}
      <progress
        class="progress choice"
        v-bind:value="pointsByType(CHOICE_TYPE)"
        max="30"
      ></progress>
    </div>

    <div class="sub">
       אבני פינה:&ensp; {{pointsByType(CORNER)}}/{{8}}
      <progress
        class="progress choice"
        v-bind:value="pointsByType(CORNER)"
        max="8"
      ></progress>
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
      MUST_TYPE: 0,
      CHOOSE_LIST_TYPE: 1,
      CHOICE_TYPE: 2,
      CORNER_TYPE: 3,
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
    pointsByType: function (type) {
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
    allPoints: function () {
      return (
        this.pointsByType(this.MUST_TYPE) +
        this.pointsByType(this.CHOOSE_LIST_TYPE) +
        this.pointsByType(this.CHOICE_TYPE) +
        this.pointsByType(this.CORNER_TYPE)
      );
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