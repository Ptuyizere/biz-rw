import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api'
import { getErrorMessage } from '@/api/axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const token = ref(localStorage.getItem('access_token') || null)
  const loading = ref(false)
  const error = ref(null)

  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.is_admin === true)

  function setAuth(data) {
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
  }

  function clearAuth() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  async function register(payload) {
    loading.value = true
    error.value = null
    try {
      const { data } = await authApi.register(payload)
      setAuth(data)
      return { success: true }
    } catch (err) {
      error.value = getErrorMessage(err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function login(payload) {
    loading.value = true
    error.value = null
    try {
      const { data } = await authApi.login(payload)
      setAuth(data)
      return { success: true }
    } catch (err) {
      error.value = getErrorMessage(err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  function logout() {
    clearAuth()
  }

  async function refreshMe() {
    try {
      const { data } = await authApi.me()
      user.value = data
      localStorage.setItem('user', JSON.stringify(data))
    } catch {
      clearAuth()
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isLoggedIn,
    isAdmin,
    register,
    login,
    logout,
    refreshMe,
  }
})
