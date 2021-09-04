<template>
  <div class="field">
    <label v-if="label" class="label">{{ label }}</label>
    <div class="control">
      <div class="field has-addons">
        <div class="control is-expanded">
          <input class="input" type="text" :value="url" disabled />
        </div>
        <div class="control">
          <button class="button" @click="copy">
            <i class="fas fa-copy"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from "vue";
import router from '@/router';
export default {
  props: {
    routeName: String,
    routeParams: {
        type: Object, required: false
    },
    label: {
      type: String,
      required: false,
    },
  },
  setup(props) {
    const base = import.meta.env.VITE_AUTH0_REDIRECT_URI;
    const href = computed(() => router.resolve({ name: props.routeName, params: props.routeParams}).href)
    const url = computed(() => new URL(href.value, base).toString());

    const copy = async () => {
      await navigator.clipboard.writeText(url.value);
    };

    return { url, copy };
  },
};
</script>

<style>
</style>