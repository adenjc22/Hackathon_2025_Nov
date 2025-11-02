import { useEffect, useState } from "react";
import { api, API_BASE } from "../utils/api";
import { FaUser, FaEdit, FaTrash, FaImages } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

export default function People() {
  const navigate = useNavigate();
  const [people, setPeople] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState("");

  const loadPeople = async () => {
    try {
      const { data } = await api.get("/api/people/");
      setPeople(data);
    } catch (err) {
      console.error("Failed to load people:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPeople();
  }, []);

  const handleUpdateName = async (personId) => {
    try {
      await api.patch(`/api/people/${personId}`, { name: editName });
      setEditingId(null);
      setEditName("");
      loadPeople();
    } catch (err) {
      console.error("Failed to update name:", err);
    }
  };

  const handleDelete = async (personId) => {
    if (!confirm("Are you sure you want to delete this person?")) return;
    
    try {
      await api.delete(`/api/people/${personId}`);
      loadPeople();
    } catch (err) {
      console.error("Failed to delete person:", err);
    }
  };

  const viewPhotos = async (personId) => {
    try {
      const { data } = await api.get(`/api/people/${personId}/photos`);
      // Navigate to dashboard with filter for these photos
      navigate(`/dashboard?person=${personId}`);
    } catch (err) {
      console.error("Failed to load photos:", err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-gray-600 dark:text-gray-400">Loading people...</div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-6 text-gray-900 dark:text-gray-100">
      {/* Header */}
      <div className="mb-8">
        <h1 className="title">People</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Recognize and name people in your photos
        </p>
      </div>

      {/* People Grid */}
      {people.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 dark:bg-gray-800 rounded-xl">
          <FaUser className="mx-auto text-6xl text-gray-300 dark:text-gray-600 mb-4" />
          <p className="text-gray-600 dark:text-gray-400">
            No people detected yet. Upload some photos with faces!
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {people.map((person) => (
            <div
              key={person.id}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow"
            >
              {/* Thumbnail */}
              <div className="aspect-square bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center">
                  {person.thumbnail_url ? (
                  <img
                    src={`${API_BASE || (import.meta.env.PROD ? 'https://memory-lane-backend.up.railway.app' : 'http://localhost:8000')}${person.thumbnail_url}`}
                    alt={person.name || "Unknown"}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <FaUser className="text-6xl text-white/50" />
                )}
              </div>

              {/* Info */}
              <div className="p-4">
                {editingId === person.id ? (
                  <div className="flex gap-2 mb-2">
                    <input
                      type="text"
                      value={editName}
                      onChange={(e) => setEditName(e.target.value)}
                      placeholder="Enter name..."
                      className="flex-1 px-3 py-1 text-sm rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700"
                      autoFocus
                      onKeyDown={(e) => {
                        if (e.key === "Enter") handleUpdateName(person.id);
                        if (e.key === "Escape") setEditingId(null);
                      }}
                    />
                    <button
                      onClick={() => handleUpdateName(person.id)}
                      className="px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600"
                    >
                      Save
                    </button>
                  </div>
                ) : (
                  <h3 className="font-semibold text-lg mb-2 truncate">
                    {person.name || "Unknown Person"}
                  </h3>
                )}

                <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                  {person.photo_count} {person.photo_count === 1 ? "photo" : "photos"}
                </p>

                {/* Actions */}
                <div className="flex gap-2">
                  <button
                    onClick={() => viewPhotos(person.id)}
                    className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors"
                    title="View photos"
                  >
                    <FaImages className="text-sm" />
                    <span className="text-sm">View</span>
                  </button>
                  <button
                    onClick={() => {
                      setEditingId(person.id);
                      setEditName(person.name || "");
                    }}
                    className="px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                    title="Edit name"
                  >
                    <FaEdit />
                  </button>
                  <button
                    onClick={() => handleDelete(person.id)}
                    className="px-3 py-2 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors"
                    title="Delete"
                  >
                    <FaTrash />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Info Box */}
      <div className="mt-8 p-6 bg-blue-50 dark:bg-blue-900/20 rounded-xl border border-blue-200 dark:border-blue-800">
        <h3 className="font-semibold mb-2 text-blue-900 dark:text-blue-300">
          How it works
        </h3>
        <ul className="text-sm text-blue-800 dark:text-blue-400 space-y-1 list-disc list-inside">
          <li>Upload photos with faces to automatically detect people</li>
          <li>Similar faces are grouped together using AI</li>
          <li>Click "Edit" to assign names to people</li>
          <li>Click "View" to see all photos of a specific person</li>
        </ul>
      </div>
    </div>
  );
}
