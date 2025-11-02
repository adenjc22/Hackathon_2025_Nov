import { useState, useCallback } from "react";
import { api } from "../utils/api";

/**
 * Custom hook for search functionality with filters and pagination
 * @returns {Object} Search state and methods
 */
export default function useSearch() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [totalResults, setTotalResults] = useState(0);
  const [searchType, setSearchType] = useState("hybrid");

  /**
   * Execute search with query and filters
   * @param {string} query - Search query
   * @param {Object} options - Search options
   */
  const search = useCallback(async (query, options = {}) => {
    if (!query?.trim()) {
      setResults([]);
      setTotalResults(0);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        query: query.trim(),
        search_type: options.searchType || "hybrid",
        limit: options.limit || 20,
        offset: options.offset || 0,
      });

      // Add filters if provided
      if (options.hasPeople !== undefined && options.hasPeople !== null) {
        params.append("has_people", options.hasPeople);
      }
      if (options.dateFrom) {
        params.append("date_from", options.dateFrom);
      }
      if (options.dateTo) {
        params.append("date_to", options.dateTo);
      }
      if (options.sortBy) {
        params.append("sort_by", options.sortBy);
      }

      const response = await api.get(`/api/search?${params.toString()}`);
      
      setResults(response.data.results || []);
      setTotalResults(response.data.total_results || 0);
      setSearchType(response.data.search_type || "hybrid");
    } catch (err) {
      console.error("Search error:", err);
      setError(err?.response?.data?.detail || "Search failed. Please try again.");
      setResults([]);
      setTotalResults(0);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Clear search results
   */
  const clearSearch = useCallback(() => {
    setResults([]);
    setTotalResults(0);
    setError(null);
  }, []);

  return {
    results,
    loading,
    error,
    totalResults,
    searchType,
    search,
    clearSearch,
  };
}
