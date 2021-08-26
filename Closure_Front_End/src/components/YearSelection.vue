<template>
  <div class="field">
    <label class="label">גרסאת שנתון</label>
    <div class="control">
      <div class="select">
        <select
          :value="modelValue"
          @input="$emit('update:modelValue', $event.target.value)"
        >
          <option v-for="year in availableYears" :key="year">{{ year }}</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["modelValue"],
  emits: ["update:modelValue"],
  data() {
    return {
      availableYears: [2017, 2018, 2019, 2020, 2021, 2022],
    };
  },
};
</script>

<style>
</style>