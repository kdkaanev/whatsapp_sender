<script setup>
import { computed, onMounted, ref } from 'vue'
import { useTemplateStore } from '../stores/templates'

const templateStore = useTemplateStore()

const searchQuery = ref('')
const sortBy = ref('Newest')
const viewMode = ref('grid')
const currentPage = ref(1)
const pageSize = 8
const activeMenuId = ref(null)

const isPageLoading = ref(false)
const pageError = ref('')
const selectedTemplate = ref(null)
const isCreateMode = ref(false)
const isSavingTemplate = ref(false)
const isDeletingTemplate = ref(false)
const modalError = ref('')
const modalMessage = ref('')
const templateForm = ref({
  name: '',
  content: '',
})

const sortOptions = ['Newest', 'Oldest', 'Alphabetical', 'Longest', 'Shortest']

const normalizeTemplate = (template) => ({
  ...template,
  name: template.name ?? 'Untitled template',
  content: template.content ?? '',
})

const normalizedTemplates = computed(() => templateStore.templates.map(normalizeTemplate))

const filteredTemplates = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  let list = normalizedTemplates.value.filter((template) => {
    if (!query) return true
    return (
      template.name.toLowerCase().includes(query) ||
      template.content.toLowerCase().includes(query)
    )
  })

  if (sortBy.value === 'Alphabetical') {
    list = [...list].sort((a, b) => a.name.localeCompare(b.name))
  } else if (sortBy.value === 'Oldest') {
    list = [...list].sort((a, b) => a.id - b.id)
  } else if (sortBy.value === 'Longest') {
    list = [...list].sort((a, b) => b.content.length - a.content.length)
  } else if (sortBy.value === 'Shortest') {
    list = [...list].sort((a, b) => a.content.length - b.content.length)
  } else {
    list = [...list].sort((a, b) => b.id - a.id)
  }

  return list
})

const totalTemplates = computed(() => filteredTemplates.value.length)
const totalPages = computed(() => Math.max(1, Math.ceil(totalTemplates.value / pageSize)))

const paginatedTemplates = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredTemplates.value.slice(start, start + pageSize)
})

const showingFrom = computed(() =>
  totalTemplates.value === 0 ? 0 : (currentPage.value - 1) * pageSize + 1,
)

const showingTo = computed(() => Math.min(currentPage.value * pageSize, totalTemplates.value))

const totalCharacters = computed(() =>
  normalizedTemplates.value.reduce((sum, template) => sum + template.content.length, 0),
)

const averageLength = computed(() => {
  if (normalizedTemplates.value.length === 0) return 0
  return Math.round(totalCharacters.value / normalizedTemplates.value.length)
})

const longestTemplate = computed(() => {
  if (normalizedTemplates.value.length === 0) return null
  return normalizedTemplates.value.reduce((longest, template) =>
    template.content.length > longest.content.length ? template : longest,
  )
})

const pageNumbers = computed(() => {
  const total = totalPages.value
  if (total <= 5) return Array.from({ length: total }, (_, index) => index + 1)

  const current = currentPage.value
  const pages = [1]
  if (current > 3) pages.push('...')
  for (let page = Math.max(2, current - 1); page <= Math.min(total - 1, current + 1); page += 1) {
    pages.push(page)
  }
  if (current < total - 2) pages.push('...')
  pages.push(total)
  return pages
})

const stats = computed(() => [
  {
    label: 'Total Templates',
    value: normalizedTemplates.value.length,
    hint: 'Templates in your library',
  },
  {
    label: 'Characters Stored',
    value: totalCharacters.value.toLocaleString(),
    hint: 'Across all template bodies',
  },
  {
    label: 'Average Length',
    value: averageLength.value.toLocaleString(),
    hint: 'Average characters per template',
  },
  {
    label: 'Longest Template',
    value: longestTemplate.value ? `${longestTemplate.value.content.length}` : '0',
    hint: longestTemplate.value?.name ?? 'No templates yet',
  },
])

const loadTemplates = async () => {
  isPageLoading.value = true
  pageError.value = ''

  try {
    await templateStore.getTemplates()
  } catch (error) {
    pageError.value = error.response?.data?.error ?? error.message ?? 'Unable to load templates.'
  } finally {
    isPageLoading.value = false
  }
}

onMounted(() => {
  loadTemplates()
})

const contentPreview = (content) => {
  const compactContent = content.replace(/\s+/g, ' ').trim()
  if (compactContent.length <= 140) return compactContent
  return `${compactContent.slice(0, 137)}...`
}

const contentLineCount = (content) => {
  if (!content) return 0
  return content.split(/\r?\n/).length
}

const resetToFirstPage = () => {
  currentPage.value = 1
}

const goToPage = (page) => {
  if (page === '...' || page < 1 || page > totalPages.value) return
  currentPage.value = page
}

const closeMenu = () => {
  activeMenuId.value = null
}

const toggleMenu = (templateId, event) => {
  event.stopPropagation()
  activeMenuId.value = activeMenuId.value === templateId ? null : templateId
}

const openCreateModal = () => {
  isCreateMode.value = true
  selectedTemplate.value = null
  templateForm.value = { name: '', content: '' }
  modalError.value = ''
  modalMessage.value = ''
  closeMenu()
}

const openTemplateModal = (template) => {
  isCreateMode.value = false
  selectedTemplate.value = template
  templateForm.value = { name: template.name, content: template.content }
  modalError.value = ''
  modalMessage.value = ''
  closeMenu()
}

const closeTemplateModal = () => {
  isCreateMode.value = false
  selectedTemplate.value = null
  modalError.value = ''
  modalMessage.value = ''
}

const activeTemplateId = computed(() => selectedTemplate.value?.id ?? null)
const isModalOpen = computed(() => isCreateMode.value || selectedTemplate.value !== null)
const modalTitle = computed(() => (activeTemplateId.value ? 'Edit template' : 'Create template'))

const saveTemplate = async () => {
  const payload = {
    name: templateForm.value.name.trim(),
    content: templateForm.value.content.trim(),
  }

  if (!payload.name || !payload.content) {
    modalError.value = 'Template name and content are required.'
    modalMessage.value = ''
    return
  }

  isSavingTemplate.value = true
  modalError.value = ''
  modalMessage.value = ''

  try {
    let savedTemplate

    if (activeTemplateId.value) {
      savedTemplate = await templateStore.updateTemplate(activeTemplateId.value, payload)
      modalMessage.value = 'Template updated successfully.'
    } else {
      savedTemplate = await templateStore.createTemplate(payload)
      modalMessage.value = 'Template created successfully.'
    }

    selectedTemplate.value = normalizeTemplate(savedTemplate)
    isCreateMode.value = false
    templateForm.value = {
      name: selectedTemplate.value.name,
      content: selectedTemplate.value.content,
    }
    resetToFirstPage()
    await loadTemplates()
  } catch (error) {
    modalError.value =
      error.response?.data?.message ?? error.response?.data?.error ?? error.message ?? 'Unable to save template.'
  } finally {
    isSavingTemplate.value = false
  }
}

const deleteTemplate = async (template) => {
  if (!template?.id) return

  if (!confirm(`Delete "${template.name}"?`)) return

  closeMenu()

  try {
    await templateStore.deleteTemplate(template.id)
    if (selectedTemplate.value?.id === template.id) {
      closeTemplateModal()
    }
    if (paginatedTemplates.value.length === 1 && currentPage.value > 1) {
      currentPage.value -= 1
    }
  } catch (error) {
    pageError.value =
      error.response?.data?.message ?? error.response?.data?.error ?? error.message ?? 'Unable to delete template.'
  }
}

const deleteSelectedTemplate = async () => {
  if (!selectedTemplate.value?.id) {
    modalError.value = 'This template cannot be deleted.'
    return
  }

  if (!confirm(`Delete "${selectedTemplate.value.name}"?`)) return

  isDeletingTemplate.value = true
  modalError.value = ''
  modalMessage.value = ''

  try {
    await templateStore.deleteTemplate(selectedTemplate.value.id)
    closeTemplateModal()
    if (paginatedTemplates.value.length === 1 && currentPage.value > 1) {
      currentPage.value -= 1
    }
  } catch (error) {
    modalError.value =
      error.response?.data?.message ?? error.response?.data?.error ?? error.message ?? 'Unable to delete template.'
  } finally {
    isDeletingTemplate.value = false
  }
}
</script>

<template>
  <div class="templates-page" @click="closeMenu">
    <header class="page-header">
      <div>
        <h1 class="page-title">Templates</h1>
        <p class="page-subtitle">Create and manage reusable message templates.</p>
      </div>

      <div class="page-header-right">
        <label class="search-wrap">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            <path d="m21 21-4.35-4.35" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
          </svg>
          <input
            v-model="searchQuery"
            type="search"
            class="search-input"
            placeholder="Search templates..."
            aria-label="Search templates"
            @input="resetToFirstPage"
          />
        </label>

        <button class="btn-primary" type="button" @click="openCreateModal">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M12 5v14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" />
            <path d="M5 12h14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" />
          </svg>
          New Template
        </button>
      </div>
    </header>

    <section class="stats-grid" aria-label="Template metrics">
      <article v-for="stat in stats" :key="stat.label" class="stat-card">
        <p class="stat-label">{{ stat.label }}</p>
        <p class="stat-value">{{ stat.value }}</p>
        <p class="stat-hint">{{ stat.hint }}</p>
      </article>
    </section>

    <section class="toolbar">
      <div class="toolbar-copy">
        <strong>Template library</strong>
        <span>Browse, edit, and delete saved templates.</span>
      </div>

      <div class="toolbar-actions">
        <label class="select-wrap">
          <span class="visually-hidden">Sort templates</span>
          <select v-model="sortBy" class="filter-select" @change="resetToFirstPage">
            <option v-for="option in sortOptions" :key="option" :value="option">Sort: {{ option }}</option>
          </select>
        </label>

        <div class="view-toggle">
          <button class="view-btn" :class="{ 'view-btn--active': viewMode === 'grid' }" type="button" aria-label="Grid view" @click="viewMode = 'grid'">
            <svg viewBox="0 0 24 24" fill="none">
              <rect x="3" y="3" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.6" />
              <rect x="14" y="3" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.6" />
              <rect x="3" y="14" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.6" />
              <rect x="14" y="14" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.6" />
            </svg>
          </button>
          <button class="view-btn" :class="{ 'view-btn--active': viewMode === 'list' }" type="button" aria-label="List view" @click="viewMode = 'list'">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            </svg>
          </button>
        </div>
      </div>
    </section>

    <section v-if="isPageLoading" class="empty-state">
      <p>Loading templates...</p>
    </section>

    <section v-else-if="pageError" class="empty-state empty-state--error">
      <p>{{ pageError }}</p>
    </section>

    <section v-else-if="totalTemplates === 0" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" class="empty-icon" aria-hidden="true">
        <rect x="5" y="4" width="14" height="16" rx="1.5" stroke="currentColor" stroke-width="1.6" />
        <path d="M9 8h6M9 12h6M9 16h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
      </svg>
      <p>No templates found. Create your first one to get started.</p>
    </section>

    <section v-else :class="viewMode === 'grid' ? 'cards-grid' : 'cards-list'">
      <article v-for="template in paginatedTemplates" :key="template.id" class="template-card" @click="openTemplateModal(template)">
        <div class="card-header">
          <div class="card-title-row">
            <h2 class="card-name">{{ template.name }}</h2>
            <span class="card-chip">#{{ template.id }}</span>
          </div>

          <div class="menu-wrap">
            <button class="action-btn" type="button" :aria-label="`Actions for ${template.name}`" @click.stop="toggleMenu(template.id, $event)">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="5" r="1" fill="currentColor" />
                <circle cx="12" cy="12" r="1" fill="currentColor" />
                <circle cx="12" cy="19" r="1" fill="currentColor" />
              </svg>
            </button>

            <div v-if="activeMenuId === template.id" class="dropdown-menu" role="menu" @click.stop>
              <button class="dropdown-item" role="menuitem" type="button" @click="openTemplateModal(template)">Edit</button>
              <button class="dropdown-item dropdown-item--danger" role="menuitem" type="button" @click="deleteTemplate(template)">Delete</button>
            </div>
          </div>
        </div>

        <p class="card-preview">{{ contentPreview(template.content) }}</p>

        <footer class="card-footer">
          <span>{{ template.content.length }} characters</span>
          <span>{{ contentLineCount(template.content) }} lines</span>
        </footer>
      </article>
    </section>

    <footer v-if="totalTemplates > 0 && !isPageLoading && !pageError" class="pagination-bar">
      <span class="pagination-info">Showing {{ showingFrom }} to {{ showingTo }} of {{ totalTemplates }} templates</span>

      <div class="pagination-controls">
        <button class="page-btn" type="button" aria-label="Previous page" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </button>

        <button
          v-for="page in pageNumbers"
          :key="page"
          class="page-btn"
          :class="{ 'page-btn--active': page === currentPage, 'page-btn--ellipsis': page === '...' }"
          type="button"
          :disabled="page === '...'"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>

        <button class="page-btn" type="button" aria-label="Next page" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </button>
      </div>
    </footer>

    <div v-if="isModalOpen" class="template-modal-backdrop" @click.self="closeTemplateModal">
      <section class="template-modal" role="dialog" aria-modal="true" :aria-label="modalTitle">
        <header class="template-modal__header">
          <div>
            <p class="template-modal__eyebrow">Template details</p>
            <h2 class="template-modal__title">{{ modalTitle }}</h2>
          </div>

          <button class="modal-close-button" type="button" aria-label="Close modal" @click="closeTemplateModal">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="m7 7 10 10" />
              <path d="m17 7-10 10" />
            </svg>
          </button>
        </header>

        <form class="template-modal__form" @submit.prevent="saveTemplate">
          <label class="modal-field modal-field--full">
            <span>Name</span>
            <input v-model="templateForm.name" type="text" maxlength="255" required />
          </label>

          <label class="modal-field modal-field--full">
            <span>Content</span>
            <textarea
              v-model="templateForm.content"
              rows="10"
              required
              placeholder="Write your reusable message template here."
            />
          </label>

          <div class="template-preview">
            <div>
              <strong>Characters</strong>
              <span>{{ templateForm.content.trim().length }}</span>
            </div>
            <div>
              <strong>Lines</strong>
              <span>{{ contentLineCount(templateForm.content) }}</span>
            </div>
          </div>

          <div v-if="modalError || modalMessage" class="modal-feedback" :class="{ 'is-error': modalError }">
            {{ modalError || modalMessage }}
          </div>

          <div class="modal-actions">
            <button class="btn-secondary" type="button" @click="closeTemplateModal">Cancel</button>
            <button
              v-if="activeTemplateId"
              class="btn-danger"
              type="button"
              :disabled="isDeletingTemplate"
              @click="deleteSelectedTemplate"
            >
              {{ isDeletingTemplate ? 'Deleting...' : 'Delete' }}
            </button>
            <button class="btn-primary" type="submit" :disabled="isSavingTemplate">
              {{ isSavingTemplate ? 'Saving...' : activeTemplateId ? 'Save changes' : 'Create template' }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </div>
</template>

<style scoped>
.templates-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.page-title {
  margin: 0 0 4px;
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
}

.page-subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 0.95rem;
}

.page-header-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.search-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 10px;
  width: 15px;
  height: 15px;
  color: #9ca3af;
  pointer-events: none;
}

.search-input {
  width: 240px;
  padding: 9px 12px 9px 32px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 0.875rem;
  color: #374151;
  background: #fff;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input:focus,
.filter-select:focus,
.modal-field input:focus,
.modal-field textarea:focus {
  border-color: #1b9a5d;
  box-shadow: 0 0 0 3px rgba(27, 154, 93, 0.12);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.stat-card,
.toolbar,
.template-card,
.template-modal {
  border: 1px solid rgba(226, 232, 240, 0.9);
  background: #ffffff;
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.05);
}

.stat-card {
  padding: 22px;
  border-radius: 20px;
}

.stat-label {
  margin: 0;
  color: #6b7280;
  font-size: 0.9rem;
  font-weight: 600;
}

.stat-value {
  margin: 10px 0 8px;
  font-size: 2rem;
  font-weight: 800;
  color: #111827;
}

.stat-hint {
  margin: 0;
  color: #1b9a5d;
  font-weight: 600;
  font-size: 0.92rem;
}

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 18px 20px;
  border-radius: 20px;
}

.toolbar-copy {
  display: grid;
  gap: 4px;
}

.toolbar-copy strong {
  color: #111827;
}

.toolbar-copy span {
  color: #6b7280;
  font-size: 0.9rem;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-select {
  min-width: 170px;
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  background: #fff;
  color: #374151;
  font: inherit;
  outline: none;
}

.view-toggle {
  display: inline-flex;
  padding: 4px;
  border-radius: 14px;
  background: #f3f4f6;
}

.view-btn {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 10px;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
}

.view-btn--active {
  background: #ffffff;
  color: #1b9a5d;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
}

.view-btn svg {
  width: 18px;
  height: 18px;
}

.cards-grid,
.cards-list {
  display: grid;
  gap: 16px;
}

.cards-grid {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

.cards-list {
  grid-template-columns: 1fr;
}

.template-card {
  display: grid;
  gap: 18px;
  padding: 22px;
  border-radius: 24px;
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.template-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 36px rgba(15, 23, 42, 0.09);
}

.card-header,
.card-title-row,
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.card-title-row {
  align-items: flex-start;
  flex-wrap: wrap;
}

.card-name {
  margin: 0;
  font-size: 1.05rem;
  color: #111827;
}

.card-chip {
  padding: 5px 10px;
  border-radius: 999px;
  background: #eef8f1;
  color: #1b9a5d;
  font-size: 0.78rem;
  font-weight: 700;
}

.card-preview {
  margin: 0;
  color: #4b5563;
  line-height: 1.6;
  white-space: pre-wrap;
}

.card-footer {
  color: #6b7280;
  font-size: 0.85rem;
  flex-wrap: wrap;
}

.menu-wrap {
  position: relative;
}

.action-btn {
  width: 38px;
  height: 38px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #fff;
  color: #6b7280;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 140px;
  padding: 8px;
  border-radius: 14px;
  background: #fff;
  border: 1px solid #e5e7eb;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.14);
  z-index: 20;
}

.dropdown-item {
  width: 100%;
  padding: 10px 12px;
  border: none;
  background: transparent;
  border-radius: 10px;
  text-align: left;
  font: inherit;
  color: #334155;
  cursor: pointer;
}

.dropdown-item:hover {
  background: #f8fafc;
}

.dropdown-item--danger {
  color: #b91c1c;
}

.empty-state {
  display: grid;
  place-items: center;
  gap: 10px;
  min-height: 240px;
  padding: 32px;
  border-radius: 24px;
  border: 1px dashed #cbd5e1;
  background: #ffffff;
  color: #64748b;
  text-align: center;
}

.empty-state--error {
  color: #b91c1c;
}

.empty-icon {
  width: 34px;
  height: 34px;
}

.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.pagination-info {
  color: #6b7280;
  font-size: 0.92rem;
}

.pagination-controls {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.page-btn {
  min-width: 40px;
  height: 40px;
  padding: 0 12px;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  background: #fff;
  color: #374151;
  font-weight: 600;
  cursor: pointer;
}

.page-btn--active {
  border-color: #1b9a5d;
  background: #1b9a5d;
  color: #fff;
}

.page-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.page-btn svg {
  width: 16px;
  height: 16px;
}

.template-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 40;
  display: grid;
  place-items: center;
  padding: 24px;
  background: rgba(15, 23, 42, 0.52);
  backdrop-filter: blur(8px);
}

.template-modal {
  width: min(720px, 100%);
  max-height: min(88vh, 760px);
  overflow: auto;
  border-radius: 24px;
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
}

.template-modal__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 24px 24px 16px;
  border-bottom: 1px solid #eef2f7;
}

.template-modal__eyebrow {
  margin: 0 0 6px;
  color: #16a34a;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.74rem;
  font-weight: 700;
}

.template-modal__title {
  margin: 0;
  font-size: 1.45rem;
  color: #0f172a;
}

.modal-close-button {
  width: 40px;
  height: 40px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #ffffff;
  color: #475569;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.modal-close-button svg {
  width: 18px;
  height: 18px;
  stroke: currentColor;
  stroke-width: 1.9;
  stroke-linecap: round;
}

.template-modal__form {
  display: grid;
  gap: 16px;
  padding: 24px;
}

.modal-field {
  display: grid;
  gap: 8px;
}

.modal-field--full {
  grid-column: 1 / -1;
}

.modal-field span {
  font-size: 0.88rem;
  font-weight: 700;
  color: #334155;
}

.modal-field input,
.modal-field textarea {
  width: 100%;
  border-radius: 14px;
  border: 1px solid #dbe3ee;
  background: #ffffff;
  padding: 12px 14px;
  font: inherit;
  color: #0f172a;
  outline: none;
  transition: border-color 0.18s ease, box-shadow 0.18s ease;
}

.modal-field textarea {
  resize: vertical;
  min-height: 220px;
}

.template-preview {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.template-preview > div {
  display: grid;
  gap: 4px;
  padding: 14px;
  border-radius: 16px;
  background: #f8fafc;
  color: #475569;
}

.template-preview strong {
  color: #111827;
}

.modal-feedback {
  padding: 12px 14px;
  border-radius: 14px;
  background: #ecfdf5;
  color: #166534;
  font-weight: 600;
}

.modal-feedback.is-error {
  background: #fef2f2;
  color: #b91c1c;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary,
.btn-danger {
  border: none;
  border-radius: 10px;
  padding: 10px 16px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary {
  background: #1b9a5d;
  color: #fff;
}

.btn-secondary {
  background: #f3f4f6;
  color: #334155;
}

.btn-danger {
  background: #fef2f2;
  color: #b91c1c;
}

.btn-primary:disabled,
.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary svg {
  width: 16px;
  height: 16px;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@media (max-width: 1023px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 767px) {
  .page-header-right,
  .toolbar,
  .toolbar-actions,
  .pagination-bar {
    width: 100%;
  }

  .search-input {
    width: 100%;
    min-width: 0;
  }

  .search-wrap {
    width: 100%;
  }

  .stats-grid,
  .template-preview {
    grid-template-columns: 1fr;
  }
}
</style>
