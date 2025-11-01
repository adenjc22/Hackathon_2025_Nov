import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth";

function SunIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" {...props}>
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" />
    </svg>
  );
}
function MoonIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" {...props}>
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </svg>
  );
}

export default function Navbar() {
  const { user, logout } = useAuth();
  const nav = useNavigate();
  const [isDark, setIsDark] = useState(true);

  useEffect(() => {
    const root = document.documentElement;
    const saved = localStorage.getItem("theme");
    const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)")?.matches;
    const enableDark = saved ? saved === "dark" : (prefersDark ?? true);
    root.classList.toggle("dark", enableDark);
    setIsDark(enableDark);
  }, []);

  const toggleTheme = () => {
    const root = document.documentElement;
    const next = !isDark;
    root.classList.toggle("dark", next);
    localStorage.setItem("theme", next ? "dark" : "light");
    setIsDark(next);
  };

  return (
    <nav
      className="
        bg-grey-500 border-b border-gray-200 shadow-md
        dark:bg-brand-dark dark:border-gray-700
      "
    >
      <div className="mx-auto max-w-6xl px-4 h-16 flex items-center justify-between">
        {/* Left */}
        <div className="flex items-center gap-8">
          <Link
            to="/"
            className="text-2xl font-bold text-brand-blue hover:text-[#33ccff] transition-colors tracking-wide"
          >
            Legacy Album
          </Link>

          {user && (
            <>
              <Link
                to="/dashboard"
                className="text-base text-gray-800 hover:text-brand-blue transition dark:text-gray-300"
              >
                Dashboard
              </Link>
              <Link
                to="/albums"
                className="text-base text-gray-800 hover:text-brand-blue transition dark:text-gray-300"
              >
                Albums
              </Link>
              <Link
                to="/search"
                className="text-base text-gray-800 hover:text-brand-blue transition dark:text-gray-300"
              >
                Search
              </Link>
            </>
          )}
        </div>

        {/* Right */}
        <div className="flex items-center gap-3">
          {/* Theme toggle */}
          <button
            onClick={toggleTheme}
            aria-label="Toggle dark mode"
            title={isDark ? "Switch to light mode" : "Switch to dark mode"}
            className="
              rounded-xl p-2 transition
              bg-gray-100 border border-gray-300 text-gray-700 hover:border-gray-400
              dark:bg-[#1f1f1f] dark:border-gray-700 dark:text-gray-300 dark:hover:border-brand-blue
            "
          >
            {isDark ? <SunIcon /> : <MoonIcon />}
          </button>

          {user ? (
            <>
              <span className="text-sm text-gray-600 dark:text-gray-400 hidden sm:inline">
                {user.email}
              </span>
              <button
                onClick={async () => {
                  await logout();
                  nav("/login");
                }}
                className="btn-primary px-4 py-2 rounded-lg text-base font-medium"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="text-base text-gray-800 hover:text-brand-blue transition dark:text-gray-300"
              >
                Login
              </Link>
              <Link
                to="/signup"
                className="text-base text-gray-800 hover:text-brand-blue transition dark:text-gray-300"
              >
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
