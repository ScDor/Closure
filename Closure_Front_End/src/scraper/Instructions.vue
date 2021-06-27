<template>
  <h1 class="title">הוראות</h1>

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
      כעת, כשהחלון של אתר המידע האישי פתוח(וטעון), יש ללחוץ על הסימניה הנ"ל.
      כשתהליך הייבוא יסתיים, החלון יסגר באופן אוטומטי.
    </li>
  </ol>
</template>

<script>
import Bookmarklet from "./Bookmarklet.vue";
export default {
  components: { Bookmarklet }
};
</script>

<style>
</style>