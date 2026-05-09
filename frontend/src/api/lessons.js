//C:\Users\Developer\PycharmProjects\devrange\frontend\src\api\lessons.js
// src/api/lessons.js
import api from "@/api/axios"

export const getLessons = (params = {}) => {
  return api.get("/lessons/", {
    params,
  })
}

export const createLesson = (data) => {
  return api.post("/lessons/", data)
}