// src/utils/api.js
import axios from "axios";

const USE_MSW = import.meta.env.VITE_USE_MSW === "true";

export const api = axios.create({
  baseURL: USE_MSW ? "" : (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"),
  withCredentials: USE_MSW ? false : true, // cookies only needed when hitting real backend
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const msg = err?.response?.data?.detail || err.message || "Request failed";
    console.error("[API ERROR]", msg);
    return Promise.reject(err);
  }
);
