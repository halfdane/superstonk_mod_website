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
          <q-toggle v-model="darkMode" label="Dark Mode" @click="toggleDarkMode"/>
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
            v-close-popup
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
      user: null,
      $q: useQuasar(),
    }
  },
  created() {
    // watch the params of the route to fetch the data again
    this.$watch(
      () => this.$route.params,
      () => {
        this.fetchData()
      },
      // fetch the data when the view is created and the data is
      // already being observed
      {immediate: true}
    )
  },
  methods: {
    fetchData() {
      this.user = null
      this.loading = true
      const path = 'http://localhost:5000/me/';
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
      this.darkMode = this.$q.dark.isActive
    }
  }
};
</script>
