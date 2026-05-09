//C:\Users\Developer\PycharmProjects\devrange\frontend\src\api\lessons.js
// src/api/lessons.js
import api from "@/api/axios"

/* GET LESSONS */
export const getLessons = (params = {}) => {
  return api.get("/lessons/", { params })
}

/* GET ONE LESSON */
export const getLesson = (id) => {
  return api.get(`/lessons/${id}/`)
}

/* CREATE */
export const createLesson = (data) => {
  return api.post("/lessons/", data)
}

/* UPDATE */
export const updateLesson = (id, data) => {
  return api.patch(`/lessons/${id}/`, data)
}

/* DELETE */
export const deleteLesson = (id) => {
  return api.delete(`/lessons/${id}/`)
}