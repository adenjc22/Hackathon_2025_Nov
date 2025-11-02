import { useState } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Login() {
  const nav = useNavigate();
  const loc = useLocation();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setErr("");
    try {
      await login(form);
      nav(loc.state?.from?.pathname || "/upload", { replace: true });
    } catch (e2) {
      setErr(e2?.response?.data?.detail || e2.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-sm px-4 py-10 text-gray-900 dark:text-gray-100">
      {/* Title */}
      <h1 className="title">Log in</h1>

      {/* Card */}
      <div className="rounded-xl border p-5 shadow-lg
                      bg-brand-light border-gray-200
                      dark:bg-brand-dark dark:border-gray-700">
        <form onSubmit={onSubmit} className="space-y-3">
          <label className="block">
            <span className="sr-only">Email</span>
            <input
              className="input"
              placeholder="Email"
              autoComplete="email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </label>

          <label className="block">
            <span className="sr-only">Password</span>
            <input
              type="password"
              className="input"
              placeholder="Password"
              autoComplete="current-password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
          </label>

          {err && (
            <p
              className="text-sm rounded-lg px-3 py-2
                         text-red-700 bg-red-100 border border-red-300
                         dark:text-red-300 dark:bg-red-900/30 dark:border-red-700/50"
              role="alert"
            >
              {err}
            </p>
          )}

          <button
            className="btn-primary w-full rounded-xl disabled:opacity-60"
            disabled={busy}
            type="submit"
          >
            {busy ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <p className="text-sm mt-4 text-gray-700 dark:text-gray-400">
          No account?{" "}
          <Link to="/signup" className="text-brand-blue hover:underline">
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
}
