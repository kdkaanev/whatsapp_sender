

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
const selectedContact = ref(null)
const contactForm = ref({
  name: '',
  email: '',
  phone: '',
  tags: '',
})
const modalError = ref('')
const modalMessage = ref('')
const isSavingContact = ref(false)
const isDeletingContact = ref(false)

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
        getContactPhone(c).toLowerCase().includes(q),
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

const getContactPhone = (contact) =>
  String(contact?.phone ?? contact?.phone_number ?? '')

const getContactTags = (contact) =>
  Array.isArray(contact?.tags) ? contact.tags : []

const parseTags = (value) =>
  value
    .split(',')
    .map((tag) => tag.trim())
    .filter(Boolean)

const fillContactForm = (contact) => {
  contactForm.value = {
    name: contact?.name ?? '',
    email: contact?.email ?? '',
    phone: getContactPhone(contact),
    tags: getContactTags(contact).join(', '),
  }
}

const openContactModal = (contact) => {
  selectedContact.value = contact
  fillContactForm(contact)
  modalError.value = ''
  modalMessage.value = ''
  closeMenu()
}

const closeContactModal = () => {
  selectedContact.value = null
  modalError.value = ''
  modalMessage.value = ''
}

const saveContact = async () => {
  if (!selectedContact.value?.id) {
    modalError.value = 'This contact cannot be edited.'
    return
  }

  isSavingContact.value = true
  modalError.value = ''
  modalMessage.value = ''

  try {
    const updatedContact = await contactStore.updateContact(selectedContact.value.id, {
      name: contactForm.value.name.trim(),
      email: contactForm.value.email.trim(),
      phone: contactForm.value.phone.trim(),
      tags: parseTags(contactForm.value.tags),
    })
    selectedContact.value = updatedContact
    fillContactForm(updatedContact)
    modalMessage.value = 'Contact updated successfully.'
  } catch (error) {
    modalError.value =
      error.response?.data?.message ?? error.message ?? 'Unable to update contact.'
  } finally {
    isSavingContact.value = false
  }
}

const handleDelete = async (id) => {
  closeMenu()
  if (!confirm('Delete this contact?')) return
  await contactStore.deleteContact(id)
}

const deleteSelectedContact = async () => {
  if (!selectedContact.value?.id) {
    modalError.value = 'This contact cannot be deleted.'
    return
  }

  if (!confirm(`Delete "${selectedContact.value.name}"?`)) return

  isDeletingContact.value = true
  modalError.value = ''
  modalMessage.value = ''

  try {
    await contactStore.deleteContact(selectedContact.value.id)
    closeContactModal()
  } catch (error) {
    modalError.value =
      error.response?.data?.message ?? error.message ?? 'Unable to delete contact.'
  } finally {
    isDeletingContact.value = false
  }
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
      :get-contact-phone="getContactPhone"
      :tag-class="tagClass"
      @toggle-select-all="toggleSelectAll"
      @toggle-select="toggleSelect"
      @toggle-menu="toggleMenu"
      @select-contact="openContactModal"
      @edit-contact="openContactModal"
      @delete-contact="handleDelete"
      @go-to-page="goToPage"
    />

    <div
      v-if="selectedContact"
      class="contact-modal-backdrop"
      @click.self="closeContactModal"
    >
      <section
        class="contact-modal"
        role="dialog"
        aria-modal="true"
        :aria-label="selectedContact.name"
      >
        <header class="contact-modal__header">
          <div>
            <p class="contact-modal__eyebrow">Contact details</p>
            <h2 class="contact-modal__title">{{ selectedContact.name }}</h2>
          </div>
          <button
            class="modal-close-button"
            type="button"
            aria-label="Close modal"
            @click="closeContactModal"
          >
            <svg viewBox="0 0 24 24" fill="none">
              <path d="m7 7 10 10" />
              <path d="m17 7-10 10" />
            </svg>
          </button>
        </header>

        <form class="contact-modal__form" @submit.prevent="saveContact">
          <label class="modal-field">
            <span>Name</span>
            <input v-model="contactForm.name" type="text" required />
          </label>

          <label class="modal-field">
            <span>Phone</span>
            <input v-model="contactForm.phone" type="tel" required />
          </label>

          <label class="modal-field modal-field--full">
            <span>Email</span>
            <input v-model="contactForm.email" type="email" />
          </label>

          <label class="modal-field modal-field--full">
            <span>Tags <em class="modal-field__hint">(comma separated)</em></span>
            <input v-model="contactForm.tags" type="text" placeholder="VIP, Client" />
          </label>

          <div
            v-if="modalError || modalMessage"
            class="modal-feedback"
            :class="{ 'is-error': modalError }"
          >
            {{ modalError || modalMessage }}
          </div>

          <div class="modal-actions">
            <button class="btn-secondary" type="button" @click="closeContactModal">
              Cancel
            </button>
            <button
              class="btn-danger"
              type="button"
              :disabled="isDeletingContact"
              @click="deleteSelectedContact"
            >
              {{ isDeletingContact ? 'Deleting...' : 'Delete' }}
            </button>
            <button class="btn-primary" type="submit" :disabled="isSavingContact">
              {{ isSavingContact ? 'Saving...' : 'Save changes' }}
            </button>
          </div>
        </form>
      </section>
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

.contact-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 40;
  display: grid;
  place-items: center;
  padding: 24px;
  background: rgba(15, 23, 42, 0.52);
  backdrop-filter: blur(8px);
}

.contact-modal {
  width: min(620px, 100%);
  max-height: min(88vh, 760px);
  overflow: auto;
  border-radius: 24px;
  border: 1px solid rgba(226, 232, 240, 0.9);
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  box-shadow: 0 30px 80px rgba(15, 23, 42, 0.25);
}

.contact-modal__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 24px 24px 16px;
  border-bottom: 1px solid #eef2f7;
}

.contact-modal__eyebrow {
  margin: 0 0 6px;
  color: #16a34a;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.74rem;
  font-weight: 700;
}

.contact-modal__title {
  margin: 0;
  font-size: 1.45rem;
  line-height: 1.2;
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

.contact-modal__form {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
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

.modal-field input {
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

.modal-field input:focus {
  border-color: #16a34a;
  box-shadow: 0 0 0 4px rgba(22, 163, 74, 0.12);
}

.modal-field__hint {
  font-style: normal;
  font-weight: 400;
  color: #94a3b8;
  font-size: 0.82rem;
}

.modal-feedback {
  grid-column: 1 / -1;
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
  grid-column: 1 / -1;
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

@media (max-width: 768px) {
  .contact-modal__form {
    grid-template-columns: 1fr;
  }
}
</style>
