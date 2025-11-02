import { useEffect, useState, useCallback } from "react";
import { FiSearch, FiAlertCircle, FiInbox } from "react-icons/fi";
import SearchBar from "../components/SearchBar";
import SearchFilters from "../components/SearchFilters";
import SearchResultsGrid from "../components/SearchResultsGrid";
import Pagination from "../components/Pagination";
import Loader from "../components/Loader";
import useSearch from "../hooks/useSearch";
import useUrlState from "../hooks/useUrlState";
import { trackSearch, trackFilterUsage, trackResultClick } from "../utils/analytics";

export default function SearchResults() {
  const { getParam, getBoolParam, getNumberParam, updateParams } = useUrlState();
  const { results, loading, error, totalResults, searchType, search, clearSearch } = useSearch();

  // Get initial values from URL
  const initialQuery = getParam("q", "");
  const initialSearchType = getParam("type", "hybrid");
  const initialSortBy = getParam("sort", "relevance");
  const initialHasPeople = getBoolParam("people", null);
  const initialDateFrom = getParam("from", "");
  const initialDateTo = getParam("to", "");
  const initialPage = getNumberParam("page", 1);

  const [query, setQuery] = useState(initialQuery);
  const [currentPage, setCurrentPage] = useState(initialPage);
  const [filters, setFilters] = useState({
    searchType: initialSearchType,
    sortBy: initialSortBy,
    hasPeople: initialHasPeople,
    dateFrom: initialDateFrom,
    dateTo: initialDateTo,
  });

  const pageSize = 20;

  // Execute search when query or filters change
  const executeSearch = useCallback(
    (searchQuery, searchFilters, page = 1) => {
      if (!searchQuery?.trim()) {
        clearSearch();
        return;
      }

      // Update URL with search params
      updateParams({
        q: searchQuery,
        type: searchFilters.searchType,
        sort: searchFilters.sortBy,
        people: searchFilters.hasPeople,
        from: searchFilters.dateFrom,
        to: searchFilters.dateTo,
        page: page > 1 ? page : null,
      });

      // Calculate offset for pagination
      const offset = (page - 1) * pageSize;

      // Execute search
      search(searchQuery, {
        searchType: searchFilters.searchType,
        sortBy: searchFilters.sortBy,
        hasPeople: searchFilters.hasPeople,
        dateFrom: searchFilters.dateFrom,
        dateTo: searchFilters.dateTo,
        limit: pageSize,
        offset: offset,
      }).then(() => {
        // Track search analytics
        trackSearch(searchQuery, searchFilters.searchType, totalResults);
      });
    },
    [search, clearSearch, updateParams, pageSize, totalResults]
  );

  // Initial search on mount if query exists
  useEffect(() => {
    if (initialQuery) {
      executeSearch(initialQuery, filters, initialPage);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Handle search bar query change
  const handleSearch = useCallback(
    (newQuery) => {
      setQuery(newQuery);
      setCurrentPage(1); // Reset to first page
      executeSearch(newQuery, filters, 1);
    },
    [filters, executeSearch]
  );

  // Handle clear search
  const handleClear = useCallback(() => {
    setQuery("");
    setCurrentPage(1);
    clearSearch();
    updateParams({ q: null, page: null });
  }, [clearSearch, updateParams]);

  // Handle filter changes
  const handleFilterChange = useCallback(
    (newFilters) => {
      setFilters(newFilters);
      setCurrentPage(1); // Reset to first page when filters change
      
      // Track filter usage
      Object.entries(newFilters).forEach(([key, value]) => {
        if (value !== filters[key] && value !== null && value !== "") {
          trackFilterUsage(key, value);
        }
      });
      
      if (query) {
        executeSearch(query, newFilters, 1);
      }
    },
    [query, filters, executeSearch]
  );

  // Handle pagination
  const handlePageChange = useCallback(
    (newPage) => {
      setCurrentPage(newPage);
      executeSearch(query, filters, newPage);
      
      // Scroll to top of results
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    [query, filters, executeSearch]
  );

  // Handle item click (optional: could open modal or navigate)
  const handleItemClick = (item) => {
    console.log("Clicked item:", item);
    
    // Track result click
    const position = results.indexOf(item);
    trackResultClick(item.id, position, item.score);
    
    // TODO: Implement modal view or detail page
  };

  const showEmptyState = !loading && !error && query && results.length === 0;
  const showResults = !loading && !error && results.length > 0;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            <FiSearch className="inline h-8 w-8 mr-2 text-brand-blue" />
            Search Your Memories
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Use natural language to find exactly what you're looking for
          </p>
        </div>

        {/* Search Bar */}
        <div className="mb-6">
          <SearchBar
            initialValue={query}
            onSearch={handleSearch}
            onClear={handleClear}
            loading={loading}
          />
        </div>

        {/* Filters */}
        <SearchFilters
          onFilterChange={handleFilterChange}
          initialFilters={filters}
        />

        {/* Search Results Summary */}
        {(showResults || loading) && (
          <div className="mb-6 flex items-center justify-between">
            <div className="text-sm text-gray-600 dark:text-gray-400">
              {loading ? (
                <span className="animate-pulse">Searching...</span>
              ) : (
                <>
                  Found <span className="font-semibold text-gray-900 dark:text-gray-100">{totalResults}</span> results
                  {query && (
                    <>
                      {" "}for "<span className="font-medium">{query}</span>"
                    </>
                  )}
                  {searchType && (
                    <span className="ml-2 text-xs px-2 py-1 rounded-full bg-gray-100 dark:bg-gray-800">
                      {searchType}
                    </span>
                  )}
                </>
              )}
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-20">
            <Loader />
            <p className="mt-4 text-gray-600 dark:text-gray-400">
              Searching through your memories...
            </p>
          </div>
        )}

        {/* Error State */}
        {error && !loading && (
          <div className="rounded-xl border-2 border-red-200 dark:border-red-900 bg-red-50 dark:bg-red-900/20 p-8 text-center">
            <FiAlertCircle className="h-12 w-12 mx-auto text-red-600 dark:text-red-400 mb-4" />
            <h3 className="text-lg font-semibold text-red-900 dark:text-red-200 mb-2">
              Search Error
            </h3>
            <p className="text-red-700 dark:text-red-300">
              {error}
            </p>
            <button
              onClick={() => handleSearch(query)}
              className="mt-4 px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Empty State */}
        {showEmptyState && (
          <div className="rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-12 text-center">
            <FiInbox className="h-16 w-16 mx-auto text-gray-400 dark:text-gray-600 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
              No results found
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              We couldn't find any photos matching "{query}"
            </p>
            <div className="space-y-2 text-sm text-gray-500 dark:text-gray-400">
              <p>Try:</p>
              <ul className="list-disc list-inside space-y-1">
                <li>Using different keywords</li>
                <li>Being more general (e.g., "beach" instead of "sunset at Malibu beach")</li>
                <li>Adjusting your filters</li>
                <li>Checking your spelling</li>
              </ul>
            </div>
          </div>
        )}

        {/* Results Grid */}
        {showResults && (
          <>
            <SearchResultsGrid results={results} onItemClick={handleItemClick} />
            
            {/* Pagination */}
            <Pagination
              currentPage={currentPage}
              totalResults={totalResults}
              pageSize={pageSize}
              onPageChange={handlePageChange}
            />
          </>
        )}

        {/* Initial State (no search yet) */}
        {!query && !loading && (
          <div className="rounded-xl border-2 border-dashed border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 p-12 text-center">
            <FiSearch className="h-16 w-16 mx-auto text-gray-400 dark:text-gray-600 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Start Your Search
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Enter a query above to search through your photos using natural language
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-left max-w-3xl mx-auto">
              <div className="p-4 rounded-lg bg-gray-50 dark:bg-gray-900">
                <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">
                  Example Searches
                </h4>
                <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                  <li>• "happy moments with friends"</li>
                  <li>• "sunset at the beach"</li>
                  <li>• "birthday party 2024"</li>
                </ul>
              </div>
              <div className="p-4 rounded-lg bg-gray-50 dark:bg-gray-900">
                <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">
                  Use Filters
                </h4>
                <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                  <li>• Filter by date range</li>
                  <li>• Include/exclude people</li>
                  <li>• Choose search method</li>
                </ul>
              </div>
              <div className="p-4 rounded-lg bg-gray-50 dark:bg-gray-900">
                <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">
                  AI-Powered
                </h4>
                <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                  <li>• Understands context</li>
                  <li>• Finds similar themes</li>
                  <li>• Smart recommendations</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
