<template>
  <q-avatar color="white" text-color="black" v-if="loading" class="loading">M</q-avatar>

  <q-avatar v-if="user" color="white" text-color="black">
    <img :src="user.avatar_url" :alt="'avatar of ' + user.name">
  </q-avatar>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      loading: false,
      user: null,
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
      { immediate: true }
    )
  },
  methods: {
    fetchData() {
      this.user = null
      this.loading = true
      const path = 'http://localhost:5000/me/';
      axios.get(path, { withCredentials: true })
        .then((response) => response.data )
        .then((data) => { this.user = data })
        .then(() => { this.loading = false })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    },
  },
};
</script>
