import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  const token = ref(localStorage.getItem('token') || null)

  const isAuthenticated = computed(() => !!user.value)

  const login = (userData, userToken) => {
    user.value = userData
    token.value = userToken
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('token', userToken)
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    logout
  }
})
