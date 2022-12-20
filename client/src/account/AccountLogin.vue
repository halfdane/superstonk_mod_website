<script>
import { useAuthStore } from 'stores/auth'

export default {
  setup () {
    const authStore = useAuthStore()
    authStore.prepare()

    return {
      authStore
    }
  }
}
</script>

<template>
  <q-card>
    <q-card-section>
      <div class="text-h6">You aren't currently logged in</div>
    </q-card-section>

    <q-card-section>
      Authentication is handled by Discord, so to log in you have to allow this website to
      access your Discord user information.
    </q-card-section>

    <q-separator inset />

    <q-card-section>
      {{this.authStore.user}}
      <q-btn :href="authStore.authenticationEndpoint" color="primary" icon="discord" label="Log in with Discord"></q-btn>
    </q-card-section>
  </q-card>
</template>
