<template>
  <div class="user" dir="rtl">
    <div class="notification has-text-centered">
      <figure class="image container is-128x128" v-if="idClaims.picture">
        <img class="is-rounded" :src="idClaims.picture">
      </figure>
      <label class="menu-label"><b>הגדרות</b></label>
      <ul class="menu-list">
        <li>
          <label class="menu-label">שם משתמש</label>
          <div class="field">{{ student.username }}</div>
        </li>

        <li>
          <label class="menu-label">שם</label>
          <div class="field">{{ idClaims.name }}</div>
        </li>

        <li>
          <label class="menu-label">מסלול נוכחי</label>
          <div class="field">{{ track }} </div>
        </li>


        <li>

          <label class="menu-label">שנת תחילת לימודים</label>
          <year-selection v-model="selectedYear" @update:modelValue="() => newTrack = null"/>
        </li>

        <li>

          <label class="menu-label">בחר מסלול מרשימה</label>
          <div class="control">
            <!-- <input class="input is-dark" type="text" /> -->
            <search-bar
              :url="`http://127.0.0.1:8000/api/v1/tracks/?limit=6&offset=15&data_year=${selectedYear}&search=`"
              :resultToString="track => track.name"
              v-model="newTrack"
            ></search-bar>
          </div>
        </li>

        <li>
          <div class="control">
            <button :disabled="!newTrack" class="button menu-label is-dark" :class="{'is-loading': saving}" @click="$emit('onSave', $event, newTrack)">
              שמירה
            </button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import SearchBar from "./SearchBar.vue";
import YearSelection from './YearSelection.vue'

export default {
  props: {
    idClaims: Object,
    student: Object,
    saving: Boolean
  },
  emits: [ "onSave" ],
  components: { SearchBar, YearSelection },

  data() {
    return {
      newTrack: null,
      selectedYear: 2022
    };
  },

  computed: {
    track() {
      if (this.student.track) {
        return this.student.track.name;
      }
      return "לא ידוע";
    }
  }
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

.user .field {
  font-size: 0.75rem;
  margin: 0.75rem;
}
</style>