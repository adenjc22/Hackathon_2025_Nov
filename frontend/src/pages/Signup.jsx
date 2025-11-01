import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Signup() {
  const nav = useNavigate();
  const { signup } = useAuth();
  const [form, setForm] = useState({ email: "", password: "", name: "" });
  const [err, setErr] = useState(""); const [busy, setBusy] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setBusy(true); setErr("");
    try {
      await signup(form);
      nav("/dashboard", { replace: true });
    } catch (e2) {
      setErr(e2?.response?.data?.detail || e2.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-sm p-6">
      <h1 className="text-2xl font-semibold mb-4">Create account</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input className="w-full border rounded-xl px-3 py-2" placeholder="Name"
               value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/>
        <input className="w-full border rounded-xl px-3 py-2" placeholder="Email"
               value={form.email} onChange={e=>setForm({...form,email:e.target.value})}/>
        <input type="password" className="w-full border rounded-xl px-3 py-2" placeholder="Password"
               value={form.password} onChange={e=>setForm({...form,password:e.target.value})}/>
        {err && <p className="text-sm text-red-600">{err}</p>}
        <button className="w-full px-3 py-2 bg-black text-white rounded-xl" disabled={busy}>
          {busy ? "Creating…" : "Sign up"}
        </button>
      </form>
    </div>
  );
}
