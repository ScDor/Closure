<template>
  <a :href="url">יבוא נתונים מהאוניברסיטה </a>
</template>

<script>
export default {
  data() {
    const FULL_PATH = process.env.VUE_APP_AUTH0_REDIRECT_URI;
    const raw = `javascript:(function(){
                         var script=document.createElement('SCRIPT');
                         script.src='${FULL_PATH}/course-scrape.umd.js';
                         script.id='courseScrapeBookmarklet';
                         document.body.appendChild(script);
                         })();
                        `;
    const url = encodeURI(raw);
    return {
      url
    };
  }
};
</script>

<style>
</style>