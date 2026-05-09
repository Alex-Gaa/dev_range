// src/stores/lessons.js
import { defineStore } from "pinia"
import {
  getLessons,
  getLesson,
  createLesson,
  updateLesson,
  deleteLesson,
} from "@/api/lessons"

export const useLessonsStore = defineStore("lessons", {
  state: () => ({
    lessons: [],
    currentLesson: null,
    loading: false,
  }),

  getters: {
    completedCount: (state) =>
      state.lessons.filter(l => l.status === "completed").length,
  },

  actions: {

    /* ALL LESSONS */
    async fetchAllLessons() {
      this.loading = true
      try {
        const res = await getLessons()
        this.lessons = res.data
      } finally {
        this.loading = false
      }
    },

    /* CHILD LESSONS */
    async fetchLessons(childId) {
      this.loading = true
      try {
        const res = await getLessons({ child: childId })
        this.lessons = res.data
      } finally {
        this.loading = false
      }
    },

    /* ONE LESSON */
    async fetchLesson(id) {
      const res = await getLesson(id)
      this.currentLesson = res.data
      return res.data
    },

    /* CREATE */
    async addLesson(childId, data) {
      const res = await createLesson({
        child: childId,
        ...data,
      })

      this.lessons.unshift(res.data)
      return res.data
    },

    /* UPDATE */
    async updateLesson(id, data) {
      const res = await updateLesson(id, data)

      this.lessons = this.lessons.map(l =>
        l.id === id ? res.data : l
      )

      if (this.currentLesson?.id === id) {
        this.currentLesson = res.data
      }

      return res.data
    },

    /* DELETE */
    async deleteLesson(id) {
      await deleteLesson(id)

      this.lessons = this.lessons.filter(l => l.id !== id)

      if (this.currentLesson?.id === id) {
        this.currentLesson = null
      }
    },
  },
})