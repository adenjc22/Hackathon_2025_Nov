// src/utils/api.js
import axios from "axios";

const USE_MSW = import.meta.env.VITE_USE_MSW === "true";

// Normalize and determine API URL based on environment
const normalizeUrlForPage = (url) => {
  if (!url) return url;
  try {
    // If page is served over HTTPS, upgrade any http:// API url to https://
    if (typeof location !== "undefined" && location.protocol === "https:") {
      if (url.startsWith("http://")) {
        return url.replace(/^http:\/\//i, "https://");
      }
    }
  } catch (e) {
    // location may be undefined in some build-time contexts; ignore
  }
  return url;
};

const getApiUrl = () => {
  if (USE_MSW) return "";

  // If VITE_API_URL is set, use it (but normalize to avoid mixed-content)
  if (import.meta.env.VITE_API_URL) {
    return normalizeUrlForPage(import.meta.env.VITE_API_URL);
  }

  // In production (Railway), use the production backend (HTTPS)
  if (import.meta.env.PROD) {
    return "https://memory-lane-backend.up.railway.app";
  }

  // In development, use localhost (HTTP)
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

// ============================================
// Albums API Functions
// ============================================

/**
 * Get all albums for current user
 * @param {Object} options - Query options
 * @returns {Promise<Array>} List of albums
 */
export async function getAlbums(options = {}) {
  const params = new URLSearchParams();
  
  if (options.autoOnly !== undefined) {
    params.append("auto_only", options.autoOnly);
  }
  if (options.limit) {
    params.append("limit", options.limit);
  }
  if (options.offset) {
    params.append("offset", options.offset);
  }

  const response = await api.get(`/api/albums?${params.toString()}`);
  return response.data;
}

/**
 * Get a single album by ID
 * @param {number} albumId - Album ID
 * @returns {Promise<Object>} Album details
 */
export async function getAlbum(albumId) {
  const response = await api.get(`/api/albums/${albumId}`);
  return response.data;
}

/**
 * Create a new album
 * @param {Object} albumData - Album data
 * @returns {Promise<Object>} Created album
 */
export async function createAlbum(albumData) {
  const response = await api.post("/api/albums", albumData);
  return response.data;
}

/**
 * Create an album from a natural language prompt
 * @param {Object} promptData - { prompt: string, title?: string }
 * @returns {Promise<Object>} Created album with matched photos
 */
export async function createAlbumFromPrompt(promptData) {
  const response = await api.post("/api/albums/create-from-prompt", promptData);
  return response.data;
}

/**
 * Update an existing album
 * @param {number} albumId - Album ID
 * @param {Object} albumData - Updated album data
 * @returns {Promise<Object>} Updated album
 */
export async function updateAlbum(albumId, albumData) {
  const response = await api.put(`/api/albums/${albumId}`, albumData);
  return response.data;
}

/**
 * Delete an album
 * @param {number} albumId - Album ID
 * @returns {Promise<Object>} Deletion result
 */
export async function deleteAlbum(albumId) {
  const response = await api.delete(`/api/albums/${albumId}`);
  return response.data;
}

/**
 * Get album suggestions for a media item
 * @param {number} mediaId - Media ID
 * @returns {Promise<Array>} Suggested albums
 */
export async function getAlbumSuggestions(mediaId) {
  const response = await api.get(`/api/albums/suggestions/${mediaId}`);
  return response.data;
}

/**
 * Regenerate album description
 * @param {number} albumId - Album ID
 * @returns {Promise<Object>} Updated album
 */
export async function regenerateAlbumDescription(albumId) {
  const response = await api.post(`/api/albums/${albumId}/regenerate-description`);
  return response.data;
}

/**
 * Rebuild all albums
 * @param {boolean} force - Force rebuild even if albums exist
 * @returns {Promise<Object>} Rebuild results
 */
export async function rebuildAlbums(force = false) {
  const params = new URLSearchParams();
  if (force) {
    params.append("force", "true");
  }
  
  const response = await api.post(`/api/albums/rebuild?${params.toString()}`);
  return response.data;
}

/**
 * Add photos to an existing album
 * @param {number} albumId - Album ID
 * @param {Array<number>} mediaIds - List of media IDs to add
 * @returns {Promise<Object>} Result
 */
export async function addPhotosToAlbum(albumId, mediaIds) {
  const response = await api.post(`/api/albums/${albumId}/add-photos`, {
    media_ids: mediaIds
  });
  return response.data;
}

/**
 * Get all media for the current user
 * @returns {Promise<Array>} List of media items
 */
export async function getAllMedia() {
  const response = await api.get("/api/upload/media");
  return response.data;
}
