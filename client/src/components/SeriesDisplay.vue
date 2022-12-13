<template>
  <q-list bordered>
    <q-item v-for="item in series" :key="item.name" clickable v-ripple>

      <q-item-section>
        <q-item-label>{{ item.meta }}</q-item-label>
        <q-item-label>{{ item.series }}</q-item-label>
      </q-item-section>
    </q-item>

  </q-list>
</template>

<script>

export default {
  data() {
    return {
      series: []
    }
  },
  mounted() {
    const connection = new WebSocket('ws://localhost:5000/mod_activity');
    connection.onmessage = (event) => {
      this.series = JSON.parse(event.data);
    };
    connection.onerror = (error) => {
      console.error('There was an un-identified Web Socket error', error);
    };
  },
}
</script>
