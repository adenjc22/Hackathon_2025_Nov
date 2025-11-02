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

// ============================================
// Search API Functions
// ============================================

/**
 * Search media with natural language query
 * @param {string} query - Search query
 * @param {Object} options - Search options
 * @returns {Promise<Object>} Search results
 */
export async function searchMedia(query, options = {}) {
  const params = new URLSearchParams({
    query: query.trim(),
    search_type: options.searchType || "hybrid",
    limit: options.limit || 20,
    offset: options.offset || 0,
  });

  // Add optional filters
  if (options.hasPeople !== undefined && options.hasPeople !== null) {
    params.append("has_people", options.hasPeople);
  }
  if (options.dateFrom) {
    params.append("date_from", options.dateFrom);
  }
  if (options.dateTo) {
    params.append("date_to", options.dateTo);
  }
  if (options.userId) {
    params.append("user_id", options.userId);
  }

  const response = await api.get(`/api/search?${params.toString()}`);
  return response.data;
}

/**
 * Get similar media based on a reference photo
 * @param {number} mediaId - Reference media ID
 * @param {Object} options - Options
 * @returns {Promise<Object>} Similar media results
 */
export async function getSimilarMedia(mediaId, options = {}) {
  const params = new URLSearchParams({
    limit: options.limit || 10,
  });

  if (options.userId) {
    params.append("user_id", options.userId);
  }

  const response = await api.get(`/api/search/similar/${mediaId}?${params.toString()}`);
  return response.data;
}

/**
 * Generate embedding for text
 * @param {string} text - Text to embed
 * @returns {Promise<Object>} Embedding data
 */
export async function generateEmbedding(text) {
  const response = await api.post("/api/embeddings", { text });
  return response.data;
}

/**
 * Reindex media embeddings
 * @param {Object} options - Reindex options
 * @returns {Promise<Object>} Reindex results
 */
export async function reindexMedia(options = {}) {
  const params = new URLSearchParams();
  
  if (options.userId) {
    params.append("user_id", options.userId);
  }
  if (options.force) {
    params.append("force", "true");
  }

  const response = await api.post(`/api/search/reindex?${params.toString()}`);
  return response.data;
}
