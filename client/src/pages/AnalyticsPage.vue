<template>
  <q-page class="row items-center justify-evenly">
    <mod-activity-graph ref="mod_activity_graph"></mod-activity-graph>
  </q-page>
</template>
<script>
import ModActivityGraph from '../components/ModActivityGraph'

export default {
  components: { ModActivityGraph }
}
</script>
