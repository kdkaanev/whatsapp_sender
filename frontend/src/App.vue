<script setup>
import { RouterView } from 'vue-router'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import SideBar from './components/SideBar.vue'
import TopBar from './components/TopBar.vue'

const route = useRoute()
const isAuthPage = computed(() => route.path === '/login')
</script>

<template>
  <div class="app-shell">
    <TopBar v-if="!isAuthPage" />

    <div class="app-layout">
      <SideBar v-if="!isAuthPage" />

      <main class="main-content" :class="{ 'main-content--auth': isAuthPage }">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8f7fb 0%, #ffffff 100%);
}

.app-layout {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  min-width: 0;
  padding: 32px;
}

.main-content--auth {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 20px;
}

@media (max-width: 1023px) {
  .app-layout {
    display: flex;
    flex-direction: column;
  }

  .main-content {
    padding: 16px;
  }
}

@media (min-width: 1024px) {
  .main-content {
    padding: 32px 40px;
  }
}
</style>
