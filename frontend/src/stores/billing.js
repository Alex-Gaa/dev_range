import { defineStore } from "pinia"
import api from "@/api/axios"

export const useBillingStore = defineStore(
  "billing",
  {
    state: () => ({
      subscription: null,
      loading: false,
    }),

    actions: {

      async fetchSubscription() {

        const res = await api.get(
          "/billing/subscription/"
        )

        this.subscription = res.data
      },

      async activate(plan = "basic") {

        const res = await api.post(
          "/billing/activate/",
          { plan }
        )

        this.subscription = res.data
      },
    },
  }
)