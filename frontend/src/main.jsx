// src/main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./styles/globals.css";

async function bootstrap() {
   if (import.meta.env.DEV) {
    const { worker } = await import("./mocks/browser");
    await worker.start({
      onUnhandledRequest: "bypass",
      serviceWorker: {
        // ensures correct path even if BASE_URL changes
        url: `${import.meta.env.BASE_URL}mockServiceWorker.js`,
      },
    });
  }

  ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode><App /></React.StrictMode>
  );
}
bootstrap();
