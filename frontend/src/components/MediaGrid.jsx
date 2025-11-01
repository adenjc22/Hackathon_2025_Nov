export default function MediaGrid({ items }) {
  if (!items?.length) return <p className="text-sm text-gray-600">No media yet.</p>;
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
      {items.map((m) => (
        <div key={m.id} className="rounded-xl overflow-hidden border bg-white">
          {m.mimeType?.startsWith("video/") ? (
            <video src={m.fileUrl} className="w-full h-40 object-cover" controls />
          ) : (
            <img src={m.fileUrl} className="w-full h-40 object-cover" alt={m.fileName} />
          )}
          <div className="p-2">
            <div className="text-sm font-medium truncate">{m.fileName}</div>
            <div className="text-xs text-gray-500">
              {m.status !== "done" ? (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-yellow-100 text-yellow-800 rounded">
                  {m.status}
                </span>
              ) : (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-green-100 text-green-800 rounded">
                  processed
                </span>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
