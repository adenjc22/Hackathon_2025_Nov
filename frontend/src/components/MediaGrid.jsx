import { FaTrashAlt as DeleteIcon } from "react-icons/fa";
import { api } from "../utils/api";

export default function MediaGrid({ items, onDelete }) {
  if (!items?.length)
    return (
      <p className="text-sm text-gray-500 dark:text-gray-400 text-center py-8">
        No media uploaded yet.
      </p>
    );

  const handleDelete = async (id) => {
    try {
      await api.delete(`/media/${id}`).catch(() => {});
      onDelete?.(id);
    } catch (e) {
      console.error("Delete failed:", e);
    }
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {items.map((m) => (
        <div
          key={m.id}
          className="
            rounded-xl overflow-hidden
            border border-gray-200 bg-white
            hover:border-brand-blue hover:shadow-lg hover:shadow-brand-blue/10
            dark:border-gray-700 dark:bg-[#1f1f1f]
            transition-all duration-200
          "
        >
          {/* Media area */}
          <div className="w-full h-44 bg-gray-100 dark:bg-gray-800">
            {m.mimeType?.startsWith("video/") ? (
              <video
                src={m.fileUrl}
                className="w-full h-full object-cover"
                controls
              />
            ) : (
              <img
                src={m.fileUrl}
                alt={m.fileName}
                className="w-full h-full object-cover block"
                loading="lazy"
                onError={(e) => {
                  e.currentTarget.src = "/demo/placeholder.jpg";
                }}
              />
            )}
          </div>

          {/* Footer */}
          <div className="p-3 flex flex-col gap-1">
            <div className="text-sm font-medium truncate text-gray-800 dark:text-gray-200">
              {m.fileName}
            </div>

            <div className="flex items-center justify-between">
              {/* Status badge */}
              <div className="text-xs">
                {m.status !== "done" ? (
                  <span className="badge badge-yellow">processing</span>
                ) : (
                  <span className="badge badge-green">processed</span>
                )}
              </div>

              {/* Delete button */}
              <button
                onClick={() => handleDelete(m.id)}
                title="Delete"
                aria-label={`Delete ${m.fileName}`}
                className="
                  inline-flex h-7 w-7 items-center justify-center
                  rounded-md transition
                  text-red-500 hover:text-red-600 hover:bg-gray-100
                  dark:text-red-400 dark:hover:text-red-300 dark:hover:bg-gray-700
                "
              >
                <DeleteIcon className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
