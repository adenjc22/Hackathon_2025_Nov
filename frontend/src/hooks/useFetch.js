import { useEffect, useRef, useState } from "react";
import axios from "axios";
import { api } from "../utils/api";

/**
 * Simple data fetcher. Re-fetches when deps change.
 * Returns { data, loading, error, refetch }.
 */
export default function useFetch(path, deps = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(!!path);
  const [error, setError] = useState(null);
  const abortControllerRef = useRef(null);

  const run = async () => {
    if (!path) return;
    setLoading(true); setError(null);
    
    // Cancel previous request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    
    // Create new AbortController for this request
    abortControllerRef.current = new AbortController();
    
    try {
      const res = await api.get(path, { 
        signal: abortControllerRef.current.signal 
      });
      setData(res.data);
    } catch (e) {
      if (!axios.isCancel?.(e) && e.name !== 'AbortError' && e.name !== 'CanceledError') {
        setError(e);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { run(); /* eslint-disable-next-line */ }, deps);
  return { data, loading, error, refetch: run };
}
