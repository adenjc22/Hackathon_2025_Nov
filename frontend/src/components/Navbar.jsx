import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Navbar() {
  const { user, logout } = useAuth();
  const nav = useNavigate();

  return (
    <nav className="border-b bg-white">
      <div className="mx-auto max-w-6xl px-4 h-14 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to="/" className="font-semibold">Legacy Album</Link>
          <Link to="/dashboard" className="text-sm hover:underline">Dashboard</Link>
          <Link to="/albums" className="text-sm hover:underline">Albums</Link>
          <Link to="/search" className="text-sm hover:underline">Search</Link>
        </div>
        <div className="flex items-center gap-3">
          {user ? (
            <>
              <span className="text-sm text-gray-600">{user.email}</span>
              <button
                className="px-3 py-1 rounded-lg bg-gray-900 text-white text-sm"
                onClick={async () => { await logout(); nav("/login"); }}
              >Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm hover:underline">Login</Link>
              <Link to="/signup" className="text-sm hover:underline">Sign up</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
