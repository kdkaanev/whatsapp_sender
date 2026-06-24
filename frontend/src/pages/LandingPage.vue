<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const features = [
    {
        title: 'Mass Contact Import',
        description: 'Upload Excel files and segment contacts with tags for high-precision campaign targeting.'
    },
    {
        title: 'Template Driven Messaging',
        description: 'Build reusable WhatsApp templates and launch personalized campaigns in a few clicks.'
    },
    {
        title: 'Live Campaign Control',
        description: 'Track delivery flow, pause campaigns, and keep your outreach timeline under control.'
    }
]

const metrics = [
    { value: '1.2M+', label: 'messages processed' },
    { value: '99.9%', label: 'delivery jobs tracked' },
    { value: '24/7', label: 'campaign operations' }
]

const year = computed(() => new Date().getFullYear())

const goToLogin = () => {
    router.push('/login')
}

const goToRegister = () => {
    router.push('/register')
}
</script>

<template>
    <div class="landing">
        <div class="landing-noise" aria-hidden="true"></div>

        <header class="landing-header">
            <div class="logo-wrap">
                <div class="logo-dot"></div>
                <span class="logo-text">WhatsApp Outreach Hub</span>
            </div>

            <button class="btn btn-ghost" type="button" @click="goToLogin">Sign In</button>
        </header>

        <section class="hero">
            <div class="hero-copy">
                <p class="eyebrow">Campaign OS For WhatsApp Teams</p>
                <h1>Send smarter WhatsApp campaigns with less effort.</h1>
                <p class="hero-subtitle">
                    One platform for contact imports, templated messages, scheduling, and campaign operations.
                    Built for teams that care about speed and control.
                </p>

                <div class="hero-actions">
                    <button class="btn btn-primary" type="button" @click="goToRegister">Create Account</button>
                    <button class="btn btn-outline" type="button" @click="goToLogin">Open Workspace</button>
                </div>
            </div>

            <div class="hero-panel" aria-label="Platform highlights">
                <h2>What you can do in minutes</h2>

                <ul class="feature-list">
                    <li v-for="feature in features" :key="feature.title" class="feature-item">
                        <h3>{{ feature.title }}</h3>
                        <p>{{ feature.description }}</p>
                    </li>
                </ul>
            </div>
        </section>

        <section class="metrics" aria-label="Platform metrics">
            <article v-for="metric in metrics" :key="metric.label" class="metric-card">
                <h3>{{ metric.value }}</h3>
                <p>{{ metric.label }}</p>
            </article>
        </section>

        <footer class="landing-footer">
            <p>© {{ year }} WhatsApp Outreach Hub</p>
            <p>Launch, automate, and scale customer conversations.</p>
        </footer>
    </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&family=Sora:wght@500;600;700&display=swap');

.landing {
    position: relative;
    min-height: 100vh;
    padding: 28px clamp(18px, 4vw, 56px) 36px;
    color: #0f172a;
    font-family: 'Manrope', sans-serif;
    background:
        radial-gradient(circle at 18% 20%, rgba(246, 215, 179, 0.58) 0%, rgba(246, 215, 179, 0) 42%),
        radial-gradient(circle at 84% 14%, rgba(133, 229, 210, 0.44) 0%, rgba(133, 229, 210, 0) 38%),
        linear-gradient(145deg, #fff4e8 0%, #f8fcfa 48%, #edf6ff 100%);
    overflow: hidden;
}

.landing-noise {
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: 0.24;
    background-image:
        linear-gradient(0deg, transparent 24%, rgba(15, 23, 42, 0.03) 25%, rgba(15, 23, 42, 0.03) 26%, transparent 27%, transparent 74%, rgba(15, 23, 42, 0.03) 75%, rgba(15, 23, 42, 0.03) 76%, transparent 77%),
        linear-gradient(90deg, transparent 24%, rgba(15, 23, 42, 0.03) 25%, rgba(15, 23, 42, 0.03) 26%, transparent 27%, transparent 74%, rgba(15, 23, 42, 0.03) 75%, rgba(15, 23, 42, 0.03) 76%, transparent 77%);
    background-size: 28px 28px;
}

.landing-header,
.hero,
.metrics,
.landing-footer {
    position: relative;
    z-index: 1;
}

.landing-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 34px;
}

.logo-wrap {
    display: inline-flex;
    align-items: center;
    gap: 12px;
}

.logo-dot {
    width: 14px;
    height: 14px;
    border-radius: 999px;
    background: linear-gradient(135deg, #14b86e 0%, #21d48d 100%);
    box-shadow: 0 0 0 6px rgba(20, 184, 110, 0.16);
}

.logo-text {
    font-family: 'Sora', sans-serif;
    font-size: 0.95rem;
    letter-spacing: 0.02em;
    font-weight: 700;
}

.hero {
    display: grid;
    grid-template-columns: 1.12fr 0.88fr;
    gap: 22px;
    align-items: stretch;
}

.hero-copy,
.hero-panel {
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.65);
    box-shadow: 0 24px 70px rgba(15, 23, 42, 0.12);
    backdrop-filter: blur(8px);
    animation: reveal-up 650ms ease both;
}

.hero-copy {
    padding: clamp(24px, 5vw, 54px);
    background: rgba(255, 255, 255, 0.7);
    animation-delay: 0.04s;
}

.eyebrow {
    display: inline-block;
    margin: 0 0 12px;
    color: #0d7a5f;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    font-family: 'Sora', sans-serif;
    font-size: 0.76rem;
    font-weight: 700;
}

h1 {
    margin: 0;
    max-width: 16ch;
    font-size: clamp(2.05rem, 4.7vw, 4rem);
    line-height: 1.05;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    margin: 18px 0 0;
    max-width: 46ch;
    color: #334155;
    font-size: clamp(1rem, 1.5vw, 1.16rem);
    line-height: 1.65;
}

.hero-actions {
    margin-top: 30px;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.hero-panel {
    background: linear-gradient(165deg, rgba(12, 74, 110, 0.94) 0%, rgba(15, 23, 42, 0.92) 100%);
    color: #f8fafc;
    padding: clamp(22px, 4vw, 34px);
    animation-delay: 0.15s;
}

.hero-panel h2 {
    margin: 0 0 18px;
    font-family: 'Sora', sans-serif;
    letter-spacing: -0.01em;
    font-size: clamp(1.2rem, 2vw, 1.55rem);
}

.feature-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 14px;
}

.feature-item {
    padding: 14px 15px;
    border-radius: 15px;
    background: rgba(148, 163, 184, 0.12);
    border: 1px solid rgba(148, 163, 184, 0.25);
}

.feature-item h3 {
    margin: 0;
    font-size: 1rem;
    font-weight: 700;
}

.feature-item p {
    margin: 8px 0 0;
    color: rgba(248, 250, 252, 0.9);
    line-height: 1.55;
    font-size: 0.96rem;
}

.metrics {
    margin-top: 22px;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
}

.metric-card {
    border-radius: 16px;
    padding: 20px 18px;
    background: rgba(255, 255, 255, 0.74);
    border: 1px solid rgba(255, 255, 255, 0.85);
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    animation: reveal-up 650ms ease both;
}

.metric-card:nth-child(1) {
    animation-delay: 0.25s;
}

.metric-card:nth-child(2) {
    animation-delay: 0.32s;
}

.metric-card:nth-child(3) {
    animation-delay: 0.39s;
}

.metric-card h3 {
    margin: 0;
    color: #0a5c48;
    font-family: 'Sora', sans-serif;
    font-size: 1.55rem;
}

.metric-card p {
    margin: 6px 0 0;
    color: #334155;
    font-size: 0.92rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.landing-footer {
    margin-top: 22px;
    display: flex;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
    color: #334155;
    font-size: 0.9rem;
}

.landing-footer p {
    margin: 0;
}

.btn {
    border: 0;
    border-radius: 12px;
    cursor: pointer;
    font-family: 'Sora', sans-serif;
    font-size: 0.92rem;
    font-weight: 700;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn:hover {
    transform: translateY(-1px);
}

.btn-primary {
    padding: 13px 18px;
    color: #ffffff;
    background: linear-gradient(135deg, #068954 0%, #13b67d 100%);
    box-shadow: 0 14px 28px rgba(6, 137, 84, 0.24);
}

.btn-outline {
    padding: 13px 18px;
    color: #0f172a;
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.45);
}

.btn-ghost {
    padding: 9px 14px;
    background: rgba(255, 255, 255, 0.78);
    border: 1px solid rgba(148, 163, 184, 0.4);
    color: #0f172a;
}

@keyframes reveal-up {
    from {
        opacity: 0;
        transform: translateY(16px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (max-width: 980px) {
    .landing {
        padding: 20px 14px 24px;
    }

    .hero {
        grid-template-columns: 1fr;
    }

    .metrics {
        grid-template-columns: 1fr;
    }

    h1 {
        max-width: 18ch;
    }

    .landing-footer {
        flex-direction: column;
    }
}
</style>