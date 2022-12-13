<template>
  <q-page class="row items-center justify-evenly">
    <mod-activity-graph></mod-activity-graph>
    <series-display></series-display>
  </q-page>
</template>
<script>
import SeriesDisplay from '../components/SeriesDisplay';
import ModActivityGraph from '../components/ModActivityGraph';
export default {
  components: {SeriesDisplay, ModActivityGraph}
}
</script>
