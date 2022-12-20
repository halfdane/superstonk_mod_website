import { router } from '../router/index'
import { useAlertStore } from 'stores/alert.store.js'
import axios from 'axios'
import { defineStore } from 'pinia'

const baseUrl = 'http://localhost:5000'

const session = axios.create({ baseURL: `${baseUrl}/session`, withCredentials: true })

function defaultErrorHandler (error) {
  const alertStore = useAlertStore()
  alertStore.error(error)
}

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')),
    returnUrl: null,
    authenticationEndpoint: null
  }),
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
          localStorage.setItem('user', JSON.stringify(user))
        })
        .then(() => {
          router.push(this.returnUrl || '/')
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
      session.get('/')
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
          localStorage.removeItem('user')
          router.push('/account/login')
        })
        .catch(defaultErrorHandler)
    }
  }
})
