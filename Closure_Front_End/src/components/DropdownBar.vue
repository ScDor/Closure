<template>
  <div class="dropdown-bar">
    <div class="dropdown" :class="{ 'is-active': isDropdownActive }">
      <div
        class="dropdown-trigger"
        @click="isDropdownActive = !isDropdownActive"
      >
        <a aria-haspopup="true" aria-controls="{ 'dropdown-menu' }">
          <span class="menu-label">{{ placeholder }}</span>
          <span class="icon is-small is-size-7">
            <i class="fa fa-angle-down" aria-hidden="true"></i>
          </span>
        </a>
      </div>
      <div class="dropdown-menu" id="dropdown-menu" role="menu">
        <div class="dropdown-content">
          <!-- items -->
          <li
            class="dropdown-item"
            v-for="sugg in suggestions"
            :key="sugg"
          >
            {{ sugg.name }}
          </li>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  props: ["placeholder", "url"],
  emits: ["clicksuggestion"],

  data() {
    return {
      isDropdownActive: false,
      suggestions: [],
    };
  },

  created() {
    this.$http
      .get(this.url)
      .then((response) => (this.suggestions = response.data.results))
      .then(console.log);
  },

  methods: {
    emitClick(event, sugg) {
      this.isDropdownActive = false;
      this.$emit("clicksuggestion", event, sugg);
    },
  },
};
</script>


<style>
.span {
  font-size: 0.75rem;
}

.dropdown-content {
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
  max-height: 15em;
  overflow: auto;
}

.dropdown-item {
  font-size: 0.75rem;
}

.dropdown-item:hover {
  background: #efefef;
  cursor: pointer;
}
</style>