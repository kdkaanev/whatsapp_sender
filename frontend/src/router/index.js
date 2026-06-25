import { createRouter, createWebHistory } from 'vue-router'
import DashBoard from '../pages/DashBoard.vue'
import ContactsPage from '../pages/ContactsPage.vue'
import CampainsPage from '../pages/CampainsPage.vue'
import MessagesPage from '../pages/MessagesPage.vue'
import TemplatesPage from '../pages/TemplatesPage.vue'
import Settings from '../pages/Settings.vue'
import LogIn from '../components/LogIn.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import LandingPage from '../pages/LandingPage.vue'
import CreateContact from '../components/CreateContactss.vue'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingPage
  },
  {
    path: '/dashboard',
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
  ,
  {
    path: '/create-contact',
    name: 'CreateContact',
    component: CreateContact
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const hasToken = Boolean(localStorage.getItem('access_token'))
  const isPublicRoute = to.path === '/' || to.path === '/login' || to.path === '/register'

  if (!isPublicRoute && !hasToken) {
    return { path: '/' }
  }

  if (to.path === '/' && hasToken) {
    return { path: '/dashboard' }
  }
})

export default router
