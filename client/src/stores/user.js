import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: undefined
  }),
  getters: {
    isAdmin: (state) => state.user && state.user.isAdmin
  },
  actions: {

    forgetUser () {
      this.user = undefined
    }
  }
})
