<template>
  <div class="modal" :class="{ 'is-active': active }">
    <div class="modal-background" @click="$emit('close')"></div>
    <div class="modal-content">
      <slot v-if="active"/>
    </div>
    <button
      class="modal-close is-large"
      aria-label="close"
      @click="$emit('close')"
    ></button>
  </div>
</template>

<script>
export default {
  props: {
    active: Boolean,
  },
  emits: ["close"],
};
</script>

<style>
</style>