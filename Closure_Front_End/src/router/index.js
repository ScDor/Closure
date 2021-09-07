import { createRouter, createWebHistory } from 'vue-router'
import CoursePlan from '../views/CoursePlan.vue'
import Settings from '../views/Settings.vue'
import CourseImport from '../views/CourseImport.vue'
import { routeGuard } from '@/auth/index.js'
import { currentCourseplan } from '@/course-store'

const redirectToCurrentPlan = () => {
  return {
    name: "Course Plan", params: {
      plan_id: currentCourseplan.value?.id ?? "unsaved"
    }
  }
}

const routes = [
  {
    path: '/',
    redirect: redirectToCurrentPlan
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    beforeEnter: routeGuard
  },
  {
    path: '/data-import',
    name: 'Scrape',
    component: CourseImport,
    beforeEnter: routeGuard
  },
  {
    path: '/plans/:plan_id',
    name: 'Course Plan',
    component: CoursePlan
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
