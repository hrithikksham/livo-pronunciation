"""
Common internal schemas.

These schemas are exchanged between services.
They are NOT exposed to the API.

Author: Hrithik
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.llm_output import LLMOutput


###############################################################################
# Provider Metadata
###############################################################################


class ProviderUsage(BaseModel):
    """
    Metadata about an external AI provider.
    """

    model_config = ConfigDict(from_attributes=True)

    provider: str

    model: str

    latency_ms: int = Field(..., ge=0)

    tokens: int | None = None


###############################################################################
# Audio Metadata
###############################################################################


class AudioMetadata(BaseModel):
    """
    Metadata extracted from normalized audio.
    """

    model_config = ConfigDict(from_attributes=True)

    duration_seconds: float = Field(..., gt=0)

    channels: int

    frame_rate: int

    sample_width: int

    frame_width: int

    file_size_mb: float = Field(..., gt=0)

    mime_type: str

    extension: str


###############################################################################
# Processed Audio
###############################################################################


class ProcessedAudio(BaseModel):
    """
    Validated audio after normalization.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
    )

    original_path: Path

    normalized_path: Path

    metadata: AudioMetadata


###############################################################################
# Word Timestamp
###############################################################################


class WordTimestamp(BaseModel):
    """
    Individual word from Whisper.
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


###############################################################################
# Speech-to-Text Result
###############################################################################


class STTResult(BaseModel):
    """
    Whisper transcription result.
    """

    model_config = ConfigDict(from_attributes=True)

    transcript: str

    language: str

    duration_seconds: float

    words: list[WordTimestamp]

    provider: ProviderUsage


###############################################################################
# Flagged Candidate
###############################################################################


class FlaggedWord(BaseModel):
    """
    Candidate word for pronunciation review.

    NOTE:
    This does NOT mean the word was mispronounced.
    It only indicates that the LLM should inspect it.
    """

    model_config = ConfigDict(from_attributes=True)

    word: str

    start: float

    end: float

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
    )

    issue_type: Literal[
        "unclear",
        "fluency",
        "stress",
        "intonation",
        "mispronunciation",
        "omission",
        "insertion",
    ]


###############################################################################
# Analysis Context
###############################################################################


class AnalysisContext(BaseModel):
    """
    Input passed into the LLM Provider.
    """

    model_config = ConfigDict(from_attributes=True)

    transcript: str

    duration_seconds: float

    reference_text: str | None = None

    flagged_words: list[FlaggedWord]

    average_confidence: float = Field(
        ...,
        ge=0,
        le=1,
    )

    speaking_rate: float = Field(
        ...,
        ge=0,
    )

    average_pause: float = Field(
        ...,
        ge=0,
    )

    filler_word_count: int = Field(
        ...,
        ge=0,
    )


###############################################################################
# Internal Analysis Result
###############################################################################


class InternalAnalysisResult(BaseModel):
    """
    Final internal domain model before
    being mapped into the public API response.
    """

    model_config = ConfigDict(from_attributes=True)

    overall_score: int = Field(
        ...,
        ge=0,
        le=100,
    )

    clarity: int = Field(
        ...,
        ge=0,
        le=100,
    )

    fluency: int = Field(
        ...,
        ge=0,
        le=100,
    )

    word_accuracy: int = Field(
        ...,
        ge=0,
        le=100,
    )

    transcript: STTResult

    flagged_words: list[FlaggedWord]

    llm_output: LLMOutput

    overall_feedback: str

    provider_usage: ProviderUsage