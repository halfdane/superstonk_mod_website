<template>
  <q-layout view="hHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
        />

        <q-toolbar-title>
          <q-avatar size="100px" font-size="52px" text-color="white" icon="policy"/>
          Superstonk Mod Website
        </q-toolbar-title>

      </q-toolbar>
    </q-header>

    <q-page-container>
      <div class="row justify-center q-pa-lg">
        <router-view/>
      </div>
    </q-page-container>
  </q-layout>
</template>

<script>
import { useAuthStore } from 'stores/auth'
import router from 'src/router'

export default {
  setup () {
    const authStore = useAuthStore()
    if (authStore.user) {
      router.push('/')
    }
  }
}
</script>
