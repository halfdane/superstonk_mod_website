<template>
  <vue-echarts
    :option="option"
    loading="true"
    style="height: 80vh; width: 100%"
    ref="chart"
  />
  <q-form class="q-gutter-md">
    <q-toggle v-model="accWeekly" label="Accumulate weekly/daily">
      <q-tooltip>Accumulate for every day or every week</q-tooltip>
    </q-toggle>
  </q-form>
  <q-form class="q-gutter-md">
    <q-toggle v-model="combineNonTeam" label="Combine non-team accounts">
      <q-tooltip
        >Non-team accounts: bots, reddit's anti-evil team etc.</q-tooltip
      >
    </q-toggle>
    <q-toggle
      v-model="combineFormerTeam"
      label="Combine accounts of former team members"
    >
      <q-tooltip>Humans that used to be bots but aren't anymore</q-tooltip>
    </q-toggle>
    <q-toggle
      v-model="combineCurrentTeam"
      label="Combine accounts of current team members"
    >
      <q-tooltip>Humans that are currently moderators</q-tooltip>
    </q-toggle>
  </q-form>
</template>

<script>
import { VueEcharts } from "vue3-echarts";
import { ref } from "vue";
import { useModactivityStore } from "./modactivity.store";
import { storeToRefs } from "pinia";

export default {
  components: {
    VueEcharts,
  },
  setup() {
    const combineNonTeam = ref(true);
    const combineFormerTeam = ref(true);
    const combineCurrentTeam = ref(true);
    const accWeekly = ref(true);

    const modactivityStore = useModactivityStore();
    const { loading } = storeToRefs(modactivityStore);

    return {
      combineNonTeam,
      combineFormerTeam,
      combineCurrentTeam,
      accWeekly,
      modactivityStore,
      loading,
    };
  },
  data() {
    return {
      graph: null,
      defaultSeriesOptions: {
        type: "line",
        stack: "Total",
        smooth: 0.2,
        symbol: "none",
        areaStyle: {},
      },
    };
  },
  watch: {
    loading() {
      if (this.loading) {
        this.$refs.chart.chart.showLoading();
      } else {
        this.updateGraphData();
        this.$refs.chart.chart.hideLoading();
      }
    },
    combineNonTeam() {
      this.updateGraphData();
    },
    combineFormerTeam() {
      this.updateGraphData();
    },
    combineCurrentTeam() {
      this.updateGraphData();
    },
    accWeekly() {
      this.updateGraphData();
    }
  },
  methods: {
    updateGraphData() {
      if (this.loading) {
        return;
      }

      // day, mod, action, count
      // [ 1649894400000, "AutoModerator", "removecomment", 237 ]
      const source = this.modactivityStore.activities;

      const accumulatedActivity = source.reduce((acc, cur) => {
        let date = cur[0];

        if (this.accWeekly) {
          const now = new Date(date)
          var firstDayOfWeek = new Date(
            now.setDate(now.getDate() - now.getDay() + 1)
          );
          date = firstDayOfWeek.valueOf();
        }

        let mod = cur[1];

        if (this.combineFormerTeam) {
          acc["EX-MODS"] = acc["EX-MODS"] || {};
        }
        if (this.combineNonTeam) {
          acc["NON-TEAM"] = acc["NON-TEAM"] || {};
        }
        if (this.combineCurrentTeam) {
          acc["MODERATORS"] = acc["MODERATORS"] || {};
        }

        if (
          this.combineFormerTeam &&
          !this.modactivityStore.moderators.includes(mod) &&
          !this.modactivityStore.nonTeam.includes(mod)
        ) {
          mod = "EX-MODS";
        } else if (
          this.combineNonTeam &&
          this.modactivityStore.nonTeam.includes(mod)
        ) {
          mod = "NON-TEAM";
        } else if (
          this.combineCurrentTeam &&
          this.modactivityStore.moderators.includes(mod)
        ) {
          mod = "MODERATORS";
        }
        acc[mod] = acc[mod] || {};
        acc[mod][date] = acc[mod][date] || 0;
        acc[mod][date] += cur[3];
        return acc;
      }, []);
      // [half_dane: {
      //     "1649894400000": 84,
      //     "1650499200000": 234,
      // }]

      const series = [];
      Object.keys(accumulatedActivity).forEach((name) => {
        const data = [];
        Object.keys(accumulatedActivity[name]).forEach((day) => {
          data.push([parseInt(day), accumulatedActivity[name][day]]);
        });

        series.push(
          Object.assign({}, this.defaultSeriesOptions, { name, data })
        );
      });

      // [{
      //     name: 'mod name ',
      //     data: [[day, total], [day, total], [day, total]]
      // }]
      this.graph = series;
    },
  },
  mounted() {
    this.modactivityStore.fetchData();
  },
  computed: {
    option() {
      if (this.graph) {
        return {
          darkMode: true,
          legend: {
            orient: "vertical",
            right: 10,
            top: "center",
            type: "scroll",
            icon: "rect",
          },
          tooltip: {
            trigger: "axis",
            formatter: function (params) {
              const string =
                "<b>" +
                new Date(params[0].value[0]).toLocaleDateString() +
                "</b><br />" +
                params
                  .filter((param) => param.value[1] !== 0)
                  .map((param) => {
                    const s = `${param.marker} ${param.seriesName} ${param.value[1]}`;
                    return s;
                  })
                  .join("<br />");
              return string;
            },
            position: function (pt) {
              return [pt[0], "0%"];
            },
          },
          title: {
            left: "center",
            text: "Mod Activity",
          },
          toolbox: {
            feature: {
              dataZoom: {
                yAxisIndex: "none",
              },
              restore: {},
              saveAsImage: {},
            },
          },
          xAxis: {
            type: "time",
            boundaryGap: false,
          },
          yAxis: {
            type: "value",
            boundaryGap: false,
          },
          dataZoom: [
            {
              xAxisIndex: [0],
              type: "slider",
              start: 80,
              end: 100,
              moveHandleSize: 20,
            },
          ],
          series: this.graph,
        };
      } else {
        return null;
      }
    },
  },
};
</script>
