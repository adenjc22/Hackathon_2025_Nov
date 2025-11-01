import { useState } from "react";
import { api } from "../utils/api";
import { FaUpload } from "react-icons/fa";

export default function UploadForm({ onComplete }) {
  const [files, setFiles] = useState([]);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const [drag, setDrag] = useState(false);

  const handleUpload = async () => {
    if (!files.length) return;
    setBusy(true);
    setErr("");
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
    <div
      className={`
        rounded-xl p-6 text-center transition
        border bg-brand-light border-gray-200
        hover:border-brand-blue/70
        dark:bg-brand-dark dark:border-gray-700 dark:hover:border-brand-blue/70
        ${drag ? "border-brand-blue shadow-[0_0_10px_#00bfff80]" : ""}
      `}
      onDragOver={(e) => {
        e.preventDefault();
        setDrag(true);
      }}
      onDragLeave={() => setDrag(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDrag(false);
        setFiles(Array.from(e.dataTransfer.files || []));
      }}
    >
      {/* Upload area */}
      <div className="flex flex-col items-center gap-3 text-gray-700 dark:text-gray-300">
        <FaUpload
          className={`text-3xl ${
            drag ? "text-brand-blue" : "text-gray-400 dark:text-gray-500"
          }`}
        />

        <p className="text-sm">
          {files.length
            ? `${files.length} file${files.length > 1 ? "s" : ""} selected`
            : "Drag and drop files here, or click to choose"}
        </p>

        <input
          multiple
          accept="image/*,video/*"
          type="file"
          className="hidden"
          id="file-input"
          onChange={(e) => setFiles(Array.from(e.target.files || []))}
        />
        <label
          htmlFor="file-input"
          className="cursor-pointer mt-2 inline-block btn-secondary text-sm"
        >
          Choose Files
        </label>
      </div>

      {/* Action row */}
      <div className="mt-5 flex flex-col sm:flex-row items-center justify-center gap-3">
        <button
          onClick={handleUpload}
          disabled={busy || !files.length}
          className="btn-primary disabled:opacity-50"
        >
          {busy ? "Uploading…" : `Upload ${files.length || ""}`}
        </button>

        {err && (
          <p className="text-sm text-red-600 dark:text-red-400" role="alert">
            {err}
          </p>
        )}
      </div>
    </div>
  );
}
