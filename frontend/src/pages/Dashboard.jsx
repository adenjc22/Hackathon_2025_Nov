import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth";
import UploadForm from "../components/UploadForm";
import MediaGrid from "../components/MediaGrid";
import { api } from "../utils/api";

export default function Dashboard() {
  const { user } = useAuth();
  const [items, setItems] = useState([]);
  const [poll, setPoll] = useState(false);

  const load = async () => {
    try {
      const { data } = await api.get("/api/upload/media/");
      // Transform the backend response to match MediaGrid's expected format
      const transformedData = data.map((item) => ({
        id: item.id,
        fileName: item.filename,
        fileUrl: `http://localhost:8000${item.file_url}`,
        mimeType: item.mime_type,
        status: "done", // Since we're not processing, mark as done
        createdAt: item.created_at,
      }));
      setItems(transformedData || []);
      setPoll(false); // No need to poll since we're not doing background processing
    } catch (err) {
      console.error("Failed to load media:", err);
    }
  };

  useEffect(() => {
    load();
  }, []);
  useEffect(() => {
    if (!poll) return;
    const id = setInterval(load, 3000);
    return () => clearInterval(id);
  }, [poll]);

  if (!user)
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-gray-600 dark:text-gray-400">
        <p className="text-lg">Please log in to view your dashboard.</p>
      </div>
    );

  return (
    <div className="mx-auto max-w-6xl px-4 py-6 space-y-8 text-gray-900 dark:text-gray-100">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <h1 className="title">Dashboard</h1>
        <button
          onClick={load}
          className="btn-secondary text-sm"
          title="Refresh media"
        >
          Refresh
        </button>
      </div>

      {/* Upload section */}
      <div className="p-4 rounded-xl border bg-brand-light border-gray-200 shadow-lg dark:bg-brand-dark dark:border-gray-700">
        <h2 className="text-lg font-medium text-gray-900 dark:text-gray-300 mb-3">
          Upload new media
        </h2>
        <UploadForm onComplete={load} />
      </div>

      {/* Media grid */}
      <div className="p-4 rounded-xl border bg-brand-light border-gray-200 shadow-lg dark:bg-brand-dark dark:border-gray-700">
        <h2 className="text-lg font-medium text-gray-900 dark:text-gray-300 mb-3">
          Your uploads
        </h2>
        <MediaGrid
          items={items}
          onDelete={(id) => setItems((prev) => prev.filter((m) => m.id !== id))}
        />
      </div>
    </div>
  );
}
