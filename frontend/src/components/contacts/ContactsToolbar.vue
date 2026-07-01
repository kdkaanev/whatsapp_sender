<script setup>
defineProps({
  searchQuery: {
    type: String,
    required: true,
  },
  selectedTag: {
    type: String,
    required: true,
  },
  allTags: {
    type: Array,
    required: true,
  },
  totalContacts: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(['update:search-query', 'update:selected-tag'])
</script>

<template>
  <div class="toolbar">
    <div class="toolbar-left">
      <div class="search-wrap">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="11" cy="11" r="7" />
          <path d="m21 21-4.35-4.35" />
        </svg>
        <input
          :value="searchQuery"
          type="search"
          class="search-input"
          placeholder="Search contacts..."
          aria-label="Search contacts"
          @input="emit('update:search-query', $event.target.value)"
        />
      </div>

      <select
        :value="selectedTag"
        class="tag-filter"
        aria-label="Filter by tag"
        @change="emit('update:selected-tag', $event.target.value)"
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
</template>

<style scoped>
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

.contacts-count {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
  white-space: nowrap;
}
</style>
