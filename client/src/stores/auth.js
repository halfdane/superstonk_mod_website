import { useAlertStore } from 'stores/alert.store.js'
import { defineStore } from 'pinia'

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
  actions: {
    async prepare () {
      this.$api.get('/session/authentication_endpoint/')
        .then((response) => response.data)
        .then((authData) => {
          this.authenticationEndpoint = authData.authentication_endpoint
        })
        .catch(defaultErrorHandler)
    },
    async callback (code, state) {
      this.$api.get('/session/callback/', { params: { code, state } })
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
      return this.$api.get('/session/')
        .then((response) => response.data)
        .then((user) => this.setUser(user))
        .catch(defaultErrorHandler)
    },
    async setAdminMode (admin) {
      this.$api.post('/session/', { admin })
        .then((response) => response.data)
        .then((user) => this.setUser(user))
        .catch(defaultErrorHandler)
    },
    logout () {
      this.$api.delete('/session/')
        .then(() => {
          this.user = null
          this.router.push('/account/login')
        })
        .catch(defaultErrorHandler)
    }
  }
})
