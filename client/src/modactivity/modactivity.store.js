import { useAlertStore } from "stores/alert.store.js";
import { defineStore } from "pinia";

function defaultErrorHandler(error) {
  const alertStore = useAlertStore();
  alertStore.error(error);
}

export const useModactivityStore = defineStore({
  id: "modactivity",
  state: () => ({
    activities: null,
    moderators: null,
    nonTeam: null,
    loading: true,
  }),
  actions: {
    async fetchData() {
      this.loading = true;
      console.log("modactivity.store.js#fetchData: fetching data");
      const response = await this.$api.get("/mod_activity");
      const data = await response.data;

      this.moderators = data.moderators;
      this.nonTeam = data.nonTeam;
      this.activities = data.dataset.source;
      this.loading = false;
    },
  },
});
