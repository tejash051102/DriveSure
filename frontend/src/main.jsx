import React from "react";
import ReactDOM from "react-dom/client";
import { HashRouter } from "react-router-dom";
import { SpeedInsights } from "@vercel/speed-insights/react";
import { Analytics } from "@vercel/analytics/react";
import App from "./App.jsx";
import "./index.css";
import { applyTheme, getStoredTheme } from "./utils/theme.js";

applyTheme(getStoredTheme());

const ignoredRuntimeMessages = [
  "A listener indicated an asynchronous response by returning true, but the message channel closed before a response was received"
];

const ignoredWarnings = [
  "Using DEFAULT root logger",
  "[DEFAULT]: WARN : Using DEFAULT root logger"
];

const originalWarn = console.warn.bind(console);
console.warn = (...args) => {
  const message = args.map((arg) => String(arg)).join(" ");
  if (ignoredWarnings.some((warning) => message.includes(warning))) return;
  originalWarn(...args);
};

window.addEventListener("unhandledrejection", (event) => {
  const message = String(event.reason?.message || event.reason || "");
  if (ignoredRuntimeMessages.some((ignored) => message.includes(ignored))) {
    event.preventDefault();
  }
});

try {
  window.history.replaceState(null, "", window.location.href);
} catch {
  // Ignore browsers that reject history state cleanup.
}

const isVercelIntegrationEnabled = (() => {
  try {
    const fromEnv = (import.meta && import.meta.env && import.meta.env.VITE_ENABLE_VERCEL_ANALYTICS === "true");
    const hostname = typeof window !== "undefined" ? window.location.hostname : "";
    const onVercelHost = hostname.endsWith('.vercel.app') || hostname.endsWith('.vercel.sh');
    return fromEnv || onVercelHost;
  } catch {
    return false;
  }
})();

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <HashRouter>
      <App />
    </HashRouter>
    {isVercelIntegrationEnabled && <SpeedInsights />}
    {isVercelIntegrationEnabled && <Analytics />}
  </React.StrictMode>
);
