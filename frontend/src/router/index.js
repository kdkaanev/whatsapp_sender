import { createRouter, createWebHistory } from 'vue-router'
import DashBoard from '../pages/DashBoard.vue'
import ContactsPage from '../pages/ContactsPage.vue'
import CampainsPage from '../pages/CampainsPage.vue'
import MessagesPage from '../pages/MessagesPage.vue'
import TemplatesPage from '../pages/TemplatesPage.vue'
import Settings from '../pages/Settings.vue'
import LogIn from '../components/LogIn.vue'
import RegisterPage from '../pages/RegisterPage.vue'

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
    path: '/login',
    name: 'Login',
    component: LogIn
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage
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

router.beforeEach((to) => {
  const hasToken = Boolean(localStorage.getItem('access_token'))
  const isPublicAuthRoute = to.path === '/login' || to.path === '/register'

  if (!isPublicAuthRoute && !hasToken) {
    return { path: '/login' }
  }

  if (isPublicAuthRoute && hasToken) {
    return { path: '/' }
  }
})

export default router
