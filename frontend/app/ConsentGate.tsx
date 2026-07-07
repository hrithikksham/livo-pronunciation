"use client";

import { useState } from "react";

import { ConsentOverlay } from "./ConsentOverlay";

// Bump this whenever the consent text materially changes — bumping it
// invalidates any previously stored acceptance, so returning users are
// re-prompted under the new terms rather than silently grandfathered in.
const CONSENT_VERSION = "1.0";
const STORAGE_KEY = "livo_consent_v";

type ConsentStatus = "checking" | "required" | "granted";

export function ConsentGate({ children }: { children: React.ReactNode }) {
  const [status, setStatus] = useState<ConsentStatus>(() => {
    try {
      return window.localStorage.getItem(STORAGE_KEY) === CONSENT_VERSION
        ? "granted"
        : "required";
    } catch {
      // localStorage unavailable (e.g. private browsing edge cases) —
      // fail safe by requiring consent every load rather than assuming it.
      return "required";
    }
  });

  function handleAccept() {
    try {
      window.localStorage.setItem(STORAGE_KEY, CONSENT_VERSION);
    } catch {
      // If we can't persist it, the user will just see the overlay again
      // next load — acceptable degradation, never a broken app.
    }
    setStatus("granted");
  }

  // Render nothing meaningful until we know consent state — avoids a
  // flash of the app before the gate can appear.
  if (status === "checking") {
    return <div className="min-h-screen bg-[#0F1113]" />;
  }

  return (
    <>
      {/* App renders underneath, but is inert until consent is granted —
          this keeps layout/mount cost identical rather than conditionally
          mounting the whole app tree on accept. */}
      <div
        aria-hidden={status !== "granted"}
        className={status !== "granted" ? "pointer-events-none select-none" : ""}
      >
        {children}
      </div>

      {status === "required" && <ConsentOverlay onAccept={handleAccept} />}
    </>
  );
}