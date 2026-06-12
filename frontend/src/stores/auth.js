//C:\Users\Developer\PycharmProjects\devrange\frontend\src\stores\auth.js
import { defineStore } from "pinia";

import {
  loginUser,
  registerUser,
  getMe,
} from "@/api/auth";
import api from "@/api/axios"; // 🔥 ДОБАВЬ ЭТОТ ИМПОРТ
export const useAuthStore = defineStore("auth", {

  state: () => ({
    user: null,

    access: localStorage.getItem("access") || null,
    refresh: localStorage.getItem("refresh") || null,

    loading: false,
    initialized: false,
  }),

  getters: {

    isReady: (state) => state.initialized,

    isAuthenticated: (state) => !!state.access,

    role: (state) => state.user?.role || null,

    fullName: (state) => {

      if (!state.user) return ""

      return `${state.user.first_name} ${state.user.last_name}`
    },
  },

  actions: {

    async register(data) {

      this.loading = true

      try {

        await registerUser(data)

      } finally {

        this.loading = false
      }
    },

    async login(data) {

      this.loading = true

      try {

        const response = await loginUser(data)

        this.access = response.data.access
        this.refresh = response.data.refresh

        localStorage.setItem("access", this.access)
        localStorage.setItem("refresh", this.refresh)

        this.user = response.data.user

      } finally {

        this.loading = false
      }
    },

    async fetchMe() {

      if (!this.access) {
        this.initialized = true
        return
      }

      try {

        const response = await getMe()

        this.user = response.data

      } catch (e) {

        this.logout()

      } finally {

        this.initialized = true
      }
    },

    async verifyEmail(email, code) {

      const response = await api.post(
        "/auth/verify-email/",
        {
          email,
          code,
        }
      )

      this.access = response.data.access
      this.refresh = response.data.refresh

      localStorage.setItem(
        "access",
        response.data.access
      )

      localStorage.setItem(
        "refresh",
        response.data.refresh
      )

      this.user = response.data.user

      return response
    },

    logout() {

      this.user = null

      this.access = null
      this.refresh = null

      this.initialized = true

      localStorage.removeItem("access")
      localStorage.removeItem("refresh")
    },
  },
})