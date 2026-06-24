<script setup>
import { ref, computed } from 'vue'

// ── Mock data ────────────────────────────────────────────────────────────────
const allTemplates = ref([
  {
    id: 1,
    name: 'Welcome Message',
    category: 'Welcome',
    favorite: true,
    body: 'Здравейте {{name}},👋\n\nБлагодарим Ви, че се свързахте с нас!\nЩе се радваме да Ви помогнем.',
    usedTimes: 34,
    updatedAgo: '2 days ago',
  },
  {
    id: 2,
    name: 'Promo 15% Off',
    category: 'Promotion',
    favorite: false,
    body: 'Здравейте {{name}},🎉\n\nПолучавате 15% отстъпка на всички продукти този уикенд.\n\nПромокод: SAVE15\nВалидно до {{date}}.',
    usedTimes: 18,
    updatedAgo: '5 days ago',
  },
  {
    id: 3,
    name: 'Reminder Appointment',
    category: 'Reminder',
    favorite: false,
    body: 'Здравейте {{name}},\n\nНапомняме Ви за предстоящата ни среща на {{date}} в {{time}}.\n\nОчакваме Ви!',
    usedTimes: 12,
    updatedAgo: '1 week ago',
  },
  {
    id: 4,
    name: 'Payment Reminder',
    category: 'Reminder',
    favorite: false,
    body: 'Здравейте {{name}},\n\nТова е приятелско напомняне за предстоящото Ви плащане в размер на {{amount}} лв.\n\nБлагодарим Ви!',
    usedTimes: 9,
    updatedAgo: '1 week ago',
  },
  {
    id: 5,
    name: 'Thank You',
    category: 'Welcome',
    favorite: false,
    body: 'Здравейте {{name}},\n\nБлагодарим за доверието!\nОчакваме Ви отново.',
    usedTimes: 25,
    updatedAgo: '1 week ago',
  },
  {
    id: 6,
    name: 'New Collection',
    category: 'Promotion',
    favorite: false,
    body: 'Здравейте {{name}},\n\nРазгледайте нашата нова колекция продукти. 🌟\n\nВижте повече тук: {{link}}',
    usedTimes: 16,
    updatedAgo: '2 weeks ago',
  },
  {
    id: 7,
    name: 'Feedback Request',
    category: 'Follow Up',
    favorite: false,
    body: 'Здравейте {{name}},\n\nЩе се радваме да чуем Вашето мнение за нашето обслужване.\n\nБлагодарим!',
    usedTimes: 7,
    updatedAgo: '2 weeks ago',
  },
  {
    id: 8,
    name: 'Happy Birthday',
    category: 'Other',
    favorite: false,
    body: 'Честит рожден ден, {{name}}! 🎂\n\nПожелаваме Ви здраве, щастие и прекрасен ден!',
    usedTimes: 4,
    updatedAgo: '3 weeks ago',
  },
  {
    id: 9,
    name: 'Order Confirmed',
    category: 'Other',
    favorite: false,
    body: 'Здравейте {{name}},\n\nВашата поръчка #{{order_id}} е потвърдена и се обработва.\n\nБлагодарим Ви!',
    usedTimes: 21,
    updatedAgo: '3 weeks ago',
  },
  {
    id: 10,
    name: 'Follow Up After Meeting',
    category: 'Follow Up',
    favorite: false,
    body: 'Здравейте {{name}},\n\nБлагодарим за срещата днес. Ще се свържем с Вас скоро с повече информация.',
    usedTimes: 11,
    updatedAgo: '1 month ago',
  },
  {
    id: 11,
    name: 'Special Offer',
    category: 'Promotion',
    favorite: true,
    body: 'Здравейте {{name}},\n\nСамо за Вас — специална оферта от {{discount}}% за следващата поръчка!',
    usedTimes: 30,
    updatedAgo: '1 month ago',
  },
  {
    id: 12,
    name: 'Re-engagement',
    category: 'Follow Up',
    favorite: true,
    body: 'Скучаем за Вас, {{name}}! 😊\n\nВижте какво ново сме подготвили специално за Вас.',
    usedTimes: 14,
    updatedAgo: '1 month ago',
  },
])

// ── State ────────────────────────────────────────────────────────────────────
const searchQuery = ref('')
const activeTab = ref('All Templates')
const selectedCategory = ref('')
const sortBy = ref('Recently Updated')
const viewMode = ref('grid')
const currentPage = ref(1)
const pageSize = 8

const tabs = ['All Templates', 'Welcome', 'Promotions', 'Reminders', 'Follow Up', 'Other']
const sortOptions = ['Recently Updated', 'Most Used', 'Alphabetical', 'Least Used']

// ── Stats ────────────────────────────────────────────────────────────────────
const stats = computed(() => [
  {
    icon: 'templates',
    label: 'Total Templates',
    value: allTemplates.value.length,
    hint: '+3 this week',
    hintColor: '#1b9a5d',
  },
  {
    icon: 'used',
    label: 'Used This Month',
    // Static mock value — replace with real usage data from backend
    value: 18,
    hint: '75% of templates',
    hintColor: '#6b7280',
  },
  {
    icon: 'star',
    label: 'Favorite Templates',
    value: allTemplates.value.filter((t) => t.favorite).length,
    hint: 'Marked as favorite',
    hintColor: '#6b7280',
  },
  {
    icon: 'tag',
    label: 'Categories',
    value: new Set(allTemplates.value.map((t) => t.category)).size,
    hint: 'Template categories',
    hintColor: '#6b7280',
  },
])

// ── Filtering & sorting ──────────────────────────────────────────────────────
const tabCategoryMap = {
  'All Templates': null,
  Welcome: 'Welcome',
  Promotions: 'Promotion',
  Reminders: 'Reminder',
  'Follow Up': 'Follow Up',
  Other: 'Other',
}

const filteredTemplates = computed(() => {
  let list = allTemplates.value

  // Tab filter
  const tabCat = tabCategoryMap[activeTab.value]
  if (tabCat) list = list.filter((t) => t.category === tabCat)

  // Category dropdown filter
  if (selectedCategory.value) list = list.filter((t) => t.category === selectedCategory.value)

  // Search
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(
      (t) => t.name.toLowerCase().includes(q) || t.body.toLowerCase().includes(q),
    )
  }

  // Sort
  if (sortBy.value === 'Most Used') list = [...list].sort((a, b) => b.usedTimes - a.usedTimes)
  else if (sortBy.value === 'Least Used') list = [...list].sort((a, b) => a.usedTimes - b.usedTimes)
  else if (sortBy.value === 'Alphabetical') list = [...list].sort((a, b) => a.name.localeCompare(b.name))

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

const pageNumbers = computed(() => {
  const total = totalPages.value
  if (total <= 5) return Array.from({ length: total }, (_, i) => i + 1)
  const cur = currentPage.value
  const pages = [1]
  if (cur > 3) pages.push('...')
  for (let p = Math.max(2, cur - 1); p <= Math.min(total - 1, cur + 1); p++) pages.push(p)
  if (cur < total - 2) pages.push('...')
  pages.push(total)
  return pages
})

// ── Methods ──────────────────────────────────────────────────────────────────
const setTab = (tab) => {
  activeTab.value = tab
  currentPage.value = 1
}

const goToPage = (p) => {
  if (p === '...' || p < 1 || p > totalPages.value) return
  currentPage.value = p
}

const toggleFavorite = (template) => {
  template.favorite = !template.favorite
}

const categoryClass = (category) => {
  const map = {
    Welcome: 'badge--welcome',
    Promotion: 'badge--promo',
    Reminder: 'badge--reminder',
    'Follow Up': 'badge--followup',
    Other: 'badge--other',
  }
  return map[category] ?? 'badge--default'
}

// Active menu
const activeMenuId = ref(null)
const toggleMenu = (id, event) => {
  event.stopPropagation()
  activeMenuId.value = activeMenuId.value === id ? null : id
}
const closeMenu = () => {
  activeMenuId.value = null
}
</script>

<template>
  <div class="templates-page" @click="closeMenu">
    <!-- ── Page header ──────────────────────────────────────────────────── -->
    <div class="page-header">
      <div class="page-header-left">
        <h1 class="page-title">Templates</h1>
        <p class="page-subtitle">Create and manage your message templates</p>
      </div>
      <div class="page-header-right">
        <div class="search-wrap">
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
            @input="currentPage = 1"
          />
        </div>
        <button class="btn-primary" type="button">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M12 5v14" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" />
            <path d="M5 12h14" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" />
          </svg>
          New Template
        </button>
      </div>
    </div>

    <!-- ── Stats cards ─────────────────────────────────────────────────── -->
    <div class="stats-grid">
      <div v-for="stat in stats" :key="stat.label" class="stat-card">
        <div class="stat-icon-wrap" :class="`stat-icon-wrap--${stat.icon}`">
          <!-- Total Templates icon -->
          <svg v-if="stat.icon === 'templates'" viewBox="0 0 24 24" fill="none">
            <path d="M17 21H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7l5 5v11a2 2 0 0 1-2 2Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M14 3v4a1 1 0 0 0 1 1h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
            <path d="M9 13h6M9 17h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
          </svg>
          <!-- Used This Month icon -->
          <svg v-else-if="stat.icon === 'used'" viewBox="0 0 24 24" fill="none">
            <path d="M22 2 11 13" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M22 2 15 22 11 13 2 9l20-7Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <!-- Favorite icon -->
          <svg v-else-if="stat.icon === 'star'" viewBox="0 0 24 24" fill="none">
            <path d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <!-- Categories icon -->
          <svg v-else-if="stat.icon === 'tag'" viewBox="0 0 24 24" fill="none">
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
            <circle cx="7" cy="7" r="1" fill="currentColor" />
          </svg>
        </div>
        <div class="stat-body">
          <p class="stat-label">{{ stat.label }}</p>
          <p class="stat-value">{{ stat.value }}</p>
          <p class="stat-hint" :style="{ color: stat.hintColor }">{{ stat.hint }}</p>
        </div>
      </div>
    </div>

    <!-- ── Filter tabs + toolbar ───────────────────────────────────────── -->
    <div class="filter-row">
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab"
          class="tab-btn"
          :class="{ 'tab-btn--active': activeTab === tab }"
          type="button"
          @click="setTab(tab)"
        >
          {{ tab }}
        </button>
      </div>

      <div class="toolbar-right">
        <div class="select-wrap">
          <svg class="select-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <select v-model="selectedCategory" class="filter-select" aria-label="Filter by category" @change="currentPage = 1">
            <option value="">All Categories</option>
            <option value="Welcome">Welcome</option>
            <option value="Promotion">Promotion</option>
            <option value="Reminder">Reminder</option>
            <option value="Follow Up">Follow Up</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div class="select-wrap">
          <svg class="select-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M3 6h18M7 12h10M11 18h2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
          </svg>
          <select v-model="sortBy" class="filter-select" aria-label="Sort by" @change="currentPage = 1">
            <option v-for="opt in sortOptions" :key="opt" :value="opt">Sort by: {{ opt }}</option>
          </select>
        </div>

        <div class="view-toggle">
          <button
            class="view-btn"
            :class="{ 'view-btn--active': viewMode === 'grid' }"
            type="button"
            aria-label="Grid view"
            @click="viewMode = 'grid'"
          >
            <svg viewBox="0 0 24 24" fill="none">
              <rect x="3" y="3" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.6" />
              <rect x="14" y="3" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.6" />
              <rect x="3" y="14" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.6" />
              <rect x="14" y="14" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.6" />
            </svg>
          </button>
          <button
            class="view-btn"
            :class="{ 'view-btn--active': viewMode === 'list' }"
            type="button"
            aria-label="List view"
            @click="viewMode = 'list'"
          >
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- ── Template cards ──────────────────────────────────────────────── -->
    <div v-if="totalTemplates === 0" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" class="empty-icon" aria-hidden="true">
        <rect x="5" y="4" width="14" height="16" rx="1.5" stroke="currentColor" stroke-width="1.6" />
        <path d="M9 8h6M9 12h6M9 16h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
      </svg>
      <p>No templates found.</p>
    </div>

    <div v-else :class="viewMode === 'grid' ? 'cards-grid' : 'cards-list'">
      <div
        v-for="tpl in paginatedTemplates"
        :key="tpl.id"
        class="template-card"
        @click.stop
      >
        <!-- Card header -->
        <div class="card-header">
          <div class="card-title-row">
            <span class="card-name">{{ tpl.name }}</span>
            <span class="category-badge" :class="categoryClass(tpl.category)">{{ tpl.category }}</span>
          </div>
          <button
            class="fav-btn"
            :class="{ 'fav-btn--active': tpl.favorite }"
            type="button"
            :aria-label="tpl.favorite ? 'Remove from favorites' : 'Add to favorites'"
            @click.stop="toggleFavorite(tpl)"
          >
            <svg viewBox="0 0 24 24" fill="none">
              <path
                d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2Z"
                :fill="tpl.favorite ? '#f59e0b' : 'none'"
                stroke="#f59e0b"
                stroke-width="1.6"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </button>

          <!-- More options button (list view) -->
          <div v-if="viewMode === 'list'" class="menu-wrap">
            <button
              class="more-btn"
              type="button"
              :aria-label="`Actions for ${tpl.name}`"
              @click.stop="toggleMenu(tpl.id, $event)"
            >
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="5" r="1" fill="currentColor" />
                <circle cx="12" cy="12" r="1" fill="currentColor" />
                <circle cx="12" cy="19" r="1" fill="currentColor" />
              </svg>
            </button>
            <div v-if="activeMenuId === tpl.id" class="dropdown-menu" role="menu" @click.stop>
              <button class="dropdown-item" role="menuitem" type="button">Edit</button>
              <button class="dropdown-item" role="menuitem" type="button">Duplicate</button>
              <button class="dropdown-item dropdown-item--danger" role="menuitem" type="button">Delete</button>
            </div>
          </div>
        </div>

        <!-- Body preview -->
        <div class="card-body">
          <p class="card-preview">{{ tpl.body }}</p>
        </div>

        <!-- Footer -->
        <div class="card-footer">
          <div class="card-meta">
            <span class="meta-text">Used {{ tpl.usedTimes }} times</span>
            <span class="meta-sep">·</span>
            <span class="meta-text">Updated {{ tpl.updatedAgo }}</span>
          </div>
          <div class="card-actions">
            <button class="action-btn" type="button" aria-label="Preview template">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M1 12S5 4 12 4s11 8 11 8-4 8-11 8S1 12 1 12Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.6" />
              </svg>
            </button>
            <button class="action-btn" type="button" aria-label="Duplicate template">
              <svg viewBox="0 0 24 24" fill="none">
                <rect x="9" y="9" width="13" height="13" rx="2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </button>
            <div class="menu-wrap">
              <button
                class="action-btn"
                type="button"
                :aria-label="`More actions for ${tpl.name}`"
                @click.stop="toggleMenu(tpl.id, $event)"
              >
                <svg viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="5" r="1" fill="currentColor" />
                  <circle cx="12" cy="12" r="1" fill="currentColor" />
                  <circle cx="12" cy="19" r="1" fill="currentColor" />
                </svg>
              </button>
              <div v-if="activeMenuId === tpl.id" class="dropdown-menu" role="menu" @click.stop>
                <button class="dropdown-item" role="menuitem" type="button">Edit</button>
                <button class="dropdown-item" role="menuitem" type="button">Duplicate</button>
                <button class="dropdown-item dropdown-item--danger" role="menuitem" type="button">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Pagination ──────────────────────────────────────────────────── -->
    <div v-if="totalTemplates > 0" class="pagination-bar">
      <span class="pagination-info">
        Showing {{ showingFrom }} to {{ showingTo }} of {{ totalTemplates }} templates
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
            <path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
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
            <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ── Layout ─────────────────────────────────────────────────────────────── */
.templates-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ── Page header ─────────────────────────────────────────────────────────── */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 4px;
}

.page-subtitle {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.page-header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* ── Search ──────────────────────────────────────────────────────────────── */
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
  padding: 9px 12px 9px 32px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 0.875rem;
  color: #374151;
  background: #fff;
  width: 220px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input:focus {
  border-color: #1b9a5d;
  box-shadow: 0 0 0 3px rgba(27, 154, 93, 0.12);
}

/* ── Primary button ──────────────────────────────────────────────────────── */
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
  white-space: nowrap;
}

.btn-primary:hover {
  background: #168a52;
}

/* ── Stats grid ──────────────────────────────────────────────────────────── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #fff;
  border: 1px solid rgba(226, 232, 240, 0.9);
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
}

.stat-icon-wrap {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon-wrap--templates {
  background: #e8f5ef;
  color: #1b9a5d;
}

.stat-icon-wrap--used {
  background: #eff6ff;
  color: #3b82f6;
}

.stat-icon-wrap--star {
  background: #fef9ec;
  color: #f59e0b;
}

.stat-icon-wrap--tag {
  background: #fdf4ff;
  color: #a855f7;
}

.stat-icon-wrap svg {
  width: 22px;
  height: 22px;
}

.stat-label {
  margin: 0;
  font-size: 0.8rem;
  color: #6b7280;
  font-weight: 500;
}

.stat-value {
  margin: 4px 0 2px;
  font-size: 1.75rem;
  font-weight: 800;
  color: #111827;
  line-height: 1;
}

.stat-hint {
  margin: 0;
  font-size: 0.78rem;
  font-weight: 500;
}

/* ── Filter row ──────────────────────────────────────────────────────────── */
.filter-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0;
}

/* ── Tabs ─────────────────────────────────────────────────────────────────── */
.tabs {
  display: flex;
  gap: 0;
  overflow-x: auto;
}

.tab-btn {
  padding: 10px 16px;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  white-space: nowrap;
  transition: color 0.2s, border-color 0.2s;
  margin-bottom: -1px;
}

.tab-btn:hover {
  color: #374151;
}

.tab-btn--active {
  color: #1b9a5d;
  border-bottom-color: #1b9a5d;
  font-weight: 600;
}

/* ── Toolbar right ───────────────────────────────────────────────────────── */
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 8px;
}

.select-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.select-icon {
  position: absolute;
  left: 9px;
  width: 13px;
  height: 13px;
  color: #9ca3af;
  pointer-events: none;
}

.filter-select {
  padding: 7px 12px 7px 28px;
  border: 1px solid #d1d5db;
  border-radius: 9px;
  font-size: 0.8rem;
  color: #374151;
  background: #fff;
  cursor: pointer;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
  transition: border-color 0.2s;
  padding-right: 24px;
}

.filter-select:focus {
  border-color: #1b9a5d;
}

/* ── View toggle ─────────────────────────────────────────────────────────── */
.view-toggle {
  display: flex;
  border: 1px solid #d1d5db;
  border-radius: 9px;
  overflow: hidden;
}

.view-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  background: #fff;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  transition: background 0.2s, color 0.2s;
}

.view-btn + .view-btn {
  border-left: 1px solid #d1d5db;
}

.view-btn:hover {
  background: #f9fafb;
  color: #374151;
}

.view-btn--active {
  background: #f0faf5;
  color: #1b9a5d;
}

.view-btn svg {
  width: 15px;
  height: 15px;
}

/* ── Cards grid ──────────────────────────────────────────────────────────── */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.cards-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* ── Template card ───────────────────────────────────────────────────────── */
.template-card {
  display: flex;
  flex-direction: column;
  background: #fff;
  border: 1px solid rgba(226, 232, 240, 0.9);
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
  overflow: hidden;
  transition: box-shadow 0.2s, transform 0.15s;
}

.template-card:hover {
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.09);
  transform: translateY(-1px);
}

/* Card header */
.card-header {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 14px 14px 10px;
}

.card-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  flex-wrap: wrap;
  min-width: 0;
}

.card-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: #111827;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Category badge */
.category-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

.badge--welcome {
  background: #e8f5ef;
  color: #1b9a5d;
}

.badge--promo {
  background: #eff6ff;
  color: #3b82f6;
}

.badge--reminder {
  background: #fff7ed;
  color: #ea580c;
}

.badge--followup {
  background: #fdf4ff;
  color: #a855f7;
}

.badge--other {
  background: #f1f5f9;
  color: #64748b;
}

.badge--default {
  background: #f3f4f6;
  color: #6b7280;
}

/* Favorite button */
.fav-btn {
  flex-shrink: 0;
  background: none;
  border: none;
  padding: 2px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #d1d5db;
  transition: color 0.2s;
  margin-left: auto;
}

.fav-btn svg {
  width: 16px;
  height: 16px;
}

.fav-btn:hover {
  color: #f59e0b;
}

.fav-btn--active {
  color: #f59e0b;
}

/* Card body */
.card-body {
  flex: 1;
  padding: 0 14px 10px;
  background: #f9fafb;
  margin: 0 14px;
  border-radius: 8px;
}

.card-preview {
  margin: 8px 0;
  font-size: 0.8rem;
  color: #4b5563;
  line-height: 1.55;
  white-space: pre-line;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Card footer */
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px 12px;
  gap: 8px;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}

.meta-text {
  font-size: 0.75rem;
  color: #9ca3af;
}

.meta-sep {
  font-size: 0.75rem;
  color: #d1d5db;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: none;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  color: #9ca3af;
  transition: background 0.15s, color 0.15s;
  padding: 0;
}

.action-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.action-btn svg {
  width: 14px;
  height: 14px;
}

/* ── Dropdown menu ───────────────────────────────────────────────────────── */
.menu-wrap {
  position: relative;
}

.more-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: none;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  color: #9ca3af;
  transition: background 0.15s, color 0.15s;
  padding: 0;
}

.more-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.more-btn svg {
  width: 14px;
  height: 14px;
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: calc(100% + 4px);
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.1);
  min-width: 130px;
  z-index: 50;
  overflow: hidden;
}

.dropdown-item {
  display: block;
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  padding: 9px 14px;
  font-size: 0.85rem;
  color: #374151;
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

/* ── Empty state ─────────────────────────────────────────────────────────── */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 60px 20px;
  color: #9ca3af;
  font-size: 0.9rem;
}

.empty-icon {
  width: 48px;
  height: 48px;
  stroke: #d1d5db;
  stroke-width: 1.4;
}

/* ── Pagination ──────────────────────────────────────────────────────────── */
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  padding-top: 4px;
}

.pagination-info {
  font-size: 0.85rem;
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
  min-width: 34px;
  height: 34px;
  padding: 0 6px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.85rem;
  color: #374151;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}

.page-btn svg {
  width: 14px;
  height: 14px;
}

.page-btn:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #d1d5db;
}

.page-btn--active {
  background: #1b9a5d;
  border-color: #1b9a5d;
  color: #fff;
  font-weight: 600;
}

.page-btn--active:hover {
  background: #168a52 !important;
}

.page-btn--ellipsis {
  cursor: default;
  border-color: transparent;
  background: none;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: default;
}

/* ── Responsive ──────────────────────────────────────────────────────────── */
@media (max-width: 1199px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .cards-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 767px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .page-header-right {
    width: 100%;
    flex-wrap: wrap;
  }

  .search-input {
    width: 100%;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .filter-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .toolbar-right {
    flex-wrap: wrap;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }

  .pagination-bar {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>

