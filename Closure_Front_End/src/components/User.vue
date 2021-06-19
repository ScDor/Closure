<template>
  <div class="user" dir="rtl">
    <div class="notification has-text-centered">
      <label class="menu-label"><b>הגדרות</b></label>
      <ul class="menu-list">
        <li>
          <label class="menu-label">שם משתמש</label>

          <div class="field">{{ username }}</div>
        </li>

        <li>
          <label class="menu-label">מסלול נוכחי</label>
          <div class="field">מסלול</div>
        </li>

        <li>
          <label class="menu-label">בחר מסלול מרשימה</label>
          <div class="control">
            <!-- <input class="input is-dark" type="text" /> -->
            <search-bar
              :url="'http://127.0.0.1:8000/api/v1/courses/?limit=6&offset=15&search='"
            ></search-bar>
          </div>
        </li>

        <li>
          <div class="control">
            <button class="button menu-label is-dark">שמור</button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import SearchBar from "./SearchBar.vue";

export default {
  props: ["username"],

  components: { SearchBar },

  data() {
    return {};
  },
};
</script>


<style>
.user .notification {
  margin-top: 3vh;
  margin-left: auto;
  margin-right: auto;
  min-width: 300px;
  max-width: 30vw;
  min-height: 30vh;
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.1);
}
/* 
.user input {
  display: block;
  padding: 10px 6px;
  width: 100%;
  box-sizing: border-box;
  border: none;
  border-bottom: 1px solid #ddd;
  background: transparent;
  box-shadow: 0px 0px 0px;
  border-radius: 0rem;
  color: #555;
}

.user input:focus {
  box-shadow: none !important;
} */

.user .is-static {
  border: none;
}

.user li {
  margin: 1.5rem;
}
</style>