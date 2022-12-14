import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { useAlertStore } from 'stores/alert.store'
import { useAuthStore } from 'stores/auth'
import { route } from 'quasar/wrappers'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.MODE === 'ssr' ? void 0 : process.env.VUE_ROUTER_BASE)
  })

  Router.beforeEach(async (to) => {
    // clear alert on route change
    const alertStore = useAlertStore()
    alertStore.clear()

    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/account/login', '/account/callback']
    const authRequired = !publicPages.includes(to.path)

    const authStore = useAuthStore()
    if (!authStore.user) {
      console.log('router/index.js#beforeEach: fetching user')
      await authStore.fetchUser()
    }

    if (authRequired && !authStore.user) {
      authStore.returnUrl = to.fullPath
      return '/account/login'
    }
  })

  return Router
})
