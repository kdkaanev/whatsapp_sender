<script setup>
const emit = defineEmits(['add-contact'])
</script>

<template>
  <button class="btn-primary" type="button" @click="emit('add-contact')">
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M12 5v14" />
      <path d="M5 12h14" />
    </svg>
    Add Contact
  </button>
</template>

<style scoped>
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
</style>
