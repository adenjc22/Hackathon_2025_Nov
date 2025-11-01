import useFetch from "../hooks/useFetch";
import Loader from "../components/Loader";

export default function Albums() {
  const { data, loading, error } = useFetch("/api/albums", []);

  if (loading) return <Loader />;
  if (error)
    return (
      <p className="p-6 text-center text-red-600 dark:text-red-400">
        Failed to load albums.
      </p>
    );

  return (
    <div className="mx-auto max-w-6xl px-4 py-6 text-gray-900 dark:text-gray-100">
      <h1 className="text-2xl font-semibold text-brand-blue mb-6">Albums</h1>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {(data || []).map((a) => (
          <div
            key={a.id}
            className="
              rounded-xl overflow-hidden border transition
              bg-brand-light border-gray-200 hover:border-brand-blue/70
              dark:bg-brand-dark dark:border-gray-700 dark:hover:border-brand-blue
              shadow-sm
            "
          >
            <img
              src={a.coverUrl}
              alt={a.title}
              className="w-full h-40 object-cover"
              loading="lazy"
              onError={(e) => {
                e.currentTarget.src = "/demo/placeholder.jpg";
              }}
            />
            <div className="p-3">
              <div className="font-medium truncate text-gray-900 dark:text-gray-200">
                {a.title}
              </div>
              <div className="text-xs mt-1 text-gray-600 dark:text-gray-400">
                {a.mediaCount} item{a.mediaCount !== 1 ? "s" : ""}
              </div>
            </div>
          </div>
        ))}
      </div>

      {!data?.length && (
        <p className="text-center mt-10 text-gray-700 dark:text-gray-400">
          No albums found.
        </p>
      )}
    </div>
  );
}
