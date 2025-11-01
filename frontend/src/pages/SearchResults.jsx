import { useSearchParams } from "react-router-dom";
import useFetch from "../hooks/useFetch";
import MediaGrid from "../components/MediaGrid";

export default function SearchResults() {
  const [params] = useSearchParams();
  const q = params.get("q") || "";
  const { data, loading, error } = useFetch(q ? `/api/search?query=${encodeURIComponent(q)}` : null, [q]);

  return (
    <div className="mx-auto max-w-6xl p-4">
      <form className="mb-4">
        <input name="q" defaultValue={q} className="w-full border rounded-xl px-3 py-2" placeholder="Search your memories…" />
      </form>
      {loading && <p>Searching…</p>}
      {error && <p className="text-red-600">Error searching.</p>}
      {data && <MediaGrid items={data} />}
    </div>
  );
}
