import { createContext, useContext, useEffect, useState } from "react";
import { api } from "../utils/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);

  // Try restore session on mount
  useEffect(() => {
    (async () => {
      const token = localStorage.getItem("accessToken");
      if (token) {
        try {
          // Set token in axios headers
          api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
          const { data } = await api.get("/api/users/me");
          setUser(data);
        } catch (_) {
          // Token invalid or expired
          localStorage.removeItem("accessToken");
          delete api.defaults.headers.common["Authorization"];
        }
      }
      setReady(true);
    })();
  }, []);

  const login = async (payload) => {
    try {
      const formData = new FormData();
      formData.append("email", payload.email);
      formData.append("password", payload.password);
      
      const { data } = await api.post("/api/auth/login", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      
      // Handle different response formats
      const token = data.access_token || data.accessToken;
      const userData = data.user || data;
      
      if (!token) {
        throw new Error("No access token received from server");
      }
      
      // Store token and set in axios headers
      localStorage.setItem("accessToken", token);
      api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      
      setUser(userData);
      return userData;
    } catch (error) {
      // Ensure errors are properly thrown
      console.error("Login error:", error);
      throw error;
    }
  };

  const signup = async (payload) => {
    try {
      const formData = new FormData();
      formData.append("email", payload.email);
      formData.append("password", payload.password);
      
      const { data } = await api.post("/api/auth/register", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      
      // Handle different response formats
      const token = data.access_token || data.accessToken;
      const userData = data.user || data;
      
      if (!token) {
        throw new Error("No access token received from server");
      }
      
      // Store token and set in axios headers
      localStorage.setItem("accessToken", token);
      api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      
      setUser(userData);
      return userData;
    } catch (error) {
      // Ensure errors are properly thrown
      console.error("Signup error:", error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await api.post("/api/auth/logout");
    } catch (_) {}
    
    // Clear token from storage and axios headers
    localStorage.removeItem("accessToken");
    delete api.defaults.headers.common["Authorization"];
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, ready, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuthCtx = () => useContext(AuthContext);
