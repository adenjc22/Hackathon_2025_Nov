import useFetch from "../hooks/useFetch";

export default function Albums() {
  const { data, loading, error } = useFetch("/api/albums", []);
  if (loading) return <p className="p-6">Loading…</p>;
  if (error) return <p className="p-6 text-red-600">Failed to load.</p>;

  return (
    <div className="mx-auto max-w-6xl p-4 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
      {(data || []).map(a => (
        <div key={a.id} className="border rounded-xl p-3">
          <img src={a.coverUrl} alt={a.title} className="w-full h-40 object-cover rounded-lg"/>
          <div className="mt-2">
            <div className="font-medium">{a.title}</div>
            <div className="text-xs text-gray-600">{a.mediaCount} items</div>
          </div>
        </div>
      ))}
    </div>
  );
}
