// api/public.js

import axios from "axios"

export default axios.create({
  baseURL: "/api"
})