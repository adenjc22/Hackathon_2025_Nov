import { useSearchParams } from "react-router-dom";
import useFetch from "../hooks/useFetch";
import MediaGrid from "../components/MediaGrid";

export default function SearchResults() {
  const [params] = useSearchParams();
  const q = params.get("q") || "";
  const { data, loading, error } = useFetch(
    q ? `/api/search?query=${encodeURIComponent(q)}` : null,
    [q]
  );

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 text-gray-900 dark:text-gray-100">
      {/* Title */}
      <h1 className="title">Search</h1>

      {/* Card */}
      <div className="rounded-xl border p-5 shadow-lg
                      bg-brand-light border-gray-200
                      dark:bg-brand-dark dark:border-gray-700">
        <form className="mb-4">
          <input
            name="q"
            defaultValue={q}
            className="input"
            placeholder="Search your memories…"
          />
        </form>

        {loading && (
          <p className="animate-pulse text-gray-700 dark:text-gray-400">Searching…</p>
        )}

        {error && (
          <p
            className="text-sm rounded-lg px-3 py-2
                       text-red-700 bg-red-100 border border-red-300
                       dark:text-red-300 dark:bg-red-900/30 dark:border-red-700/50"
            role="alert"
          >
            Error searching.
          </p>
        )}

        {data && <MediaGrid items={data} />}
      </div>
    </div>
  );
}
