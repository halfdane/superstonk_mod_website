<template>
  <q-btn round v-if="user">
    <q-avatar size="40px" color="white" text-color="black">
      <img :src="user.avatarUrl" :alt="'avatar of ' + user.name">
    </q-avatar>

    <q-menu>
      <div class="row no-wrap q-pa-md">
        <div class="column">
          <div class="text-h6 q-mb-md">Settings</div>
          <q-toggle v-model="darkMode"
                    unchecked-icon="dark_mode"
                    checked-icon="light_mode"
                    @click="toggleDarkMode"
                    :label="'Switch to ' + (darkMode?'light':'dark') + ' mode'"/>
          <q-toggle v-if="user.isDev"
                    v-model="user.isAdmin"
                    @click="toggleAdminMode"
                    :label="'Switch to ' + (user.isAdmin?'user':'admin') + ' mode'"/>
        </div>

        <q-separator vertical inset class="q-mx-lg"/>

        <div class="column items-center">
          <q-avatar size="72px">
            <img :src="user.avatarUrl" :alt="'avatar of ' + user.name">
          </q-avatar>

          <div class="text-h6 q-mt-md q-mb-xs">{{ user.name }}</div>
          <div class="text-body1 q-mt-md q-mb-xs">Superstonk {{ user.role }} Moderator</div>
          <div class="text-caption q-mt-md q-mb-xs">
            <span v-if="user.isAdmin">Admin</span>
            <span v-if="user.isDev">Dev</span>
          </div>

          <q-btn
            color="primary"
            label="Logout"
            push
            size="sm"
            @click="logout"
          />
        </div>
      </div>
    </q-menu>
  </q-btn>
</template>

<script>
import { useQuasar } from 'quasar'
import { storeToRefs } from 'pinia/dist/pinia'
import { useAuthStore } from 'stores/auth'

export default {
  data () {
    return {
      darkMode: false
    }
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    const { rememberUser, forgetUser } = authStore

    const $q = useQuasar()
    $q.dark.set($q.cookies.get('darkmode') === 'true')

    return {
      authStore,
      user,
      rememberUser,
      forgetUser
    }
  },
  created () {
    this.darkMode = this.$q.dark.isActive
  },
  methods: {
    toggleAdminMode () {
      this.authStore.setAdminMode(this.user.isAdmin)
    },
    toggleDarkMode () {
      this.$q.dark.toggle()
      this.$q.cookies.set('darkmode', this.$q.dark.isActive)
    },
    logout () {
      this.authStore.logout()
    }
  }
}
</script>
