import { useEffect, useState } from "react";
import { FaMoon, FaSun } from "react-icons/fa";

export default function ThemeToggle() {
  const [dark, setDark] = useState(
    document.documentElement.classList.contains("dark")
  );

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  return (
    <button
      onClick={() => setDark(!dark)}
      className="fixed bottom-4 right-4 p-3 rounded-full bg-gray-700 hover:bg-brand-blue text-white transition"
      title="Toggle dark mode"
    >
      {dark ? <FaSun /> : <FaMoon />}
    </button>
  );
}
