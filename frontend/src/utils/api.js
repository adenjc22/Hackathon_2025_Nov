// src/utils/api.js
import axios from "axios";

const USE_MSW = import.meta.env.VITE_USE_MSW === "true";

// Determine API URL based on environment
const getApiUrl = () => {
  if (USE_MSW) return "";
  
  // If VITE_API_URL is set, use it
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  
  // In production (Railway), use the production backend
  if (import.meta.env.PROD) {
    return "https://memory-lane-backend.up.railway.app";
  }
  
  // In development, use localhost
  return "http://localhost:8000";
};

const API_BASE = getApiUrl();

console.log("API_BASE URL (utils/api.js):", API_BASE); // Debug log

export const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
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
