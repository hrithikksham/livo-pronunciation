"use client";

/**
 * useAnalysis
 *
 * Handles:
 * - File selection
 * - Audio analysis
 * - Loading state
 * - Error state
 * - Result state
 *
 * Author: Hrithik
 */

import { useState } from "react";

import { analyzeAudio } from "@/lib/api";

import { STATUS } from "@/lib/constants";

import type { AnalysisResult } from "@/types/analysis";

export function useAnalysis() {
  /////////////////////////////////////////////////////////////////////////////
  // State
  /////////////////////////////////////////////////////////////////////////////

  const [file, setFile] = useState<File | null>(null);

  const [status, setStatus] = useState<
    (typeof STATUS)[keyof typeof STATUS]
  >(STATUS.IDLE);

  const [result, setResult] =
    useState<AnalysisResult | null>(null);

  const [error, setError] =
    useState<string | null>(null);

  /////////////////////////////////////////////////////////////////////////////
  // Select File
  /////////////////////////////////////////////////////////////////////////////

  function selectFile(selectedFile: File) {
    setFile(selectedFile);
    setResult(null);
    setError(null);
    setStatus(STATUS.READY);
  }

  /////////////////////////////////////////////////////////////////////////////
  // Remove File
  /////////////////////////////////////////////////////////////////////////////

  function clearFile() {
    setFile(null);
    setResult(null);
    setError(null);
    setStatus(STATUS.IDLE);
  }

  /////////////////////////////////////////////////////////////////////////////
  // Analyze
  /////////////////////////////////////////////////////////////////////////////

  async function analyze() {
    if (!file) return;

    try {
      setStatus(STATUS.ANALYZING);
      setError(null);

      const response = await analyzeAudio(file);

      setResult(response);

      setStatus(STATUS.SUCCESS);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Something went wrong.";

      setError(message);

      setStatus(STATUS.ERROR);
    }
  }

  /////////////////////////////////////////////////////////////////////////////
  // Reset
  /////////////////////////////////////////////////////////////////////////////

  function reset() {
    setFile(null);
    setResult(null);
    setError(null);
    setStatus(STATUS.IDLE);
  }

  /////////////////////////////////////////////////////////////////////////////
  // Derived State
  /////////////////////////////////////////////////////////////////////////////

  const isIdle = status === STATUS.IDLE;

  const isReady = status === STATUS.READY;

  const isAnalyzing =
    status === STATUS.ANALYZING;

  const isSuccess =
    status === STATUS.SUCCESS;

  const isError =
    status === STATUS.ERROR;

  /////////////////////////////////////////////////////////////////////////////
  // Exposed API
  /////////////////////////////////////////////////////////////////////////////

  return {
    file,
    status,
    result,
    error,

    isIdle,
    isReady,
    isAnalyzing,
    isSuccess,
    isError,

    selectFile,
    clearFile,
    analyze,
    reset,
  };
}