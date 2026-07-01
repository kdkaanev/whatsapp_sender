<script setup>
import { ref } from 'vue'

const emit = defineEmits(['import'])
const csvInputRef = ref(null)

const handleImportCSV = () => {
  csvInputRef.value?.click()
}

const onCSVFileChange = (event) => {
  const file = event.target.files?.[0]
  emit('import', file)
  event.target.value = ''
}
</script>

<template>
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
</template>

<style scoped>
.hidden-input {
  display: none;
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
</style>
