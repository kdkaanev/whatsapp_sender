<script setup>
import { useAuthStore } from '../stores/auth.js'
import { RouterLink, useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
    authStore.logout()
    router.push('/login')
}
</script>

<template>
    <aside class="sidebar">
        <div class="sidebar-header">
            <h2>Campaign Manager</h2>
        </div>
        
        <nav class="sidebar-nav">
            <div class="nav-section">
                <h3 class="nav-title">Main</h3>
                <ul class="nav-list">
                    <li>
                        <RouterLink to="/" class="nav-item">
                            <span class="nav-icon">📊</span>
                            <span class="nav-text">Dashboard</span>
                        </RouterLink>
                    </li>
                    <li>
                        <RouterLink to="/contacts" class="nav-item">
                            <span class="nav-icon">👥</span>
                            <span class="nav-text">Contacts</span>
                        </RouterLink>
                    </li>
                    <li>
                        <RouterLink to="/campaigns" class="nav-item">
                            <span class="nav-icon">📣</span>
                            <span class="nav-text">Campaigns</span>
                        </RouterLink>
                    </li>
                </ul>
            </div>

            <div class="nav-section">
                <h3 class="nav-title">Communication</h3>
                <ul class="nav-list">
                    <li>
                        <RouterLink to="/messages" class="nav-item">
                            <span class="nav-icon">💬</span>
                            <span class="nav-text">Messages</span>
                        </RouterLink>
                    </li>
                    <li>
                        <RouterLink to="/templates" class="nav-item">
                            <span class="nav-icon">📝</span>
                            <span class="nav-text">Templates</span>
                        </RouterLink>
                    </li>
                </ul>
            </div>

            <div class="nav-section">
                <h3 class="nav-title">Account</h3>
                <ul class="nav-list">
                    <li>
                        <RouterLink to="/settings" class="nav-item">
                            <span class="nav-icon">⚙️</span>
                            <span class="nav-text">Settings</span>
                        </RouterLink>
                    </li>
                    <li>
                        <button @click="logout" class="nav-item logout-btn">
                            <span class="nav-icon">🚪</span>
                            <span class="nav-text">Logout</span>
                        </button>
                    </li>
                </ul>
            </div>
        </nav>
    </aside>
</template>

<style scoped>
.sidebar {
    width: 260px;
    height: 100vh;
    background: transparent;
    color: #111111;
    padding: 0;
    position: sticky;
    top: 0;
    overflow-y: auto;
    box-shadow: none;
    z-index: 100;
    flex: 0 0 auto;
    border-right: 1px solid rgba(229, 231, 235, 0.7);
}

@media (max-width: 1023px) {
    .sidebar {
        display: none;
    }
}

.sidebar-header {
    padding: 20px;
    border-bottom: 1px solid rgba(229, 231, 235, 0.7);
}

.sidebar-header h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 700;
    color: #111111;
}

.sidebar-nav {
    padding: 20px 0;
}

.nav-section {
    margin-bottom: 30px;
}

.nav-title {
    padding: 0 20px;
    margin: 0 0 10px 0;
    font-size: 0.75rem;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #6b7280;
}

.nav-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 20px;
    color: #111111;
    text-decoration: none;
    transition: all 0.3s ease;
    border-left: 3px solid transparent;
    background-color: transparent;
    border: none;
    cursor: pointer;
    width: 100%;
    text-align: left;
    font-size: 1rem;
    font-family: inherit;
    border-radius: 4px;
}

.nav-item:hover {
    background-color:#b3e2c4 ;
    border-left-color: #b3e2c4;
    padding-left: 17px;
}

.nav-item.router-link-active {
    background-color: #b3e2c4;
    border-left-color: #b3e2c4;
    color: #166534;
    font-weight: 700;
}

.nav-icon {
    font-size: 1.25rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
}

.nav-text {
    flex: 1;
}

.logout-btn {
    color: #111111;
}

.logout-btn:hover {
    background-color: #f3f4f6;
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