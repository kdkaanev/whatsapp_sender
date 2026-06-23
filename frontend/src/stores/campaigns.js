import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useCampaignStore = defineStore('campaigns', () => {
  const campaigns = ref([])
  const loading = ref(false)
  const error = ref(null)

  const getCampaigns = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/campaigns/')
      campaigns.value = response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const getCampaign = async (id) => {
    try {
      const response = await api.get(`/campaigns/${id}/`)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const createCampaign = async (campaignData) => {
    try {
      const response = await api.post('/campaigns/create/', campaignData)
      campaigns.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const sendSMS = async (campaignId) => {
    try {
      const response = await api.post(`/campaigns/${campaignId}/send-sms/`)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const sendWhatsApp = async (campaignId) => {
    try {
      const response = await api.post(`/campaigns/${campaignId}/send-whatsapp/`)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const getStatistics = async (campaignId) => {
    try {
      const response = await api.get(`/campaigns/${campaignId}/statistics/`)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const getMessages = async (campaignId) => {
    try {
      const response = await api.get(`/campaigns/${campaignId}/messages/`)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const getTaskStatus = async (taskId) => {
    try {
      const response = await api.get(`/tasks/${taskId}/`)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  return {
    campaigns,
    loading,
    error,
    getCampaigns,
    getCampaign,
    createCampaign,
    sendSMS,
    sendWhatsApp,
    getStatistics,
    getMessages,
    getTaskStatus,
  }
})
