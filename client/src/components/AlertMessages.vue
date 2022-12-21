<template>
  <q-banner v-if="alert" inline-actions rounded class="bg-orange text-white">
    {{ alert.message }}
    <template v-slot:action>
      <q-btn flat label="Dismiss" @click="alertStore.clear()"/>
    </template>
  </q-banner>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useAlertStore } from 'stores/alert.store'

const alertStore = useAlertStore()
const { alert } = storeToRefs(alertStore)
</script>
