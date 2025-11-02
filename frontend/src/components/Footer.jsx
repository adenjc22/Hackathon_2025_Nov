import { Link } from "react-router-dom";
import { FaLinkedin, FaGithub } from "react-icons/fa";

export default function Footer() {
  const linkedIns = [
    { name: "Thomas Crone", url: "https://www.linkedin.com/in/thomas-crone-bb807b214/" },
    { name: "Aden Campbell", url: "https://www.linkedin.com/in/aden-campbell-229422381/" },
    { name: "Louis Gunther", url: "https://www.linkedin.com/in/louis-gunther-mcgee-241837293/" },
  ];

  const githubs = [
    { name: "ThomasCrone4", url: "https://github.com/ThomasCrone4" },
    { name: "adenjc22", url: "https://github.com/adenjc22" },
    { name: "louisgunther-06", url: "https://github.com/louisgunther-06" },
  ];

  return (
    <footer className="mt-16 border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-brand-dark">
      <div className="mx-auto max-w-6xl px-4 py-8">
        {/* Links Row */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 mb-4">
          {/* LinkedIn Links - Left */}
          <div className="flex items-start gap-4">
            <FaLinkedin className="text-brand-blue text-xl mt-0.5" />
            <div className="flex flex-col gap-2">
              {linkedIns.map((person, idx) => (
                <a
                  key={idx}
                  href={person.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-gray-600 hover:text-brand-blue dark:text-gray-400 dark:hover:text-brand-blue transition"
                >
                  {person.name}
                </a>
              ))}
            </div>
          </div>

          {/* GitHub Links - Right */}
          <div className="flex items-start gap-4">
            <FaGithub className="text-gray-800 dark:text-gray-300 text-xl mt-0.5" />
            <div className="flex flex-col gap-2">
              {githubs.map((person, idx) => (
                <a
                  key={idx}
                  href={person.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-gray-600 hover:text-brand-blue dark:text-gray-400 dark:hover:text-brand-blue transition"
                >
                  {person.name}
                </a>
              ))}
            </div>
          </div>
        </div>

        {/* Copyright */}
        <p className="text-xs text-left text-gray-500 dark:text-gray-500">
          Made with ❤️ at DurHack 2025 · Powered by FastAPI & React
        </p>
      </div>
    </footer>
  );
}
