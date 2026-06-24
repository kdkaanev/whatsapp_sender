<script setup>
import { ref, computed, nextTick, watch } from 'vue'

// ── Mock conversations ───────────────────────────────────────────────────────
const allConversations = ref([
  {
    id: 1,
    name: 'Иван Петров',
    phone: '+359 88 123 4567',
    initials: 'ИП',
    avatarColor: '#4f46e5',
    preview: 'Здравейте! Имаме специална промоция...',
    status: 'Delivered',
    time: '10:15',
    date: '24.06.2026',
    email: 'ivan.petrov@example.com',
    tags: ['VIP', 'Client'],
    added: '15.05.2026 14:30',
    lastActive: '24.06.2026 10:17',
    campaign: 'Summer Promo 2026',
    campaignSent: '24.06.2026 10:15',
    campaignRecipients: 520,
    messageId: 'wamid.HBgNMTU0ODkw...',
    messages: [
      {
        id: 1,
        type: 'sent',
        text: 'Здравейте Иван,\n🎉\n\nИмаме специална промоция само за Вас!\nВъзползвайте се от 15% отстъпка на всички продукти през този уикенд.\n\nОчакваме Ви! 🙌\n\nВашият екип',
        time: '10:15',
        status: 'Delivered',
      },
      { id: 2, type: 'received', text: 'Благодаря! Ще се възползвам.', time: '10:17' },
    ],
  },
  {
    id: 2,
    name: 'Мария Георгиева',
    phone: '+359 88 234 5678',
    initials: 'МГ',
    avatarColor: '#db2777',
    preview: 'Благодаря! Ще се възползвам.',
    status: 'Read',
    time: '10:12',
    date: '24.06.2026',
    email: 'maria.georgieva@example.com',
    tags: ['Client'],
    added: '10.04.2026 09:20',
    lastActive: '24.06.2026 10:12',
    campaign: 'Summer Promo 2026',
    campaignSent: '24.06.2026 10:10',
    campaignRecipients: 520,
    messageId: 'wamid.HBgNMTU0OGcd...',
    messages: [
      {
        id: 1,
        type: 'sent',
        text: 'Здравейте Мария,\n🎉\n\nИмаме специална промоция само за Вас!\nВъзползвайте се от 15% отстъпка на всички продукти през този уикенд.\n\nОчакваме Ви! 🙌\n\nВашият екип',
        time: '10:10',
        status: 'Read',
      },
      { id: 2, type: 'received', text: 'Благодаря! Ще се възползвам.', time: '10:12' },
    ],
  },
  {
    id: 3,
    name: 'Георги Георгиев',
    phone: '+359 88 345 6789',
    initials: 'ГГ',
    avatarColor: '#059669',
    preview: 'Кога изтича промоцията?',
    status: 'Delivered',
    time: '10:10',
    date: '24.06.2026',
    email: 'georgi.georgiev@example.com',
    tags: [],
    added: '22.03.2026 11:00',
    lastActive: '24.06.2026 10:10',
    campaign: 'Summer Promo 2026',
    campaignSent: '24.06.2026 10:08',
    campaignRecipients: 520,
    messageId: 'wamid.HBgNMTU0OHef...',
    messages: [
      {
        id: 1,
        type: 'sent',
        text: 'Здравейте Георги,\n🎉\n\nИмаме специална промоция само за Вас!\nВъзползвайте се от 15% отстъпка на всички продукти през този уикенд.\n\nОчакваме Ви! 🙌\n\nВашият екип',
        time: '10:08',
        status: 'Delivered',
      },
      { id: 2, type: 'received', text: 'Кога изтича промоцията?', time: '10:10' },
    ],
  },
  {
    id: 4,
    name: 'Елена Димитрова',
    phone: '+359 88 456 7890',
    initials: 'ЕД',
    avatarColor: '#7c3aed',
    preview: 'Чудесно, благодаря!',
    status: 'Read',
    time: '10:05',
    date: '24.06.2026',
    email: 'elena.dimitrova@example.com',
    tags: ['VIP'],
    added: '05.05.2026 15:45',
    lastActive: '24.06.2026 10:05',
    campaign: 'Summer Promo 2026',
    campaignSent: '24.06.2026 10:00',
    campaignRecipients: 520,
    messageId: 'wamid.HBgNMTU0OIgh...',
    messages: [
      {
        id: 1,
        type: 'sent',
        text: 'Здравейте Елена,\n🎉\n\nИмаме специална промоция само за Вас!\nВъзползвайте се от 15% отстъпка на всички продукти през този уикенд.\n\nОчакваме Ви! 🙌\n\nВашият екип',
        time: '10:00',
        status: 'Read',
      },
      { id: 2, type: 'received', text: 'Чудесно, благодаря!', time: '10:05' },
    ],
  },
  {
    id: 5,
    name: 'Димитър Стоянов',
    phone: '+359 88 567 8901',
    initials: 'ДС',
    avatarColor: '#8b5cf6',
    preview: 'Изпращате ли до друг град?',
    status: 'Sent',
    time: '09:58',
    date: '24.06.2026',
    email: 'dimitar.stoyanov@example.com',
    tags: [],
    added: '14.02.2026 08:30',
    lastActive: '24.06.2026 09:58',
    campaign: 'Summer Promo 2026',
    campaignSent: '24.06.2026 09:55',
    campaignRecipients: 520,
    messageId: 'wamid.HBgNMTU0OJij...',
    messages: [
      {
        id: 1,
        type: 'sent',
        text: 'Здравейте Димитър,\n🎉\n\nИмаме специална промоция само за Вас!\nВъзползвайте се от 15% отстъпка на всички продукти през този уикенд.\n\nОчакваме Ви! 🙌\n\nВашият екип',
        time: '09:55',
        status: 'Sent',
      },
      { id: 2, type: 'received', text: 'Изпращате ли до друг град?', time: '09:58' },
    ],
  },
  {
    id: 6,
    name: 'Николай Николов',
    phone: '+359 88 678 9012',
    initials: 'НН',
    avatarColor: '#0891b2',
    preview: 'Ок, ще проверя.',
    status: 'Read',
    time: '09:45',
    date: '24.06.2026',
    email: 'nikolay.nikolov@example.com',
    tags: ['Client'],
    added: '20.01.2026 12:00',
    lastActive: '24.06.2026 09:45',
    campaign: 'Summer Promo 2026',
    campaignSent: '24.06.2026 09:40',
    campaignRecipients: 520,
    messageId: 'wamid.HBgNMTU0OKkl...',
    messages: [
      {
        id: 1,
        type: 'sent',
        text: 'Здравейте Николай,\n🎉\n\nИмаме специална промоция само за Вас!\nВъзползвайте се от 15% отстъпка на всички продукти през този уикенд.\n\nОчакваме Ви! 🙌\n\nВашият екип',
        time: '09:40',
        status: 'Read',
      },
      { id: 2, type: 'received', text: 'Ок, ще проверя.', time: '09:45' },
    ],
  },
  {
    id: 7,
    name: 'София Василева',
    phone: '+359 88 789 0123',
    initials: 'СВ',
    avatarColor: '#d97706',
    preview: 'Много добра оферта!',
    status: 'Read',
    time: '09:40',
    date: '24.06.2026',
    email: 'sofia.vasileva@example.com',
    tags: ['VIP'],
    added: '18.03.2026 10:15',
    lastActive: '24.06.2026 09:40',
    campaign: 'Summer Promo 2026',
    campaignSent: '24.06.2026 09:35',
    campaignRecipients: 520,
    messageId: 'wamid.HBgNMTU0OLmn...',
    messages: [
      {
        id: 1,
        type: 'sent',
        text: 'Здравейте София,\n🎉\n\nИмаме специална промоция само за Вас!\nВъзползвайте се от 15% отстъпка на всички продукти през този уикенд.\n\nОчакваме Ви! 🙌\n\nВашият екип',
        time: '09:35',
        status: 'Read',
      },
      { id: 2, type: 'received', text: 'Много добра оферта!', time: '09:40' },
    ],
  },
  {
    id: 8,
    name: 'Пламен Петров',
    phone: '+359 88 890 1234',
    initials: 'ПП',
    avatarColor: '#16a34a',
    preview: 'Благодаря за информацията.',
    status: 'Delivered',
    time: '09:30',
    date: '24.06.2026',
    email: 'plamen.petrov@example.com',
    tags: [],
    added: '01.04.2026 09:00',
    lastActive: '24.06.2026 09:30',
    campaign: 'Summer Promo 2026',
    campaignSent: '24.06.2026 09:25',
    campaignRecipients: 520,
    messageId: 'wamid.HBgNMTU0OMop...',
    messages: [
      {
        id: 1,
        type: 'sent',
        text: 'Здравейте Пламен,\n🎉\n\nИмаме специална промоция само за Вас!\nВъзползвайте се от 15% отстъпка на всички продукти през този уикенд.\n\nОчакваме Ви! 🙌\n\nВашият екип',
        time: '09:25',
        status: 'Delivered',
      },
      { id: 2, type: 'received', text: 'Благодаря за информацията.', time: '09:30' },
    ],
  },
])

// ── State ────────────────────────────────────────────────────────────────────
const activeTab = ref('All Messages')
const searchQuery = ref('')
const messageText = ref('')
const selectedConversation = ref(allConversations.value[0])
const currentPage = ref(1)
const pageSize = 8
const totalMessages = 1245
const chatScrollRef = ref(null)

const tabs = ['All Messages', 'Sent', 'Delivered', 'Read', 'Failed']

// ── Filtering ────────────────────────────────────────────────────────────────
const filteredConversations = computed(() => {
  let list = allConversations.value
  if (activeTab.value !== 'All Messages') {
    list = list.filter((c) => c.status === activeTab.value)
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(
      (c) => c.name.toLowerCase().includes(q) || c.preview.toLowerCase().includes(q),
    )
  }
  return list
})

const totalPages = computed(() => Math.ceil(totalMessages / pageSize))

const pageNumbers = computed(() => {
  const total = totalPages.value
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  const cur = currentPage.value
  const pages = [1]
  if (cur > 3) pages.push('...')
  for (let p = Math.max(2, cur - 1); p <= Math.min(total - 1, cur + 1); p++) pages.push(p)
  if (cur < total - 2) pages.push('...')
  pages.push(total)
  return pages
})

const showingFrom = computed(() => (currentPage.value - 1) * pageSize + 1)
const showingTo = computed(() => Math.min(currentPage.value * pageSize, totalMessages))

// ── Methods ──────────────────────────────────────────────────────────────────
const setTab = (tab) => {
  activeTab.value = tab
  currentPage.value = 1
}

const goToPage = (p) => {
  if (p === '...' || p < 1 || p > totalPages.value) return
  currentPage.value = p
}

const selectConversation = (conv) => {
  selectedConversation.value = conv
}

const statusClass = (status) => {
  const map = {
    Delivered: 'status--delivered',
    Read: 'status--read',
    Sent: 'status--sent',
    Failed: 'status--failed',
  }
  return map[status] ?? ''
}

const tagClass = (tag) => {
  const map = {
    VIP: 'tag--vip',
    Client: 'tag--client',
  }
  return map[tag] ?? 'tag--default'
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatScrollRef.value) {
    chatScrollRef.value.scrollTop = chatScrollRef.value.scrollHeight
  }
}

const sendMessage = () => {
  if (!messageText.value.trim() || !selectedConversation.value) return
  selectedConversation.value.messages.push({
    id: Date.now(),
    type: 'sent',
    text: messageText.value.trim(),
    time: new Date().toLocaleTimeString('bg-BG', { hour: '2-digit', minute: '2-digit' }),
    status: 'Sent',
  })
  messageText.value = ''
  scrollToBottom()
}

const handleKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).catch(() => {})
}

watch(selectedConversation, () => scrollToBottom(), { immediate: true })
</script>

<template>
  <div class="messages-page">
    <!-- ── Page header ─────────────────────────────────────────────────────── -->
    <div class="page-header">
      <div class="page-header-left">
        <h1 class="page-title">Messages</h1>
        <p class="page-subtitle">Track and manage all your messages in one place</p>
      </div>
      <div class="page-header-right">
        <div class="search-wrap">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            <path d="m21 21-4.35-4.35" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
          </svg>
          <input type="search" class="search-input" placeholder="Search messages..." aria-label="Search messages" />
        </div>
        <button class="btn-outline" type="button">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          Filters
        </button>
        <button class="btn-outline" type="button">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
            <polyline points="7 10 12 15 17 10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
            <line x1="12" y1="15" x2="12" y2="3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
          </svg>
          Export
        </button>
      </div>
    </div>

    <!-- ── Tabs + date range ───────────────────────────────────────────────── -->
    <div class="tabs-row">
      <div class="tabs" role="tablist">
        <button
          v-for="tab in tabs"
          :key="tab"
          class="tab-btn"
          :class="{ 'tab-btn--active': activeTab === tab }"
          type="button"
          role="tab"
          :aria-selected="activeTab === tab"
          @click="setTab(tab)"
        >
          {{ tab }}
        </button>
      </div>
      <div class="date-range">
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <rect x="3" y="4" width="18" height="18" rx="2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
          <path d="M16 2v4M8 2v4M3 10h18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
        </svg>
        25 May – 25 Jun 2026
        <svg class="chevron-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
    </div>

    <!-- ── Three-column layout ─────────────────────────────────────────────── -->
    <div class="messages-layout">
      <!-- Left: Conversation list -->
      <div class="conv-panel">
        <div class="conv-search">
          <div class="conv-search-wrap">
            <svg class="conv-search-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
              <path d="m21 21-4.35-4.35" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            </svg>
            <input
              v-model="searchQuery"
              type="search"
              class="conv-search-input"
              placeholder="Search by contact or message..."
              aria-label="Search conversations"
            />
          </div>
          <button class="btn-filter" type="button">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            Filter
          </button>
        </div>

        <div class="conv-list" role="list">
          <div
            v-for="conv in filteredConversations"
            :key="conv.id"
            class="conv-item"
            :class="{ 'conv-item--active': selectedConversation?.id === conv.id }"
            role="listitem"
            tabindex="0"
            @click="selectConversation(conv)"
            @keydown.enter="selectConversation(conv)"
          >
            <div class="conv-avatar" :style="{ background: conv.avatarColor }">
              {{ conv.initials }}
            </div>
            <div class="conv-info">
              <div class="conv-info-top">
                <span class="conv-name">{{ conv.name }}</span>
                <span class="conv-status" :class="statusClass(conv.status)">{{ conv.status }}</span>
              </div>
              <div class="conv-info-bottom">
                <span class="conv-preview">{{ conv.preview }}</span>
                <span class="conv-time">{{ conv.time }}</span>
              </div>
            </div>
          </div>

          <div v-if="filteredConversations.length === 0" class="conv-empty">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <p>No messages found.</p>
          </div>
        </div>

        <div class="conv-footer">
          <p class="conv-showing">
            Showing {{ showingFrom }} to {{ showingTo }} of {{ totalMessages.toLocaleString() }} messages
          </p>
          <div class="pagination">
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

      <!-- Middle: Chat view -->
      <div class="chat-panel" v-if="selectedConversation">
        <!-- Chat header -->
        <div class="chat-header">
          <div class="chat-header-left">
            <div class="chat-avatar" :style="{ background: selectedConversation.avatarColor }">
              {{ selectedConversation.initials }}
            </div>
            <div class="chat-contact-info">
              <p class="chat-contact-name">{{ selectedConversation.name }}</p>
              <p class="chat-contact-phone">{{ selectedConversation.phone }}</p>
            </div>
          </div>
          <div class="chat-header-right">
            <span class="conv-status" :class="statusClass(selectedConversation.status)">
              {{ selectedConversation.status }}
            </span>
            <span class="chat-date">{{ selectedConversation.date }}  {{ selectedConversation.time }}</span>
          </div>
        </div>

        <!-- Campaign banner -->
        <div class="campaign-banner">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6" />
            <path d="M12 8v4M12 16h.01" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
          </svg>
          <span>
            This message was sent as part of the campaign
            <a href="#" class="campaign-link">{{ selectedConversation.campaign }}</a>
            <svg viewBox="0 0 24 24" fill="none" class="campaign-link-icon" aria-hidden="true">
              <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </span>
        </div>

        <!-- Messages -->
        <div class="chat-messages" ref="chatScrollRef">
          <div
            v-for="msg in selectedConversation.messages"
            :key="msg.id"
            class="chat-msg"
            :class="msg.type === 'sent' ? 'chat-msg--sent' : 'chat-msg--received'"
          >
            <div class="chat-bubble">
              <p class="chat-bubble-text">{{ msg.text }}</p>
              <div class="chat-bubble-meta">
                <span class="chat-bubble-time">{{ msg.time }}</span>
                <svg
                  v-if="msg.type === 'sent'"
                  class="chat-tick"
                  :class="msg.status === 'Read' ? 'chat-tick--read' : 'chat-tick--delivered'"
                  viewBox="0 0 24 24"
                  fill="none"
                  aria-hidden="true"
                >
                  <path d="M4 12l5 5L20 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  <path d="M9 12l5 5L20 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Message input -->
        <div class="chat-input-row">
          <div class="chat-input-wrap">
            <div class="chat-input-actions">
              <button class="chat-action-btn" type="button" aria-label="Emoji">
                <svg viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6" />
                  <path d="M8 14s1.5 2 4 2 4-2 4-2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
                  <circle cx="9" cy="10" r="1" fill="currentColor" />
                  <circle cx="15" cy="10" r="1" fill="currentColor" />
                </svg>
              </button>
              <button class="chat-action-btn" type="button" aria-label="Attach file">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </button>
              <button class="chat-action-btn" type="button" aria-label="Insert template">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M8 6h8M8 10h5M8 14h8M8 18h5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
                  <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="1.6" />
                </svg>
              </button>
            </div>
            <textarea
              v-model="messageText"
              class="chat-textarea"
              placeholder="Type a message..."
              rows="1"
              aria-label="Message input"
              @keydown="handleKeydown"
            ></textarea>
            <button class="btn-send" type="button" :disabled="!messageText.trim()" @click="sendMessage">
              <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M22 2 11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M22 2 15 22 11 13 2 9l20-7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              Send
            </button>
          </div>
        </div>
      </div>

      <!-- Right: Details panel -->
      <div class="details-panel" v-if="selectedConversation">
        <!-- Contact Details -->
        <div class="details-section">
          <div class="details-section-header">
            <h3 class="details-section-title">Contact Details</h3>
            <div class="details-section-actions">
              <button class="btn-text" type="button">Edit</button>
              <button class="btn-icon" type="button" aria-label="More options">
                <svg viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="5" r="1" fill="currentColor" />
                  <circle cx="12" cy="12" r="1" fill="currentColor" />
                  <circle cx="12" cy="19" r="1" fill="currentColor" />
                </svg>
              </button>
            </div>
          </div>

          <div class="contact-preview">
            <div class="contact-preview-avatar" :style="{ background: selectedConversation.avatarColor }">
              {{ selectedConversation.initials }}
            </div>
            <div>
              <p class="contact-preview-name">{{ selectedConversation.name }}</p>
              <p class="contact-preview-phone">{{ selectedConversation.phone }}</p>
            </div>
          </div>

          <div class="details-rows">
            <div class="details-row">
              <span class="details-label">Email</span>
              <span class="details-value">{{ selectedConversation.email }}</span>
            </div>
            <div class="details-row">
              <span class="details-label">Tags</span>
              <div class="details-tags">
                <span
                  v-for="tag in selectedConversation.tags"
                  :key="tag"
                  class="tag"
                  :class="tagClass(tag)"
                >{{ tag }}</span>
                <span v-if="selectedConversation.tags.length === 0" class="details-value">—</span>
              </div>
            </div>
            <div class="details-row">
              <span class="details-label">Added</span>
              <span class="details-value">{{ selectedConversation.added }}</span>
            </div>
            <div class="details-row">
              <span class="details-label">Last Active</span>
              <span class="details-value">{{ selectedConversation.lastActive }}</span>
            </div>
          </div>

          <button class="btn-full-outline" type="button">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M4 18a5 5 0 0 1 10 0" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            View Contact
          </button>
        </div>

        <!-- Campaign Details -->
        <div class="details-section">
          <h3 class="details-section-title">Campaign Details</h3>
          <div class="details-rows">
            <div class="details-row">
              <span class="details-label">Campaign Name</span>
              <div class="details-value-row">
                <span class="details-value">{{ selectedConversation.campaign }}</span>
                <svg viewBox="0 0 24 24" fill="none" class="details-link-icon" aria-hidden="true">
                  <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </div>
            </div>
            <div class="details-row">
              <span class="details-label">Sent</span>
              <span class="details-value">{{ selectedConversation.campaignSent }}</span>
            </div>
            <div class="details-row">
              <span class="details-label">Recipients</span>
              <span class="details-value">{{ selectedConversation.campaignRecipients }}</span>
            </div>
          </div>

          <button class="btn-full-outline" type="button">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M5 11.5 19 5l-6.5 14-2.5-5-5-2.5Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            View Campaign
          </button>
        </div>

        <!-- Message Details -->
        <div class="details-section">
          <h3 class="details-section-title">Message Details</h3>
          <div class="details-rows">
            <div class="details-row">
              <span class="details-label">Status</span>
              <span class="msg-status-badge" :class="statusClass(selectedConversation.status)">
                {{ selectedConversation.status }}
              </span>
            </div>
            <div class="details-row">
              <span class="details-label">Channel</span>
              <div class="details-value-row">
                <svg viewBox="0 0 24 24" fill="none" class="whatsapp-icon" aria-hidden="true">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z" fill="#25D366" />
                  <path d="M12 2C6.477 2 2 6.477 2 12c0 1.89.525 3.66 1.438 5.168L2 22l4.978-1.304A9.96 9.96 0 0 0 12 22c5.523 0 10-4.477 10-10S17.523 2 12 2z" stroke="#25D366" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <span class="details-value">WhatsApp</span>
              </div>
            </div>
            <div class="details-row details-row--msgid">
              <span class="details-label">Message ID</span>
              <div class="details-value-row">
                <span class="details-value msg-id">{{ selectedConversation.messageId }}</span>
                <button
                  class="btn-copy"
                  type="button"
                  aria-label="Copy message ID"
                  @click="copyToClipboard(selectedConversation.messageId)"
                >
                  <svg viewBox="0 0 24 24" fill="none">
                    <rect x="9" y="9" width="13" height="13" rx="2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ── Page shell ─────────────────────────────────────────────────────────────── */
.messages-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

/* ── Page header ────────────────────────────────────────────────────────────── */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 4px;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
}

.page-header-right {
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
  left: 12px;
  width: 16px;
  height: 16px;
  color: #94a3b8;
  pointer-events: none;
}

.search-input {
  padding: 9px 14px 9px 36px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.875rem;
  background: #fff;
  color: #1e293b;
  width: 220px;
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: #1b9a5d;
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 9px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #fff;
  color: #374151;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}

.btn-outline svg {
  width: 16px;
  height: 16px;
}

.btn-outline:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

/* ── Tabs row ───────────────────────────────────────────────────────────────── */
.tabs-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 0;
}

.tabs {
  display: flex;
  gap: 4px;
}

.tab-btn {
  padding: 10px 18px;
  border: none;
  background: transparent;
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: color 0.2s, border-color 0.2s;
  margin-bottom: -1px;
}

.tab-btn:hover {
  color: #1b9a5d;
}

.tab-btn--active {
  color: #1b9a5d;
  border-bottom-color: #1b9a5d;
}

.date-range {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #374151;
  background: #fff;
  cursor: pointer;
  white-space: nowrap;
}

.date-range svg {
  width: 15px;
  height: 15px;
  color: #64748b;
}

.chevron-icon {
  width: 14px !important;
  height: 14px !important;
}

/* ── Three-column layout ────────────────────────────────────────────────────── */
.messages-layout {
  display: flex;
  gap: 0;
  flex: 1;
  min-height: 0;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  overflow: hidden;
  background: #fff;
}

/* ── Conversation panel ─────────────────────────────────────────────────────── */
.conv-panel {
  width: 320px;
  flex: 0 0 320px;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e2e8f0;
  overflow: hidden;
}

.conv-search {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px;
  border-bottom: 1px solid #f1f5f9;
}

.conv-search-wrap {
  position: relative;
  flex: 1;
}

.conv-search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 15px;
  height: 15px;
  color: #94a3b8;
  pointer-events: none;
}

.conv-search-input {
  width: 100%;
  padding: 8px 10px 8px 32px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 0.8125rem;
  background: #f8fafc;
  color: #1e293b;
  outline: none;
  transition: border-color 0.2s;
}

.conv-search-input:focus {
  border-color: #1b9a5d;
  background: #fff;
}

.btn-filter {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: #fff;
  color: #374151;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
}

.btn-filter svg {
  width: 14px;
  height: 14px;
}

.btn-filter:hover {
  background: #f1f5f9;
}

.conv-list {
  flex: 1;
  overflow-y: auto;
}

.conv-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  cursor: pointer;
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.15s;
  outline: none;
}

.conv-item:hover {
  background: #f8fafc;
}

.conv-item--active {
  background: #eef8f1;
  border-left: 3px solid #1b9a5d;
}

.conv-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 0.8rem;
  font-weight: 700;
  flex-shrink: 0;
}

.conv-info {
  flex: 1;
  min-width: 0;
}

.conv-info-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  margin-bottom: 4px;
}

.conv-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conv-info-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}

.conv-preview {
  font-size: 0.8rem;
  color: #64748b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.conv-time {
  font-size: 0.75rem;
  color: #94a3b8;
  white-space: nowrap;
  flex-shrink: 0;
}

.conv-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 40px 20px;
  color: #94a3b8;
  text-align: center;
}

.conv-empty svg {
  width: 40px;
  height: 40px;
}

.conv-footer {
  padding: 12px 14px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #fafafa;
}

.conv-showing {
  font-size: 0.75rem;
  color: #64748b;
  margin: 0;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}

.page-btn {
  min-width: 28px;
  height: 28px;
  padding: 0 6px;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  background: #fff;
  color: #374151;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, border-color 0.15s;
}

.page-btn svg {
  width: 14px;
  height: 14px;
}

.page-btn:hover:not(:disabled) {
  background: #f1f5f9;
  border-color: #cbd5e1;
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

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ── Status badges ─────────────────────────────────────────────────────────── */
.conv-status {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
  white-space: nowrap;
  flex-shrink: 0;
}

.status--delivered {
  background: #d1fae5;
  color: #065f46;
}

.status--read {
  background: #ede9fe;
  color: #5b21b6;
}

.status--sent {
  background: #f1f5f9;
  color: #475569;
}

.status--failed {
  background: #fee2e2;
  color: #991b1b;
}

/* ── Chat panel ─────────────────────────────────────────────────────────────── */
.chat-panel {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e2e8f0;
  overflow: hidden;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  border-bottom: 1px solid #e2e8f0;
  gap: 12px;
}

.chat-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 0.8rem;
  font-weight: 700;
  flex-shrink: 0;
}

.chat-contact-name {
  font-size: 0.9375rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 2px;
}

.chat-contact-phone {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0;
}

.chat-header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-date {
  font-size: 0.8rem;
  color: #64748b;
  white-space: nowrap;
}

.campaign-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: #eff6ff;
  border-bottom: 1px solid #dbeafe;
  font-size: 0.8125rem;
  color: #1e40af;
}

.campaign-banner svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: #3b82f6;
}

.campaign-link {
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
  margin-left: 3px;
}

.campaign-link:hover {
  text-decoration: underline;
}

.campaign-link-icon {
  width: 14px;
  height: 14px;
  display: inline-block;
  vertical-align: middle;
  color: #2563eb;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px 18px;
  background: #f8f7fb;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-msg {
  display: flex;
}

.chat-msg--sent {
  justify-content: flex-end;
}

.chat-msg--received {
  justify-content: flex-start;
}

.chat-bubble {
  max-width: 70%;
  padding: 12px 14px;
  border-radius: 12px;
  font-size: 0.875rem;
  line-height: 1.5;
  position: relative;
}

.chat-msg--sent .chat-bubble {
  background: #d1fae5;
  color: #1e293b;
  border-bottom-right-radius: 4px;
}

.chat-msg--received .chat-bubble {
  background: #ffffff;
  color: #1e293b;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.chat-bubble-text {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.chat-bubble-meta {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
  margin-top: 6px;
}

.chat-bubble-time {
  font-size: 0.7rem;
  color: #94a3b8;
}

.chat-tick {
  width: 16px;
  height: 16px;
}

.chat-tick--delivered {
  color: #94a3b8;
}

.chat-tick--read {
  color: #1b9a5d;
}

.chat-input-row {
  padding: 12px 14px;
  border-top: 1px solid #e2e8f0;
  background: #fff;
}

.chat-input-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 8px 8px 8px 10px;
  background: #f8fafc;
}

.chat-input-actions {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

.chat-action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: #64748b;
  cursor: pointer;
  border-radius: 8px;
  transition: background 0.15s, color 0.15s;
  flex-shrink: 0;
}

.chat-action-btn svg {
  width: 18px;
  height: 18px;
}

.chat-action-btn:hover {
  background: #e2e8f0;
  color: #1b9a5d;
}

.chat-textarea {
  flex: 1;
  border: none;
  background: transparent;
  resize: none;
  font-size: 0.875rem;
  color: #1e293b;
  outline: none;
  line-height: 1.5;
  min-height: 36px;
  max-height: 120px;
  overflow-y: auto;
}

.chat-textarea::placeholder {
  color: #94a3b8;
}

.btn-send {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 9px 18px;
  background: #1b9a5d;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
  flex-shrink: 0;
}

.btn-send svg {
  width: 16px;
  height: 16px;
}

.btn-send:hover:not(:disabled) {
  background: #15803d;
}

.btn-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ── Details panel ──────────────────────────────────────────────────────────── */
.details-panel {
  width: 280px;
  flex: 0 0 280px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.details-section {
  padding: 18px 16px;
  border-bottom: 1px solid #e2e8f0;
}

.details-section:last-child {
  border-bottom: none;
}

.details-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.details-section-title {
  font-size: 0.9375rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 14px;
}

.details-section-header .details-section-title {
  margin: 0;
}

.details-section-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.btn-text {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #1b9a5d;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 6px;
  transition: background 0.15s;
}

.btn-text:hover {
  background: #eef8f1;
}

.btn-icon {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: #64748b;
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.15s;
}

.btn-icon svg {
  width: 18px;
  height: 18px;
}

.btn-icon:hover {
  background: #f1f5f9;
}

.contact-preview {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.contact-preview-avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 0.875rem;
  font-weight: 700;
  flex-shrink: 0;
}

.contact-preview-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 2px;
}

.contact-preview-phone {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0;
}

.details-rows {
  display: flex;
  flex-direction: column;
  gap: 11px;
  margin-bottom: 16px;
}

.details-row {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.details-label {
  font-size: 0.78rem;
  color: #94a3b8;
  font-weight: 500;
  min-width: 80px;
  flex-shrink: 0;
  padding-top: 2px;
}

.details-value {
  font-size: 0.8125rem;
  color: #1e293b;
  font-weight: 500;
  word-break: break-all;
}

.details-value-row {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
}

.details-link-icon {
  width: 14px;
  height: 14px;
  color: #1b9a5d;
  flex-shrink: 0;
}

.details-tags {
  display: flex;
  align-items: center;
  gap: 5px;
  flex-wrap: wrap;
}

.tag {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
}

.tag--vip {
  background: #fef3c7;
  color: #92400e;
}

.tag--client {
  background: #ede9fe;
  color: #5b21b6;
}

.tag--default {
  background: #f1f5f9;
  color: #475569;
}

.btn-full-outline {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  width: 100%;
  padding: 9px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: #fff;
  color: #374151;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}

.btn-full-outline svg {
  width: 15px;
  height: 15px;
}

.btn-full-outline:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.msg-status-badge {
  font-size: 0.78rem;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 8px;
}

.details-row--msgid .details-value-row {
  min-width: 0;
}

.msg-id {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100px;
  display: inline-block;
}

.whatsapp-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.btn-copy {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  display: flex;
  align-items: center;
  padding: 2px;
  border-radius: 4px;
  transition: color 0.15s;
  flex-shrink: 0;
}

.btn-copy svg {
  width: 14px;
  height: 14px;
}

.btn-copy:hover {
  color: #1b9a5d;
}

/* ── Scrollbar styling ─────────────────────────────────────────────────────── */
.conv-list::-webkit-scrollbar,
.chat-messages::-webkit-scrollbar,
.details-panel::-webkit-scrollbar {
  width: 5px;
}

.conv-list::-webkit-scrollbar-track,
.chat-messages::-webkit-scrollbar-track,
.details-panel::-webkit-scrollbar-track {
  background: transparent;
}

.conv-list::-webkit-scrollbar-thumb,
.chat-messages::-webkit-scrollbar-thumb,
.details-panel::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.5);
  border-radius: 3px;
}

/* ── Responsive ────────────────────────────────────────────────────────────── */
@media (max-width: 1100px) {
  .details-panel {
    display: none;
  }
}

@media (max-width: 768px) {
  .conv-panel {
    width: 100%;
    flex: unset;
    border-right: none;
  }

  .chat-panel {
    display: none;
  }

  .messages-layout {
    flex-direction: column;
  }
}
</style>

