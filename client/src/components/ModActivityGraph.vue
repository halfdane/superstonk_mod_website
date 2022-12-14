<template>
  <vue-echarts :option='option' loading="true" style='height: 80vh; width: 100%' ref='chart'/>
  <q-form class="q-gutter-md">
    <q-toggle v-model="combineNonTeam" label="Combine non-team accounts">
      <q-tooltip>Non-team accounts: bots, reddit's anti-evil team etc.</q-tooltip>
    </q-toggle>
    <q-toggle v-model="combineFormerTeam" label="Combine accounts of former team members">
      <q-tooltip>Humans that used to be bots but aren't anymore</q-tooltip>
    </q-toggle>
    <q-toggle v-model="combineCurrentTeam" label="Combine accounts of current team members">
      <q-tooltip>Humans that are currently moderators</q-tooltip>
    </q-toggle>
  </q-form>
</template>

<script>
import {VueEcharts} from 'vue3-echarts';
import {ref} from 'vue';
import axios from 'axios';

export default {
  components: {
    VueEcharts,
  },
  setup() {
    const combineNonTeam = ref(true);
    const combineFormerTeam = ref(true);
    const combineCurrentTeam = ref(true);

    return {
      combineNonTeam,
      combineFormerTeam,
      combineCurrentTeam,
    }
  },
  data() {
    return {
      graph: null
    }
  },
  watch: {
    combineNonTeam() { this.getData(); },
    combineFormerTeam() { this.getData(); },
    combineCurrentTeam() { this.getData(); },
  },
  methods: {
    getData() {
      this.$refs.chart.chart.showLoading();
      const defaultSeriesOptions = {type: 'line', stack: 'Total', smooth: false, symbol: 'none', areaStyle: {}};
      const path = `http://localhost:5000/mod_activity?combineNonTeam=${this.combineNonTeam}&combineFormerTeam=${this.combineFormerTeam}&combineCurrentTeam=${this.combineCurrentTeam}`;
      axios.get(path, {withCredentials: true})
        .then((response) => response.data)
        .then((data) => {
          this.graph = data.map(singleModSeries => Object.assign({}, defaultSeriesOptions, singleModSeries))
          this.$refs.chart.chart.hideLoading();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    },
  },
  mounted() {
    this.getData();
  },
  computed: {
    option() {
      if (this.graph) {
        return  {
          darkMode: true,
          legend: {
            orient: 'vertical',
            right: 10,
            top: 'center',
            type: 'scroll',
            icon: 'rect'
          },
          tooltip: {
            trigger: 'axis',
            formatter: function (params) {
              let string = params
                .filter(param => param.value[1] !== 0)
                .map(param => `${param.marker} ${param.seriesName} ${param.value[1]}`)
                .join('<br />');
              return string;
            },
            position: function (pt) {
              return [pt[0], '0%'];
            }
          },
          title: {
            left: 'center',
            text: 'Mod Activity'
          },
          toolbox: {
            feature: {
              dataZoom: {
                yAxisIndex: 'none'
              },
              restore: {},
              saveAsImage: {}
            }
          },
          xAxis: {
            type: 'time',
            boundaryGap: false
          },
          yAxis: {
            type: 'value',
            boundaryGap: false
          },
          dataZoom: [
            {
              xAxisIndex: [0],
              type: 'slider',
              start: 80,
              end: 100,
              moveHandleSize: 20
            }
          ],
          series: this.graph
        }
      } else {
        return null;
      }
    }
  }
}
</script>
