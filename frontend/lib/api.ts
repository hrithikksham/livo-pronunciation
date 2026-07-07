/**
 * API Client
 *
 * Handles communication with the FastAPI backend.
 *
 * Author: Hrithik
 */

import axios, { AxiosError } from "axios";

import {
  ANALYZE_ENDPOINT,
  API_BASE_URL,
} from "./constants";

import type {
  AnalysisResult,
  ErrorResponse,
} from "@/types/analysis";

///////////////////////////////////////////////////////////////////////////////
// Axios Instance
///////////////////////////////////////////////////////////////////////////////

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
});

///////////////////////////////////////////////////////////////////////////////
// Analyze Audio
///////////////////////////////////////////////////////////////////////////////

export async function analyzeAudio(
  file: File,
): Promise<AnalysisResult> {
  const formData = new FormData();

  formData.append("audio", file);

  try {
    const response = await api.post<AnalysisResult>(
      ANALYZE_ENDPOINT,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      },
    );

    return response.data;
  } catch (error) {
    const err = error as AxiosError<ErrorResponse>;

    if (err.response?.data?.error?.message) {
      throw new Error(
        err.response.data.error.message,
      );
    }

    throw new Error(
      "Failed to analyze pronunciation.",
    );
  }
}

///////////////////////////////////////////////////////////////////////////////
// Health Check
///////////////////////////////////////////////////////////////////////////////

export async function healthCheck(): Promise<boolean> {
  try {
    await api.get("/health");

    return true;
  } catch {
    return false;
  }
}