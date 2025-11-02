import { useSearchParams } from "react-router-dom";
import { useCallback } from "react";

/**
 * Hook to manage state in URL query parameters
 * Allows for shareable URLs and browser history navigation
 * @returns {Object} URL state and update methods
 */
export default function useUrlState() {
  const [searchParams, setSearchParams] = useSearchParams();

  /**
   * Get value from URL params
   */
  const getParam = useCallback(
    (key, defaultValue = null) => {
      return searchParams.get(key) || defaultValue;
    },
    [searchParams]
  );

  /**
   * Get boolean value from URL params
   */
  const getBoolParam = useCallback(
    (key, defaultValue = null) => {
      const value = searchParams.get(key);
      if (value === null) return defaultValue;
      return value === "true";
    },
    [searchParams]
  );

  /**
   * Get number value from URL params
   */
  const getNumberParam = useCallback(
    (key, defaultValue = null) => {
      const value = searchParams.get(key);
      if (value === null) return defaultValue;
      const num = parseInt(value, 10);
      return isNaN(num) ? defaultValue : num;
    },
    [searchParams]
  );

  /**
   * Update URL params
   */
  const updateParams = useCallback(
    (updates, replace = false) => {
      const newParams = new URLSearchParams(searchParams);

      Object.entries(updates).forEach(([key, value]) => {
        if (value === null || value === undefined || value === "") {
          newParams.delete(key);
        } else {
          newParams.set(key, String(value));
        }
      });

      setSearchParams(newParams, { replace });
    },
    [searchParams, setSearchParams]
  );

  /**
   * Clear specific params
   */
  const clearParams = useCallback(
    (keys) => {
      const newParams = new URLSearchParams(searchParams);
      keys.forEach((key) => newParams.delete(key));
      setSearchParams(newParams);
    },
    [searchParams, setSearchParams]
  );

  /**
   * Clear all params
   */
  const clearAllParams = useCallback(() => {
    setSearchParams(new URLSearchParams());
  }, [setSearchParams]);

  return {
    getParam,
    getBoolParam,
    getNumberParam,
    updateParams,
    clearParams,
    clearAllParams,
    searchParams,
  };
}
