<template>
  <a :href="url">ייבוא נתונים מהאוניברסיטה </a>
</template>

<script>
export default {
  data() {
    // TODO: rename "VUE_APP_AUTH0_REDIRECT_URI" to be more informative
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