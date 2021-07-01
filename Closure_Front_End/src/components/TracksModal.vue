<template>
  <div class="modal">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <label class="modal-card-title menu-label is-size-7"
          ><b>מסלולים</b></label
        >
        <button class="delete is-small" @click="$emit('clickclose')"></button>
      </header>
      <section class="modal-card-body">
        <!-- Content ... -->
        <li
          class="dropdown-item"
          v-for="sugg in suggestions"
          :key="sugg"
          @click="emitClick($event, sugg)"
        >
          {{ sugg.name }}
        </li>
      </section>
      <footer class="modal-card-foot">
        <!-- <button class="button is-success">Save changes</button> -->
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  props: ["url"],
  emits: ["clickclose", "clicksuggestion"],
  data() {
    return {
      suggestions: [],
    };
  },

  created() {
    this.$http
      .get(this.url)
      .then((response) => (this.suggestions = response.data.results));
  },

  methods: {
    emitClick(event, sugg) {
      this.$emit("clicksuggestion", event, sugg);
    },
  },
};
</script>

<style>
.modal-card {
  font-size: 0.75rem;
  max-height: 70vh;
}

.modal-card-head {
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
}

.modal-card-head label {
  margin-top: 0.75rem;
}

.modal-card-body {
  overflow: auto;
}
</style>