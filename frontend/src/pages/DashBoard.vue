<script setup>
const summaryCards = [
	{ label: 'Active campaigns', value: '12', hint: '+3 this week' },
	{ label: 'Contacts synced', value: '1,248', hint: '98% match rate' },
	{ label: 'Messages sent', value: '8,420', hint: 'All channels' },
]
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
		</header>

		<div class="card-grid">
			<article v-for="card in summaryCards" :key="card.label" class="metric-card">
				<p class="metric-label">{{ card.label }}</p>
				<p class="metric-value">{{ card.value }}</p>
				<p class="metric-hint">{{ card.hint }}</p>
			</article>
		</div>
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

.card-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 16px;
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

@media (max-width: 1023px) {
	.hero {
		padding: 20px;
	}

	.card-grid {
		grid-template-columns: 1fr;
	}
}
</style>
