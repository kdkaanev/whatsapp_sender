import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))

  const isAuthenticated = computed(() => !!accessToken.value)

  const register = async (email, password) => {
    try {
      const response = await api.post('/auth/register/', {
        email,
        password,
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  const login = async (email, password) => {
    try {
      const response = await api.post('/auth/login/', {
        email,
        password,
      })
      accessToken.value = response.data.access
      refreshToken.value = response.data.refresh
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      await getProfile()
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  const getProfile = async () => {
    try {
      const response = await api.get('/auth/profile/')
      user.value = response.data
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  const logout = () => {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    register,
    login,
    getProfile,
    logout,
  }
})
