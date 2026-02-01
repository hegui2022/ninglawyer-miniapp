import { createRouter, createWebHistory } from 'vue-router'
import CaseInput from '@/views/CaseInput.vue'

const routes = [
  {
    path: '/',
    redirect: '/case-input'
  },
  {
    path: '/case-input',
    name: 'CaseInput',
    component: CaseInput
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
