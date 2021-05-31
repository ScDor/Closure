<template>
  <p class="menu-label">ניווט</p>
  <ul class="menu-list">
    <li>
      <div class="control has-icons-left has-icons-right is-size-7">
        <input
          class="input is-dark is-size-7"
          type="course"
          placeholder="חפש קורס"
        />
        <span class="icon is-small is-right">
          <i class="fas fa-search"></i>
        </span>
      </div>
    </li>
  </ul>
</template>


<script>
import axios from "axios";
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  
  setup() {
    console.log("hey");
    /* var res =axios.get(
      "http://127.0.0.1:8000/api/v1/courses/?limit=10&offset=10&search=670",
      {
        headers: {
          Authorization: "Token d614bfa8fd3863b6d859f2f16c795c8b775b2243",
        },
      }
    ).then(courses => courses )
    console.log(res); */
    var res  = axios.get(
      "http://127.0.0.1:8000/api/v1/courses/?limit=10&offset=10&search=670",
      {
        headers: {
          Authorization: "Token d614bfa8fd3863b6d859f2f16c795c8b775b2243",
        },
      }
    )
      .then((response) => console.log(response.data.results));
  }
});
</script>
