<template>
  <div id="courseScrapeRoot" class="box block has-text-centered" dir="rtl">
    <h1 class="title">ייבוא קורסים מהאוניברסיטה</h1>

    <div v-if="status === 'initializing'">
      <h2 class="subtitle">מאתחל...</h2>
      <progress class="progress is-primary max=100" >15%</progress>
    </div>

    <div v-if="status === 'startedFetching'">
      <h2 class="subtitle">מחלץ קורסים מאתר האוניברסיטה</h2>
      <progress class="progress is-primary max=100" >15%</progress>
    </div>

    <div v-if="errors.length > 0">
    <div v-for="error in errors" :key="error.message" class="notification is-danger">
      <strong>שגיאה:</strong>
      <br/>
      {{ error.message }}
      <br/>
      <strong>פרטים טכניים:</strong>
      <br/>
      {{ error.detail }}
    </div>
    </div>

    <div v-if="warnings.length > 0">
      <div v-for="warning in warnings" :key="warning.message" class="notification is-warning">
      <strong>אזהרה:</strong>
      <br/>
      {{ warning.message }}
      <br/>
      <strong>פרטים טכניים:</strong>
      <br/>
      {{ JSON.stringify(warning.exception) }}
      </div>
    </div>

    <div v-if="status === 'ready'">
      <button class="button is-large is-primary" @click="beginScrapeHandler">התחלה</button>
    </div>

    <div v-if="status === 'finished'">
      <button class="button is-large is-success" @click="continueHandler">המשך מהאתר</button>
    </div>
  </div>
</template>

<script>

import { reactive, toRefs } from 'vue'
import { install } from './course-scrape-communication.js'
import { warnings, ScrapeError } from './course-scrape-errors.js'
import { fetchCoursesAndGradesDocument, beginScrape } from './course-scrape-logic.js'


export default {
  setup() {

    const state = reactive({
      status: "initializing",
      errors: []
    })

    const nonReactiveState = {
    }

    const handleException = (ex) => {
      console.error(ex)
      state.status = "error"

      if (ex instanceof ScrapeError) {
        state.errors.push({
          message: ex.message,
          detail: ex.cause.toString()
        })
      } else {
        state.errors.push({
          message: "שגיאה כלשהי",
          detail: ex.toString()
        })
      }
    }



    Promise.all([
      fetchCoursesAndGradesDocument(document),
      install()
    ]).then(([gradesDocument, opener])   => {
      nonReactiveState.opener = opener
      nonReactiveState.gradesDocument = gradesDocument
      state.status = "ready"
    }, handleException)

    const beginScrapeHandler = async () => {
      try {
        state.status = "startedFetching"
        await beginScrape(nonReactiveState.gradesDocument)
        state.status = "finished"
      } catch (ex) {
        handleException(ex)
      }
    }

    const continueHandler = () => {
      window.blur()
      nonReactiveState.opener.focus()
      window.close()
    }

    return { ...toRefs(state), beginScrapeHandler, warnings, continueHandler }
  }
}
</script>

<style scoped>
  @import "https://cdn.jsdelivr.net/npm/bulma@0.9.2/css/bulma-rtl.min.css";
  #courseScrapeRoot {
    margin: 5vh 5vw 5vh 5vw;
  }
</style>