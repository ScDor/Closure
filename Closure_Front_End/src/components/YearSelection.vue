<template>
  <div class="field">
    <label class="label" v-if="label">{{ label }}</label>
    <div class="control">
      <vue-multiselect
        v-model="optionModel"
        :modelValue="optionModel"
        @update:modelValue="
          (newOpt) => $emit('update:modelValue', newOpt?.value)
        "
        placeholder="לא נבחרה שנה"
        :options="supportedYears"
        :searchable="true"
        :internal-search="true"
        label="label"
        track-by="value"
      >
        <template #noOptions> יש להזין שם מסלול </template>

        <template #noResult> לא נמצא מסלול עם השם הנ"ל </template>
      </vue-multiselect>
    </div>
  </div>
</template>

<script>
import VueMultiselect from "vue-multiselect";
import { computed } from "vue";

const supportedYears = [
  { value: 2017, label: '2016-2017 תשע"ז' },
  { value: 2018, label: '2017-2018 תשע"ח' },
  { value: 2019, label: '2018-2019 תשע"ט' },
  { value: 2020, label: '2019-2020 תש"ף' },
  { value: 2021, label: '2020-2021 תשפ"א' },
  { value: 2022, label: '2021-2022 תשפ"ב' },
];

export default {
  props: {
    modelValue: {
      type: Number
    },
    label: {
      type: String,
      required: false,
    },
  },
  emits: ["update:modelValue"],
  components: { VueMultiselect },
  setup(props, { emit }) {
    const modelToOption = new Map(
      supportedYears.map((option) => [option.value, option])
    );

    const optionModel = computed({
      get() {
        return modelToOption.get(props.modelValue);
      },
      set(selectedOption) {
        emit("update:modelValue", selectedOption?.value ?? undefined);
      },
    });
    return { supportedYears, optionModel };
  },
};
</script>

<style>
</style>