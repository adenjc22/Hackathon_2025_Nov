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
    const formData = new FormData();
    formData.append("email", payload.email);
    formData.append("password", payload.password);
    
    const { data } = await api.post("/api/auth/login", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    
    // Store token and set in axios headers
    localStorage.setItem("accessToken", data.accessToken);
    api.defaults.headers.common["Authorization"] = `Bearer ${data.accessToken}`;
    
    setUser(data.user);
    return data.user;
  };

  const signup = async (payload) => {
    const formData = new FormData();
    formData.append("email", payload.email);
    formData.append("password", payload.password);
    
    const { data } = await api.post("/api/auth/register", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    
    // Store token and set in axios headers
    localStorage.setItem("accessToken", data.accessToken);
    api.defaults.headers.common["Authorization"] = `Bearer ${data.accessToken}`;
    
    setUser(data.user);
    return data.user;
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
