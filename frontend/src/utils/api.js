import axios from "axios";

// Point this at your FastAPI base (dev env variable preferred)
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  withCredentials: true, // if backend sets httpOnly cookies
});

// Basic error surfacing
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const msg = err?.response?.data?.detail || err.message || "Request failed";
    console.error("[API ERROR]", msg);
    return Promise.reject(err);
  }
);
