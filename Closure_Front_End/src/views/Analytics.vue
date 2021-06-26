<template>

<div class="columns">
  <div class="column">
    <PieChart/>
  </div>
  <div class="column">
    <LineChart/>
  </div>
  <div class="column">
  </div>
  <div class="column">
  </div>
</div>


</template>

<script>
import PieChart from "../components/PieChart.vue";
import LineChart from "../components/LineChart.vue";

export default {
  name: "Analytics",
  components: { PieChart,LineChart },
  data() {},

  methods: {},
};
</script>

<style>

</style>