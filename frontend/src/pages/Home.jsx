import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="mx-auto max-w-4xl px-6 py-16 text-center text-gray-900 dark:text-gray-100">
      {/* Hero Section */}
      <h1 className="title text-4xl sm:text-5xl pb-2 sm:pb-3 leading-[1.25]">
        Memory Lane
      </h1>
      
      <h2 className="text-xl sm:text-2xl font-semibold text-gray-600 dark:text-gray-400 mb-6">
        Intelligent archiving for generations
      </h2>

      <p className="text-base max-w-2xl mx-auto mb-8 text-gray-700 dark:text-gray-400">
        Organize your family's photo collection with AI-powered facial recognition and smart tagging. 
        Preserve precious memories and make them easily accessible for future generations.
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
          <h3 className="font-semibold text-brand-blue mb-2"> Facial Recognition</h3>
          <p className="text-sm text-gray-700 dark:text-gray-400">
            Automatically identify and group family members across your entire photo collection.
          </p>
        </div>

        <div className="rounded-xl border p-5 transition hover:border-brand-blue
                        bg-brand-light border-gray-200
                        dark:bg-brand-dark dark:border-gray-700">
          <h3 className="font-semibold text-brand-blue mb-2">Smart Tagging</h3>
          <p className="text-sm text-gray-700 dark:text-gray-400">
            AI analyzes and tags photos with scenes, objects, and events for effortless searching.
          </p>
        </div>

        <div className="rounded-xl border p-5 transition hover:border-brand-blue
                        bg-brand-light border-gray-200
                        dark:bg-brand-dark dark:border-gray-700">
          <h3 className="font-semibold text-brand-blue mb-2">Family Archive</h3>
          <p className="text-sm text-gray-700 dark:text-gray-400">
            Build a secure digital legacy that your family can treasure for generations to come.
          </p>
        </div>
      </div>
    </div>
  );
}
