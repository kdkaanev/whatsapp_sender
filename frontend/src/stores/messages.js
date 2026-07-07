import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useMessageStore = defineStore('messages', () => {
  const messages = ref([])
  const loading = ref(false)
  const error = ref(null)

  const getMessages = async ({ campaignId = null, status = '' } = {}) => {
    loading.value = true
    error.value = null
    try {
      const params = {}
      if (campaignId !== null && campaignId !== undefined) {
        params.campaign_id = campaignId
      }
      if (status) {
        params.status = status
      }

      const response = await api.get('/messages/', { params })
      messages.value = Array.isArray(response.data) ? response.data : []
      return messages.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    messages,
    loading,
    error,
    getMessages,
  }
})
