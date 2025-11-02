import { useState, useEffect } from "react";
import { FiSearch, FiX } from "react-icons/fi";
import useDebounce from "../hooks/useDebounce";

/**
 * Search bar component with debouncing and clear functionality
 * @param {Object} props
 * @param {string} props.initialValue - Initial search value
 * @param {Function} props.onSearch - Callback when search is triggered
 * @param {Function} props.onClear - Callback when search is cleared
 * @param {boolean} props.loading - Loading state
 * @param {string} props.placeholder - Input placeholder
 */
export default function SearchBar({
  initialValue = "",
  onSearch,
  onClear,
  loading = false,
  placeholder = "Search your memories with natural language...",
}) {
  const [inputValue, setInputValue] = useState(initialValue);
  const debouncedValue = useDebounce(inputValue, 500);

  // Trigger search when debounced value changes
  useEffect(() => {
    if (debouncedValue && onSearch) {
      onSearch(debouncedValue);
    }
  }, [debouncedValue, onSearch]);

  // Update input when initial value changes (e.g., from URL)
  useEffect(() => {
    setInputValue(initialValue);
  }, [initialValue]);

  const handleClear = () => {
    setInputValue("");
    if (onClear) {
      onClear();
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() && onSearch) {
      onSearch(inputValue.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative w-full">
      <div className="relative">
        {/* Search icon */}
        <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500">
          <FiSearch className={`h-5 w-5 ${loading ? "animate-pulse" : ""}`} />
        </div>

        {/* Input field */}
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={placeholder}
          disabled={loading}
          className="
            w-full pl-12 pr-12 py-4 
            rounded-xl border-2
            bg-white dark:bg-gray-800
            border-gray-200 dark:border-gray-700
            focus:border-brand-blue focus:ring-2 focus:ring-brand-blue/20
            dark:focus:border-brand-blue
            text-gray-900 dark:text-gray-100
            placeholder-gray-400 dark:placeholder-gray-500
            transition-all duration-200
            disabled:opacity-60 disabled:cursor-not-allowed
          "
        />

        {/* Clear button */}
        {inputValue && !loading && (
          <button
            type="button"
            onClick={handleClear}
            className="
              absolute right-4 top-1/2 -translate-y-1/2
              p-1 rounded-full
              text-gray-400 hover:text-gray-600
              dark:text-gray-500 dark:hover:text-gray-300
              hover:bg-gray-100 dark:hover:bg-gray-700
              transition-all duration-200
            "
            aria-label="Clear search"
          >
            <FiX className="h-5 w-5" />
          </button>
        )}

        {/* Loading spinner */}
        {loading && (
          <div className="absolute right-4 top-1/2 -translate-y-1/2">
            <div className="animate-spin rounded-full h-5 w-5 border-2 border-brand-blue border-t-transparent" />
          </div>
        )}
      </div>

      {/* Search tips */}
      <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
        Try: "happy moments with friends", "sunset photos", "beach vacation 2024"
      </div>
    </form>
  );
}
