import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getAlbums, getAlbum, rebuildAlbums, deleteAlbum, createAlbum, createAlbumFromPrompt, getAllMedia } from "../utils/api";
import Loader from "../components/Loader";

export default function Albums() {
  const [albums, setAlbums] = useState([]);
  const [selectedAlbum, setSelectedAlbum] = useState(null);
  const [loading, setLoading] = useState(true);
  const [rebuilding, setRebuilding] = useState(false);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState("all"); // all, auto, manual
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [createMode, setCreateMode] = useState("prompt"); // prompt or manual
  const [creating, setCreating] = useState(false);
  const [allMedia, setAllMedia] = useState([]);
  const [selectedMediaIds, setSelectedMediaIds] = useState([]);
  const [loadingMedia, setLoadingMedia] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadAlbums();
  }, [filter]);

  useEffect(() => {
    // Load media when modal opens in manual mode
    if (showCreateModal && createMode === "manual") {
      loadAllMedia();
    }
  }, [showCreateModal, createMode]);

  const loadAllMedia = async () => {
    try {
      setLoadingMedia(true);
      const data = await getAllMedia();
      setAllMedia(data);
    } catch (err) {
      console.error("Failed to load media:", err);
    } finally {
      setLoadingMedia(false);
    }
  };

  const loadAlbums = async () => {
    try {
      setLoading(true);
      setError(null);
      const options = {};
      if (filter === "auto") {
        options.autoOnly = true;
      } else if (filter === "manual") {
        options.autoOnly = false;
      }
      const data = await getAlbums(options);
      setAlbums(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load albums");
    } finally {
      setLoading(false);
    }
  };

  const handleRebuild = async () => {
    if (!confirm("Create AI albums from your photos? This will analyze your library and create smart albums based on AI tags.")) {
      return;
    }
    
    try {
      setRebuilding(true);
      setError(null);
      const result = await rebuildAlbums(true);
      alert(`Success! Created ${result.total_albums} AI albums from ${result.photos_processed} photos.`);
      await loadAlbums();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create AI albums");
    } finally {
      setRebuilding(false);
    }
  };

  const handleAlbumClick = async (album) => {
    try {
      const fullAlbum = await getAlbum(album.id);
      setSelectedAlbum(fullAlbum);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load album details");
    }
  };

  const handleDeleteAlbum = async (albumId) => {
    if (!confirm("Delete this album? Photos will not be deleted, only the album.")) {
      return;
    }
    
    try {
      await deleteAlbum(albumId);
      setAlbums(albums.filter(a => a.id !== albumId));
      if (selectedAlbum?.id === albumId) {
        setSelectedAlbum(null);
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to delete album");
    }
  };

  const handleCreateAlbum = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
      setCreating(true);
      setError(null);
      
      if (createMode === "prompt") {
        const prompt = formData.get("prompt");
        const title = formData.get("title");
        
        const result = await createAlbumFromPrompt({
          prompt,
          title: title || undefined
        });
        
        // Show the created album details
        setSelectedAlbum(result);
      } else {
        const title = formData.get("title");
        
        const result = await createAlbum({
          title,
          media_ids: selectedMediaIds
        });
        
        setAlbums([result, ...albums]);
      }
      
      setShowCreateModal(false);
      setSelectedMediaIds([]); // Reset selection
      await loadAlbums();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create album");
    } finally {
      setCreating(false);
    }
  };

  const toggleMediaSelection = (mediaId) => {
    setSelectedMediaIds(prev => {
      if (prev.includes(mediaId)) {
        return prev.filter(id => id !== mediaId);
      } else {
        return [...prev, mediaId];
      }
    });
  };

  const getImageUrl = (url) => {
    if (!url) return "/placeholder.jpg";
    if (url.startsWith("http")) return url;
    const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000";
    return `${apiBase}${url}`;
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-6 space-y-8 text-gray-900 dark:text-gray-100">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="title">Smart Albums</h1>
          <p className="text-gray-600 dark:text-gray-400 text-sm mt-1">
            AI-organized photo collections based on content and themes
          </p>
        </div>
        
        <div className="flex gap-3">
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn-primary px-4 py-2 text-sm"
          >
            Create Album
          </button>
          <button
            onClick={handleRebuild}
            disabled={rebuilding}
            className="btn-secondary px-4 py-2 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {rebuilding ? "Creating..." : "Add AI Albums"}
          </button>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 border-b border-gray-200 dark:border-gray-700">
        <button
          onClick={() => setFilter("all")}
          className={`px-4 py-2 font-medium transition border-b-2 ${
            filter === "all"
              ? "text-brand-blue border-brand-blue"
              : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 border-transparent"
          }`}
        >
          All Albums
        </button>
        <button
          onClick={() => setFilter("auto")}
          className={`px-4 py-2 font-medium transition border-b-2 ${
            filter === "auto"
              ? "text-brand-blue border-brand-blue"
              : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 border-transparent"
          }`}
        >
          AI Generated
        </button>
        <button
          onClick={() => setFilter("manual")}
          className={`px-4 py-2 font-medium transition border-b-2 ${
            filter === "manual"
              ? "text-brand-blue border-brand-blue"
              : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 border-transparent"
          }`}
        >
          Manual
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl">
          <p className="text-red-800 dark:text-red-200">{error}</p>
        </div>
      )}

        {/* Loading State */}
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <Loader />
          </div>
        ) : albums.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-gray-600 dark:text-gray-400 text-lg mb-4">
              No albums found
            </p>
            <p className="text-gray-500 dark:text-gray-500 text-sm">
              Upload some photos and they will be automatically organized into smart albums
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {albums.map((album) => (
              <div
                key={album.id}
                className="rounded-xl overflow-hidden border transition bg-brand-light border-gray-200 hover:border-brand-blue/70 dark:bg-brand-dark dark:border-gray-700 dark:hover:border-brand-blue shadow-sm cursor-pointer"
                onClick={() => handleAlbumClick(album)}
              >
                {/* Album Cover */}
                <div className="aspect-video bg-gray-200 dark:bg-gray-700 overflow-hidden">
                  {album.cover_url ? (
                    <img
                      src={getImageUrl(album.cover_url)}
                      alt={album.title}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-gray-400">
                      <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                  )}
                </div>

                {/* Album Info */}
                <div className="p-3">
                  <div className="flex justify-between items-start mb-1">
                    <h3 className="font-medium truncate text-gray-900 dark:text-gray-200">
                      {album.title}
                    </h3>
                    {album.is_auto_generated && (
                      <span className="text-xs px-2 py-0.5 bg-brand-blue/10 text-brand-blue rounded-full ml-2 flex-shrink-0">
                        AI
                      </span>
                    )}
                  </div>
                  
                  {album.description && (
                    <p className="text-xs text-gray-600 dark:text-gray-400 mb-2 line-clamp-1">
                      {album.description}
                    </p>
                  )}
                  
                  <div className="flex justify-between items-center text-xs text-gray-500 dark:text-gray-500">
                    <span>{album.media_count} {album.media_count === 1 ? 'photo' : 'photos'}</span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeleteAlbum(album.id);
                      }}
                      className="text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Album Detail Modal */}
        {selectedAlbum && (
          <div
            className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
            onClick={() => setSelectedAlbum(null)}
          >
            <div
              className="bg-brand-light dark:bg-brand-dark rounded-xl border border-gray-200 dark:border-gray-700 max-w-4xl w-full max-h-[90vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Modal Header */}
              <div className="sticky top-0 bg-brand-light dark:bg-brand-dark border-b border-gray-200 dark:border-gray-700 p-6">
                <div className="flex justify-between items-start">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-200 mb-2">
                      {selectedAlbum.title}
                    </h2>
                    {selectedAlbum.description && (
                      <p className="text-gray-600 dark:text-gray-400">
                        {selectedAlbum.description}
                      </p>
                    )}
                    <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                      {selectedAlbum.media_items?.length || 0} photos
                      {selectedAlbum.is_auto_generated && " • AI Generated"}
                    </p>
                  </div>
                  <button
                    onClick={() => setSelectedAlbum(null)}
                    className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>

              {/* Modal Content - Photo Grid */}
              <div className="p-6">
                {selectedAlbum.media_items && selectedAlbum.media_items.length > 0 ? (
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {selectedAlbum.media_items.map((media) => (
                      <div
                        key={media.id}
                        className="aspect-square bg-gray-200 dark:bg-gray-700 rounded-xl overflow-hidden hover:opacity-80 transition cursor-pointer"
                        onClick={() => window.open(getImageUrl(media.file_url), "_blank")}
                      >
                        <img
                          src={getImageUrl(media.file_url)}
                          alt={media.caption || "Photo"}
                          className="w-full h-full object-cover"
                        />
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-center text-gray-500 dark:text-gray-400 py-8">
                    No photos in this album
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Create Album Modal */}
        {showCreateModal && (
          <div
            className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
            onClick={() => {
              setShowCreateModal(false);
              setSelectedMediaIds([]);
            }}
          >
            <div
              className="bg-brand-light dark:bg-brand-dark rounded-xl border border-gray-200 dark:border-gray-700 max-w-2xl w-full p-6"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Modal Header */}
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-200">
                  Create New Album
                </h2>
                <button
                  onClick={() => {
                    setShowCreateModal(false);
                    setSelectedMediaIds([]);
                  }}
                  className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {/* Mode Tabs */}
              <div className="flex gap-2 mb-6 border-b border-gray-200 dark:border-gray-700">
                <button
                  onClick={() => setCreateMode("prompt")}
                  className={`px-4 py-2 font-medium transition ${
                    createMode === "prompt"
                      ? "text-brand-blue border-b-2 border-brand-blue"
                      : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100"
                  }`}
                >
                  AI Search
                </button>
                <button
                  onClick={() => setCreateMode("manual")}
                  className={`px-4 py-2 font-medium transition ${
                    createMode === "manual"
                      ? "text-brand-blue border-b-2 border-brand-blue"
                      : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100"
                  }`}
                >
                  Manual
                </button>
              </div>

              {/* Create Form */}
              <form onSubmit={handleCreateAlbum}>
                {createMode === "prompt" ? (
                  <>
                    <div className="mb-4">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Describe the photos you want
                      </label>
                      <textarea
                        name="prompt"
                        required
                        rows={4}
                        placeholder="E.g., 'all photos with dogs', 'sunset beach pictures', 'photos of people smiling outdoors'"
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:ring-2 focus:ring-brand-blue focus:border-transparent"
                      />
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                        Use natural language to describe what photos to include. AI will search your library.
                      </p>
                    </div>
                    
                    <div className="mb-6">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Album Title (Optional)
                      </label>
                      <input
                        type="text"
                        name="title"
                        placeholder="Leave blank to auto-generate from prompt"
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:ring-2 focus:ring-brand-blue focus:border-transparent"
                      />
                    </div>
                  </>
                ) : (
                  <>
                    <div className="mb-4">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Album Title
                      </label>
                      <input
                        type="text"
                        name="title"
                        required
                        placeholder="E.g., 'Summer Vacation 2024'"
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:ring-2 focus:ring-brand-blue focus:border-transparent"
                      />
                    </div>

                    <div className="mb-6">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Select Photos (Optional)
                      </label>
                      
                      {loadingMedia ? (
                        <div className="flex justify-center py-8">
                          <Loader />
                        </div>
                      ) : allMedia.length === 0 ? (
                        <p className="text-sm text-gray-500 dark:text-gray-400 py-4">
                          No photos available. Upload photos first.
                        </p>
                      ) : (
                        <div className="max-h-64 overflow-y-auto border border-gray-300 dark:border-gray-600 rounded-lg p-2 bg-gray-50 dark:bg-gray-800">
                          <div className="grid grid-cols-4 gap-2">
                            {allMedia.map((media) => (
                              <div
                                key={media.id}
                                onClick={() => toggleMediaSelection(media.id)}
                                className={`relative aspect-square rounded-lg overflow-hidden cursor-pointer border-2 transition ${
                                  selectedMediaIds.includes(media.id)
                                    ? "border-brand-blue ring-2 ring-brand-blue"
                                    : "border-transparent hover:border-gray-400 dark:hover:border-gray-500"
                                }`}
                              >
                                <img
                                  src={getImageUrl(media.url)}
                                  alt={media.filename}
                                  className="w-full h-full object-cover"
                                />
                                {selectedMediaIds.includes(media.id) && (
                                  <div className="absolute top-1 right-1 bg-brand-blue text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">
                                    ✓
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                        Selected: {selectedMediaIds.length} photos
                      </p>
                    </div>
                  </>
                )}

                {/* Action Buttons */}
                <div className="flex justify-end gap-3">
                  <button
                    type="button"
                    onClick={() => {
                      setShowCreateModal(false);
                      setSelectedMediaIds([]);
                    }}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={creating}
                    className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {creating ? "Creating..." : "Create Album"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
    </div>
  );
}
