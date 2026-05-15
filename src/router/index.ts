import { createRouter, createWebHistory } from 'vue-router'

import Login from '@/views/LoginPage.vue'
import AppButtonDisplay from '@/views/AppButtonDisplayPage.vue'
import AppCardDisplay from '@/views/AppCardDisplayPage.vue'
import Components from '@/views/Components.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/Components',
    name: 'Components',
    component: Components,
    children: [
      {
        path: 'AppButtonDisplay',
        name: 'AppButtonDisplay',
        component: AppButtonDisplay
      },
      {
        path: 'AppCardDisplay',
        name: 'AppCardDisplay',
        component: AppCardDisplay
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

export default router
