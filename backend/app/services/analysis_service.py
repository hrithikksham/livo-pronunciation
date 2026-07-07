"""
Analysis Service.

Responsible for:
- Processing Whisper transcription
- Extracting pronunciation candidates
- Computing speech statistics
- Building AnalysisContext

Author: Hrithik
"""

from __future__ import annotations

from functools import lru_cache

from app.schemas.common import (
    AnalysisContext,
    FlaggedWord,
    STTResult,
    WordTimestamp,
)

from app.services.base import BaseService


class AnalysisService(BaseService):
    """
    Prepares deterministic analysis before sending
    the transcript to the LLM.
    """

    LOW_CONFIDENCE_THRESHOLD = 0.80

    FILLER_WORDS = {
        "uh",
        "um",
        "umm",
        "erm",
        "hmm",
        "ah",
        "like",
        "actually",
        "basically",
    }

    ###########################################################################
    # Public API
    ###########################################################################

    async def analyze(
        self,
        stt: STTResult,
    ) -> AnalysisContext:

        self.log_start("Speech Analysis")

        flagged_words = self._extract_candidates(stt)

        context = AnalysisContext(
            transcript=stt.transcript,
            reference_text=None,
            flagged_words=flagged_words,
            duration_seconds=stt.duration_seconds,
            average_confidence=self.average_confidence(stt),
            speaking_rate=self.speaking_rate(stt),
            average_pause=self.average_pause(stt),
            filler_word_count=self.filler_word_count(stt),
        )

        self.log_success("Speech Analysis")

        return context

    ###########################################################################
    # Candidate Extraction
    ###########################################################################

    def _extract_candidates(
        self,
        stt: STTResult,
    ) -> list[FlaggedWord]:

        candidates: list[FlaggedWord] = []

        for word in stt.words:

            issue = self._detect_issue(word)

            if issue:
                candidates.append(issue)

        return candidates

    ###########################################################################
    # Word Classification
    ###########################################################################

    def _detect_issue(
        self,
        word: WordTimestamp,
    ) -> FlaggedWord | None:

        text = word.word.strip().lower()

        if not text:
            return None

        if text.isdigit():
            return None

        if len(text) <= 1:
            return None

        if text in self.FILLER_WORDS:

            return FlaggedWord(
                word=word.word,
                start=word.start,
                end=word.end,
                confidence=word.confidence,
                issue_type="fluency",
            )

        if word.confidence < self.LOW_CONFIDENCE_THRESHOLD:

            return FlaggedWord(
                word=word.word,
                start=word.start,
                end=word.end,
                confidence=word.confidence,
                issue_type="unclear",
            )

        return None

    ###########################################################################
    # Statistics
    ###########################################################################

    def speaking_rate(
        self,
        stt: STTResult,
    ) -> float:

        if stt.duration_seconds <= 0:
            return 0.0

        minutes = stt.duration_seconds / 60

        return len(stt.words) / minutes

    def average_pause(
        self,
        stt: STTResult,
    ) -> float:

        if len(stt.words) < 2:
            return 0.0

        pauses = [
            max(0.0, current.start - previous.end)
            for previous, current in zip(
                stt.words,
                stt.words[1:],
            )
        ]

        if not pauses:
            return 0.0

        return sum(pauses) / len(pauses)

    def average_confidence(
        self,
        stt: STTResult,
    ) -> float:

        if not stt.words:
            return 1.0

        return (
            sum(word.confidence for word in stt.words)
            / len(stt.words)
        )

    def filler_word_count(
        self,
        stt: STTResult,
    ) -> int:

        return sum(
            1
            for word in stt.words
            if word.word.strip().lower() in self.FILLER_WORDS
        )


@lru_cache
def get_analysis_service() -> AnalysisService:
    return AnalysisService()