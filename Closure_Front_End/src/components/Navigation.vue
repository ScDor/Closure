<template>
  <p class="menu-label">ניווט</p>

  <div class="dropdown is-active">
    <div class="dropdown-trigger">
      <div class="field">
        <div class="control has-icons-left has-icons-right is-size-7">
          <input
            class="input is-dark is-size-7"
            type="course"
            placeholder="חפש קורס"
            v-model="query"
            @keyup="searchCourses"
          />
          <span class="icon is-small is-right">
            <i class="fas fa-search"></i>
          </span>
        </div>
      </div>
    </div>

    <div class="dropdown-menu" id="dropdown-menu" role="menu">
      <div class="dropdown-content">
        <a class="dropdown-item" v-for='item in info'>{{item}}</a>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
// import { Navigation } from "@vue/composition-api";

export default({
  data() {
    return {
      info: null,
      query: "",
    };
  },

  methods: {
    searchCourses() {
      axios
        .get(
          "http://127.0.0.1:8000/api/v1/courses/?limit=15&offset=15&search=" +
            this.query,
          {
            headers: {
              Authorization: "Token d614bfa8fd3863b6d859f2f16c795c8b775b2243",
            },
          }
        )
        .then((response) => (this.info = response.data.results));
        
      /* if (this.info) {
        this.info.forEach((element) => {
          console.log(element);
        });
      } */
    },
  },

  setup() {
    /* var res =axios.get(
      "http://127.0.0.1:8000/api/v1/courses/?limit=10&offset=10&search=670",
      {
        headers: {
          Authorization: "Token d614bfa8fd3863b6d859f2f16c795c8b775b2243",
        },
      }
    ).then(courses => courses )
    console.log(res); */
  },
});
</script>
