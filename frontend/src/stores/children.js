//C:\Users\Developer\PycharmProjects\devrange\frontend\src\stores\children.js
import { defineStore } from "pinia"

import {
  getChildren,
  createChild,
} from "@/api/children"

export const useChildrenStore = defineStore("children", {

  state: () => ({
    children: [],
    loading: false,
  }),

  actions: {

    async fetchChildren() {

      this.loading = true

      try {

        const response = await getChildren()

        this.children = response.data

      } catch (e) {

        console.error("FETCH CHILDREN ERROR:", e)

      } finally {

        this.loading = false
      }
    },

    async addChild(data) {

      try {

        const response = await createChild(data)

        this.children.unshift(response.data)

        return response.data

      } catch (e) {

        console.error("CREATE CHILD ERROR:", e)

        throw e
      }
    },
  },
})