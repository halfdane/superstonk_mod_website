<template>
  {{ number }}
</template>

<script>

export default {
  data() {
    return {
      number: 0,
    };
  },
  mounted() {
    console.log('connecting to websocket');
    const connection = new WebSocket('ws://localhost:5000/random');
    console.log('connected to websocket');
    connection.onmessage = (event) => {
      // Vue data binding means you don't need any extra work to
      // update your UI. Just set the `time` and Vue will automatically
      // update the `<h2>`.
      this.number = event.data;
    };
  },
};

</script>
