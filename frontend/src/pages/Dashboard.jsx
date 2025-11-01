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
    const { data } = await api.get("/api/upload/media"); // GET list
    setItems(data || []);
    setPoll(data?.some((m) => m.status !== "done"));
  };

  useEffect(() => { load(); }, []);
  useEffect(() => {
    if (!poll) return;
    const id = setInterval(load, 3000);
    return () => clearInterval(id);
  }, [poll]);

  if (!user) return <p className="p-6">Please log in.</p>;
  return (
    <div className="mx-auto max-w-6xl p-4 space-y-6">
      <UploadForm onComplete={load}/>
      <MediaGrid items={items}/>
    </div>
  );
}
