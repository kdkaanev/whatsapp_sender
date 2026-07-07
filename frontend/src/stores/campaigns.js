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
      campaigns.value.push(response.data.campaign)
      return response.data.campaign
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const updateCampaign = async (campaignId, campaignData) => {
    try {
      const response = await api.patch(`/campaigns/${campaignId}/`, campaignData)
      const updatedCampaign = response.data.campaign

      campaigns.value = campaigns.value.map((campaign) =>
        campaign.id === campaignId ? updatedCampaign : campaign
      )

      return updatedCampaign
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const deleteCampaign = async (campaignId) => {
    try {
      await api.delete(`/campaigns/${campaignId}/`)
      campaigns.value = campaigns.value.filter((campaign) => campaign.id !== campaignId)
    } catch (err) {
      error.value = err.message
      throw err
    }
  } 

  const sendSMS = async (campaignId, messageBody) => {
    try {
      const response = await api.post(`/campaigns/${campaignId}/send-sms/`, { message: messageBody })
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const sendWhatsApp = async (campaignId, messageBody) => {
    try {
      const response = await api.post(`/campaigns/${campaignId}/send-whatsapp/`, { message: messageBody })
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
    updateCampaign,
    deleteCampaign,
    sendSMS,
    sendWhatsApp,
    getStatistics,
    getMessages,
    getTaskStatus,
  }
})
