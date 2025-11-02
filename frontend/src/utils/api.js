// src/utils/api.js
import axios from "axios";

const USE_MSW = import.meta.env.VITE_USE_MSW === "true";

export const api = axios.create({
  baseURL: USE_MSW ? "" : (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"),
  withCredentials: false,  // Temporarily disabled for CORS debugging
});

// Add token from localStorage to requests automatically
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const msg = err?.response?.data?.detail || err.message || "Request failed";
    console.error("[API ERROR]", msg);
    
    // If 401, clear token
    if (err?.response?.status === 401) {
      localStorage.removeItem("accessToken");
      delete api.defaults.headers.common["Authorization"];
    }
    
    return Promise.reject(err);
  }
);
