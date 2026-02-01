import { createRouter, createWebHistory } from 'vue-router'
import CaseList from '@/views/CaseList.vue'
import CaseInput from '@/views/CaseInput.vue'
import CaseDetail from '@/views/CaseDetail.vue'

const routes = [
  {
    path: '/',
    redirect: '/case-list'
  },
  {
    path: '/case-list',
    name: 'CaseList',
    component: CaseList
  },
  {
    path: '/case-input',
    name: 'CaseInput',
    component: CaseInput
  },
  {
    path: '/case-detail/:id',
    name: 'CaseDetail',
    component: CaseDetail
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
