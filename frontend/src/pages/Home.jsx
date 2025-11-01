import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="mx-auto max-w-4xl px-6 py-16 text-center text-gray-900 dark:text-gray-100">
      {/* Hero Section */}
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

      {/* Feature Highlights */}
      <div className="grid sm:grid-cols-3 gap-6 text-left mt-12">
        <div className="rounded-xl border p-5 transition hover:border-brand-blue
                        bg-brand-light border-gray-200
                        dark:bg-brand-dark dark:border-gray-700">
          <h3 className="font-semibold text-brand-blue mb-2">✨ Smart Albums</h3>
          <p className="text-sm text-gray-700 dark:text-gray-400">
            AI automatically groups your uploads by theme, emotion, and location.
          </p>
        </div>

        <div className="rounded-xl border p-5 transition hover:border-brand-blue
                        bg-brand-light border-gray-200
                        dark:bg-brand-dark dark:border-gray-700">
          <h3 className="font-semibold text-brand-blue mb-2">🧠 Intelligent Search</h3>
          <p className="text-sm text-gray-700 dark:text-gray-400">
            Find any photo using natural language — “me at the beach in 2022”.
          </p>
        </div>

        <div className="rounded-xl border p-5 transition hover:border-brand-blue
                        bg-brand-light border-gray-200
                        dark:bg-brand-dark dark:border-gray-700">
          <h3 className="font-semibold text-brand-blue mb-2">🔒 Private & Secure</h3>
          <p className="text-sm text-gray-700 dark:text-gray-400">
            Your memories stay safe and private. You control what you share.
          </p>
        </div>
      </div>
    </div>
  );
}
