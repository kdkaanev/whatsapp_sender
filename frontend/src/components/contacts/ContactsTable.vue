<script setup>
defineProps({
  loading: {
    type: Boolean,
    required: true,
  },
  error: {
    type: String,
    default: '',
  },
  totalContacts: {
    type: Number,
    required: true,
  },
  allOnPageSelected: {
    type: Boolean,
    required: true,
  },
  selectedIds: {
    type: Object,
    required: true,
  },
  paginatedContacts: {
    type: Array,
    required: true,
  },
  activeMenuId: {
    type: Number,
    default: null,
  },
  currentPage: {
    type: Number,
    required: true,
  },
  totalPages: {
    type: Number,
    required: true,
  },
  pageNumbers: {
    type: Array,
    required: true,
  },
  showingFrom: {
    type: Number,
    required: true,
  },
  showingTo: {
    type: Number,
    required: true,
  },
  formatDate: {
    type: Function,
    required: true,
  },
  getContactPhone: {
    type: Function,
    required: true,
  },
  tagClass: {
    type: Function,
    required: true,
  },
})

const emit = defineEmits([
  'toggle-select-all',
  'toggle-select',
  'toggle-menu',
  'edit-contact',
  'select-contact',
  'delete-contact',
  'go-to-page',
])
</script>

<template>
  <div class="table-card">
    <div v-if="loading" class="state-message">
      <span class="spinner" aria-label="Loading"></span>
      Loading contacts…
    </div>

    <div v-else-if="error" class="state-message state-message--error">
      Failed to load contacts. Please try again.
    </div>

    <div v-else-if="totalContacts === 0" class="state-message">
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" class="empty-icon">
        <path d="M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" />
        <path d="M4 18a5 5 0 0 1 10 0" />
        <path d="M17 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z" />
        <path d="M14.5 18a4.5 4.5 0 0 1 5.5-4.4" />
      </svg>
      <span>No contacts found.</span>
    </div>

    <div v-else class="table-wrap">
      <table class="contacts-table">
        <thead>
          <tr>
            <th class="col-check">
              <input
                type="checkbox"
                :checked="allOnPageSelected"
                :indeterminate="selectedIds.size > 0 && !allOnPageSelected"
                aria-label="Select all on page"
                @change="emit('toggle-select-all')"
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
            @click="emit('select-contact', contact)"
          >
            <td class="col-check">
              <input
                type="checkbox"
                :checked="selectedIds.has(contact.id)"
                :aria-label="`Select ${contact.name}`"
                @click.stop
                @change="emit('toggle-select', contact.id)"
              />
            </td>
            <td class="col-name">{{ contact.name }}</td>
            <td class="col-phone">{{ getContactPhone(contact) }}</td>
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
                  @click.stop="emit('toggle-menu', contact.id, $event)"
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
                  <button
                    class="dropdown-item"
                    role="menuitem"
                    type="button"
                    @click="emit('edit-contact', contact)"
                  >Edit</button>
                  <button
                    class="dropdown-item dropdown-item--danger"
                    role="menuitem"
                    type="button"
                    @click="emit('delete-contact', contact.id)"
                  >Delete</button>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

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
          @click="emit('go-to-page', currentPage - 1)"
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
          @click="emit('go-to-page', p)"
        >
          {{ p }}
        </button>
        <button
          class="page-btn"
          type="button"
          aria-label="Next page"
          :disabled="currentPage === totalPages"
          @click="emit('go-to-page', currentPage + 1)"
        >
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M9 18l6-6-6-6" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.table-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.06);
  border: 1px solid #f1f5f9;
  overflow: hidden;
}

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
