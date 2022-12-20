<script>
import { useAuthStore } from 'stores/auth'

export default {
  setup () {
    const authStore = useAuthStore()
    const queryString = window.location.search
    const params = new URLSearchParams(queryString)
    const code = params.get('code')
    const state = params.get('state')
    return {
      code,
      state,
      authStore
    }
  },
  mounted () {
    this.authStore.callback(this.code, this.state)
  },
  unmounted () {
    window.location.search = ''
  }
}
</script>

<template>
  <div class='card m-3'>
    <h4 class='card-header'>Login</h4>
    <div class='card-body'>
      <span>Henlo, I'm back: {{ this.authStore.user }}</span>
      <span>Code: {{ this.code }}</span>
      <span>State: {{ this.state }}</span>
    </div>
  </div>
</template>
