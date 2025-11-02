import { FiImage, FiVideo, FiEye, FiCalendar, FiUsers, FiTag } from "react-icons/fi";

/**
 * Grid component for displaying search results with metadata
 * @param {Object} props
 * @param {Array} props.results - Array of search results
 * @param {Function} props.onItemClick - Callback when item is clicked
 */
export default function SearchResultsGrid({ results, onItemClick }) {
  if (!results || results.length === 0) {
    return null;
  }

  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    } catch {
      return "Unknown date";
    }
  };

  const getRelevanceColor = (score) => {
    if (score >= 0.8) return "text-green-600 dark:text-green-400";
    if (score >= 0.6) return "text-yellow-600 dark:text-yellow-400";
    return "text-gray-600 dark:text-gray-400";
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {results.map((item) => (
        <div
          key={item.id}
          onClick={() => onItemClick?.(item)}
          className="
            group cursor-pointer
            rounded-xl overflow-hidden
            border-2 border-gray-200 dark:border-gray-700
            bg-white dark:bg-gray-800
            hover:border-brand-blue hover:shadow-xl hover:shadow-brand-blue/10
            dark:hover:border-brand-blue
            transition-all duration-300
          "
        >
          {/* Image/Video preview */}
          <div className="relative w-full h-56 bg-gray-100 dark:bg-gray-900 overflow-hidden">
            {item.filename?.match(/\.(mp4|webm|ogg)$/i) ? (
              <>
                <video
                  src={item.file_url}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  preload="metadata"
                />
                <div className="absolute top-2 right-2 p-2 rounded-full bg-black/60 backdrop-blur-sm">
                  <FiVideo className="h-4 w-4 text-white" />
                </div>
              </>
            ) : (
              <>
                <img
                  src={item.file_url}
                  alt={item.caption || item.filename}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  loading="lazy"
                  onError={(e) => {
                    e.currentTarget.src = "/demo/placeholder.jpg";
                  }}
                />
                <div className="absolute top-2 right-2 p-2 rounded-full bg-black/60 backdrop-blur-sm">
                  <FiImage className="h-4 w-4 text-white" />
                </div>
              </>
            )}

            {/* Relevance score badge */}
            <div className="absolute bottom-2 left-2 px-3 py-1 rounded-full bg-black/60 backdrop-blur-sm">
              <span className={`text-sm font-medium ${getRelevanceColor(item.score)}`}>
                {Math.round(item.score * 100)}% match
              </span>
            </div>

            {/* Match type badge */}
            <div className="absolute top-2 left-2 px-2 py-1 rounded text-xs font-medium bg-black/60 backdrop-blur-sm text-white">
              {item.match_type}
            </div>
          </div>

          {/* Content */}
          <div className="p-4 space-y-3">
            {/* Caption */}
            {item.caption && (
              <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">
                {item.caption}
              </p>
            )}

            {/* Metadata row 1 */}
            <div className="flex flex-wrap gap-3 text-xs text-gray-500 dark:text-gray-400">
              {/* Date */}
              <div className="flex items-center gap-1">
                <FiCalendar className="h-3 w-3" />
                <span>{formatDate(item.created_at)}</span>
              </div>

              {/* People indicator */}
              {item.has_people && (
                <div className="flex items-center gap-1 text-brand-blue">
                  <FiUsers className="h-3 w-3" />
                  <span>People</span>
                </div>
              )}
            </div>

            {/* Tags */}
            {item.tags && item.tags.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {item.tags.slice(0, 5).map((tag, idx) => (
                  <span
                    key={idx}
                    className="
                      inline-flex items-center gap-1
                      px-2 py-0.5 rounded-full text-xs
                      bg-gray-100 dark:bg-gray-700
                      text-gray-700 dark:text-gray-300
                    "
                  >
                    <FiTag className="h-3 w-3" />
                    {tag}
                  </span>
                ))}
                {item.tags.length > 5 && (
                  <span className="text-xs text-gray-500 dark:text-gray-400 px-2">
                    +{item.tags.length - 5} more
                  </span>
                )}
              </div>
            )}

            {/* Emotion indicator */}
            {item.emotion && (
              <div className="text-xs text-gray-500 dark:text-gray-400">
                Mood: {item.emotion.dominant || "neutral"}
              </div>
            )}

            {/* Filename */}
            <p className="text-xs text-gray-400 dark:text-gray-500 truncate">
              {item.filename}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
