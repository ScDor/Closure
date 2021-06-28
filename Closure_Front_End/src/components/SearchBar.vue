<template>
  <div class="control has-icons-right">
    <input
      class="input is-dark"
      :placeholder="placeholder"
      v-model="query"
      @keyup="search"
    />

    <span class="icon is-right is-size-7">
      <i class="fas fa-search"></i>
    </span>
  </div>

  <div class="dropdown is-active" :class="{ hide: hide }">
    <div class="dropdown-menu">
      <div class="dropdown-content">
        <li
          class="dropdown-item"
          v-for="sugg in suggestions"
          :key="sugg"
          @click="emitClick($event, sugg)"
        >
          {{ sugg.name }}
        </li>
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
      hide: true,
      query: "",
      suggestions: [],
    };
  },

  methods: /**
   * this method uses the axios package to access our local database, and search
   * courses according to the given query.
   * notice that the drop down menu is hidden unless there are actual restults for the search.
   * more on the implementation of the search on the backend part of the project.
   */ {
    search() {
      this.$http
        .get(this.url + this.query)
        .then((response) => (this.suggestions = response.data.results))
        .then((this.hide = !this.suggestions.length || this.query == ""))
    },

    emitClick(event, sugg) {
      this.hide = true;
      this.query = "";
      this.$emit("clicksuggestion", event, sugg);
    },
  },
};
</script>


<style>
.input {
  min-width: 15.5vw;
  padding: 0.25rem;
  margin: auto;
  margin-top: 0.2rem;
  font-size: 0.75rem;
}

.span {
  font-size: 0.75rem;
}

.dropdown-menu {
  min-width: 15.5vw;
  margin-right: 0.2rem;
}

.dropdown-content {
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
}

.hide {
  display: none;
}

.dropdown-item {
  font-size: 0.75rem;
}

.dropdown-item:hover {
  background: #efefef;
  cursor: pointer;
}
</style>