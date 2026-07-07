/**
 * Application Constants
 *
 * Author: Hrithik
 */

///////////////////////////////////////////////////////////////////////////////
// API
///////////////////////////////////////////////////////////////////////////////

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "https://livo-pronunciation.onrender.com";

export const ANALYZE_ENDPOINT = "/analyze";

///////////////////////////////////////////////////////////////////////////////
// Audio Upload
///////////////////////////////////////////////////////////////////////////////

export const MAX_FILE_SIZE_MB = 25;

export const MAX_DURATION_SECONDS = 40;

export const MIN_DURATION_SECONDS = 35;

export const SUPPORTED_AUDIO_TYPES = [
  "audio/mpeg",
  "audio/mp3",
  "audio/wav",
  "audio/x-wav",
  "audio/webm",
  "audio/ogg",
  "audio/mp4",
  "audio/x-m4a",
  "audio/flac",
];

export const SUPPORTED_AUDIO_EXTENSIONS = [
  ".mp3",
  ".wav",
  ".webm",
  ".ogg",
  ".m4a",
  ".flac",
];

///////////////////////////////////////////////////////////////////////////////
// UI
///////////////////////////////////////////////////////////////////////////////

export const APP_NAME = "Pronunciation Scorer";

export const APP_DESCRIPTION =
  "AI-powered English pronunciation analysis.";

export const ANALYZE_BUTTON_TEXT = "Analyze Pronunciation";

export const ANALYZE_AGAIN_BUTTON_TEXT = "Analyze Another Audio";

///////////////////////////////////////////////////////////////////////////////
// Upload Status
///////////////////////////////////////////////////////////////////////////////

export const STATUS = {
  IDLE: "idle",
  READY: "ready",
  UPLOADING: "uploading",
  ANALYZING: "analyzing",
  SUCCESS: "success",
  ERROR: "error",
} as const;

export type AnalysisStatus =
  (typeof STATUS)[keyof typeof STATUS];

///////////////////////////////////////////////////////////////////////////////
// Score Colors
///////////////////////////////////////////////////////////////////////////////

export const SCORE_COLORS = {
  excellent: "#16A34A",
  good: "#2563EB",
  average: "#D97706",
  poor: "#DC2626",
} as const;