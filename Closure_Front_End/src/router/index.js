import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Settings from '../views/Settings.vue'
import { routeGuard } from '@/auth/index.js'
import CourseScrapeStatus from '@/scraper/CourseScrapeStatus.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    beforeEnter: routeGuard
  },
  {
    path: '/scrape',
    name: 'Scrape',
    component: CourseScrapeStatus,
    meta: { hideNavbar: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
