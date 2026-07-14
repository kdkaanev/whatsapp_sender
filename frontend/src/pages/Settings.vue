<script setup>
import { computed, reactive, ref } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const STORAGE_KEYS = {
  profile: 'settings_profile',
  notifications: 'settings_notifications',
  twoFactor: 'settings_two_factor',
}

const fallbackProfile = {
  fullName: 'John Doe',
  email: 'john.doe@acme.com',
  companyName: 'Acme Ltd.',
}

const UI_MESSAGES = {
  profileSaved: 'Changes saved locally on this device.',
  securityNote: 'Security changes are stored as local preferences in this version.',
  deleteUnavailable: 'Account deletion requires backend support and is not available yet.',
}

const MAX_NOTIFICATION_BADGE_COUNT = 3

const readStoredValue = (key, fallback) => {
  try {
    const rawValue = localStorage.getItem(key)
    return rawValue ? JSON.parse(rawValue) : fallback
  } catch (error) {
    console.warn(`Unable to parse stored settings for ${key}.`, error)
    return fallback
  }
}

const writeStoredValue = (key, value) => {
  try {
    localStorage.setItem(key, JSON.stringify(value))
  } catch (error) {
    console.warn(`Unable to store settings for ${key}.`, error)
  }
}

const profileForm = reactive({
  fullName: '',
  email: '',
  companyName: '',
})

const passwordForm = reactive({
  current: '',
  newPassword: '',
  confirm: '',
})

const defaultNotificationSettings = [
  {
    id: 'email',
    title: 'Email Notifications',
    description: 'Receive email notifications',
    enabled: true,
    icon: 'mail',
  },
  {
    id: 'completed',
    title: 'Campaign Completed',
    description: 'Notify me when a campaign is completed',
    enabled: true,
    icon: 'check',
  },
  {
    id: 'failed',
    title: 'Campaign Failed',
    description: 'Notify me when a campaign fails',
    enabled: true,
    icon: 'close',
  },
  {
    id: 'weekly',
    title: 'Weekly Summary',
    description: 'Receive a weekly summary of your activity',
    enabled: true,
    icon: 'calendar',
  },
]

const notificationSettings = ref(
  readStoredValue(STORAGE_KEYS.notifications, defaultNotificationSettings),
)

const twoFactorEnabled = ref(readStoredValue(STORAGE_KEYS.twoFactor, false))
const saveMessage = ref('')

const capitalizeFirstLetter = (word) =>
  word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()

const formatNameFromEmail = (email) => {
  const localPart = email.split('@')[0] ?? ''
  const words = localPart
    .split(/[._-]+/)
    .map((word) => word.trim())
    .filter(Boolean)

  if (!words.length) return 'John Doe'

  return words.map(capitalizeFirstLetter).join(' ')
}

const syncProfileForm = () => {
  const storedProfile = readStoredValue(STORAGE_KEYS.profile, null)
  if (storedProfile) {
    profileForm.fullName = storedProfile.fullName ?? ''
    profileForm.email = storedProfile.email ?? ''
    profileForm.companyName = storedProfile.companyName ?? ''
    return
  }

  const user = authStore.user

  if (!user) return

  const firstName = user.first_name?.trim() ?? ''
  const lastName = user.last_name?.trim() ?? ''
  const fullName = [firstName, lastName].filter(Boolean).join(' ')

  profileForm.fullName = fullName || formatNameFromEmail(user.email ?? '')
  profileForm.email = user.email ?? profileForm.email
}

syncProfileForm()

const displayProfile = computed(() => ({
  fullName: profileForm.fullName.trim() || fallbackProfile.fullName,
  email: profileForm.email.trim() || fallbackProfile.email,
  companyName: profileForm.companyName.trim() || fallbackProfile.companyName,
}))

let saveMessageTimeoutId

const notificationCount = computed(() =>
  Math.min(MAX_NOTIFICATION_BADGE_COUNT, notificationSettings.value.length),
)

const userInitials = computed(() =>
  displayProfile.value.fullName
    .trim()
    .split(' ')
    .filter(Boolean)
    .map((part) => part[0])
    .slice(0, 2)
    .join('')
    .toUpperCase(),
)

const saveProfile = () => {
  writeStoredValue(STORAGE_KEYS.profile, {
    fullName: profileForm.fullName.trim(),
    email: profileForm.email.trim(),
    companyName: profileForm.companyName.trim(),
  })
  saveMessage.value = UI_MESSAGES.profileSaved
  clearTimeout(saveMessageTimeoutId)
  saveMessageTimeoutId = window.setTimeout(() => {
    saveMessage.value = ''
  }, 3000)
}

const toggleNotification = (settingId) => {
  const setting = notificationSettings.value.find((item) => item.id === settingId)
  if (setting) {
    setting.enabled = !setting.enabled
    writeStoredValue(STORAGE_KEYS.notifications, notificationSettings.value)
  }
}

const toggleTwoFactor = () => {
  twoFactorEnabled.value = !twoFactorEnabled.value
  writeStoredValue(STORAGE_KEYS.twoFactor, twoFactorEnabled.value)
}
</script>

<template>
  <section class="settings-page">
    <header class="settings-toolbar">
      <label class="search-box" for="settings-search">
        <span class="search-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none">
            <circle cx="11" cy="11" r="6.5" />
            <path d="M16 16 21 21" />
          </svg>
        </span>
        <input
          id="settings-search"
          type="search"
          placeholder="Search anything..."
          aria-label="Search coming soon"
          disabled
        />
        <span class="shortcut">⌘ K</span>
      </label>

      <div class="toolbar-actions">
        <button
          class="notification-button"
          type="button"
          :aria-label="`Notifications, ${notificationCount} unread`"
        >
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M6 16.5h12" />
            <path d="M8 16.5v-5a4 4 0 1 1 8 0v5" />
            <path d="M10 19a2 2 0 0 0 4 0" />
          </svg>
          <span class="notification-badge">{{ notificationCount }}</span>
        </button>

        <div class="profile-chip">
          <div class="profile-avatar">{{ userInitials }}</div>
          <div>
            <p class="profile-name">{{ displayProfile.fullName }}</p>
            <p class="profile-company">{{ displayProfile.companyName }}</p>
          </div>
        </div>
      </div>
    </header>

    <header class="page-header">
      <div>
        <h1>Settings</h1>
        <p>Manage your account settings and preferences</p>
      </div>
    </header>

    <div class="settings-grid">
      <article class="settings-card">
        <div class="card-heading">
          <div class="card-icon card-icon--green" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z" />
              <path d="M4 20a8 8 0 0 1 16 0" />
            </svg>
          </div>
          <div>
            <h2>Profile</h2>
            <p>Update your personal and company information.</p>
          </div>
        </div>

        <form class="form-stack" @submit.prevent="saveProfile">
          <label class="field">
            <span>Full Name</span>
            <input
              v-model="profileForm.fullName"
              type="text"
              autocomplete="name"
              :placeholder="fallbackProfile.fullName"
            />
          </label>

          <label class="field">
            <span>Email Address</span>
            <input
              v-model="profileForm.email"
              type="email"
              autocomplete="email"
              :placeholder="fallbackProfile.email"
            />
          </label>

          <label class="field">
            <span>Company Name</span>
            <input
              v-model="profileForm.companyName"
              type="text"
              autocomplete="organization"
              :placeholder="fallbackProfile.companyName"
            />
          </label>

          <div class="card-footer">
            <button class="primary-button" type="submit">Save Changes</button>
            <p v-if="saveMessage" class="status-message" role="status" aria-live="polite">
              {{ saveMessage }}
            </p>
          </div>
        </form>
      </article>

      <article class="settings-card">
        <div class="card-heading">
          <div class="card-icon card-icon--green" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M12 3 5 6v5c0 4.5 2.9 8.6 7 10 4.1-1.4 7-5.5 7-10V6l-7-3Z" />
            </svg>
          </div>
          <div>
            <h2>Security</h2>
            <p>Change your password and secure your account.</p>
          </div>
        </div>

        <form class="form-stack" @submit.prevent>
          <label class="field">
            <span>Current Password</span>
            <div class="password-field">
              <input
                v-model="passwordForm.current"
                type="password"
                autocomplete="current-password"
                placeholder="••••••••"
                disabled
              />
              <button
                class="icon-button"
                type="button"
                aria-label="Current password unavailable"
                disabled
              >
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z" />
                  <circle cx="12" cy="12" r="3" />
                </svg>
              </button>
            </div>
          </label>

          <label class="field">
            <span>New Password</span>
            <div class="password-field">
              <input
                v-model="passwordForm.newPassword"
                type="password"
                autocomplete="new-password"
                placeholder="••••••••"
                disabled
              />
              <button
                class="icon-button"
                type="button"
                aria-label="New password unavailable"
                disabled
              >
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z" />
                  <circle cx="12" cy="12" r="3" />
                </svg>
              </button>
            </div>
          </label>

          <label class="field">
            <span>Confirm New Password</span>
            <div class="password-field">
              <input
                v-model="passwordForm.confirm"
                type="password"
                autocomplete="new-password"
                placeholder="••••••••"
                disabled
              />
              <button
                class="icon-button"
                type="button"
                aria-label="Confirmation password unavailable"
                disabled
              >
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z" />
                  <circle cx="12" cy="12" r="3" />
                </svg>
              </button>
            </div>
          </label>

          <div class="divider"></div>

          <div class="toggle-row">
            <div>
              <h3>Two-factor Authentication</h3>
              <p>Add an extra layer of security to your account.</p>
            </div>
            <button
              class="toggle-button"
              :class="{ 'is-enabled': twoFactorEnabled }"
              type="button"
              :aria-pressed="twoFactorEnabled"
              @click="toggleTwoFactor"
            >
              <span></span>
            </button>
          </div>
          <p class="helper-text">{{ UI_MESSAGES.securityNote }}</p>
        </form>
      </article>

      <article class="settings-card">
        <div class="card-heading">
          <div class="card-icon card-icon--green" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M12 3a4 4 0 0 1 4 4v1.2a5 5 0 0 0 1.1 3.1l.6.8A2 2 0 0 1 16 15H8a2 2 0 0 1-1.7-2.9l.6-.8A5 5 0 0 0 8 8.2V7a4 4 0 0 1 4-4Z" />
              <path d="M10 18a2 2 0 1 0 4 0" />
            </svg>
          </div>
          <div>
            <h2>Notifications</h2>
            <p>Choose what you want to be notified about.</p>
          </div>
        </div>

        <div class="notification-list">
          <div
            v-for="setting in notificationSettings"
            :key="setting.id"
            class="notification-row"
          >
            <div class="notification-copy">
              <div class="notification-icon" aria-hidden="true">
                <svg v-if="setting.icon === 'mail'" viewBox="0 0 24 24" fill="none">
                  <rect x="4" y="6" width="16" height="12" rx="2" />
                  <path d="m5 8 7 5 7-5" />
                </svg>
                <svg v-else-if="setting.icon === 'check'" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="8" />
                  <path d="m8.5 12 2.5 2.5 4.5-5" />
                </svg>
                <svg v-else-if="setting.icon === 'close'" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="8" />
                  <path d="m9.5 9.5 5 5" />
                  <path d="m14.5 9.5-5 5" />
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none">
                  <rect x="5" y="4" width="14" height="15" rx="2" />
                  <path d="M8 2.5v3" />
                  <path d="M16 2.5v3" />
                  <path d="M5 9h14" />
                </svg>
              </div>
              <div>
                <h3>{{ setting.title }}</h3>
                <p>{{ setting.description }}</p>
              </div>
            </div>

            <button
              class="toggle-button"
              :class="{ 'is-enabled': setting.enabled }"
              type="button"
              :aria-pressed="setting.enabled"
              @click="toggleNotification(setting.id)"
            >
              <span></span>
            </button>
          </div>
        </div>
      </article>

      <article class="settings-card">
        <div class="card-heading">
          <div class="card-icon card-icon--red" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M12 3 3 20h18L12 3Z" />
              <path d="M12 9v4" />
              <circle cx="12" cy="16.5" r=".8" fill="currentColor" stroke="none" />
            </svg>
          </div>
          <div>
            <h2>Danger Zone</h2>
            <p>Irreversible and destructive actions.</p>
          </div>
        </div>

        <div class="danger-panel">
          <div>
            <h3>Delete Account</h3>
            <p>Once you delete your account, there is no going back. Please be certain.</p>
            <p class="helper-text helper-text--danger">{{ UI_MESSAGES.deleteUnavailable }}</p>
          </div>
          <button class="danger-button danger-button--disabled" type="button" disabled>
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M4 7h16" />
              <path d="M9 7V5h6v2" />
              <path d="M8 10v7" />
              <path d="M12 10v7" />
              <path d="M16 10v7" />
              <path d="M6 7l1 12h10l1-12" />
            </svg>
            Delete Account
          </button>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.settings-page {
  display: grid;
  gap: 28px;
}



.settings-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 18px 10px 0;
}

.search-box {
  flex: 1;
  max-width: 420px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 14px;
  min-height: 54px;
  border-radius: 16px;
  border: 1px solid rgba(226, 232, 240, 0.95);
  background: #ffffff;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04);
}

.search-box input {
  flex: 1;
  border: 0;
  outline: none;
  font: inherit;
  color: #111827;
  background: transparent;
}

.search-box input::placeholder {
  color: #94a3b8;
}

.search-icon,
.shortcut,
.notification-button,
.profile-avatar,
.card-icon,
.notification-icon,
.icon-button {
  flex: 0 0 auto;
}

.search-icon svg,
.notification-button svg,
.card-icon svg,
.notification-icon svg,
.icon-button svg,
.danger-button svg {
  width: 20px;
  height: 20px;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.search-icon {
  color: #94a3b8;
}

.shortcut {
  padding: 6px 8px;
  border-radius: 10px;
  border: 1px solid rgba(226, 232, 240, 1);
  color: #94a3b8;
  font-size: 0.85rem;
  font-weight: 700;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.notification-button {
  position: relative;
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  border: 1px solid rgba(226, 232, 240, 0.95);
  background: #ffffff;
  color: #64748b;
  cursor: pointer;
}

.icon-button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.notification-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  min-width: 20px;
  height: 20px;
  padding: 0 5px;
  display: inline-grid;
  place-items: center;
  border-radius: 999px;
  background: #22c55e;
  color: #ffffff;
  font-size: 0.75rem;
  font-weight: 700;
}

.profile-chip {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 14px 8px 8px;
  border-radius: 18px;
  border: 1px solid rgba(226, 232, 240, 0.95);
  background: #ffffff;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04);
}

.profile-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #22c55e 0%, #15803d 100%);
  color: #ffffff;
  font-weight: 800;
}

.profile-name,
.profile-company {
  margin: 0;
}

.profile-name {
  font-weight: 700;
  color: #0f172a;
}

.profile-company {
  margin-top: 2px;
  color: #64748b;
  font-size: 0.92rem;
}

.page-header h1 {
  margin: 0;
  font-size: clamp(2rem, 3vw, 2.75rem);
  color: #0f172a;
}

.page-header p {
  margin: 10px 0 0;
  color: #64748b;
  font-size: 1.05rem;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 22px;
}

.settings-card {
  padding: 22px;
  border-radius: 24px;
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.95);
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.05);
}

.card-heading {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 24px;
}

.card-heading h2,
.card-heading p,
.toggle-row h3,
.toggle-row p,
.notification-copy h3,
.notification-copy p,
.danger-panel h3,
.danger-panel p {
  margin: 0;
}

.card-heading h2 {
  font-size: 1.65rem;
  color: #0f172a;
}

.card-heading p,
.toggle-row p,
.notification-copy p,
.danger-panel p {
  margin-top: 6px;
  color: #64748b;
  line-height: 1.5;
}

.card-icon {
  width: 56px;
  height: 56px;
  display: grid;
  place-items: center;
  border-radius: 18px;
}

.card-icon--green {
  color: #16a34a;
  background: linear-gradient(180deg, #eefcf3 0%, #e0f8e8 100%);
}

.card-icon--red {
  color: #ef4444;
  background: linear-gradient(180deg, #fff1f1 0%, #fee2e2 100%);
}

.form-stack {
  display: grid;
  gap: 18px;
}

.field {
  display: grid;
  gap: 8px;
}

.field span {
  color: #111827;
  font-weight: 700;
  font-size: 0.96rem;
}

.field input {
  width: 100%;
  min-height: 52px;
  padding: 0 16px;
  border-radius: 14px;
  border: 1px solid rgba(209, 213, 219, 0.95);
  background: #ffffff;
  color: #111827;
  font: inherit;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;
}

.field input:focus {
  border-color: rgba(27, 154, 93, 0.7);
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.12);
}

.password-field {
  position: relative;
}

.password-field input {
  padding-right: 56px;
}

.icon-button {
  position: absolute;
  top: 50%;
  right: 12px;
  transform: translateY(-50%);
  width: 36px;
  height: 36px;
  border: 0;
  border-radius: 10px;
  background: transparent;
  color: #94a3b8;
  display: grid;
  place-items: center;
  cursor: pointer;
}

.card-footer {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
  padding-top: 6px;
}

.primary-button,
.danger-button {
  min-height: 50px;
  padding: 0 20px;
  border: 0;
  border-radius: 14px;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
}

.primary-button {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: #ffffff;
  box-shadow: 0 14px 24px rgba(34, 197, 94, 0.2);
}

.status-message {
  margin: 0;
  color: #15803d;
  font-weight: 600;
}

.helper-text {
  margin: 0;
  color: #64748b;
  font-size: 0.92rem;
}

.helper-text--danger {
  color: #b91c1c;
}

.divider {
  height: 1px;
  background: rgba(226, 232, 240, 1);
}

.toggle-row,
.notification-row,
.danger-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}

.toggle-row h3,
.notification-copy h3,
.danger-panel h3 {
  font-size: 1.05rem;
  color: #0f172a;
}

.toggle-button {
  width: 50px;
  height: 30px;
  padding: 3px;
  border: 0;
  border-radius: 999px;
  background: #d1d5db;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.toggle-button span {
  display: block;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #ffffff;
  transition: transform 0.2s ease;
}

.toggle-button.is-enabled {
  background: #22c55e;
}

.toggle-button.is-enabled span {
  transform: translateX(20px);
}

.notification-list {
  display: grid;
  gap: 4px;
}

.notification-row {
  padding: 14px 0;
  border-top: 1px solid rgba(241, 245, 249, 1);
}

.notification-row:first-child {
  border-top: 0;
  padding-top: 0;
}

.notification-copy {
  display: flex;
  align-items: center;
  gap: 14px;
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  color: #16a34a;
  background: linear-gradient(180deg, #eefcf3 0%, #e0f8e8 100%);
}

.danger-panel {
  padding: 18px 18px 18px 20px;
  border-radius: 18px;
  background: linear-gradient(180deg, #fff5f5 0%, #fff1f1 100%);
  border: 1px solid rgba(254, 202, 202, 0.9);
}

.danger-panel h3 {
  color: #ef4444;
}

.danger-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: #ffffff;
  white-space: nowrap;
}

.danger-button--disabled {
  cursor: not-allowed;
  opacity: 0.72;
  box-shadow: none;
}

@media (max-width: 1199px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 767px) {
  .settings-page {
    gap: 22px;
  }

  .settings-toolbar,
  .card-heading,
  .toggle-row,
  .notification-row,
  .danger-panel {
    align-items: stretch;
  }

  .settings-toolbar,
  .toolbar-actions,
  .toggle-row,
  .notification-row,
  .danger-panel {
    flex-direction: column;
  }

  .search-box {
    max-width: none;
  }

  .toolbar-actions {
    align-items: stretch;
  }

  .notification-button {
    align-self: flex-start;
  }

  .profile-chip,
  .toggle-button,
  .danger-button {
    align-self: flex-start;
  }

  .settings-card {
    padding: 20px;
  }

  .notification-copy {
    align-items: flex-start;
  }
}
</style>
