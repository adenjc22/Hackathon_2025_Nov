import { useState } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Login() {
  const nav = useNavigate();
  const loc = useLocation();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
  const [err, setErr] = useState(""); const [busy, setBusy] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setBusy(true); setErr("");
    try {
      await login(form);
      nav(loc.state?.from?.pathname || "/dashboard", { replace: true });
    } catch (e2) {
      setErr(e2?.response?.data?.detail || e2.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-sm p-6">
      <h1 className="text-2xl font-semibold mb-4">Log in</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input className="w-full border rounded-xl px-3 py-2" placeholder="Email"
               value={form.email} onChange={e=>setForm({...form,email:e.target.value})}/>
        <input type="password" className="w-full border rounded-xl px-3 py-2" placeholder="Password"
               value={form.password} onChange={e=>setForm({...form,password:e.target.value})}/>
        {err && <p className="text-sm text-red-600">{err}</p>}
        <button className="w-full px-3 py-2 bg-black text-white rounded-xl" disabled={busy}>
          {busy ? "Signing in…" : "Sign in"}
        </button>
      </form>
      <p className="text-sm mt-3">No account? <Link className="underline" to="/signup">Sign up</Link></p>
    </div>
  );
}
