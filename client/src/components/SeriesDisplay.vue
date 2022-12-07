<template>
  {{ series }}
</template>

<script>

export default {
  data() {
    return {
      series: null,
    };
  },
  mounted() {
    const connection = new WebSocket('ws://localhost:5000/mod_activity');
    connection.onmessage = (event) => {
      this.series = event.data;
    };
    connection.onerror = (error) => {
      console.error('There was an un-identified Web Socket error', error);
    };
  },
};

</script>
