<template>
  <vue-echarts :option='option' loading="true" style='height: 80vh; width: 100%' ref='chart' @selectchanged="mouseover"/>
</template>

<script>
import {VueEcharts} from 'vue3-echarts';

export default {
  components: {
    VueEcharts,
  },
  data() {
    return {
      graph: [],
    }
  },
  computed: {
    option() {
      return {
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
      };
    }
  },
  methods: {
    mouseover(a, b, c) {
      console.log(a, b, c)
    }
  },
  mounted() {
    const connection = new WebSocket('ws://localhost:5000/mod_activity_egraph');
    connection.onmessage = (event) => {
      const result = JSON.parse(event.data);
      this.graph = result.map(series =>
        Object.assign({}, {type: 'line', stack: 'Total', smooth: true, symbol: 'none', areaStyle: {}}, series))
    };
    connection.onerror = (error) => {
      console.error('There was an un-identified Web Socket error', error);
    };
    this.$refs.chart.chart.on('click', function(params) {
      // Print name in console
      console.log(params.name);
    });
    console.log(this.$refs.chart.chart)
  },
}
</script>
