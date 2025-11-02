import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../utils/api";
import { FaUpload, FaCheckCircle } from "react-icons/fa";

export default function Upload() {
  const navigate = useNavigate();
  const [files, setFiles] = useState([]);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const [success, setSuccess] = useState(false);
  const [drag, setDrag] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!files.length) return;
    
    setBusy(true);
    setErr("");
    setSuccess(false);

    try {
      // Upload each file individually to /api/upload/media/ endpoint
      const uploadPromises = files.map(async (file) => {
        const fd = new FormData();
        fd.append("file", file);
        return api.post("/api/upload/media/", fd, {
          headers: { "Content-Type": "multipart/form-data" },
        });
      });

      await Promise.all(uploadPromises);
      setSuccess(true);
      setFiles([]);
      
      // Redirect to dashboard after 2 seconds
      setTimeout(() => {
        navigate("/dashboard");
      }, 2000);
    } catch (e) {
      setErr(e?.response?.data?.detail || e.message);
    } finally {
      setBusy(false);
    }
  };

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files || []);
    setFiles(selectedFiles);
    setSuccess(false);
    setErr("");
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDrag(false);
    const droppedFiles = Array.from(e.dataTransfer.files || []);
    setFiles(droppedFiles);
    setSuccess(false);
    setErr("");
  };

  return (
    <div className="mx-auto max-w-2xl px-4 py-10">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-2 text-gray-900 dark:text-gray-100">
          Upload Your Images
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Share your memories by uploading photos to your album
        </p>
      </div>

      {/* Upload Card */}
      <div className="rounded-xl border shadow-lg p-8
                      bg-brand-light border-gray-200
                      dark:bg-brand-dark dark:border-gray-700">
        
        {/* Drop Zone */}
        <div
          className={`
            rounded-xl p-10 text-center transition-all
            border-2 border-dashed
            ${drag 
              ? "border-brand-blue bg-blue-50 dark:bg-blue-900/20 shadow-[0_0_20px_#00bfff40]" 
              : "border-gray-300 dark:border-gray-600 hover:border-brand-blue/50"
            }
          `}
          onDragOver={(e) => {
            e.preventDefault();
            setDrag(true);
          }}
          onDragLeave={() => setDrag(false)}
          onDrop={handleDrop}
        >
          <div className="flex flex-col items-center gap-4">
            <FaUpload
              className={`text-5xl transition-colors ${
                drag 
                  ? "text-brand-blue" 
                  : "text-gray-400 dark:text-gray-500"
              }`}
            />

            <div>
              <p className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-1">
                {files.length
                  ? `${files.length} file${files.length > 1 ? "s" : ""} selected`
                  : "Drag and drop your images here"}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                or click below to browse
              </p>
            </div>

            <input
              multiple
              accept="image/jpeg,image/png"
              type="file"
              className="hidden"
              id="file-input"
              onChange={handleFileChange}
            />
            <label
              htmlFor="file-input"
              className="cursor-pointer inline-block px-6 py-3 rounded-lg
                         bg-gray-200 hover:bg-gray-300 text-gray-800
                         dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-gray-100
                         transition-colors font-medium"
            >
              Browse Files
            </label>

            <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
              Supported formats: JPEG, PNG • Max size: 10MB per file
            </p>
          </div>
        </div>

        {/* Selected Files Preview */}
        {files.length > 0 && (
          <div className="mt-6">
            <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Selected Files:
            </h3>
            <ul className="space-y-1 max-h-40 overflow-y-auto">
              {files.map((file, idx) => (
                <li 
                  key={idx} 
                  className="text-sm text-gray-600 dark:text-gray-400 flex items-center gap-2"
                >
                  <span className="text-brand-blue">•</span>
                  <span className="truncate">{file.name}</span>
                  <span className="text-xs text-gray-500">
                    ({(file.size / 1024 / 1024).toFixed(2)} MB)
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Error Message */}
        {err && (
          <div
            className="mt-6 text-sm rounded-lg px-4 py-3
                       text-red-700 bg-red-100 border border-red-300
                       dark:text-red-300 dark:bg-red-900/30 dark:border-red-700/50"
            role="alert"
          >
            <strong>Error:</strong> {err}
          </div>
        )}

        {/* Success Message */}
        {success && (
          <div
            className="mt-6 text-sm rounded-lg px-4 py-3 flex items-center gap-2
                       text-green-700 bg-green-100 border border-green-300
                       dark:text-green-300 dark:bg-green-900/30 dark:border-green-700/50"
            role="alert"
          >
            <FaCheckCircle className="text-lg" />
            <span>
              <strong>Success!</strong> Your images have been uploaded. Redirecting to dashboard...
            </span>
          </div>
        )}

        {/* Action Buttons */}
        <div className="mt-6 flex flex-col sm:flex-row gap-3 justify-center">
          <button
            onClick={handleUpload}
            disabled={busy || !files.length || success}
            className="btn-primary px-8 py-3 rounded-lg disabled:opacity-50 
                       disabled:cursor-not-allowed text-base font-medium"
          >
            {busy ? "Uploading..." : `Upload ${files.length || ""} ${files.length === 1 ? "Image" : "Images"}`}
          </button>

          <button
            onClick={() => navigate("/dashboard")}
            disabled={busy}
            className="px-8 py-3 rounded-lg text-base font-medium
                       bg-gray-200 hover:bg-gray-300 text-gray-800
                       dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-gray-100
                       transition-colors disabled:opacity-50"
          >
            Skip for Now
          </button>
        </div>
      </div>
    </div>
  );
}
