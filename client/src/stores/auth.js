import { useAlertStore } from 'stores/alert.store.js'
import axios from 'axios'
import { defineStore } from 'pinia'

if (process.env.DEV) {
  console.log('I\'m on a development build')
  const baseUrl = 'http://localhost:5000'
} else if (process.env.PROD) {
  const baseUrl = ''
  console.log('I\'m on a production build')
}


const session = axios.create({ baseURL: `${baseUrl}/session`, withCredentials: true })

function defaultErrorHandler (error) {
  const alertStore = useAlertStore()
  alertStore.error(error)
}

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    user: null,
    returnUrl: null,
    authenticationEndpoint: null
  }),
  mounted () {
    console.log('auth.js#mounted: calling fetchUser')
    this.fetchUser()
  },
  actions: {
    async prepare () {
      session.get('/authentication_endpoint/')
        .then((response) => response.data)
        .then((authData) => {
          this.authenticationEndpoint = authData.authentication_endpoint
        })
        .catch(defaultErrorHandler)
    },
    async callback (code, state) {
      session.get('/callback/', { params: { code, state } })
        .then((response) => response.data)
        .then((user) => {
          this.user = user
          // use window location instead of this.router.push
          // because discord returns to this url with the parameters
          // *before* the #, which looks weird.
          // Since the router ignores everything before the #, this is the
          // easiest way to clean up the URL
          window.location = '/'
        })
        .catch(defaultErrorHandler)
    },
    setUser: function (user) {
      this.user = {
        name: user.name,
        avatarUrl: user.avatar_url,
        isAdmin: user.is_admin,
        isDev: user.is_dev,
        role: user.role
      }
    },
    async fetchUser () {
      console.log('auth.js#fetchUser: sending get')
      return session.get('/')
        .then((response) => response.data)
        .then((user) => this.setUser(user))
        .catch(defaultErrorHandler)
    },
    async setAdminMode (admin) {
      session.post('/', { admin })
        .then((response) => response.data)
        .then((user) => this.setUser(user))
        .catch(defaultErrorHandler)
    },
    logout () {
      session.delete('/')
        .then(() => {
          this.user = null
          this.router.push('/account/login')
        })
        .catch(defaultErrorHandler)
    }
  }
})
