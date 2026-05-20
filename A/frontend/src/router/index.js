import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Cats from '../views/Cats.vue'
import Feeding from '../views/Feeding.vue'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/cats',
    name: 'cats',
    component: Cats,
    meta: { requiresAuth: true }
  },
  {
    path: '/feeding',
    name: 'feeding',
    component: Feeding,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/')
  } else {
    next()
  }
})

export default router
