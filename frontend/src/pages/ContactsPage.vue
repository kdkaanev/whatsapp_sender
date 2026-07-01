

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useContactStore } from '../stores/contacts'
import { useAuthStore } from '../stores/auth'
import ContactsToolbar from '../components/contacts/ContactsToolbar.vue'
import ContactsTable from '../components/contacts/ContactsTable.vue'
import ContactFormDialog from '../components/contacts/ContactFormDialog.vue'
import ImportDialog from '../components/contacts/ImportDialog.vue'
import router from '../router/index.js'

const contactStore = useContactStore()
const authStore = useAuthStore()

// Search & filter state
const searchQuery = ref('')
const selectedTag = ref('')
const currentPage = ref(1)
const pageSize = 10

// Row selection
const selectedIds = ref(new Set())

// Actions menu
const activeMenuId = ref(null)

// Load contacts on mount
onMounted(() => {
  contactStore.showAllContacts()
  contactStore.getContacts({ search: searchQuery.value, tag: selectedTag.value })
  authStore.getProfile()
})

// Reset page when search/filter changes
watch([searchQuery, selectedTag], () => {
  currentPage.value = 1
  selectedIds.value = new Set()
})

// --- Computed ---

const allTags = computed(() => {
  const tags = new Set()
  contactStore.contacts.forEach((c) => {
    if (Array.isArray(c.tags)) c.tags.forEach((t) => tags.add(t))
  })
  return Array.from(tags).sort()
})

const filteredContacts = computed(() => {
  let result = contactStore.contacts
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(
      (c) =>
        c.name.toLowerCase().includes(q) ||
        c.phone_number.toLowerCase().includes(q),
    )
  }
  if (selectedTag.value) {
    result = result.filter(
      (c) => Array.isArray(c.tags) && c.tags.includes(selectedTag.value),
    )
  }
  return result
})

const totalContacts = computed(() => filteredContacts.value.length)
const totalPages = computed(() => Math.max(1, Math.ceil(totalContacts.value / pageSize)))

const paginatedContacts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredContacts.value.slice(start, start + pageSize)
})

const showingFrom = computed(() =>
  totalContacts.value === 0 ? 0 : (currentPage.value - 1) * pageSize + 1,
)
const showingTo = computed(() =>
  Math.min(currentPage.value * pageSize, totalContacts.value),
)

const allOnPageSelected = computed(
  () =>
    paginatedContacts.value.length > 0 &&
    paginatedContacts.value.every((c) => selectedIds.value.has(c.id)),
)

// Pagination pages list (with ellipsis)
const pageNumbers = computed(() => {
  const total = totalPages.value
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  const cur = currentPage.value
  const pages = []
  pages.push(1)
  if (cur > 3) pages.push('...')
  for (let p = Math.max(2, cur - 1); p <= Math.min(total - 1, cur + 1); p++) {
    pages.push(p)
  }
  if (cur < total - 2) pages.push('...')
  pages.push(total)
  return pages
})

// --- Methods ---

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const day = String(d.getDate()).padStart(2, '0')
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const year = d.getFullYear()
  return `${day}.${month}.${year}`
}

const tagClass = (tag) => {
  const map = {
    VIP: 'tag--vip',
    Client: 'tag--client',
    Supplier: 'tag--supplier',
    New: 'tag--new',
  }
  return map[tag] ?? 'tag--default'
}

const toggleSelectAll = () => {
  if (allOnPageSelected.value) {
    paginatedContacts.value.forEach((c) => selectedIds.value.delete(c.id))
  } else {
    paginatedContacts.value.forEach((c) => selectedIds.value.add(c.id))
  }
  selectedIds.value = new Set(selectedIds.value)
}

const toggleSelect = (id) => {
  const next = new Set(selectedIds.value)
  next.has(id) ? next.delete(id) : next.add(id)
  selectedIds.value = next
}

const goToPage = (p) => {
  if (p === '...' || p < 1 || p > totalPages.value) return
  currentPage.value = p
  selectedIds.value = new Set()
}

const toggleMenu = (id, event) => {
  event.stopPropagation()
  activeMenuId.value = activeMenuId.value === id ? null : id
}

const closeMenu = () => {
  activeMenuId.value = null
}

const handleDelete = async (id) => {
  closeMenu()
  if (!confirm('Delete this contact?')) return
  await contactStore.deleteContact(id)
}

const onCSVImport = async (file) => {
  if (!file) return
  await contactStore.importContacts(file)
}

const addContact = () => {
  router.push({ name: 'CreateContact' })
}


</script>

<template>
  <div class="contacts-page" @click="closeMenu">
    <div class="page-header">
      <h1 class="page-title">Contacts</h1>
      <div class="header-actions">
        <ImportDialog @import="onCSVImport" />
        <ContactFormDialog @add-contact="addContact" />
        <button class="btn-icon" type="button" aria-label="More options">
          <svg viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="5" r="1" fill="currentColor" />
            <circle cx="12" cy="12" r="1" fill="currentColor" />
            <circle cx="12" cy="19" r="1" fill="currentColor" />
          </svg>
        </button>
      </div>
    </div>

    <ContactsToolbar
      :search-query="searchQuery"
      :selected-tag="selectedTag"
      :all-tags="allTags"
      :total-contacts="totalContacts"
      @update:search-query="searchQuery = $event"
      @update:selected-tag="selectedTag = $event"
    />

    <ContactsTable
      :loading="contactStore.loading"
      :error="contactStore.error"
      :total-contacts="totalContacts"
      :all-on-page-selected="allOnPageSelected"
      :selected-ids="selectedIds"
      :paginated-contacts="paginatedContacts"
      :active-menu-id="activeMenuId"
      :current-page="currentPage"
      :total-pages="totalPages"
      :page-numbers="pageNumbers"
      :showing-from="showingFrom"
      :showing-to="showingTo"
      :format-date="formatDate"
      :tag-class="tagClass"
      @toggle-select-all="toggleSelectAll"
      @toggle-select="toggleSelect"
      @toggle-menu="toggleMenu"
      @delete-contact="handleDelete"
      @go-to-page="goToPage"
    />
  </div>
</template>

<style scoped>
.contacts-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Header */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: #fff;
  color: #6b7280;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  cursor: pointer;
  padding: 0;
  transition: background 0.2s;
}

.btn-icon:hover {
  background: #f9fafb;
}

.btn-icon svg {
  width: 16px;
  height: 16px;
}
</style>
