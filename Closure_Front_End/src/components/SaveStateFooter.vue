<template>
  <footer class="footer" dir="rtl">

    <div class="content has-text-centered">
      {{ lastSaved }}
      <br/>
      מלוכלך:
      {{ isDirty }}
    </div>

    <div class="content has-text-centered">
      <p>
        פרויקט
        <strong>Closure</strong>
      </p>
    </div>

    <div class="content has-text-centered">
      <a class="button" href="https://github.com/scdor/closure">
        <span class="icon">
          <i class="fab fa-github"></i>
        </span>
        <span>GitHub</span>
      </a>
    </div>
  </footer>
</template>

<script>
import { computed } from 'vue'
import { currentCourseplan, isDirty } from '@/course-store'
export default {
  setup() {
    const lastSaved = computed(() => {
      if (currentCourseplan.value.modified_at) {
        const date = new Date(currentCourseplan.value.modified_at)
        return `נשמר לאחרונה ב${date.toLocaleString()}`
      }
      return "טרם נשמר"
    })
    return {
      isDirty, lastSaved
    }
  }
};
</script>

<style>
</style>