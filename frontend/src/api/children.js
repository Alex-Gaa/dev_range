import api from "@/api/axios"

export const getChildren = () => {
  return api.get("/children/")
}

export const createChild = (data) => {
  return api.post("/children/", data)
}