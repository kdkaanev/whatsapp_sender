<script setup>
import { useAuthStore } from '../stores/auth.js'
import { RouterLink, useRoute, useRouter } from 'vue-router'

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const isActive = (path) => {
    if (path === '/') {
        return route.path === '/'
    }

    return route.path === path || route.path.startsWith(`${path}/`)
}

const logout = () => {
    authStore.logout()
    router.push('/login')
}
</script>

<template>
    <aside class="sidebar">
        <nav class="sidebar-nav">
            <ul class="nav-list">
                <li>
                    <RouterLink to="/" class="nav-item" :class="{ 'is-active': isActive('/') }">
                        <span class="nav-icon" aria-hidden="true">
                            <svg viewBox="0 0 24 24" fill="none">
                                <path d="M4 10.5L12 4l8 6.5" />
                                <path d="M6.5 9.5V19h11V9.5" />
                                <path d="M10 19v-5h4v5" />
                            </svg>
                        </span>
                        <span class="nav-text">Dashboard</span>
                    </RouterLink>
                </li>
                <li>
                    <RouterLink to="/contacts" class="nav-item" :class="{ 'is-active': isActive('/contacts') }">
                        <span class="nav-icon" aria-hidden="true">
                            <svg viewBox="0 0 24 24" fill="none">
                                <path d="M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" />
                                <path d="M4 18a5 5 0 0 1 10 0" />
                                <path d="M17 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z" />
                                <path d="M14.5 18a4.5 4.5 0 0 1 5.5-4.4" />
                            </svg>
                        </span>
                        <span class="nav-text">Contacts</span>
                    </RouterLink>
                </li>
                <li>
                    <RouterLink to="/campaigns" class="nav-item" :class="{ 'is-active': isActive('/campaigns') }">
                        <span class="nav-icon" aria-hidden="true">
                            <svg viewBox="0 0 24 24" fill="none">
                                <path d="M5 11.5 19 5l-6.5 14-2.5-5-5-2.5Z" />
                                <path d="m10 14 4-4" />
                            </svg>
                        </span>
                        <span class="nav-text">Campaigns</span>
                    </RouterLink>
                </li>
                <li>
                    <RouterLink to="/messages" class="nav-item" :class="{ 'is-active': isActive('/messages') }">
                        <span class="nav-icon" aria-hidden="true">
                            <svg viewBox="0 0 24 24" fill="none">
                                <path d="M5 6.5h14v9H9l-4 3v-12Z" />
                                <path d="M9 10.5h6" />
                            </svg>
                        </span>
                        <span class="nav-text">Messages</span>
                    </RouterLink>
                </li>
                <li>
                    <RouterLink to="/templates" class="nav-item" :class="{ 'is-active': isActive('/templates') }">
                        <span class="nav-icon" aria-hidden="true">
                            <svg viewBox="0 0 24 24" fill="none">
                                <rect x="5" y="4" width="14" height="16" rx="1.5" />
                                <path d="M9 8h2" />
                                <path d="M13 8h2" />
                                <path d="M9 12h2" />
                                <path d="M13 12h2" />
                                <path d="M9 16h6" />
                            </svg>
                        </span>
                        <span class="nav-text">Templates</span>
                    </RouterLink>
                </li>
                <li>
                    <RouterLink to="/settings" class="nav-item" :class="{ 'is-active': isActive('/settings') }">
                        <span class="nav-icon" aria-hidden="true">
                            <svg viewBox="0 0 24 24" fill="none">
                                <path d="M12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7Z" />
                                <path d="M19 12a7 7 0 0 0-.1-1l2-1.6-2-3.4-2.5 1a7.4 7.4 0 0 0-1.7-1L14.4 3h-4.8l-.3 3a7.4 7.4 0 0 0-1.7 1l-2.5-1-2 3.4 2 1.6a7 7 0 0 0 0 2l-2 1.6 2 3.4 2.5-1a7.4 7.4 0 0 0 1.7 1l.3 3h4.8l.3-3a7.4 7.4 0 0 0 1.7-1l2.5 1 2-3.4-2-1.6c.1-.3.1-.7.1-1Z" />
                            </svg>
                        </span>
                        <span class="nav-text">Settings</span>
                    </RouterLink>
                </li>
            </ul>

            <button @click="logout" class="nav-item logout-btn" type="button" aria-label="Log out of account">
                <span class="nav-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M9 5H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h3" />
                        <path d="M16 17l5-5-5-5" />
                        <path d="M21 12H9" />
                    </svg>
                </span>
                <span class="nav-text">Logout</span>
            </button>
        </nav>
    </aside>
</template>

<style scoped>
.sidebar {
    width: 240px;
    height: 100vh;
    background: #ffffff;
    color: #1f2937;
    padding: 20px 18px;
    position: sticky;
    top: 0;
    overflow-y: auto;
    box-shadow: 18px 0 40px rgba(15, 23, 42, 0.05);
    z-index: 100;
    flex: 0 0 auto;
    border-right: 1px solid rgba(226, 232, 240, 0.9);
}

@media (max-width: 1023px) {
    .sidebar {
        display: none;
    }
}

.sidebar-nav {
    min-height: 100%;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.nav-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 10px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 16px;
    color: #111827;
    text-decoration: none;
    transition: background-color 0.2s ease, color 0.2s ease, box-shadow 0.2s ease;
    background-color: transparent;
    border: none;
    cursor: pointer;
    width: 100%;
    text-align: left;
    font-size: 1.05rem;
    font-weight: 600;
    font-family: inherit;
    border-radius: 16px;
}

.nav-item:hover {
    background: #edf2f7;
}

.nav-item.is-active {
    background: linear-gradient(180deg, #eef8f1 0%, #f4fbf6 100%);
    color: #1b9a5d;
    font-weight: 700;
    box-shadow: 0 8px 20px rgba(27, 154, 93, 0.08);
}

.nav-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    color: inherit;
    flex: 0 0 auto;
}

.nav-icon svg {
    width: 100%;
    height: 100%;
    fill: none;
    stroke: currentColor;
    stroke-width: 1.8;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.nav-text {
    flex: 1;
}

.logout-btn {
    margin-top: auto;
    color: #4b5563;
}

.logout-btn:hover {
    background: #f8fafc;
}

/* Scrollbar styling */
.sidebar::-webkit-scrollbar {
    width: 6px;
}

.sidebar::-webkit-scrollbar-track {
    background: transparent;
}

.sidebar::-webkit-scrollbar-thumb {
    background: rgba(148, 163, 184, 0.7);
    border-radius: 3px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
    background: rgba(100, 116, 139, 0.9);
}
</style>