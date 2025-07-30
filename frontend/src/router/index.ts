import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('../views/Projects.vue')
  },
  {
    path: '/papers',
    name: 'Papers',
    component: () => import('../views/Papers.vue')
  },
  {
    path: '/patents',
    name: 'Patents',
    component: () => import('../views/Patents.vue')
  },
  {
    path: '/team',
    name: 'Team',
    component: () => import('../views/Team.vue')
  },
  {
    path: '/funding',
    name: 'Funding',
    component: () => import('../views/Funding.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
    