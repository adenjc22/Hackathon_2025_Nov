import { createContext, useContext, useEffect, useState } from "react";
import { api } from "../utils/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);

  // Try restore session on mount
  useEffect(() => {
    (async () => {
      try {
        const { data } = await api.get("/api/users/me"); // implement on backend
        setUser(data);
      } catch (_) {} // not logged in
      setReady(true);
    })();
  }, []);

  const login = async (payload) => {
    const { data } = await api.post("/api/auth/login", payload);
    setUser(data.user);
    return data.user;
  };

  const signup = async (payload) => {
    const { data } = await api.post("/api/auth/signup", payload);
    setUser(data.user);
    return data.user;
  };

  const logout = async () => {
    try { await api.post("/api/auth/logout"); } catch (_) {}
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, ready, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuthCtx = () => useContext(AuthContext);
