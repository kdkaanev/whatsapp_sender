<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import router from '../router'

import { useCampaignStore } from '../stores/campaigns'

const campaignStore = useCampaignStore()

const searchTerm = ref('')
const activeTab = ref('All Campaigns')
const selectedDateRange = ref('25 May – 25 Jun 2026')
const currentPage = ref(1)
const pageSize = 8
const selectedCampaign = ref(null)
const campaignForm = ref({
  name: '',
  description: '',
  status: 'draft',
  messageBody: '',
})
const modalError = ref('')
const modalMessage = ref('')
const isSavingCampaign = ref(false)
const isSendingCampaign = ref(false)
const isDeletingCampaign = ref(false)
const isPageLoading = ref(false)
const pageError = ref('')
const campaignStatsById = ref({})
const pendingRefreshTimers = ref([])

const filterTabs = ['All Campaigns', 'Sent', 'Scheduled', 'Drafts', 'Failed']

const statusFilterMap = {
  'All Campaigns': () => true,
  Sent: (campaign) => ['Sent', 'Delivered'].includes(campaign.status),
  Scheduled: (campaign) => campaign.status === 'Scheduled',
  Drafts: (campaign) => campaign.status === 'Draft',
  Failed: (campaign) => campaign.status === 'Failed',
}

const normalizeStatus = (status) => {
  if (!status) {
    return 'Draft'
  }

  return status.charAt(0).toUpperCase() + status.slice(1).toLowerCase()
}

const formatCampaignDate = (value) => {
  if (!value) {
    return ' - '
  }

  if (typeof value === 'string' && value.includes('.') && value.includes(':')) {
    return value
  }

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return value
  }

  return new Intl.DateTimeFormat('bg-BG', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

const normalizeCampaign = (campaign) => ({
  ...campaign,
  id: campaign.id,
  name: campaign.name ?? 'Untitled campaign',
  description: campaign.description ?? campaign.preview ?? '',
  preview: campaign.preview ?? campaign.description ?? '',
  recipients: campaignStatsById.value[campaign.id]?.total ?? campaign.recipients ?? 0,
  status: normalizeStatus(campaign.status),
  sent: campaignStatsById.value[campaign.id]?.sent ?? campaign.sent ?? null,
  deliveredCount: campaignStatsById.value[campaign.id]?.delivered ?? campaign.deliveredCount ?? null,
  deliveredRate:
    campaignStatsById.value[campaign.id]?.total > 0
      ? Number(
          (
            (campaignStatsById.value[campaign.id].delivered /
              campaignStatsById.value[campaign.id].total) *
            100
          ).toFixed(1),
        )
      : campaign.deliveredRate ?? null,
  readCount: campaign.readCount ?? null,
  readRate: campaign.readRate ?? null,
  failedCount: campaignStatsById.value[campaign.id]?.failed ?? campaign.failedCount ?? null,
  failedRate:
    campaignStatsById.value[campaign.id]?.total > 0
      ? Number(
          (
            (campaignStatsById.value[campaign.id].failed / campaignStatsById.value[campaign.id].total) *
            100
          ).toFixed(1),
        )
      : campaign.failedRate ?? null,
  createdAt: formatCampaignDate(campaign.createdAt ?? campaign.created_at),
})

const normalizedCampaigns = computed(() => campaignStore.campaigns.map(normalizeCampaign))

const summaryCards = computed(() => {
  const totalCampaigns = normalizedCampaigns.value.length
  const sentTotal = normalizedCampaigns.value.reduce((sum, campaign) => sum + (campaign.sent ?? 0), 0)
  const deliveredTotal = normalizedCampaigns.value.reduce((sum, campaign) => sum + (campaign.deliveredCount ?? 0), 0)
  const failedTotal = normalizedCampaigns.value.reduce((sum, campaign) => sum + (campaign.failedCount ?? 0), 0)
  const readTotal = normalizedCampaigns.value.reduce((sum, campaign) => sum + (campaign.readCount ?? 0), 0)
  const deliveryRate = sentTotal > 0 ? ((deliveredTotal / sentTotal) * 100).toFixed(1) : '0.0'
  const readRate = deliveredTotal > 0 ? ((readTotal / deliveredTotal) * 100).toFixed(1) : '0.0'

  return [
    {
      label: 'Total Campaigns',
      value: totalCampaigns.toLocaleString(),
      detail: 'Loaded from API',
      color: 'green',
      icon: 'campaigns',
    },
    {
      label: 'Sent',
      value: sentTotal.toLocaleString(),
      detail: 'Total messages sent',
      color: 'blue',
      icon: 'sent',
    },
    {
      label: 'Delivered',
      value: deliveredTotal.toLocaleString(),
      detail: `${deliveryRate}% delivery rate`,
      color: 'purple',
      icon: 'delivered',
    },
    {
      label: 'Read',
      value: readTotal.toLocaleString(),
      detail: `${readRate}% read rate`,
      color: 'amber',
      icon: 'read',
    },
    {
      label: 'Failed',
      value: failedTotal.toLocaleString(),
      detail: sentTotal > 0 ? `${((failedTotal / sentTotal) * 100).toFixed(1)}% failed rate` : '0.0% failed rate',
      color: 'red',
      icon: 'failed',
    },
  ]
})

const filteredCampaigns = computed(() => {
  const query = searchTerm.value.trim().toLowerCase()
  const matchesTab = statusFilterMap[activeTab.value] ?? statusFilterMap['All Campaigns']

  return normalizedCampaigns.value.filter((campaign) => {
    const matchesSearch =
      query === '' ||
      campaign.name.toLowerCase().includes(query) ||
      campaign.preview.toLowerCase().includes(query) ||
      campaign.description.toLowerCase().includes(query)

    return matchesSearch && matchesTab(campaign)
  })
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredCampaigns.value.length / pageSize)))

const visibleCampaigns = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredCampaigns.value.slice(start, start + pageSize)
})

const paginationPages = computed(() => Array.from({ length: totalPages.value }, (_, index) => index + 1))

const tableRangeLabel = computed(() => {
  if (filteredCampaigns.value.length === 0) {
    return 'Showing 0 campaigns'
  }

  const start = (currentPage.value - 1) * pageSize + 1
  const end = Math.min(start + pageSize - 1, filteredCampaigns.value.length)
  return `Showing ${start} to ${end} of ${filteredCampaigns.value.length} campaigns`
})

const loadCampaignStats = async () => {
  const statsEntries = await Promise.all(
    campaignStore.campaigns.map(async (campaign) => {
      const response = await campaignStore.getMessages(campaign.id)
      return [campaign.id, response.statistics ?? null]
    }),
  )

  campaignStatsById.value = statsEntries.reduce((acc, [campaignId, statistics]) => {
    if (statistics) {
      acc[campaignId] = statistics
    }
    return acc
  }, {})
}

const loadCampaignData = async () => {
  isPageLoading.value = true
  pageError.value = ''
  try {
    await campaignStore.getCampaigns()
    await loadCampaignStats()
  } catch (error) {
    pageError.value = error.response?.data?.error ?? error.message ?? 'Unable to load campaigns.'
  } finally {
    isPageLoading.value = false
  }
}

onMounted(() => {
  loadCampaignData()
})

onBeforeUnmount(() => {
  pendingRefreshTimers.value.forEach((timerId) => clearTimeout(timerId))
  pendingRefreshTimers.value = []
})

const queueStatusRefresh = () => {
  const firstTimer = setTimeout(() => {
    loadCampaignData()
  }, 2500)

  const secondTimer = setTimeout(() => {
    loadCampaignData()
  }, 7000)

  pendingRefreshTimers.value.push(firstTimer, secondTimer)
}

const selectTab = (tab) => {
  activeTab.value = tab
  currentPage.value = 1
}

const updateSearch = () => {
  currentPage.value = 1
}

const goToPage = (page) => {
  currentPage.value = page
}

const changePage = (direction) => {
  const nextPage = currentPage.value + direction

  if (nextPage >= 1 && nextPage <= totalPages.value) {
    currentPage.value = nextPage
  }
}

const formatMetric = (count, rate) => {
  if (count === null || rate === null) {
    return ' - '
  }

  return `${count.toLocaleString()} (${rate}%)`
}

const statusClass = (status) => `status--${status.toLowerCase()}`

const progressWidth = (value) => ({
  width: `${Math.max(0, Math.min(value ?? 0, 100))}%`,
})

const openCampaignModal = (campaign) => {
  selectedCampaign.value = campaign
  campaignForm.value = {
    name: campaign.name ?? '',
    description: campaign.description ?? campaign.preview ?? '',
    status: (campaign.status ?? 'draft').toLowerCase(),
    messageBody: campaign.description ?? campaign.preview ?? '',
  }
  modalError.value = ''
  modalMessage.value = ''
}

const closeCampaignModal = () => {
  selectedCampaign.value = null
  modalError.value = ''
  modalMessage.value = ''
}

const saveCampaign = async () => {
  if (!selectedCampaign.value?.id) {
    modalError.value = 'This campaign cannot be saved.'
    return
  }

  isSavingCampaign.value = true
  modalError.value = ''
  modalMessage.value = ''

  try {
    const updatedCampaign = await campaignStore.updateCampaign(selectedCampaign.value.id, {
      name: campaignForm.value.name,
      description: campaignForm.value.description,
      status: campaignForm.value.status,
    })

    selectedCampaign.value = normalizeCampaign(updatedCampaign)
    campaignForm.value = {
      name: updatedCampaign.name ?? '',
      description: updatedCampaign.description ?? '',
      status: (updatedCampaign.status ?? 'draft').toLowerCase(),
    }
    await loadCampaignData()
    closeCampaignModal()
  } catch (error) {
    modalError.value = error.response?.data?.message ?? error.message ?? 'Unable to update campaign.'
  } finally {
    isSavingCampaign.value = false
  }
}

const sendSelectedCampaign = async () => {
  if (!selectedCampaign.value?.id) {
    modalError.value = 'This campaign cannot be sent.'
    return
  }

  if (!campaignForm.value.messageBody.trim()) {
    modalError.value = 'Message body is required before sending.'
    return
  }

  isSendingCampaign.value = true
  modalError.value = ''
  modalMessage.value = ''

  try {
    await campaignStore.sendWhatsApp(selectedCampaign.value.id, campaignForm.value.messageBody)
    await loadCampaignData()
    closeCampaignModal()
    queueStatusRefresh()
  } catch (error) {
    modalError.value = error.response?.data?.error ?? error.message ?? 'Unable to send campaign.'
  } finally {
    isSendingCampaign.value = false
  }
}

const deleteSelectedCampaign = async () => {
  if (!selectedCampaign.value?.id) {
    modalError.value = 'This campaign cannot be deleted.'
    return
  }

  if (!confirm(`Delete "${selectedCampaign.value.name}"?`)) {
    return
  }

  isDeletingCampaign.value = true
  modalError.value = ''
  modalMessage.value = ''

  try {
    await campaignStore.deleteCampaign(selectedCampaign.value.id)
    closeCampaignModal()
    await loadCampaignData()
  } catch (error) {
    modalError.value = error.response?.data?.message ?? error.message ?? 'Unable to delete campaign.'
  } finally {
    isDeletingCampaign.value = false
  }
}
</script>

<template>
  <div class="campaigns-page">
    <header class="page-header">
      <h1 class="page-title">Campaigns</h1>

      <div class="header-actions">
        <label class="search-input">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="11" cy="11" r="6" />
            <path d="m20 20-4.2-4.2" />
          </svg>
          <input
            v-model="searchTerm"
            type="search"
            placeholder="Search campaigns..."
            @input="updateSearch"
          >
        </label>

        <button class="icon-button" type="button" aria-label="Notifications">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M15 17H5l2-2.5V10a5 5 0 0 1 10 0v4.5L19 17h-4Z" />
            <path d="M11 20a2 2 0 0 0 4 0" />
          </svg>
          <span class="notification-badge">3</span>
        </button>

        <button @click="router.push({ name: 'CreateCampaign' })" class="primary-button" type="button">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M12 5v14" />
            <path d="M5 12h14" />
          </svg>
          New Campaign
        </button>
      </div>
    </header>

    <section class="stats-grid" aria-label="Campaign metrics">
      <article
        v-for="card in summaryCards"
        :key="card.label"
        class="stat-card"
        :class="`stat-card--${card.color}`"
      >
        <div class="stat-icon">
          <svg v-if="card.icon === 'campaigns'" viewBox="0 0 24 24" fill="none">
            <path d="M5 11.5 19 5l-6.5 14-2.5-5-5-2.5Z" />
            <path d="m10 14 4-4" />
          </svg>
          <svg v-else-if="card.icon === 'sent'" viewBox="0 0 24 24" fill="none">
            <path d="M8 7h8a3 3 0 0 1 3 3v4a3 3 0 0 1-3 3h-2l-3 2v-2H8a3 3 0 0 1-3-3v-4a3 3 0 0 1 3-3Z" />
          </svg>
          <svg v-else-if="card.icon === 'delivered'" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="8" />
            <path d="m8.5 12 2.3 2.3 4.7-4.8" />
          </svg>
          <svg v-else-if="card.icon === 'read'" viewBox="0 0 24 24" fill="none">
            <path d="M2.5 12S6 6.5 12 6.5 21.5 12 21.5 12 18 17.5 12 17.5 2.5 12 2.5 12Z" />
            <circle cx="12" cy="12" r="2.5" />
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none">
            <path d="m8 8 8 8" />
            <path d="m16 8-8 8" />
          </svg>
        </div>

        <div class="stat-copy">
          <span class="stat-label">{{ card.label }}</span>
          <strong class="stat-value">{{ card.value }}</strong>
          <span class="stat-detail">{{ card.detail }}</span>
        </div>
      </article>
    </section>

    <section class="campaigns-panel">
      <div class="toolbar">
        <div class="tabs" role="tablist" aria-label="Campaign filters">
          <button
            v-for="tab in filterTabs"
            :key="tab"
            class="tab-button"
            :class="{ 'is-active': activeTab === tab }"
            type="button"
            role="tab"
            :aria-selected="activeTab === tab"
            @click="selectTab(tab)"
          >
            {{ tab }}
          </button>
        </div>

        <div class="toolbar-actions">
          <button class="secondary-button" type="button">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <rect x="4" y="5" width="16" height="15" rx="2" />
              <path d="M4 10h16" />
              <path d="M8 3v4" />
              <path d="M16 3v4" />
            </svg>
            {{ selectedDateRange }}
          </button>

          <button class="secondary-button" type="button">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M4 5h16" />
              <path d="M7 5v5l5 5 5-5V5" />
            </svg>
            Filters
          </button>

          <button class="secondary-button" type="button">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M12 4v11" />
              <path d="m8 11 4 4 4-4" />
              <path d="M5 20h14" />
            </svg>
            Export
          </button>
        </div>
      </div>

      <div class="table-wrapper">
        <table class="campaigns-table">
          <thead>
            <tr>
              <th>Campaign Name</th>
              <th>Recipients</th>
              <th>Status</th>
              <th>Sent</th>
              <th>Delivered</th>
              <th>Read</th>
              <th>Failed</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="isPageLoading">
              <td colspan="9" class="empty-state">
                Loading campaigns...
              </td>
            </tr>

            <tr v-else-if="pageError">
              <td colspan="9" class="empty-state">
                {{ pageError }}
              </td>
            </tr>

            <template v-else>
              <tr
                v-for="campaign in visibleCampaigns"
                :key="campaign.id ?? campaign.name"
                class="campaign-row"
                @click="openCampaignModal(campaign)"
              >
                <td class="campaign-name-cell">
                  <strong>{{ campaign.name }}</strong>
                  <span>{{ campaign.preview }}</span>
                </td>
                <td>{{ campaign.recipients.toLocaleString() }}</td>
                <td>
                  <span class="status-badge" :class="statusClass(campaign.status)">
                    {{ campaign.status }}
                  </span>
                </td>
                <td>{{ campaign.sent === null ? ' - ' : campaign.sent.toLocaleString() }}</td>
                <td>
                  <div class="metric-cell">
                    <span>{{ formatMetric(campaign.deliveredCount, campaign.deliveredRate) }}</span>
                    <div class="progress-track">
                      <div class="progress-bar progress-bar--green" :style="progressWidth(campaign.deliveredRate)" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="metric-cell">
                    <span>{{ formatMetric(campaign.readCount, campaign.readRate) }}</span>
                    <div class="progress-track">
                      <div class="progress-bar progress-bar--blue" :style="progressWidth(campaign.readRate)" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="metric-cell">
                    <span>{{ formatMetric(campaign.failedCount, campaign.failedRate) }}</span>
                    <div class="progress-track">
                      <div class="progress-bar progress-bar--red" :style="progressWidth(campaign.failedRate)" />
                    </div>
                  </div>
                </td>
                <td>{{ campaign.createdAt }}</td>
                <td>
                  <div class="row-actions">
                    <button
                      class="table-icon-button"
                      type="button"
                      aria-label="View campaign details"
                      @click.stop="openCampaignModal(campaign)"
                    >
                      <svg viewBox="0 0 24 24" fill="none">
                        <rect x="4.5" y="4.5" width="15" height="15" rx="3" />
                        <path d="M8 11h8" />
                        <path d="M8 15h5" />
                      </svg>
                    </button>
                    <button class="table-icon-button" type="button" aria-label="Duplicate campaign" @click.stop>
                      <svg viewBox="0 0 24 24" fill="none">
                        <rect x="9" y="7" width="10" height="12" rx="2" />
                        <path d="M6 15H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v1" />
                      </svg>
                    </button>
                    <button class="table-icon-button" type="button" aria-label="More options" @click.stop>
                      <svg viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="5" r="1" fill="currentColor" />
                        <circle cx="12" cy="12" r="1" fill="currentColor" />
                        <circle cx="12" cy="19" r="1" fill="currentColor" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>

              <tr v-if="visibleCampaigns.length === 0">
                <td colspan="9" class="empty-state">
                  No campaigns match the selected filters.
                </td>
              </tr>
            </template>

          </tbody>
        </table>
      </div>

      <footer class="table-footer">
        <span class="footer-copy">{{ tableRangeLabel }}</span>

        <div class="pagination">
          <button
            class="pagination-button pagination-button--icon"
            type="button"
            aria-label="Previous page"
            :disabled="currentPage === 1"
            @click="changePage(-1)"
          >
            <svg viewBox="0 0 24 24" fill="none">
              <path d="m15 18-6-6 6-6" />
            </svg>
          </button>

          <button
            v-for="page in paginationPages"
            :key="page"
            class="pagination-button"
            :class="{ 'is-active': currentPage === page }"
            type="button"
            @click="goToPage(page)"
          >
            {{ page }}
          </button>

          <button
            class="pagination-button pagination-button--icon"
            type="button"
            aria-label="Next page"
            :disabled="currentPage === totalPages"
            @click="changePage(1)"
          >
            <svg viewBox="0 0 24 24" fill="none">
              <path d="m9 6 6 6-6 6" />
            </svg>
          </button>
        </div>
      </footer>
    </section>

    <div v-if="selectedCampaign" class="campaign-modal-backdrop" @click.self="closeCampaignModal">
      <section class="campaign-modal" role="dialog" aria-modal="true" :aria-label="selectedCampaign.name">
        <header class="campaign-modal__header">
          <div>
            <p class="campaign-modal__eyebrow">Campaign details</p>
            <h2 class="campaign-modal__title">{{ selectedCampaign.name }}</h2>
          </div>

          <button class="modal-close-button" type="button" aria-label="Close modal" @click="closeCampaignModal">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="m7 7 10 10" />
              <path d="m17 7-10 10" />
            </svg>
          </button>
        </header>

        <form class="campaign-modal__form" @submit.prevent="saveCampaign">
          <label class="modal-field">
            <span>Name</span>
            <input v-model="campaignForm.name" type="text" />
          </label>

          <label class="modal-field">
            <span>Status</span>
            <select v-model="campaignForm.status">
              <option value="draft">Draft</option>
              <option value="scheduled">Scheduled</option>
              <option value="sent">Sent</option>
              <option value="delivered">Delivered</option>
              <option value="failed">Failed</option>
            </select>
          </label>

          <label class="modal-field modal-field--full">
            <span>Description</span>
            <textarea v-model="campaignForm.description" rows="4"></textarea>
          </label>

          <label class="modal-field modal-field--full">
            <span>Message body <em class="modal-field__hint">(sent to contacts)</em></span>
            <textarea v-model="campaignForm.messageBody" rows="4" placeholder="Enter the message that will be sent to contacts..."></textarea>
          </label>

          <div v-if="modalError || modalMessage" class="modal-feedback" :class="{ 'is-error': modalError }">
            {{ modalError || modalMessage }}
          </div>

          <div class="modal-actions">
            <button class="secondary-button" type="button" @click="closeCampaignModal">
              Cancel
            </button>
            <button
              class="secondary-button secondary-button--danger"
              type="button"
              :disabled="isDeletingCampaign || !selectedCampaign.id"
              @click="deleteSelectedCampaign"
            >
              {{ isDeletingCampaign ? 'Deleting...' : 'Delete' }}
            </button>
            <button class="secondary-button" type="button" :disabled="isSendingCampaign || !selectedCampaign.id" @click="sendSelectedCampaign">
              {{ isSendingCampaign ? 'Sending...' : 'Send' }}
            </button>
            <button class="primary-button" type="submit" :disabled="isSavingCampaign || !selectedCampaign.id">
              {{ isSavingCampaign ? 'Saving...' : 'Save changes' }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </div>
</template>

<style scoped>
.campaigns-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.page-title {
  margin: 0;
  font-size: 1.9rem;
  line-height: 1.1;
  font-weight: 700;
  color: #111827;
}

.header-actions,
.toolbar-actions,
.row-actions,
.pagination {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-input {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 280px;
  padding: 0 16px;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  min-height: 46px;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
}

.search-input svg,
.icon-button svg,
.primary-button svg,
.secondary-button svg,
.table-icon-button svg,
.pagination-button svg,
.stat-icon svg {
  width: 18px;
  height: 18px;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.search-input input {
  width: 100%;
  border: none;
  outline: none;
  font: inherit;
  color: #111827;
  background: transparent;
}

.icon-button,
.primary-button,
.secondary-button,
.table-icon-button,
.tab-button,
.pagination-button {
  border: 1px solid #e2e8f0;
  background: #ffffff;
  color: #334155;
  border-radius: 12px;
  font: inherit;
  cursor: pointer;
  transition: border-color 0.2s ease, background-color 0.2s ease, color 0.2s ease, box-shadow 0.2s ease;
}

.icon-button,
.table-icon-button,
.pagination-button--icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.icon-button {
  width: 46px;
  height: 46px;
  position: relative;
}

.notification-badge {
  position: absolute;
  top: 7px;
  right: 7px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 999px;
  background: #ef4444;
  color: #ffffff;
  font-size: 0.7rem;
  line-height: 16px;
  font-weight: 700;
}

.primary-button,
.secondary-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  min-height: 46px;
  padding: 0 18px;
  font-weight: 600;
}

.primary-button {
  border-color: #16a34a;
  background: linear-gradient(180deg, #16a34a 0%, #0f9f47 100%);
  color: #ffffff;
  box-shadow: 0 10px 24px rgba(22, 163, 74, 0.2);
}

.secondary-button {
  color: #334155;
}

.secondary-button--danger {
  color: #b91c1c;
  border-color: #fecaca;
  background: #fef2f2;
}

.icon-button:hover,
.secondary-button:hover,
.table-icon-button:hover,
.pagination-button:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.primary-button:hover {
  background: linear-gradient(180deg, #15803d 0%, #0f9f47 100%);
}

.secondary-button--danger:hover {
  background: #fee2e2;
  border-color: #fca5a5;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 18px;
}

.stat-card,
.campaigns-panel {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #eef2f7;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
}

.stat-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 24px 20px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
}

.stat-copy {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-label {
  color: #475569;
  font-size: 0.95rem;
}

.stat-value {
  font-size: 2rem;
  line-height: 1;
  color: #111827;
}

.stat-detail {
  font-size: 0.95rem;
}

.stat-card--green .stat-icon {
  background: #ebfbf0;
  color: #16a34a;
}

.stat-card--green .stat-detail {
  color: #16a34a;
}

.stat-card--blue .stat-icon {
  background: #ecf4ff;
  color: #2563eb;
}

.stat-card--blue .stat-detail {
  color: #2563eb;
}

.stat-card--purple .stat-icon {
  background: #f3e8ff;
  color: #7c3aed;
}

.stat-card--purple .stat-detail {
  color: #475569;
}

.stat-card--amber .stat-icon {
  background: #fff7e8;
  color: #f59e0b;
}

.stat-card--amber .stat-detail {
  color: #475569;
}

.stat-card--red .stat-icon {
  background: #feeeee;
  color: #ef4444;
}

.stat-card--red .stat-detail {
  color: #ef4444;
}

.campaigns-panel {
  overflow: hidden;
}

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 20px 24px 14px;
  border-bottom: 1px solid #eef2f7;
  flex-wrap: wrap;
}

.tabs {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.tab-button {
  padding: 0 6px 14px;
  border: none;
  border-bottom: 3px solid transparent;
  border-radius: 0;
  background: transparent;
  color: #475569;
  font-weight: 600;
}

.tab-button.is-active {
  color: #16a34a;
  border-bottom-color: #16a34a;
}

.table-wrapper {
  overflow-x: auto;
}

.campaigns-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1180px;
}

.campaigns-table th,
.campaigns-table td {
  padding: 18px 20px;
  text-align: left;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
  white-space: nowrap;
}

.campaigns-table th {
  color: #64748b;
  font-size: 0.82rem;
  font-weight: 700;
}

.campaigns-table td {
  color: #0f172a;
  font-size: 0.92rem;
}

.campaign-row {
  cursor: pointer;
  transition: background-color 0.18s ease;
}

.campaign-row:hover {
  background: #f8fafc;
}

.campaign-name-cell {
  min-width: 220px;
}

.campaign-name-cell strong,
.campaign-name-cell span {
  display: block;
}

.campaign-name-cell span {
  margin-top: 6px;
  color: #64748b;
  font-size: 0.82rem;
  max-width: 240px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 82px;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 700;
}

.status--sent {
  background: #eafaf0;
  color: #16a34a;
}

.status--delivered {
  background: #eef4ff;
  color: #2563eb;
}

.status--scheduled {
  background: #fff7e8;
  color: #f59e0b;
}

.status--draft {
  background: #f1f5f9;
  color: #475569;
}

.status--failed {
  background: #feeeee;
  color: #ef4444;
}

.metric-cell {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 120px;
}

.progress-track {
  width: 100%;
  height: 4px;
  border-radius: 999px;
  background: #e5e7eb;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: inherit;
}

.progress-bar--green {
  background: #16a34a;
}

.progress-bar--blue {
  background: #2563eb;
}

.progress-bar--red {
  background: #ef4444;
}

.row-actions {
  gap: 8px;
}

.table-icon-button {
  width: 36px;
  height: 36px;
}

.table-icon-button svg circle {
  stroke: none;
}

.empty-state {
  text-align: center;
  color: #64748b !important;
  padding: 32px 20px !important;
}

.table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 18px 24px;
  flex-wrap: wrap;
}

.footer-copy {
  color: #64748b;
  font-size: 0.92rem;
}

.pagination-button {
  min-width: 36px;
  height: 36px;
  padding: 0 12px;
}

.pagination-button.is-active {
  border-color: #bfdbfe;
  color: #2563eb;
  background: #eff6ff;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.campaign-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 40;
  display: grid;
  place-items: center;
  padding: 24px;
  background: rgba(15, 23, 42, 0.52);
  backdrop-filter: blur(8px);
}

.campaign-modal {
  width: min(640px, 100%);
  max-height: min(88vh, 760px);
  overflow: auto;
  border-radius: 24px;
  border: 1px solid rgba(226, 232, 240, 0.9);
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  box-shadow: 0 30px 80px rgba(15, 23, 42, 0.25);
}

.campaign-modal__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 24px 24px 16px;
  border-bottom: 1px solid #eef2f7;
}

.campaign-modal__eyebrow {
  margin: 0 0 6px;
  color: #16a34a;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.74rem;
  font-weight: 700;
}

.campaign-modal__title {
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

.campaign-modal__form {
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

.modal-field input,
.modal-field select,
.modal-field textarea {
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

.modal-field textarea {
  resize: vertical;
  min-height: 132px;
}

.modal-field input:focus,
.modal-field select:focus,
.modal-field textarea:focus {
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
  padding-top: 4px;
  flex-wrap: wrap;
}

.modal-actions .secondary-button:disabled,
.modal-actions .primary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 1380px) {
  .stats-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .search-input {
    min-width: 220px;
  }
}

@media (max-width: 720px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .header-actions,
  .toolbar-actions,
  .pagination {
    width: 100%;
    flex-wrap: wrap;
  }

  .search-input {
    min-width: 100%;
  }

  .primary-button,
  .secondary-button {
    justify-content: center;
    width: 100%;
  }

  .table-footer {
    align-items: stretch;
  }

  .campaign-modal__form {
    grid-template-columns: 1fr;
  }

  .campaign-modal__header,
  .campaign-modal__form {
    padding-left: 18px;
    padding-right: 18px;
  }

  .campaign-modal-backdrop {
    padding: 16px;
  }
}
</style>
