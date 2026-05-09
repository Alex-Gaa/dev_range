//C:\Users\Developer\PycharmProjects\devrange\frontend\src\stores\lessons.js
import { defineStore } from "pinia"
import { getLessons, createLesson } from "@/api/lessons"

export const useLessonsStore = defineStore("lessons", {
  state: () => ({
    lessons: [],
    loading: false,
  }),

  getters: {
    completedCount: (state) =>
      state.lessons.filter(l => l.status === "completed").length,
  },

  actions: {
    // 📚 ВСЕ уроки
    async fetchAllLessons() {
      this.loading = true

      try {
        const res = await getLessons()
        this.lessons = res.data
      } finally {
        this.loading = false
      }
    },

    // 📚 уроки конкретного ребенка
    async fetchLessons(childId) {
      this.loading = true

      try {
        const res = await getLessons({
          child: childId,
        })

        this.lessons = res.data
      } finally {
        this.loading = false
      }
    },

    // ➕ создать урок
    async addLesson(childId, data) {
      const res = await createLesson({
        child: childId,
        ...data,
      })

      this.lessons.unshift(res.data)
    },
  },
})