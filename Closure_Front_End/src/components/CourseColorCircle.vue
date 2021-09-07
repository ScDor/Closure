<template>
  <span class="icon is-small is-right is-size-7" :class="colorClass">
    <i class="fas fa-circle" ></i>
  </span>
</template>

<script>
import { computed } from "vue";
export default {
  props: {
    courseType: {
      type: String,
      required: false,
    },
  },
  setup(props) {
    const colorClass = computed(() => {
      switch (props.courseType) {
        case "MUST":
          return "must";
        case "CHOICE":
          return "choice";
        case "CHOOSE_FROM_LIST":
          return "choose_from_list";
        case "CORNER_STONE":
          return "corner_stone";
        case "SUPPLEMENTARY":
          return "supplementary";
        default:
          return "supplementary";
      }
    });
    return { colorClass }
  },
};
</script>

<style scoped>
.must {
  color: #bc87d0;
}

.choose_from_list {
  color: #fbaf5d;
}

.corner_stone {
  color: #69d85e;
}

.supplementary {
  color: #bfbfbf;
}

.choice {
  color: #f06eaa;
}
</style>