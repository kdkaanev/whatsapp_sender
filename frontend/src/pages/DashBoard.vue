<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const loadingStats = ref(false)
const statsError = ref('')
const loadingCampaigns = ref(false)
const campaignsError = ref('')
const recentCampaigns = ref([])

const stats = ref({
	total_contacts: 0,
	campaigns: {
		total: 0,
		active: 0,
	},
	messages_sent: 0,
	delivery_rate: 0,
})

const formatNumber = (value) => new Intl.NumberFormat().format(value || 0)

const summaryCards = computed(() => [
	{ label: 'Total Contacts', value: formatNumber(stats.value.total_contacts), hint: 'All saved contacts' },
	{
		label: 'Campaigns',
		value: `${formatNumber(stats.value.campaigns.total)} / ${formatNumber(stats.value.campaigns.active)}`,
		hint: 'Total / Active',
	},
	{ label: 'Messages Sent', value: formatNumber(stats.value.messages_sent), hint: 'Sent + Delivered' },
	{ label: 'Delivery Rate', value: `${Number(stats.value.delivery_rate || 0).toFixed(2)}%`, hint: 'Delivered / Attempted' },
])

const getDashboardStats = async () => {
	loadingStats.value = true
	statsError.value = ''
	try {
		const response = await api.get('/dashboard/stats/')
		stats.value = {
			...stats.value,
			...response.data,
		}
	} catch (err) {
		statsError.value = err?.response?.data?.detail || 'Failed to load dashboard statistics.'
	} finally {
		loadingStats.value = false
	}
}

const formatDate = (value) => {
	if (!value) {
		return 'N/A'
	}

	return new Date(value).toLocaleDateString(undefined, {
		year: 'numeric',
		month: 'short',
		day: '2-digit',
	})
}

const getRecentCampaigns = async () => {
	loadingCampaigns.value = true
	campaignsError.value = ''
	try {
		const response = await api.get('/campaigns/')
		const campaigns = Array.isArray(response.data) ? response.data : []

		recentCampaigns.value = [...campaigns]
			.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
			.slice(0, 5)
	} catch (err) {
		campaignsError.value = err?.response?.data?.detail || 'Failed to load campaigns.'
	} finally {
		loadingCampaigns.value = false
	}
}

const goToCreateCampaign = () => {
	router.push('/create-campaign')
}

onMounted(() => {
	getDashboardStats()
	getRecentCampaigns()
})
</script>

<template>
	<section class="dashboard-page">
		<header class="hero">
			<div>
				<p class="eyebrow">Overview</p>
				<h1 class="title">Dashboard</h1>
				<p class="subtitle">
					Track campaign activity, contact growth, and recent messaging performance from one place.
				</p>
			</div>
			<button class="add-campaign-btn" type="button" @click="goToCreateCampaign">+AddCampaigns</button>
		</header>

		<div class="card-grid">
			<p v-if="loadingStats" class="status-text">Loading statistics...</p>
			<p v-else-if="statsError" class="status-text status-text--error">{{ statsError }}</p>
			<article v-for="card in summaryCards" :key="card.label" class="metric-card">
				<p class="metric-label">{{ card.label }}</p>
				<p class="metric-value">{{ card.value }}</p>
				<p class="metric-hint">{{ card.hint }}</p>
			</article>
		</div>

		<section class="table-card">
			<div class="table-head">
				<h2>Latest 5 Campaigns</h2>
			</div>
			<p v-if="loadingCampaigns" class="status-text">Loading campaigns...</p>
			<p v-else-if="campaignsError" class="status-text status-text--error">{{ campaignsError }}</p>
			<p v-else-if="recentCampaigns.length === 0" class="status-text">No campaigns found.</p>
			<div v-else class="table-wrap">
				<table>
					<thead>
						<tr>
							<th>Name</th>
							<th>Status</th>
							<th>Created</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="campaign in recentCampaigns" :key="campaign.id">
							<td>{{ campaign.name || 'Untitled campaign' }}</td>
							<td>
								<span class="status-pill">{{ campaign.status || 'draft' }}</span>
							</td>
							<td>{{ formatDate(campaign.created_at) }}</td>
						</tr>
					</tbody>
				</table>
			</div>
		</section>
	</section>
</template>

<style scoped>
.dashboard-page {
	display: grid;
	gap: 24px;
}

.hero {
	display: flex;
	align-items: end;
	justify-content: space-between;
	gap: 20px;
	padding: 28px;
	border-radius: 24px;
	background: linear-gradient(135deg, #ffffff 0%, #f1f7f3 100%);
	border: 1px solid rgba(226, 232, 240, 0.9);
	box-shadow: 0 18px 40px rgba(15, 23, 42, 0.06);
}

.eyebrow {
	margin: 0 0 8px;
	text-transform: uppercase;
	letter-spacing: 0.12em;
	font-size: 0.75rem;
	font-weight: 700;
	color: #1b9a5d;
}

.title {
	margin: 0;
	font-size: clamp(2rem, 3vw, 3rem);
	line-height: 1.05;
}

.subtitle {
	max-width: 56ch;
	margin: 12px 0 0;
	color: #4b5563;
	font-size: 1rem;
	line-height: 1.6;
}

.add-campaign-btn {
	height: 44px;
	padding: 0 18px;
	border: none;
	border-radius: 999px;
	background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
	color: #ffffff;
	font-size: 0.9rem;
	font-weight: 700;
	letter-spacing: 0.01em;
	cursor: pointer;
	box-shadow: 0 10px 20px rgba(21, 128, 61, 0.25);
	transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.add-campaign-btn:hover {
	transform: translateY(-1px);
	box-shadow: 0 14px 24px rgba(21, 128, 61, 0.3);
}

.card-grid {
	display: grid;
	grid-template-columns: repeat(4, minmax(0, 1fr));
	gap: 16px;
}

.status-text {
	grid-column: 1 / -1;
	margin: 0;
	padding: 12px 16px;
	border-radius: 12px;
	background: #f8fafc;
	border: 1px solid rgba(226, 232, 240, 0.9);
	color: #475569;
	font-weight: 600;
}

.status-text--error {
	background: #fff1f2;
	border-color: #fecdd3;
	color: #be123c;
}

.metric-card {
	padding: 22px;
	border-radius: 20px;
	background: #ffffff;
	border: 1px solid rgba(226, 232, 240, 0.9);
	box-shadow: 0 12px 28px rgba(15, 23, 42, 0.05);
}

.metric-label {
	margin: 0;
	color: #6b7280;
	font-size: 0.9rem;
	font-weight: 600;
}

.metric-value {
	margin: 10px 0 8px;
	font-size: clamp(1.8rem, 2.5vw, 2.4rem);
	font-weight: 800;
	color: #111827;
}

.metric-hint {
	margin: 0;
	color: #1b9a5d;
	font-weight: 600;
}

.table-card {
	padding: 20px;
	border-radius: 20px;
	background: #ffffff;
	border: 1px solid rgba(226, 232, 240, 0.9);
	box-shadow: 0 12px 28px rgba(15, 23, 42, 0.05);
	display: grid;
	gap: 14px;
}

.table-head h2 {
	margin: 0;
	font-size: 1.1rem;
	color: #0f172a;
}

.table-wrap {
	overflow-x: auto;
}

table {
	width: 100%;
	border-collapse: collapse;
	min-width: 460px;
}

th,
td {
	text-align: left;
	padding: 12px 10px;
	border-bottom: 1px solid #e2e8f0;
	font-size: 0.95rem;
}

th {
	color: #64748b;
	font-weight: 700;
}

td {
	color: #0f172a;
}

.status-pill {
	display: inline-block;
	padding: 4px 10px;
	border-radius: 999px;
	background: #ecfdf5;
	color: #166534;
	font-size: 0.82rem;
	font-weight: 700;
	text-transform: capitalize;
}

@media (max-width: 1023px) {
	.hero {
		align-items: start;
		flex-direction: column;
		padding: 20px;
	}

	.card-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
}

@media (max-width: 640px) {
	.card-grid {
		grid-template-columns: 1fr;
	}
}
</style>
