import { useState } from "react";
import { FiFilter, FiX, FiCalendar, FiUsers } from "react-icons/fi";

/**
 * Advanced search filters component
 * @param {Object} props
 * @param {Function} props.onFilterChange - Callback when filters change
 * @param {Object} props.initialFilters - Initial filter values
 */
export default function SearchFilters({ onFilterChange, initialFilters = {} }) {
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    hasPeople: initialFilters.hasPeople ?? null,
    dateFrom: initialFilters.dateFrom || "",
    dateTo: initialFilters.dateTo || "",
    searchType: initialFilters.searchType || "hybrid",
    sortBy: initialFilters.sortBy || "relevance",
  });

  const updateFilter = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    if (onFilterChange) {
      onFilterChange(newFilters);
    }
  };

  const clearFilters = () => {
    const emptyFilters = {
      hasPeople: null,
      dateFrom: "",
      dateTo: "",
      searchType: "hybrid",
      sortBy: "relevance",
    };
    setFilters(emptyFilters);
    if (onFilterChange) {
      onFilterChange(emptyFilters);
    }
  };

  const hasActiveFilters =
    filters.hasPeople !== null ||
    filters.dateFrom ||
    filters.dateTo ||
    filters.searchType !== "hybrid" ||
    filters.sortBy !== "relevance";

  return (
    <div className="w-full">
      {/* Filter toggle button */}
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="
            inline-flex items-center gap-2 px-4 py-2
            rounded-lg border
            bg-white dark:bg-gray-800
            border-gray-200 dark:border-gray-700
            text-gray-700 dark:text-gray-300
            hover:bg-gray-50 dark:hover:bg-gray-700
            transition-all duration-200
          "
        >
          <FiFilter className="h-4 w-4" />
          <span className="font-medium">Filters</span>
          {hasActiveFilters && (
            <span className="px-2 py-0.5 text-xs rounded-full bg-brand-blue text-white">
              Active
            </span>
          )}
        </button>

        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="
              text-sm text-gray-600 dark:text-gray-400
              hover:text-brand-blue dark:hover:text-brand-blue
              transition-colors duration-200
            "
          >
            Clear all
          </button>
        )}
      </div>

      {/* Filter panel */}
      {showFilters && (
        <div className="p-6 rounded-xl border bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 space-y-6 mb-6">
          {/* Search Type */}
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
              Search Method
            </label>
            <select
              value={filters.searchType}
              onChange={(e) => updateFilter("searchType", e.target.value)}
              className="
                w-full px-4 py-2 rounded-lg border
                bg-white dark:bg-gray-900
                border-gray-200 dark:border-gray-700
                text-gray-900 dark:text-gray-100
                focus:border-brand-blue focus:ring-2 focus:ring-brand-blue/20
                transition-all duration-200
              "
            >
              <option value="hybrid">🤖 Hybrid (AI + Keywords) - Recommended</option>
              <option value="semantic">🧠 Semantic (AI Only)</option>
              <option value="text">📝 Text (Keywords Only)</option>
            </select>
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              Hybrid combines AI understanding with keyword matching for best results
            </p>
          </div>

          {/* Sort By */}
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
              Sort By
            </label>
            <select
              value={filters.sortBy}
              onChange={(e) => updateFilter("sortBy", e.target.value)}
              className="
                w-full px-4 py-2 rounded-lg border
                bg-white dark:bg-gray-900
                border-gray-200 dark:border-gray-700
                text-gray-900 dark:text-gray-100
                focus:border-brand-blue focus:ring-2 focus:ring-brand-blue/20
                transition-all duration-200
              "
            >
              <option value="relevance">⭐ Best Match</option>
              <option value="newest">🕒 Newest First</option>
              <option value="oldest">📅 Oldest First</option>
            </select>
          </div>

          {/* People Filter */}
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
              <FiUsers className="inline h-4 w-4 mr-1" />
              People in Photos
            </label>
            <div className="flex gap-2">
              <button
                onClick={() => updateFilter("hasPeople", null)}
                className={`
                  flex-1 px-4 py-2 rounded-lg border transition-all duration-200
                  ${
                    filters.hasPeople === null
                      ? "bg-brand-blue text-white border-brand-blue"
                      : "bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
                  }
                `}
              >
                Any
              </button>
              <button
                onClick={() => updateFilter("hasPeople", true)}
                className={`
                  flex-1 px-4 py-2 rounded-lg border transition-all duration-200
                  ${
                    filters.hasPeople === true
                      ? "bg-brand-blue text-white border-brand-blue"
                      : "bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
                  }
                `}
              >
                With People
              </button>
              <button
                onClick={() => updateFilter("hasPeople", false)}
                className={`
                  flex-1 px-4 py-2 rounded-lg border transition-all duration-200
                  ${
                    filters.hasPeople === false
                      ? "bg-brand-blue text-white border-brand-blue"
                      : "bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
                  }
                `}
              >
                No People
              </button>
            </div>
          </div>

          {/* Date Range */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                <FiCalendar className="inline h-4 w-4 mr-1" />
                From Date
              </label>
              <input
                type="date"
                value={filters.dateFrom}
                onChange={(e) => updateFilter("dateFrom", e.target.value)}
                className="
                  w-full px-4 py-2 rounded-lg border
                  bg-white dark:bg-gray-900
                  border-gray-200 dark:border-gray-700
                  text-gray-900 dark:text-gray-100
                  focus:border-brand-blue focus:ring-2 focus:ring-brand-blue/20
                  transition-all duration-200
                "
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                <FiCalendar className="inline h-4 w-4 mr-1" />
                To Date
              </label>
              <input
                type="date"
                value={filters.dateTo}
                onChange={(e) => updateFilter("dateTo", e.target.value)}
                className="
                  w-full px-4 py-2 rounded-lg border
                  bg-white dark:bg-gray-900
                  border-gray-200 dark:border-gray-700
                  text-gray-900 dark:text-gray-100
                  focus:border-brand-blue focus:ring-2 focus:ring-brand-blue/20
                  transition-all duration-200
                "
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
