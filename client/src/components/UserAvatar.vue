<template>
  <q-avatar color="white" text-color="black" v-if="!user" class="loading">M</q-avatar>

  <q-btn round v-if="user">
    <q-avatar size="40px" color="white" text-color="black">
      <img :src="user.avatar_url" :alt="'avatar of ' + user.name">
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
          <q-toggle v-if="user.is_dev"
                    v-model="user.is_admin"
                    @click="toggleAdminMode"
                    :label="'Switch to ' + (user.is_admin?'user':'admin') + ' mode'"/>
        </div>

        <q-separator vertical inset class="q-mx-lg"/>

        <div class="column items-center">
          <q-avatar size="72px">
            <img :src="user.avatar_url" :alt="'avatar of ' + user.name">
          </q-avatar>

          <div class="text-h6 q-mt-md q-mb-xs">{{ user.name }}</div>
          <div class="text-body1 q-mt-md q-mb-xs">Superstonk {{ user.role }} Moderator</div>
          <div class="text-caption q-mt-md q-mb-xs">
            <span v-if="user.is_admin">Admin</span>
            <span v-if="user.is_dev">Dev</span>
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
import axios from 'axios'
import { useQuasar } from 'quasar'

export default {
  data () {
    return {
      darkMode: false,
      loading: false,
      user: null
    }
  },
  setup () {
    const $q = useQuasar()
    $q.dark.set($q.cookies.get('darkmode') === 'true')
  },
  created () {
    this.fetchData()
    this.darkMode = this.$q.dark.isActive
  },
  methods: {
    fetchData () {
      this.user = null
      this.loading = true
      const path = 'http://localhost:5000/session/'
      axios.get(path, { withCredentials: true })
        .then((response) => response.data)
        .then((data) => {
          this.user = data
        })
        .then(() => {
          this.loading = false
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    toggleAdminMode () {
      const path = 'http://localhost:5000/session/'
      axios.post(path, { admin: this.user.is_admin }, { withCredentials: true })
        .then((response) => response.data)
        .then((data) => {
          this.user = data
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    toggleDarkMode () {
      this.$q.dark.toggle()
      this.$q.cookies.set('darkmode', this.$q.dark.isActive)
    },
    logout () {
      const path = 'http://localhost:5000/session/'
      axios.delete(path, { withCredentials: true })
        .then((response) => response.data)
        .then((data) => {
          this.user = data
        })
        .then(() => {
          this.loading = false
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    }
  }
}
</script>
