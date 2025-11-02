import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiSearch } from "react-icons/fi";

/**
 * Quick search component for navbar
 * Simple search input that redirects to full search page
 */
export default function QuickSearch() {
  const [query, setQuery] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query.trim())}`);
      setQuery("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="relative">
        <FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 dark:text-gray-500" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Quick search..."
          className="
            w-48 pl-9 pr-3 py-1.5
            rounded-lg border
            bg-white dark:bg-gray-800
            border-gray-200 dark:border-gray-700
            text-sm text-gray-900 dark:text-gray-100
            placeholder-gray-400 dark:placeholder-gray-500
            focus:border-brand-blue focus:ring-1 focus:ring-brand-blue/20
            dark:focus:border-brand-blue
            transition-all duration-200
          "
        />
      </div>
    </form>
  );
}
