"""
Public API response schemas.

These models are returned to the frontend.

Author: Hrithik
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


###############################################################################
# Score Breakdown
###############################################################################


class ScoreBreakdown(BaseModel):
    """
    Individual pronunciation scores.
    """

    model_config = ConfigDict(from_attributes=True)

    clarity: int = Field(..., ge=0, le=100)

    fluency: int = Field(..., ge=0, le=100)

    word_accuracy: int = Field(..., ge=0, le=100)


###############################################################################
# Mistake
###############################################################################


class Mistake(BaseModel):
    """
    Individual pronunciation issue.
    """

    model_config = ConfigDict(from_attributes=True)

    word: str

    issue_type: Literal[
        "mispronunciation",
        "stress",
        "intonation",
        "fluency",
        "omission",
        "insertion",
        "unclear",
    ]

    timestamp_seconds: float = Field(
        ...,
        ge=0,
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
    )

    explanation: str

    suggestion: str


###############################################################################
# Transcript Word
###############################################################################


class TranscriptWord(BaseModel):
    """
    Individual transcript word.
    """

    model_config = ConfigDict(from_attributes=True)

    word: str

    start: float = Field(..., ge=0)

    end: float = Field(..., ge=0)

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
    )

    highlighted: bool = False


###############################################################################
# Transcript
###############################################################################


class Transcript(BaseModel):
    """
    Complete transcript.
    """

    model_config = ConfigDict(from_attributes=True)

    text: str

    words: list[TranscriptWord]


###############################################################################
# Analysis Result
###############################################################################


class AnalysisResult(BaseModel):
    """
    Successful pronunciation analysis response.
    """

    model_config = ConfigDict(from_attributes=True)

    overall_score: int = Field(
        ...,
        ge=0,
        le=100,
    )

    score_breakdown: ScoreBreakdown

    transcript: Transcript

    duration_seconds: float = Field(
        ...,
        ge=0,
    )

    mistakes: list[Mistake] = Field(
        default_factory=list,
    )

    overall_feedback: str


###############################################################################
# Error Response
###############################################################################


class ErrorBody(BaseModel):
    """
    Standard API error body.
    """

    model_config = ConfigDict(from_attributes=True)

    code: str

    message: str

    request_id: str | None = None


class ErrorResponse(BaseModel):
    """
    Standard API error response.
    """

    model_config = ConfigDict(from_attributes=True)

    error: ErrorBody