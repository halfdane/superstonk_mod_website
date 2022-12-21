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
  }
}
</script>

<template>
  <div class='card m-3'>
    <h4 class='card-header'>Login successful</h4>
    <div class='card-body'>
      <span>
        You'll be redirected automatically. If that doesn't work, please click here:
        <q-btn href="/" color="primary" icon="discord" label="Back to the main page"></q-btn>
      </span>
    </div>
  </div>
</template>
