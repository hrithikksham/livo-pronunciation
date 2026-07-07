"use client";

import { ChangeEvent, DragEvent, useState } from "react";
import { motion, AnimatePresence, type Variants } from "framer-motion";
import { RotateCcw, ArrowRight, CheckCircle2, AlertCircle } from "lucide-react";

import { useAnalysis } from "@/hooks/useAnalysis";
import { APP_NAME, APP_DESCRIPTION } from "@/lib/constants";

// ── Motion tokens ────────────────────────────────────────────
const SPRING = { type: "spring", stiffness: 300, damping: 30 } as const;

const REVEAL: Variants = {
  hidden: { opacity: 0, y: 12 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" } },
};

const STAGGER: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.06 } },
};

export default function Home() {
  const {
    file,
    result,
    error,
    isReady,
    isAnalyzing,
    isSuccess,
    isError,
    selectFile,
    analyze,
    reset,
  } = useAnalysis();

  const [isDragging, setIsDragging] = useState(false);
  const docked = isAnalyzing || isSuccess || isError;

  function onFileChange(e: ChangeEvent<HTMLInputElement>) {
    const selected = e.target.files?.[0];
    if (selected) selectFile(selected);
  }

  function onDrop(e: DragEvent<HTMLLabelElement>) {
    e.preventDefault();
    setIsDragging(false);
    const dropped = e.dataTransfer.files?.[0];
    if (dropped) selectFile(dropped);
  }

  return (
    <main className="min-h-screen bg-[#0F1113] text-[#EDEDE8] font-sans antialiased">
      <div className="mx-auto flex min-h-screen w-full max-w-[1040px] flex-col items-center px-4 md:px-6 py-10 md:py-16 overflow-x-hidden">
        
        {/* ── Intro copy — only shown before anything is docked ── */}
        <AnimatePresence>
          {!docked && (
            <motion.div
              initial={{ opacity: 1 }}
              exit={{ opacity: 0, transition: { duration: 0.2 } }}
              className="mb-8 md:mb-12 flex flex-col items-center text-center px-4"
            >
              <h1 className="text-[24px] md:text-[28px] font-medium tracking-tight">{APP_NAME}</h1>
              <p className="mt-2 text-[14px] md:text-[15px] text-[#EDEDE8]/55">{APP_DESCRIPTION}</p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── The Listening Bar — docks from centered to top-fixed ── */}
        <motion.div
          layout
          transition={SPRING}
          className={`w-full ${docked ? "max-w-[640px]" : "max-w-[560px]"}`}
        >
          <motion.label
            layout
            transition={SPRING}
            onDragOver={(e) => {
              e.preventDefault();
              setIsDragging(true);
            }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={onDrop}
            className={`group relative flex w-full cursor-pointer items-center gap-3 md:gap-4 overflow-hidden rounded-3xl md:rounded-full border px-4 md:px-6 py-3 md:py-0 transition-colors duration-150 ${
              docked ? "min-h-[56px]" : "min-h-[64px]"
            } ${
              isDragging
                ? "border-[#E8A33D]/60 bg-[#E8A33D]/[0.06]"
                : "border-white/[0.08] bg-[#181B1E] hover:border-white/[0.14]"
            }`}
          >
            <Waveform active={isAnalyzing} />

            <div className="flex min-w-0 flex-1 flex-col">
              {file ? (
                <span className="truncate text-[13px] md:text-[14px] font-medium text-[#EDEDE8]">
                  {file.name}
                </span>
              ) : (
                <span className="text-[13px] md:text-[14px] font-medium text-[#EDEDE8]/70">
                  Drop audio or click to browse
                </span>
              )}
              {!file && !docked && (
                <span className="font-mono text-[10px] md:text-[11px] uppercase tracking-widest text-[#EDEDE8]/35 mt-0.5">
                  MP3 · WAV · M4A · WEBM · OGG
                </span>
              )}
            </div>

            {isAnalyzing && (
              <span className="shrink-0 font-mono text-[10px] md:text-[12px] uppercase tracking-widest text-[#E8A33D]">
                scanning
              </span>
            )}

            {!docked && (
              <input
                hidden
                type="file"
                accept="audio/*"
                onChange={onFileChange}
              />
            )}
          </motion.label>

          {/* Analyze / Reset controls */}
          <AnimatePresence mode="wait">
            {!docked && file && (
              <motion.button
                key="analyze"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                onClick={analyze}
                disabled={!isReady}
                className="mt-4 flex h-12 w-full items-center justify-center gap-2 rounded-full bg-[#E8A33D] text-[14px] font-medium text-[#0F1113] transition-opacity hover:opacity-90 disabled:opacity-40"
              >
                Analyze pronunciation
                <ArrowRight className="h-4 w-4" />
              </motion.button>
            )}
          </AnimatePresence>

          {docked && (
            <div className="mt-3 flex items-center justify-between px-1">
              <span className="font-mono text-[10px] md:text-[12px] uppercase tracking-widest text-[#EDEDE8]/40">
                {isAnalyzing ? "Listening to your recording…" : result ? `${result.duration_seconds.toFixed(1)}s runtime` : ""}
              </span>
              {(isSuccess || isError) && (
                <button
                  onClick={reset}
                  className="flex items-center gap-1.5 font-mono text-[10px] md:text-[12px] uppercase tracking-widest text-[#EDEDE8]/50 transition-colors hover:text-[#EDEDE8]"
                >
                  <RotateCcw className="h-3 w-3 md:h-3.5 md:w-3.5" />
                  Reset
                </button>
              )}
            </div>
          )}
        </motion.div>

        {/* ── Error ── */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              className="mt-6 flex w-full max-w-[640px] items-start gap-3 rounded-2xl border border-[#E2685A]/25 bg-[#E2685A]/[0.06] p-4 md:p-5"
            >
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-[#E2685A]" />
              <p className="text-[13px] md:text-[14px] leading-relaxed text-[#E2685A]">{error}</p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── Results canvas ── */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial="hidden"
              animate="visible"
              variants={STAGGER}
              className="mt-12 md:mt-16 flex w-full max-w-[840px] flex-col gap-12 md:gap-16"
            >
              {/* Score */}
              <motion.section variants={REVEAL} className="flex flex-col md:flex-row items-center md:items-start gap-8 md:gap-12 w-full">
                <ScoreArc score={result.overall_score} />
                <div className="flex w-full md:flex-1 flex-col gap-4 md:gap-5">
                  <SubScore label="Clarity" value={result.score_breakdown.clarity} />
                  <SubScore label="Fluency" value={result.score_breakdown.fluency} />
                  <SubScore label="Word accuracy" value={result.score_breakdown.word_accuracy} />
                </div>
              </motion.section>

              {/* Transcript */}
              <motion.section variants={REVEAL} className="w-full">
                <SectionLabel>Transcript</SectionLabel>
                <p className="mt-4 md:mt-5 max-w-[760px] text-[16px] md:text-[19px] leading-[1.9] md:leading-[2.1] text-[#EDEDE8]/85">
                  {result.transcript.words.map((word, i) => (
                    <span
                      key={i}
                      className={
                        word.highlighted
                          ? "inline-block relative mr-[0.3em] text-[#EDEDE8] after:absolute after:-bottom-0.5 md:after:-bottom-1 after:left-0 after:h-[2px] after:w-full after:bg-[#E8A33D]/70"
                          : "inline-block mr-[0.3em]"
                      }
                    >
                      {word.word}
                    </span>
                  ))}
                </p>
              </motion.section>

              {/* Mistakes */}
              <motion.section variants={REVEAL} className="w-full">
                <SectionLabel>Corrections</SectionLabel>
                {result.mistakes.length === 0 ? (
                  <div className="mt-4 md:mt-5 flex items-center gap-3 rounded-2xl border border-[#6FCF97]/20 bg-[#6FCF97]/[0.06] px-4 md:px-5 py-3 md:py-4">
                    <CheckCircle2 className="h-4 w-4 shrink-0 text-[#6FCF97]" />
                    <span className="text-[13px] md:text-[14px] text-[#6FCF97]">No corrections needed — clean delivery.</span>
                  </div>
                ) : (
                  <div className="mt-4 md:mt-5 flex flex-col divide-y divide-white/[0.06]">
                    {result.mistakes.map((mistake, i) => (
                      <div key={i} className="flex flex-col gap-2 py-4 md:py-5 first:pt-0">
                        <div className="flex flex-wrap items-baseline gap-2 md:gap-3">
                          <span className="text-[16px] md:text-[17px] font-medium text-[#EDEDE8]">{mistake.word}</span>
                          <span className="font-mono text-[10px] md:text-[11px] uppercase tracking-widest text-[#EDEDE8]/40">
                            {mistake.issue_type}
                          </span>
                        </div>
                        <p className="text-[13px] md:text-[14px] leading-relaxed text-[#EDEDE8]/60">{mistake.explanation}</p>
                        <div className="flex items-start md:items-center gap-2 text-[13px] md:text-[14px] text-[#E8A33D] mt-1 md:mt-0">
                          <ArrowRight className="mt-1 md:mt-0 h-3.5 w-3.5 shrink-0" />
                          <span>{mistake.suggestion}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </motion.section>

              {/* Feedback */}
              <motion.section variants={REVEAL} className="pb-12 md:pb-16 w-full">
                <SectionLabel>AI feedback</SectionLabel>
                <p className="mt-4 md:mt-5 max-w-[720px] text-[15px] md:text-[16px] leading-relaxed text-[#EDEDE8]/70">
                  {result.overall_feedback}
                </p>
              </motion.section>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </main>
  );
}

// ── Subcomponents ─────────────────────────────────────────────

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <span className="font-mono text-[11px] md:text-[12px] uppercase tracking-widest text-[#EDEDE8]/40 block">
      {children}
    </span>
  );
}

function SubScore({ label, value }: { label: string; value: number }) {
  return (
    <div className="flex flex-col gap-2 w-full">
      <div className="flex items-baseline justify-between">
        <span className="text-[13px] md:text-[14px] text-[#EDEDE8]/60">{label}</span>
        <span className="font-mono text-[13px] md:text-[14px] text-[#EDEDE8]">{value}</span>
      </div>
      <div className="h-[3px] w-full overflow-hidden rounded-full bg-white/[0.06]">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 1.1, ease: "easeOut", delay: 0.15 }}
          className="h-full rounded-full bg-[#E8A33D]"
        />
      </div>
    </div>
  );
}

function ScoreArc({ score }: { score: number }) {
  const r = 54;
  const stroke = 6;
  const nr = r - stroke;
  const circumference = nr * 2 * Math.PI;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="relative flex shrink-0 items-center justify-center scale-90 md:scale-100">
      <svg width={r * 2} height={r * 2} className="-rotate-90">
        <circle cx={r} cy={r} r={nr} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth={stroke} />
        <motion.circle
          cx={r} cy={r} r={nr} fill="none"
          stroke="#E8A33D" strokeWidth={stroke} strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.4, ease: "easeOut", delay: 0.1 }}
        />
      </svg>
      <span className="absolute font-mono text-[36px] md:text-[40px] font-medium text-[#EDEDE8]">
        {score}
      </span>
    </div>
  );
}

function Waveform({ active }: { active: boolean }) {
  const bars = [4, 8, 14, 10, 16, 9, 5, 12, 7];
  return (
    <div className="flex h-4 md:h-5 shrink-0 items-center gap-[2px] md:gap-[3px]">
      {bars.map((h, i) => (
        <motion.span
          key={i}
          className="w-[2px] rounded-full bg-[#E8A33D]/70"
          animate={
            active
              ? { height: [h, h * 1.8, h * 0.6, h], opacity: [0.5, 1, 0.6, 0.5] }
              : { height: h, opacity: 0.3 }
          }
          transition={
            active
              ? { duration: 0.9, repeat: Infinity, delay: i * 0.06, ease: "easeInOut" }
              : { duration: 0.3 }
          }
        />
      ))}
    </div>
  );
}