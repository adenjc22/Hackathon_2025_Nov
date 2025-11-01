import { useState } from "react";
import { api } from "../utils/api";

export default function UploadForm({ onComplete }) {
  const [files, setFiles] = useState([]);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  const handleUpload = async () => {
    if (!files.length) return;
    setBusy(true); setErr("");
    const fd = new FormData();
    files.forEach((f) => fd.append("files", f));
    try {
      await api.post("/api/upload/media", fd, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      onComplete?.();
      setFiles([]);
    } catch (e) {
      setErr(e?.response?.data?.detail || e.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="rounded-xl border p-4">
      <input
        multiple
        accept="image/*,video/*"
        type="file"
        onChange={(e) => setFiles(Array.from(e.target.files || []))}
      />
      <div className="mt-3 flex items-center gap-3">
        <button
          onClick={handleUpload}
          disabled={busy || !files.length}
          className="px-3 py-2 bg-black text-white rounded-lg disabled:opacity-50"
        >
          {busy ? "Uploading…" : `Upload ${files.length || ""}`}
        </button>
        {err && <p className="text-sm text-red-600">{err}</p>}
      </div>
    </div>
  );
}
