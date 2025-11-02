import { Link } from "react-router-dom";
import { useEffect } from "react";

export default function Home() {
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/health/");
        console.log("health status", res.status, await res.json());
      } catch (e) {
        console.error("health fetch failed", e);
      }
    })();
  }, []);

  return (
    <div className="mx-auto max-w-4xl px-6 py-16 text-center text-gray-900 dark:text-gray-100">
      <h1 className="title text-4xl sm:text-5xl pb-2 sm:pb-3 mb-10 leading-[1.25]">
        Legacy Album
      </h1>

      <p className="text-lg max-w-2xl mx-auto mb-8 text-gray-700 dark:text-gray-400">
        Preserve your memories with the power of AI.
        Upload photos and videos, we’ll automatically organize them
        into albums, generate captions, and help you rediscover your best moments.
      </p>

      <div className="flex flex-wrap justify-center gap-4 mb-12">
        <Link to="/dashboard" className="btn-primary text-lg px-5 py-3 rounded-xl">
          Get Started
        </Link>
        <Link to="/signup" className="btn-secondary text-lg px-5 py-3 rounded-xl">
          Create an Account
        </Link>
      </div>

      <div className="grid sm:grid-cols-3 gap-6 text-left mt-12">
        {/* cards... */}
      </div>
    </div>
  );
}
