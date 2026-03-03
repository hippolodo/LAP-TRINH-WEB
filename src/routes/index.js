import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import LoginPage from '../pages/LoginPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
