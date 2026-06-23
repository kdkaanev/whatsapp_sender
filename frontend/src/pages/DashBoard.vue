<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const dateRange = ref('25 May – 25 Jun 2026')

const stats = ref([
  {
    label: 'Contacts',
    value: '1,245',
    change: '+12 this week',
    color: 'green',
    icon: 'contacts',
  },
  {
    label: 'Campaigns',
    value: '18',
    change: '+2 this week',
    color: 'purple',
    icon: 'campaigns',
  },
  {
    label: 'Messages Sent',
    value: '5,420',
    change: '+820 this week',
    color: 'blue',
    icon: 'messages',
  },
  {
    label: 'Delivery Rate',
    value: '97.3%',
    change: '+1.2% this week',
    color: 'teal',
    icon: 'delivery',
  },
])

const campaigns = ref([
  {
    name: 'Summer Promo 2026',
    recipients: 520,
    status: 'Sent',
    sent: 520,
    delivered: '508 (97.7%)',
    read: '410 (78.8%)',
    created: '24.06.2026',
  },
  {
    name: 'Black Friday Offer',
    recipients: 1200,
    status: 'Delivered',
    sent: 1200,
    delivered: '1,164 (97%)',
    read: '875 (72.9%)',
    created: '21.06.2026',
  },
  {
    name: 'VIP Customers',
    recipients: 312,
    status: 'Scheduled',
    sent: null,
    delivered: null,
    read: null,
    created: '25.06.2026 09:00',
  },
  {
    name: 'New Collection',
    recipients: 450,
    status: 'Draft',
    sent: null,
    delivered: null,
    read: null,
    created: '23.06.2026',
  },
])

const goToCampaigns = () => {
  router.push('/campaigns')
}

const refresh = () => {
  // Re-fetch dashboard data when connected to a backend
}
</script>

<template>
  <div class="dashboard">
    <!-- NewTest -->
    <!-- Header -->
    <div class="dashboard-header">
      <h1 class="dashboard-title">Dashboard</h1>
      <div class="header-actions">
        <div class="date-range">
          <svg class="date-icon" viewBox="0 0 24 24" fill="none">
            <rect x="3" y="4" width="18" height="17" rx="2" />
            <path d="M3 9h18" />
            <path d="M8 2v4" />
            <path d="M16 2v4" />
          </svg>
          <span>{{ dateRange }}</span>
        </div>
        <button class="refresh-btn" type="button" aria-label="Refresh" @click="refresh">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M4 4v5h5" />
            <path d="M20 20v-5h-5" />
            <path d="M4 9a9 9 0 0 1 15.6-6.1L20 4" />
            <path d="M20 15a9 9 0 0 1-15.6 6.1L4 20" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div
        v-for="stat in stats"
        :key="stat.label"
        class="stat-card"
        :class="`stat-card--${stat.color}`"
      >
        <div class="stat-card-body">
          <div class="stat-info">
            <span class="stat-label">{{ stat.label }}</span>
            <span class="stat-value">{{ stat.value }}</span>
            <span class="stat-change">{{ stat.change }}</span>
          </div>
          <div class="stat-icon-wrap">
            <!-- Contacts icon -->
            <svg v-if="stat.icon === 'contacts'" viewBox="0 0 24 24" fill="none">
              <path d="M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" />
              <path d="M4 18a5 5 0 0 1 10 0" />
              <path d="M17 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z" />
              <path d="M14.5 18a4.5 4.5 0 0 1 5.5-4.4" />
            </svg>
            <!-- Campaigns icon -->
            <svg v-if="stat.icon === 'campaigns'" viewBox="0 0 24 24" fill="none">
              <path d="M5 11.5 19 5l-6.5 14-2.5-5-5-2.5Z" />
              <path d="m10 14 4-4" />
            </svg>
            <!-- Messages icon -->
            <svg v-if="stat.icon === 'messages'" viewBox="0 0 24 24" fill="none">
              <path d="M22 2 11 13" />
              <path d="M22 2 15 22l-4-9-9-4 20-7Z" />
            </svg>
            <!-- Delivery Rate icon -->
            <svg v-if="stat.icon === 'delivery'" viewBox="0 0 24 24" fill="none">
              <path d="M3 17l6-6 4 4 8-9" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Campaigns -->
    <div class="campaigns-section">
      <div class="section-header">
        <h2 class="section-title">Recent Campaigns</h2>
        <button class="view-all-btn" type="button" @click="goToCampaigns">View all</button>
      </div>

      <div class="table-wrapper">
        <table class="campaigns-table">
          <thead>
            <tr>
              <th>Campaign</th>
              <th>Recipients</th>
              <th>Status</th>
              <th>Sent</th>
              <th>Delivered</th>
              <th>Read</th>
              <th>Created</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="campaign in campaigns" :key="campaign.name">
              <td class="campaign-name">{{ campaign.name }}</td>
              <td>{{ campaign.recipients.toLocaleString() }}</td>
              <td>
                <span class="status-badge" :class="`status--${campaign.status.toLowerCase()}`">
                  {{ campaign.status }}
                </span>
              </td>
              <td>{{ campaign.sent !== null ? campaign.sent.toLocaleString() : '–' }}</td>
              <td>{{ campaign.delivered ?? '–' }}</td>
              <td>{{ campaign.read ?? '–' }}</td>
              <td class="created-cell">{{ campaign.created }}</td>
              <td class="actions-cell">
                <button class="more-btn" type="button" aria-label="More options">
                  <svg viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="5" r="1" fill="currentColor" />
                    <circle cx="12" cy="12" r="1" fill="currentColor" />
                    <circle cx="12" cy="19" r="1" fill="currentColor" />
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- New Campaign Button -->
    <div class="new-campaign-wrap">
      <button class="new-campaign-btn" type="button" @click="goToCampaigns">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M12 5v14" />
          <path d="M5 12h14" />
        </svg>
        New Campaign
      </button>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

/* Header */
.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.dashboard-title {
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

.date-range {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 8px 14px;
  font-size: 0.875rem;
  color: #374151;
  font-weight: 500;
}

.date-icon {
  width: 16px;
  height: 16px;
  stroke: #6b7280;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
  flex: 0 0 auto;
}

.refresh-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  transition: background 0.2s;
}

.refresh-btn:hover {
  background: #f1f5f9;
}

.refresh-btn svg {
  width: 16px;
  height: 16px;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

@media (max-width: 1100px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 22px 22px 18px;
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.06);
  border: 1px solid #f1f5f9;
}

.stat-card-body {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.01em;
}

.stat-value {
  font-size: 1.9rem;
  font-weight: 700;
  color: #111827;
  line-height: 1.1;
  margin-top: 4px;
}

.stat-change {
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 2px;
}

.stat-icon-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  border-radius: 12px;
  flex: 0 0 auto;
}

.stat-icon-wrap svg {
  width: 22px;
  height: 22px;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

/* Color variants */
.stat-card--green .stat-label { color: #1b9a5d; }
.stat-card--green .stat-icon-wrap {
  background: #eef8f1;
  color: #1b9a5d;
}
.stat-card--green .stat-icon-wrap svg { stroke: #1b9a5d; }

.stat-card--purple .stat-label { color: #7c3aed; }
.stat-card--purple .stat-icon-wrap {
  background: #f3eeff;
  color: #7c3aed;
}
.stat-card--purple .stat-icon-wrap svg { stroke: #7c3aed; }

.stat-card--blue .stat-label { color: #2563eb; }
.stat-card--blue .stat-icon-wrap {
  background: #eff6ff;
  color: #2563eb;
}
.stat-card--blue .stat-icon-wrap svg { stroke: #2563eb; }

.stat-card--teal .stat-label { color: #0d9488; }
.stat-card--teal .stat-icon-wrap {
  background: #f0fdfa;
  color: #0d9488;
}
.stat-card--teal .stat-icon-wrap svg { stroke: #0d9488; }

/* Campaigns Section */
.campaigns-section {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.06);
  border: 1px solid #f1f5f9;
  overflow: hidden;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px 16px;
  border-bottom: 1px solid #f1f5f9;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.view-all-btn {
  background: none;
  border: none;
  color: #1b9a5d;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}

.view-all-btn:hover {
  background: #eef8f1;
}

.table-wrapper {
  overflow-x: auto;
}

.campaigns-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.campaigns-table th {
  text-align: left;
  padding: 12px 16px;
  color: #6b7280;
  font-weight: 600;
  font-size: 0.8rem;
  border-bottom: 1px solid #f1f5f9;
  white-space: nowrap;
}

.campaigns-table td {
  padding: 14px 16px;
  color: #374151;
  border-bottom: 1px solid #f8fafc;
  white-space: nowrap;
}

.campaigns-table tbody tr:last-child td {
  border-bottom: none;
}

.campaigns-table tbody tr:hover {
  background: #fafbfc;
}

.campaign-name {
  font-weight: 600;
  color: #111827 !important;
}

.created-cell {
  color: #6b7280 !important;
  font-size: 0.8rem;
}

/* Status badges */
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.78rem;
  font-weight: 600;
}

.status--sent {
  background: #eef8f1;
  color: #1b9a5d;
}

.status--delivered {
  background: #eff6ff;
  color: #2563eb;
}

.status--scheduled {
  background: #fffbeb;
  color: #d97706;
}

.status--draft {
  background: #f3f4f6;
  color: #6b7280;
}

.actions-cell {
  width: 40px;
  padding: 14px 8px !important;
}

.more-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
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

/* New Campaign Button */
.new-campaign-wrap {
  display: flex;
  justify-content: center;
  padding-bottom: 8px;
}

.new-campaign-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #1b9a5d;
  color: #ffffff;
  border: none;
  border-radius: 12px;
  padding: 14px 32px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 14px rgba(27, 154, 93, 0.3);
}

.new-campaign-btn:hover {
  background: #168a52;
  box-shadow: 0 6px 18px rgba(27, 154, 93, 0.4);
}

.new-campaign-btn svg {
  width: 18px;
  height: 18px;
  stroke: currentColor;
  stroke-width: 2.5;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}
</style>
