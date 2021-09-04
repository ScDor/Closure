<template>
  State: {{ state }}
  <home v-if="state === States.LOADED" />
  <div v-else class="section" dir="rtl">
    <div class="box" id="loadPlanBox">
      <div class="content loading" v-if="state === States.FETCHING">
        <p>טוען...</p>
        <progress class="progress is-small is-primary" max="100">15%</progress>
      </div>

      <div
        v-if="state === States.NOT_AUTH_OR_DOESNT_EXIST"
        class="notification is-danger"
      >
        הקורס המצויין לא קיים, או שאיננו פומבי. במידה וזהו הקורס שלך, יש להתחבר
        עם החשבון אשר יצר את התכנית.
      </div>

      <div v-if="state === States.UNKNOWN_ERROR" class="notification is-danger">
        <strong>חלה שגיאה</strong>
        <p>{{ error }}</p>
      </div>

      <div
        v-if="isDirty && state === States.AVAILABLE"
        class="notification is-warning"
      >
        <strong>אזהרה</strong>
        <p>
          תכנית הלימודים הנוכחית טרם נשמרה. פתיחת תכנית חדשה תגרום לאובדן
          השינויים/התכנית הנוכחית.
        </p>
        <div class="buttons">
          <button class="button is-danger" @click="ignorePrompt = true">
            טען/י בכל זאת
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute } from "vue-router";
import { reactive, inject, toRefs, watch } from "vue";
import { loadPlan, currentCourseplan, isDirty } from "@/course-store.js";
import Home from "@/views/Home.vue";

const States = {
  UNDEFINED: "undefined",
  FETCHING: "fetching",
  NOT_AUTH_OR_DOESNT_EXIST: "not_auth_or_does_not_exist",
  AVAILABLE: "available",
  LOADED: "loaded",
  UNKNOWN_ERROR: "unkown_error",
};

export default {
  components: { Home },
  setup() {
    const { student } = toRefs(inject("studentAndClaims"));
    const state = reactive({
      fetchedCourseplan: null,
      state: States.UNDEFINED,
      error: "",
      ignorePrompt: false,
    });

    const http = inject("http");
    const onNavigateToPlan = async (planId) => {
      console.log("onNavigateToPlan: planId:", planId);
      if (currentCourseplan.value?.id === planId) {
        console.log("onNavigateToPlan: plan unchanged");
        return;
      }
      if (planId === "unsaved") {
        console.log("onNavigateToPlan: unsaved plan");
        console.assert(
          currentCourseplan.value?.owner === undefined,
          "Can go to unsaved plan only if the current plan isn't saved"
        );
        state.state = States.LOADED;
        return;
      }
      state.state = States.FETCHING;
      state.error = "";
      try {
        const res = await http.get(`/course_plans/${planId}`);
        state.fetchedCourseplan = res.data;
        console.log("onNavigateToPlan: fetched", res.data);
        console.log("onNavigateToPlan: student", JSON.stringify(student));

        state.ignorePrompt = false;
        state.state = States.AVAILABLE;
      } catch (ex) {
        if (ex.response.status === 404) {
          state.state = States.NOT_AUTH_OR_DOESNT_EXIST;
        } else {
          state.state = States.UNKNOWN_ERROR;
          state.error = ex.toString();
        }
      }
    };

    watch(
      [() => state.ignorePrompt, isDirty, () => state.state],
      async ([ignorePrompt, dirty, curState]) => {
        if (curState === States.AVAILABLE && (!dirty || ignorePrompt)) {
          console.log("watch - loading plan", state.fetchedCourseplan);
          await loadPlan(state.fetchedCourseplan);
          state.state = States.LOADED;
        }
      }
    );

    const route = useRoute();
    onNavigateToPlan(route.params["plan_id"]);

    watch(
      () => route.params["plan_id"],
      (planId) => onNavigateToPlan(planId)
    );

    return {
      student,
      ...toRefs(state),
      States,
      isDirty,
    };
  },
};
</script>

<style>
#loadPlanBox {
  display: flex;
  flex-direction: column;
  text-align: center;
}
</style>