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
    const connection = new WebSocket('ws://localhost:5000/random');
    connection.onmessage = (event) => {
      this.number = event.data;
    };
    connection.onerror = (error) => {
      console.error('There was an un-identified Web Socket error', error);
    };
  },
};

</script>
