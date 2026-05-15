import api from "@/api/axios"

export const getChildren = () => {
  return api.get("/children/")
}

export const createChild = (data) => {
  return api.post("/children/", data)
}

/* ACCEPT INVITE */
export const acceptInvite = (data) => {
  return api.post(
    "/children/accept-invite/",
    data
  )
}