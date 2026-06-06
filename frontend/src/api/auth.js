//C:\Users\Developer\PycharmProjects\devrange\frontend\src\api\auth.js
import api from "./axios";

export const registerUser = async (data) => {
  return await api.post("/auth/register/", data);
};

export const loginUser = async (data) => {
  return await api.post("/auth/login/", data);
};

export const getMe = async () => {
  return await api.get("/auth/me/");
};

export const updateProfile = async (data) => {
  return await api.patch("/auth/profile/", data);
};