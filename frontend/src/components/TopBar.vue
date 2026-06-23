<script setup>
import { ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const isOpen = ref(false)

const menuItems = [
  { to: '/', label: 'Dashboard' },
  { to: '/contacts', label: 'Contacts' },
  { to: '/campaigns', label: 'Campaigns' },
  { to: '/messages', label: 'Messages' },
  { to: '/templates', label: 'Templates' },
  { to: '/settings', label: 'Settings' }
]

const toggleMenu = () => {
  isOpen.value = !isOpen.value
}

watch(
  () => route.fullPath,
  () => {
    isOpen.value = false
  }
)
</script>

<template>
  <header class="topbar">
    <div class="topbar-inner">
      <h1 class="brand">Campaign Manager</h1>
      <button class="menu-btn" type="button" @click="toggleMenu" aria-label="Open menu">
        ☰
      </button>
    </div>

    <nav v-if="isOpen" class="dropdown" aria-label="Mobile menu">
      <RouterLink v-for="item in menuItems" :key="item.to" :to="item.to" class="dropdown-link">
        {{ item.label }}
      </RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.topbar {
  display: none;
}

@media (max-width: 1023px) {
  .topbar {
    display: block;
    position: sticky;
    top: 0;
    z-index: 140;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid rgba(229, 231, 235, 0.8);
  }

  .topbar-inner {
    height: 64px;
    padding: 0 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .brand {
    margin: 0;
    font-size: 1.05rem;
    font-weight: 700;
    color: #111111;
  }

  .menu-btn {
    border: 1px solid rgba(209, 213, 219, 0.9);
    border-radius: 10px;
    padding: 8px 12px;
    background: #ffffff;
    color: #111111;
    font-weight: 600;
    cursor: pointer;
  }

  .dropdown {
    display: grid;
    gap: 6px;
    padding: 0 12px 12px;
    background: rgba(255, 255, 255, 0.94);
    border-top: 1px solid rgba(229, 231, 235, 0.7);
  }

  .dropdown-link {
    text-decoration: none;
    color: #111111;
    padding: 10px 12px;
    border-radius: 8px;
    border: 1px solid rgba(229, 231, 235, 0.8);
    background: #ffffff;
    font-weight: 500;
  }

  .dropdown-link.router-link-active {
    background: #b3e2c4;
    border-color: #b3e2c4;
    color: #166534;
    font-weight: 700;
  }
}
</style>
