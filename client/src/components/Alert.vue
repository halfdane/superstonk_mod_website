<template>
  <div v-if="message !== ''">
    <div class="alert alert-success" role="alert">{{ message }}</div>
    <br>
  </div>
</template>

<script>
export default {
  props: ['message'],
};
</script>
