import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useTemplateStore = defineStore('templates', () => {
  const templates = ref([])
  const loading = ref(false)
  const error = ref(null)

  const extractTemplatePayload = (payload) => payload?.template ?? payload

  const getTemplates = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await api.get('/templates/')
      templates.value = response.data
      return templates.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const getTemplate = async (templateId) => {
    try {
      const response = await api.get(`/templates/${templateId}/`)
      return extractTemplatePayload(response.data)
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const createTemplate = async (templateData) => {
    try {
      const response = await api.post('/templates/create/', templateData)
      const createdTemplate = extractTemplatePayload(response.data)
      templates.value.unshift(createdTemplate)
      return createdTemplate
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const updateTemplate = async (templateId, templateData) => {
    try {
      const response = await api.patch(`/templates/${templateId}/`, templateData)
      const updatedTemplate = extractTemplatePayload(response.data)
      templates.value = templates.value.map((template) =>
        template.id === templateId ? updatedTemplate : template,
      )
      return updatedTemplate
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const deleteTemplate = async (templateId) => {
    try {
      await api.delete(`/templates/${templateId}/`)
      templates.value = templates.value.filter((template) => template.id !== templateId)
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  return {
    templates,
    loading,
    error,
    getTemplates,
    getTemplate,
    createTemplate,
    updateTemplate,
    deleteTemplate,
  }
})
