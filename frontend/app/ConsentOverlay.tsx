"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Mic, ShieldCheck } from "lucide-react";

export function ConsentOverlay({ onAccept }: { onAccept: () => void }) {
  const [acknowledged, setAcknowledged] = useState(false);

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="consent-heading"
      className="fixed inset-0 z-50 flex items-center justify-center bg-[#0F1113]/90 backdrop-blur-sm px-6"
    >
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, ease: "easeOut" }}
        className="w-full max-w-[480px] rounded-[20px] border border-white/[0.08] bg-[#181B1E] p-8"
      >
        <div className="flex h-11 w-11 items-center justify-center rounded-full bg-[#E8A33D]/10">
          <Mic className="h-5 w-5 text-[#E8A33D]" strokeWidth={2} />
        </div>

        <h2
          id="consent-heading"
          className="mt-5 text-[19px] font-semibold tracking-tight text-[#EDEDE8]"
        >
          Before you begin
        </h2>

        <p className="mt-2 text-[14px] leading-relaxed text-[#EDEDE8]/60">
          This tool analyzes a short recording of your voice to score your
          English pronunciation. Here&apos;s exactly what that involves:
        </p>

        <ul className="mt-5 flex flex-col gap-3">
          <ConsentPoint>
            Your audio is sent to our AI providers (Groq, OpenAI) solely to
            generate a transcript and pronunciation feedback.
          </ConsentPoint>
          <ConsentPoint>
            Your recording is <strong className="text-[#EDEDE8]">never stored</strong> —
            it&apos;s deleted from our server immediately after analysis completes.
          </ConsentPoint>
          <ConsentPoint>
            We don&apos;t create an account, keep history, or use your voice
            for anything beyond generating your result on this page.
          </ConsentPoint>
        </ul>

        <label className="mt-6 flex cursor-pointer items-start gap-3 rounded-xl border border-white/[0.08] bg-[#0F1113] p-4">
          <input
            type="checkbox"
            checked={acknowledged}
            onChange={(e) => setAcknowledged(e.target.checked)}
            className="mt-0.5 h-4 w-4 shrink-0 accent-[#E8A33D]"
          />
          <span className="text-[13px] leading-relaxed text-[#EDEDE8]/70">
            I understand and consent to my audio being processed as described
            above, in line with applicable data protection law.
          </span>
        </label>

        <button
          onClick={onAccept}
          disabled={!acknowledged}
          className="mt-5 flex h-12 w-full items-center justify-center gap-2 rounded-full bg-[#E8A33D] text-[14px] font-medium text-[#0F1113] transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-30"
        >
          <ShieldCheck className="h-4 w-4" />
          Accept and continue
        </button>

        <p className="mt-4 font-mono text-[11px] uppercase tracking-widest text-[#EDEDE8]/30">
          No account required · No audio retained
        </p>
      </motion.div>
    </div>
  );
}

function ConsentPoint({ children }: { children: React.ReactNode }) {
  return (
    <li className="flex gap-2.5 text-[13px] leading-relaxed text-[#EDEDE8]/70">
      <span className="mt-[7px] h-1 w-1 shrink-0 rounded-full bg-[#E8A33D]/60" />
      {children}
    </li>
  );
}