import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="mt-16 border-t border-gray-800">
      <div className="mx-auto max-w-6xl px-4 py-8 text-center">
        <p className="text-xs text-gray-500">
          Made at DurHack 2025 · Powered by FastAPI & React
        </p>

        {/* Optional mini-nav (remove if you don't have these routes yet) */}
        {/* <nav className="mt-3 flex items-center justify-center gap-4 text-xs text-gray-500">
          <Link to="/privacy" className="hover:text-brand-blue">Privacy</Link>
          <span aria-hidden>•</span>
          <Link to="/terms" className="hover:text-brand-blue">Terms</Link>
        </nav> */}
      </div>
    </footer>
  );
}
