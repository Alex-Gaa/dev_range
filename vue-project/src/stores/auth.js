//C:\Users\Developer\PycharmProjects\devrange\vue-project\src\stores\auth.js
import { defineStore } from "pinia";
import api from "../api/axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    access: localStorage.getItem("access") || null,
    refresh: localStorage.getItem("refresh") || null,
  }),

  getters: {
    isAuth: (state) => !!state.access,
    fullName: (state) =>
      state.user ? `${state.user.first_name} ${state.user.last_name}` : "",
  },

  actions: {
    async login(username, password) {
      const res = await api.post("api/auth/login/", {
        username,
        password,
      });

      this.access = res.data.access;
      this.refresh = res.data.refresh;

      localStorage.setItem("access", this.access);
      localStorage.setItem("refresh", this.refresh);

      await this.fetchUser();
    },

    async register(data) {
      await api.post("/api/auth/register/", data);

      return this.login(data.email, data.password);
    },

    async fetchUser() {
      if (!this.access) return;

      const res = await api.get("api/auth/me/", {
        headers: {
          Authorization: `Bearer ${this.access}`,
        },
      });

      this.user = res.data;
    },

    logout() {
      this.user = null;
      this.access = null;
      this.refresh = null;

      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
    },
  },
});