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
          <div class="control" >
            <multiselect
              placeholder="חיפוש מסלול"
              v-model="newTrack"
              searchable
              :delay="0"
              :minChars="1"
              :resolveOnLoad="false"
              :options="fetchTracks"
            />
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
import YearSelection from './YearSelection.vue'
import Multiselect from '@vueform/multiselect';
import { fetchDjangoListIntoSelectOptions } from '@/utils.js';

export default {
  props: {
    idClaims: Object,
    student: Object,
    saving: Boolean
  },
  emits: [ "onSave" ],
  components: { YearSelection, Multiselect},
  inject: [ "http"],

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
  },

  methods: {
    async fetchTracks(query) {
      const url = `tracks/?limit=6&offset=15&data_year=${this.selectedYear}&search=${query}`;
      return await fetchDjangoListIntoSelectOptions(this.http, url, track => track.name);
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
<style src="@vueform/multiselect/themes/default.css"></style>