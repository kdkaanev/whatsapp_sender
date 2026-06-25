import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useContactStore = defineStore('contacts', () => {
  const contacts = ref([])
  const loading = ref(false)
  const error = ref(null)

  const getContacts = async ({ search = '', tag = '' } = {}) => {
    loading.value = true
    error.value = null
    try {
      const params = {}
      if (search) params.search = search
      if (tag) params.tag = tag
      const response = await api.get('/contacts/', { params })
      contacts.value = response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const showAllContacts = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/contacts/')
      contacts.value = response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const createContact = async (contactData) => {
    try {
      const response = await api.post('/contacts/create/', contactData)
      contacts.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const updateContact = async (id, contactData) => {
    try {
      const response = await api.patch(`/contacts/${id}/`, contactData)
      const index = contacts.value.findIndex((c) => c.id === id)
      if (index !== -1) {
        contacts.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const deleteContact = async (id) => {
    try {
      await api.delete(`/contacts/${id}/`)
      contacts.value = contacts.value.filter((c) => c.id !== id)
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const importContacts = async (file) => {
    try {
      const formData = new FormData()
      formData.append('file', file)
      const response = await api.post('/contacts/import/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      await getContacts()
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  return {
    contacts,
    loading,
    error,
    getContacts,
    createContact,
    updateContact,
    deleteContact,
    importContacts,
    showAllContacts
  }
})
