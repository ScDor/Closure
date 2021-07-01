<template>
  <div class="user">
    <div class="notification">
      <ul class="menu-list">
        <li>
          <label class="menu-label">שם משתמש</label>
          <div class="field">{{ name }}</div>
        </li>

        <li>
          <label class="menu-label">מסלול נוכחי</label>
          <div class="field">{{ track.name }}</div>
        </li>

        <li>
          <button class="button field menu-label" @click="showModal = true">
            בחר מסלול חדש מרשימה
          </button>
        </li>

        <tracks-modal
          :class="{ 'is-active': showModal }"
          :url="'tracks/?limit=50&offset=15'"
          @clickclose="showModal = false"
          @clicksuggestion="trackClick"
        ></tracks-modal>
      </ul>
    </div>
  </div>
</template>

<script>
import TracksModal from "./TracksModal.vue";

export default {
  components: { TracksModal },

  data() {
    return {
      showModal: false,
      name: "",
      track: { track_number: 0, name: "לא נבחר מסלול" },
      track_pk: 0,
    };
  },

  created() {
    this.$http.get("/student/me").then((response) => this.getInfo(response));
  },

  methods: {
    /** Get student info from the DB */
    getInfo(student) {
      this.name = student.data.username;
      this.track_pk = student.data.track_pk;
      const curtarck = student.data.track;
      if (curtarck) {
        this.track = curtarck;
      }
    },

    /**  Updates user's track */
    trackClick(event, clickedTrack) {
      // update user track
      this.$root.track = clickedTrack;

      this.showModal = false;
      this.track = clickedTrack;
      this.track_pk = clickedTrack.pk;
      this.$http.post("/student/me/", { track_pk: this.track_pk, courses: [] });
      this.$http.get("/student/me").then(console.log);
    },
  },
};
</script>


<style>
.user .notification {
  margin-top: 3vh;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  padding-left: 0.25rem;
  padding-right: 0.25rem;
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

.user .field {
  font-size: 0.75rem;
  margin: 1rem;
}
</style>