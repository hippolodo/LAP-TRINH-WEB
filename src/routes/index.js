import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import LoginPage from '../pages/LoginPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import AppointmentBooking from '../features/appointments/AppointmentBooking.vue'
import AppointmentList from '../features/appointments/AppointmentList.vue'
import ProfilePage from '../pages/ProfilePage.vue'

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
  {
    path: '/appointments',
    name: 'AppointmentBooking',
    component: AppointmentBooking
  },
  {
    path: '/my-appointments',
    name: 'AppointmentList',
    component: AppointmentList
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfilePage
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
