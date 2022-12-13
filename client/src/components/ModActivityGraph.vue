<style scoped>
:deep(.highlight){
  border: 2px solid grey;
}
:deep(.highlight) b{
  font-weight: bold;
}
:deep(b) {
  font-weight: normal;
}
</style>


<script>
import Dygraphs from 'dygraphs';
import {h} from 'vue';

export default {
  render() {
    return [
      h('div', {id: 'vue-dygraphs' + this.randomId, style: this.graphStyle}),
      h('div', {id: 'vue-dygraphs-labels' + this.randomId}),
    ]
  },
  data() {
    return {
      graph: null,
      graphData: [],
      labels: [],
      randomId: Math.floor(Math.random() * 6) + 1,
      waitingForUpdate: false,
    }
  },
  props: {
    graphOptions: {stackedGraph: true},
    graphStyle: {
      type: Object,
      default() {
        return {
          width: '100%',
          height: '500px',
        }
      },
    },
  },
  mounted() {
    const connection = new WebSocket('ws://localhost:5000/mod_activity');
    connection.onmessage = (event) => {
      const result = JSON.parse(event.data);
      result.series.forEach(day_array => day_array[0] = new Date(day_array[0]))

      this.graphData = result.series
      this.labels = result.meta.labels;
      this.renderGraph();
    };
    connection.onerror = (error) => {
      console.error('There was an un-identified Web Socket error', error);
    };
  },
  methods: {
    renderGraph() {
      const now = new Date();
      const lastWeek = new Date(now.getFullYear(), now.getMonth() - 1, now.getDate());

      this.$data.graph = new Dygraphs(
        'vue-dygraphs' + this.randomId,
        this.graphData,
        {
          width: 480,
          height: 320,
          labels: this.labels,
          stackedGraph: true,

          highlightCircleSize: 2,
          strokeWidth: 1,
          strokeBorderWidth: null,

          showRangeSelector: true,
          dateWindow: [lastWeek, now],

          labelsDiv: 'vue-dygraphs-labels' + this.randomId,

          highlightSeriesOpts: {
            strokeWidth: 3,
            strokeBorderWidth: 1,
            highlightCircleSize: 5
          }
        });
      var onclick = () => {
        if (this.$data.graph.isSeriesLocked()) {
          this.$data.graph.clearSelection();
        } else {
          this.$data.graph.setSelection(this.$data.graph.getSelection(), this.$data.graph.getHighlightSeries(), true);
        }
      };
      this.$data.graph.updateOptions({clickCallback: onclick}, true);
      this.$data.graph.setSelection(false, 's005');


    },
    updateGraph() {
      // Merge data and options
      let obj = Object.assign({}, this.graphOptions, {file: this.graphData})
      this.$data.graph.updateOptions(obj)
    },
  },
}
</script>
