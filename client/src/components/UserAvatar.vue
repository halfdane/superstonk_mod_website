<template>
  <q-avatar color="white" text-color="black" v-if="loading" class="loading">M</q-avatar>

  <q-btn round>
    <q-avatar v-if="user" size="40px" color="white" text-color="black">
      <img :src="user.avatar_url" :alt="'avatar of ' + user.name">
    </q-avatar>

    <q-menu>
      <div class="row no-wrap q-pa-md">
        <div class="column">
          <div class="text-h6 q-mb-md">Settings</div>
          <q-toggle v-model="darkMode"
                    checked-icon="dark_mode"
                    unchecked-icon="light_mode"
                    @click="toggleDarkMode"/>
        </div>

        <q-separator vertical inset class="q-mx-lg"/>

        <div class="column items-center">
          <q-avatar size="72px">
            <img :src="user.avatar_url" :alt="'avatar of ' + user.name">
          </q-avatar>

          <div class="text-subtitle1 q-mt-md q-mb-xs">{{ user.name }}</div>

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
import axios from 'axios';
import { useQuasar } from 'quasar';

export default {
  data() {
    return {
      darkMode: false,
      loading: false,
      user: null
    }
  },
  setup () {
    const $q = useQuasar();
    $q.dark.set($q.cookies.get('darkmode') === 'true' );
  },
  created() {
    this.fetchData();
    this.darkMode = this.$q.dark.isActive;
  },
  methods: {
    fetchData() {
      this.user = null
      this.loading = true
      const path = 'http://localhost:5000/session/';
      axios.get(path, {withCredentials: true})
        .then((response) => response.data)
        .then((data) => {
          this.user = data
        })
        .then(() => {
          this.loading = false
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    },
    toggleDarkMode() {
      this.$q.dark.toggle();
      this.$q.cookies.set('darkmode', this.$q.dark.isActive);
    },
    logout() {
      const path = 'http://localhost:5000/session/';
      axios.delete(path, {withCredentials: true})
        .then((response) => response.data)
        .then((data) => {
          this.user = data
        })
        .then(() => {
          this.loading = false
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })    }
  },
};
</script>
