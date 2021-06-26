<template>

<div class="columns">
  <div class="column">
    <BarChart/>
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
import BarChart from "../components/BarChart.vue";
import LineChart from "../components/LineChart.vue";

export default {
  name: "Analytics",
  components: { BarChart,LineChart },
  data() {},

  methods: {},
};
</script>

<style>

</style>