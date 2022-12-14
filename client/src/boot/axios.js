import { boot } from 'quasar/wrappers'
import axios from 'axios'
import { useAuthStore } from 'stores/auth'
import { useModactivityStore } from 'src/modactivity/modactivity.store'

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
axios.defaults.withCredentials = true

function calculateBaseUrl () {
  if (process.env.DEV) {
    console.log('I\'m on a development build')
    return { baseURL: 'http://localhost:5000' }
  } else if (process.env.PROD) {
    console.log('I\'m on a production build')
    return {}
  }
}

const options = { ...calculateBaseUrl(), ...{ withCredentials: true } }
const api = axios.create(options)

export default boot(({ app, store }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  const authStore = useAuthStore(store)
  authStore.$api = api

  const modactivityStore = useModactivityStore(store)
  modactivityStore.$api = api

  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})

export { api }
