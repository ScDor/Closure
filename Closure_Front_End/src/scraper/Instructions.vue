<template>
  <div class="container">
    <h2 class="title is-2 has-text-centered">הוראות</h2>

    <ol>
      <li>
        ראשית, יש לגרור את הקישור הבא אל שורת הסימניות:
        <bookmarklet />
      </li>
      <li>
        כעת, יש ללחוץ על הכפתור התחתון על מנט לנווט אל אתר המידע האישי
        <br />
        שימו לב, אין לנווט לאתר בעזרת כרטיסיה נפרדת, אלא בהכרח דרך הכרטיסיה/חלון
        שנפתח עם לחיצת הכפתור למטה
      </li>
      <li>
        כעת, יש ללחוץ על הסימניה מתוך אתר המידע האישי. כשתהליך היבוא יסתיים,
        החלון יסגר באופן אוטומטי.
      </li>
    </ol>
  </div>
</template>

<script>
import Bookmarklet from "./Bookmarklet.vue";
export default {
  components: { Bookmarklet }
};
</script>

<style>
</style>