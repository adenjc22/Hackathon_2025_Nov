// src/utils/api.js
import axios from "axios";

const USE_MSW = import.meta.env.VITE_USE_MSW === "true";
const API_BASE = USE_MSW ? "" : (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000");

export const api = axios.create({
  baseURL: API_BASE,
  withCredentials: !USE_MSW, // only send cookies to real backend
  timeout: 15_000,
});

// ---- optional: attach JWT if you use header-based auth
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token"); // or a zustand/store selector
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ---- error normalization (your existing one is good)
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const msg =
      err?.response?.data?.detail ||
      err?.response?.data?.message ||
      err.message ||
      "Request failed";
    console.error("[API ERROR]", msg);
    return Promise.reject(Object.assign(err, { friendlyMessage: msg }));
  }
);
// src/utils/api.js (continued)

// ---- Auth
export const AuthAPI = {
  register: (email, password) =>
    api.post("/api/auth/register", { email, password }).then(r => r.data),

  login: async (email, password) => {
    const data = await api.post("/api/auth/login", { email, password }).then(r => r.data);
    // If backend returns JWT, store it. If using cookies, skip this.
    if (data?.access_token) localStorage.setItem("token", data.access_token);
    return data;
  },

  me: () => api.get("/api/auth/me").then(r => r.data),

  logout: async () => {
    try { await api.post("/api/auth/logout"); } finally {
      localStorage.removeItem("token");
    }
  },
};

// ---- Users
export const UsersAPI = {
  list: (params) => api.get("/api/users", { params }).then(r => r.data),
  get: (id) => api.get(`/api/users/${id}`).then(r => r.data),
  create: (payload) => api.post("/api/users", payload).then(r => r.data),
  update: (id, payload) => api.put(`/api/users/${id}`, payload).then(r => r.data),
  remove: (id) => api.delete(`/api/users/${id}`).then(r => r.data),
};

// ---- File uploads (multipart)
export const UploadsAPI = {
  upload: (file, extra = {}) => {
    const form = new FormData();
    form.append("file", file); // field name must match your backend
    Object.entries(extra).forEach(([k, v]) => form.append(k, v));
    return api.post("/api/uploads", form, {
      headers: { "Content-Type": "multipart/form-data" },
    }).then(r => r.data);
  },
};

// ---- Pagination helper (cursor/page)
export function buildPageParams({ page = 1, pageSize = 20, q, sort } = {}) {
  const params = { page, page_size: pageSize };
  if (q) params.q = q;
  if (sort) params.sort = sort; // e.g. "created_at:desc"
  return params;
}
