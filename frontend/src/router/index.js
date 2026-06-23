import { createRouter, createWebHistory } from 'vue-router'
import DashBoard from '../pages/DashBoard.vue'
import ContactsPage from '../pages/ContactsPage.vue'
import CampainsPage from '../pages/CampainsPage.vue'
import MessagesPage from '../pages/MessagesPage.vue'
import TemplatesPage from '../pages/TemplatesPage.vue'
import Settings from '../pages/Settings.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: DashBoard
  },
  {
    path: '/contacts',
    name: 'Contacts',
    component: ContactsPage
  },
  {
    path: '/campaigns',
    name: 'Campaigns',
    component: CampainsPage
  },
  {
    path: '/messages',
    name: 'Messages',
    component: MessagesPage
  },
  {
    path: '/templates',
    name: 'Templates',
    component: TemplatesPage
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
