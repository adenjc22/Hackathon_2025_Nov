import { useEffect, useRef, useState } from "react";
import { api } from "../utils/api";

/**
 * Simple data fetcher. Re-fetches when deps change.
 * Returns { data, loading, error, refetch }.
 */
export default function useFetch(path, deps = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(!!path);
  const [error, setError] = useState(null);
  const cancelRef = useRef(null);

  const run = async () => {
    if (!path) return;
    setLoading(true); setError(null);
    if (cancelRef.current) cancelRef.current.cancel();
    cancelRef.current = api.CancelToken.source?.() || { token: undefined };
    try {
      const res = await api.get(path, { cancelToken: cancelRef.current.token });
      setData(res.data);
    } catch (e) {
      if (!axios.isCancel?.(e)) setError(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { run(); /* eslint-disable-next-line */ }, deps);
  return { data, loading, error, refetch: run };
}
