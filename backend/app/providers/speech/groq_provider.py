"""
Groq Whisper Speech Provider.

Concrete implementation of the SpeechProvider interface
using Groq Whisper Large v3.

Author: Hrithik
"""

from __future__ import annotations

import time
from functools import lru_cache

from groq import AsyncGroq

from app.constants import (
    WHISPER_LANGUAGE,
    WHISPER_MODEL,
    WHISPER_TEMPERATURE,
)
from app.core.config import settings
from app.core.exceptions import STTProviderError
from app.core.logging import get_logger

from app.providers.speech.base import SpeechProvider

from app.schemas.common import (
    ProcessedAudio,
    ProviderUsage,
    STTResult,
    WordTimestamp,
)

logger = get_logger(__name__)


class GroqWhisperProvider(SpeechProvider):
    """
    Speech provider backed by Groq Whisper.
    """

    provider_name = "groq"
    model_name = WHISPER_MODEL

    def __init__(self) -> None:
        self.client = AsyncGroq(
            api_key=settings.GROQ_API_KEY,
        )

    async def transcribe(
        self,
        audio: ProcessedAudio,
    ) -> STTResult:

        logger.info("Starting transcription...")

        started = time.perf_counter()

        try:

            if not audio.normalized_path.exists():
                raise FileNotFoundError(audio.normalized_path)

            with open(audio.normalized_path, "rb") as file:

                response = await self.client.audio.transcriptions.create(
                    file=file,
                    model=self.model_name,
                    language=WHISPER_LANGUAGE,
                    temperature=WHISPER_TEMPERATURE,
                    response_format="verbose_json",
                    timestamp_granularities=["word"],
                )

        except Exception as exc:

            logger.exception("Groq Whisper transcription failed.")

            raise STTProviderError() from exc

        latency = int((time.perf_counter() - started) * 1000)

        ######################################################################
        # DEBUG (remove later)
        ######################################################################

        logger.info(
            "Response words type: %s",
            type(getattr(response, "words", None)),
        )

        if getattr(response, "words", None):
            logger.info(
                "First word object: %s",
                response.words[0],
            )

        ######################################################################
        # Parse words
        ######################################################################

        words: list[WordTimestamp] = []

        response_words = getattr(response, "words", [])

        for item in response_words:

            # Dictionary response
            if isinstance(item, dict):

                words.append(
                    WordTimestamp(
                        word=item.get("word", ""),
                        start=float(item.get("start", 0.0)),
                        end=float(item.get("end", 0.0)),
                        confidence=float(
                            item.get("probability", 1.0)
                        ),
                    )
                )

                continue

            # SDK object response
            words.append(
                WordTimestamp(
                    word=getattr(item, "word", ""),
                    start=float(getattr(item, "start", 0.0)),
                    end=float(getattr(item, "end", 0.0)),
                    confidence=float(
                        getattr(item, "probability", 1.0)
                    ),
                )
            )

        logger.info(
            "Transcription completed. Parsed %d words.",
            len(words),
        )

        return STTResult(
            transcript=getattr(response, "text", ""),
            language=getattr(response, "language", "en"),
            duration_seconds=audio.metadata.duration_seconds,
            words=words,
            provider=ProviderUsage(
                provider=self.provider_name,
                model=self.model_name,
                latency_ms=latency,
                tokens=None,
            ),
        )


@lru_cache
def get_speech_provider() -> SpeechProvider:
    """
    Dependency Injection Provider.
    """
    return GroqWhisperProvider()