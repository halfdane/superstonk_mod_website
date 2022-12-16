<template>
  <q-banner v-if="show_banner" inline-actions rounded class="bg-orange text-white">
    {{ message }}
    <template v-slot:action>
      <q-btn flat label="Dismiss" @click="show_banner=false"/>
    </template>
  </q-banner>
</template>

<script>
export default {
  props: ['message'],
  data () {
    return {
      show_banner: this.message !== ''
    }
  }
}
</script>
