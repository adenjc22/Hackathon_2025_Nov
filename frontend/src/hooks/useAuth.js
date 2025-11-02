// src/hooks/useAuth.js
import { useCallback, useState } from "react";
import { register, login } from "../lib/api";

export function useAuth() {
  const [user, setUser] = useState(null);

  const signup = useCallback(async (form) => {
    // map your form to backend shape
    const { email, password } = form;
    const { data } = await register(email, password);
    // For now the API returns a message; set a minimal client state
    setUser({ email }); 
    return data;
  }, []);

  const signin = useCallback(async ({ email, password }) => {
    const { data } = await login(email, password);
    setUser({ email });
    return data;
  }, []);

  const signout = useCallback(() => setUser(null), []);

  return { user, signup, signin, signout };
}
