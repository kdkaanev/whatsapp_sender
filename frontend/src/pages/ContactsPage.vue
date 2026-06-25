

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useContactStore } from '../stores/contacts'
import { useAuthStore } from '../stores/auth'
import CreateContacts from '../components/CreateContactss.vue'
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

// CSV import ref
const csvInputRef = ref(null)

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

const handleImportCSV = () => {
  csvInputRef.value?.click()
}

const onCSVFileChange = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return
  await contactStore.importContacts(file)
  event.target.value = ''
}

const addContact = () => {
  router.push({ name: 'CreateContact' })
}


</script>

<template>
  <div class="contacts-page" @click="closeMenu">
    <!-- Header -->
    <div class="page-header">
      <h1 class="page-title">Contacts</h1>
      <div class="header-actions">
        <button class="btn-secondary" type="button" @click.stop="handleImportCSV">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
          Import CSV
        </button>
        <input
          ref="csvInputRef"
          type="file"
          accept=".csv"
          class="hidden-input"
          @change="onCSVFileChange"
        />
        <button @click="addContact" class="btn-primary" type="button">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M12 5v14" />
            <path d="M5 12h14" />
          </svg>
          Add Contact
        </button>
        <button class="btn-icon" type="button" aria-label="More options">
          <svg viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="5" r="1" fill="currentColor" />
            <circle cx="12" cy="12" r="1" fill="currentColor" />
            <circle cx="12" cy="19" r="1" fill="currentColor" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="toolbar-left">
        <div class="search-wrap">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="11" cy="11" r="7" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <input
            v-model="searchQuery"
            type="search"
            class="search-input"
            placeholder="Search contacts..."
            aria-label="Search contacts"
          />
        </div>

        <select
          v-model="selectedTag"
          class="tag-filter"
          aria-label="Filter by tag"
        >
          <option value="">All Tags</option>
          <option v-for="tag in allTags" :key="tag" :value="tag">{{ tag }}</option>
        </select>

        <button class="btn-outline" type="button">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3Z" />
          </svg>
          More Filters
        </button>
      </div>

      <span class="contacts-count">
        {{ totalContacts.toLocaleString() }}
        {{ totalContacts === 1 ? 'contact' : 'contacts' }}
      </span>
    </div>

    <!-- Table Card -->
    <div class="table-card">
      <!-- Loading state -->
      <div v-if="contactStore.loading" class="state-message">
        <span class="spinner" aria-label="Loading"></span>
        Loading contacts…
      </div>

      <!-- Error state -->
      <div v-else-if="contactStore.error" class="state-message state-message--error">
        Failed to load contacts. Please try again.
      </div>

      <!-- Empty state -->
      <div v-else-if="totalContacts === 0" class="state-message">
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" class="empty-icon">
          <path d="M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" />
          <path d="M4 18a5 5 0 0 1 10 0" />
          <path d="M17 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z" />
          <path d="M14.5 18a4.5 4.5 0 0 1 5.5-4.4" />
        </svg>
        <span>No contacts found.</span>
      </div>

      <!-- Table -->
      <div v-else class="table-wrap">
        <table class="contacts-table">
          <thead>
            <tr>
              <th class="col-check">
                <input
                  type="checkbox"
                  :checked="allOnPageSelected"
                  :indeterminate="
                    selectedIds.size > 0 && !allOnPageSelected
                  "
                  aria-label="Select all on page"
                  @change="toggleSelectAll"
                />
              </th>
              <th>Name</th>
              <th>Phone</th>
              <th>Tags</th>
              <th class="col-added">
                Added
                <svg class="sort-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M12 5v14" />
                  <path d="M7 10l5-5 5 5" />
                </svg>
              </th>
              <th class="col-actions"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="contact in paginatedContacts"
              :key="contact.id"
              :class="{ 'row--selected': selectedIds.has(contact.id) }"
            >
              <td class="col-check">
                <input
                  type="checkbox"
                  :checked="selectedIds.has(contact.id)"
                  :aria-label="`Select ${contact.name}`"
                  @change="toggleSelect(contact.id)"
                />
              </td>
              <td class="col-name">{{ contact.name }}</td>
              <td class="col-phone">{{ contact.phone_number }}</td>
              <td class="col-tags">
                <span
                  v-for="tag in contact.tags"
                  :key="tag"
                  class="tag"
                  :class="tagClass(tag)"
                >{{ tag }}</span>
                <span v-if="!contact.tags || contact.tags.length === 0" class="no-tags">—</span>
              </td>
              <td class="col-added">{{ formatDate(contact.created_at) }}</td>
              <td class="col-actions">
                <div class="menu-wrap">
                  <button
                    class="more-btn"
                    type="button"
                    :aria-label="`Actions for ${contact.name}`"
                    @click.stop="toggleMenu(contact.id, $event)"
                  >
                    <svg viewBox="0 0 24 24" fill="none">
                      <circle cx="12" cy="5" r="1" fill="currentColor" />
                      <circle cx="12" cy="12" r="1" fill="currentColor" />
                      <circle cx="12" cy="19" r="1" fill="currentColor" />
                    </svg>
                  </button>
                  <div
                    v-if="activeMenuId === contact.id"
                    class="dropdown-menu"
                    role="menu"
                    @click.stop
                  >
                    <button class="dropdown-item" role="menuitem" type="button">Edit</button>
                    <button
                      class="dropdown-item dropdown-item--danger"
                      role="menuitem"
                      type="button"
                      @click="handleDelete(contact.id)"
                    >Delete</button>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="totalContacts > 0" class="pagination-bar">
        <span class="pagination-info">
          Showing {{ showingFrom }} to {{ showingTo }} of
          {{ totalContacts.toLocaleString() }} contacts
        </span>
        <div class="pagination-controls">
          <button
            class="page-btn"
            type="button"
            aria-label="Previous page"
            :disabled="currentPage === 1"
            @click="goToPage(currentPage - 1)"
          >
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M15 18l-6-6 6-6" />
            </svg>
          </button>
          <button
            v-for="p in pageNumbers"
            :key="p"
            class="page-btn"
            :class="{
              'page-btn--active': p === currentPage,
              'page-btn--ellipsis': p === '...',
            }"
            type="button"
            :disabled="p === '...'"
            @click="goToPage(p)"
          >
            {{ p }}
          </button>
          <button
            class="page-btn"
            type="button"
            aria-label="Next page"
            :disabled="currentPage === totalPages"
            @click="goToPage(currentPage + 1)"
          >
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M9 18l6-6-6-6" />
            </svg>
          </button>
        </div>
      </div>
    </div>
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

.hidden-input {
  display: none;
}

/* Buttons */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: #1b9a5d;
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 9px 18px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(27, 154, 93, 0.25);
}

.btn-primary:hover {
  background: #168a52;
}

.btn-primary svg {
  width: 15px;
  height: 15px;
  stroke: currentColor;
  stroke-width: 2.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: #fff;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  padding: 9px 18px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #f9fafb;
}

.btn-secondary svg {
  width: 15px;
  height: 15px;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
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

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #fff;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  padding: 8px 14px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-outline:hover {
  background: #f9fafb;
}

.btn-outline svg {
  width: 14px;
  height: 14px;
  stroke: #6b7280;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* Toolbar */
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.toolbar-left {
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
  stroke: #9ca3af;
  stroke-width: 1.8;
  stroke-linecap: round;
  pointer-events: none;
}

.search-input {
  padding: 8px 12px 8px 32px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 0.875rem;
  color: #374151;
  background: #fff;
  width: 200px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input:focus {
  border-color: #1b9a5d;
  box-shadow: 0 0 0 3px rgba(27, 154, 93, 0.1);
}

.tag-filter {
  padding: 8px 32px 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 0.875rem;
  color: #374151;
  background: #fff;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%236b7280' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  cursor: pointer;
  outline: none;
  transition: border-color 0.2s;
}

.tag-filter:focus {
  border-color: #1b9a5d;
}

.contacts-count {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
  white-space: nowrap;
}

/* Table Card */
.table-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.06);
  border: 1px solid #f1f5f9;
  overflow: hidden;
}

/* States */
.state-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 64px 24px;
  color: #6b7280;
  font-size: 0.9rem;
}

.state-message--error {
  color: #dc2626;
}

.empty-icon {
  width: 48px;
  height: 48px;
  stroke: #d1d5db;
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.spinner {
  width: 28px;
  height: 28px;
  border: 3px solid #e5e7eb;
  border-top-color: #1b9a5d;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Table */
.table-wrap {
  overflow-x: auto;
}

.contacts-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.contacts-table th {
  text-align: left;
  padding: 12px 16px;
  color: #6b7280;
  font-weight: 600;
  font-size: 0.8rem;
  border-bottom: 1px solid #f1f5f9;
  white-space: nowrap;
  background: #fafafa;
}

.contacts-table td {
  padding: 13px 16px;
  color: #374151;
  border-bottom: 1px solid #f8fafc;
  vertical-align: middle;
}

.contacts-table tbody tr:last-child td {
  border-bottom: none;
}

.contacts-table tbody tr:hover {
  background: #fafbfc;
}

.contacts-table tbody tr.row--selected {
  background: #f0fdf6;
}

/* Column widths */
.col-check {
  width: 44px;
  padding-left: 16px !important;
  padding-right: 4px !important;
}

.col-name {
  font-weight: 600;
  color: #111827 !important;
  min-width: 160px;
}

.col-phone {
  color: #374151;
  white-space: nowrap;
}

.col-tags {
  min-width: 120px;
}

.col-added {
  color: #6b7280 !important;
  font-size: 0.8rem;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 4px;
}

.contacts-table th.col-added {
  display: table-cell;
}

.sort-icon {
  width: 12px;
  height: 12px;
  stroke: #9ca3af;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  vertical-align: middle;
  display: inline-block;
  margin-left: 3px;
}

.col-actions {
  width: 48px;
  padding: 8px !important;
}

/* Tags */
.tag {
  display: inline-flex;
  align-items: center;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-right: 4px;
}

.tag--vip {
  background: #fef9c3;
  color: #a16207;
  border: 1px solid #fde68a;
}

.tag--client {
  background: #e0f2fe;
  color: #0369a1;
  border: 1px solid #bae6fd;
}

.tag--supplier {
  background: #f3e8ff;
  color: #7c3aed;
  border: 1px solid #ddd6fe;
}

.tag--new {
  background: #ffedd5;
  color: #c2410c;
  border: 1px solid #fed7aa;
}

.tag--default {
  background: #f3f4f6;
  color: #6b7280;
  border: 1px solid #e5e7eb;
}

.no-tags {
  color: #d1d5db;
}

/* Row actions */
.menu-wrap {
  position: relative;
}

.more-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background: none;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  color: #9ca3af;
  padding: 0;
  transition: background 0.2s, color 0.2s;
}

.more-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.more-btn svg {
  width: 16px;
  height: 16px;
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: calc(100% + 4px);
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.12);
  z-index: 50;
  min-width: 130px;
  padding: 4px 0;
  overflow: hidden;
}

.dropdown-item {
  display: block;
  width: 100%;
  text-align: left;
  padding: 9px 16px;
  font-size: 0.875rem;
  color: #374151;
  background: none;
  border: none;
  cursor: pointer;
  transition: background 0.15s;
}

.dropdown-item:hover {
  background: #f9fafb;
}

.dropdown-item--danger {
  color: #dc2626;
}

.dropdown-item--danger:hover {
  background: #fef2f2;
}

/* Pagination */
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  padding: 14px 20px;
  border-top: 1px solid #f1f5f9;
}

.pagination-info {
  font-size: 0.8rem;
  color: #6b7280;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 4px;
}

.page-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  height: 32px;
  padding: 0 6px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
  color: #374151;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}

.page-btn:hover:not(:disabled):not(.page-btn--active):not(.page-btn--ellipsis) {
  background: #f9fafb;
  border-color: #d1d5db;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-btn--active {
  background: #1b9a5d;
  border-color: #1b9a5d;
  color: #fff;
}

.page-btn--ellipsis {
  border-color: transparent;
  background: transparent;
  cursor: default;
}

.page-btn svg {
  width: 14px;
  height: 14px;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}
</style>

