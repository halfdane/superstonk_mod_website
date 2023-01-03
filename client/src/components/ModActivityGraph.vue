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
import { VueEcharts } from 'vue3-echarts'
import { ref } from 'vue'

export default {
  components: {
    VueEcharts
  },
  setup () {
    const combineNonTeam = ref(true)
    const combineFormerTeam = ref(true)
    const combineCurrentTeam = ref(true)

    return {
      combineNonTeam,
      combineFormerTeam,
      combineCurrentTeam
    }
  },
  data () {
    return {
      graph: null
    }
  },
  watch: {
    combineNonTeam () {
      this.getData()
    },
    combineFormerTeam () {
      this.getData()
    },
    combineCurrentTeam () {
      this.getData()
    }
  },
  methods: {
    getData () {
      this.$refs.chart.chart.showLoading()
      const defaultSeriesOptions = { type: 'line', stack: 'Total', smooth: false, symbol: 'none', areaStyle: {} }
      this.$api.get('/mod_activity')
        .then((response) => response.data)
        .then((data) => {
          console.log(data)
          const moderators = data.moderators
          const nonTeam = data.nonTeam
          const dataset = data.dataset
          const source = dataset.source
          // day, mod, action, count
          // [ 1649894400000, "AutoModerator", "removecomment", 237 ]

          const accumulatedActivity = source.reduce((acc, cur) => {
            let mod = cur[1]
            if (this.combineFormerTeam && (!moderators.includes(mod)) && (!nonTeam.includes(mod))) {
              mod = 'EX-MODS'
            } else if (this.combineNonTeam && nonTeam.includes(mod)) {
              mod = 'NON-TEAM'
            } else if (this.combineCurrentTeam) {
              mod = 'MODERATORS'
            }
            acc[mod] = acc[mod] || {}
            acc[mod][cur[0]] = acc[mod][cur[0]] || 0
            acc[mod][cur[0]] += cur[3]
            return acc
          }, [])
          // [half_dane: {
          //     "1649894400000": 84,
          //     "1650499200000": 234,
          // }]
          const series = []
          Object.keys(accumulatedActivity).forEach((name) => {
            data = []
            Object.keys(accumulatedActivity[name]).forEach((day) => {
              data.push([parseInt(day), accumulatedActivity[name][day]])
            })

            series.push(Object.assign({}, defaultSeriesOptions, { name, data }))
          })

          // [{
          //     name: 'mod name ',
          //     data: [[day, total], [day, total], [day, total]]
          // }]

          this.graph = series.map(singleModSeries => Object.assign({}, defaultSeriesOptions, singleModSeries))
          console.log(this.graph)
          this.$refs.chart.chart.hideLoading()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    }
  },
  mounted () {
    this.getData()
  },
  computed: {
    option () {
      if (this.graph) {
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
              const string = params
                .filter(param => param.value[1] !== 0)
                .map(param => `${param.marker} ${param.seriesName} ${param.value[1]}`)
                .join('<br />')
              return string
            },
            position: function (pt) {
              return [pt[0], '0%']
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
        return null
      }
    }
  }
}
</script>
