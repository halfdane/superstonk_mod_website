import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { useAlertStore } from 'stores/alert.store'
import { useAuthStore } from 'stores/auth'

const createHistory = process.env.SERVER
  ? createMemoryHistory
  : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

export const router = createRouter({
  scrollBehavior: () => ({ left: 0, top: 0 }),
  routes,

  // Leave this as is and make changes in quasar.conf.js instead!
  // quasar.conf.js -> build -> vueRouterMode
  // quasar.conf.js -> build -> publicPath
  history: createHistory(process.env.MODE === 'ssr' ? void 0 : process.env.VUE_ROUTER_BASE)
})

router.beforeEach(async (to) => {
  // clear alert on route change
  const alertStore = useAlertStore()
  alertStore.clear()

  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/account/login', '/account/callback']
  const authRequired = !publicPages.includes(to.path)
  
  const authStore = useAuthStore()
  authStore.fetchUser()

  if (authRequired && !authStore.user) {
    authStore.returnUrl = to.fullPath
    return '/account/login'
  }
})
