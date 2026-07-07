"""
Mapper Service.

Maps internal domain models into public API response models.

"""

from __future__ import annotations

from app.schemas.common import InternalAnalysisResult
from app.schemas.response import (
    AnalysisResult,
    Mistake,
    ScoreBreakdown,
    Transcript,
    TranscriptWord,
)
from app.services.base import BaseService


class MapperService(BaseService):
    """
    Maps internal models to API response models.
    """

    def to_response(
        self,
        result: InternalAnalysisResult,
    ) -> AnalysisResult:
        """
        Convert InternalAnalysisResult into
        AnalysisResult.
        """

        self.log_start("Response Mapping")

        transcript = Transcript(
            text=result.transcript.transcript,
            words=[
                TranscriptWord(
                    word=word.word,
                    start=word.start,
                    end=word.end,
                    confidence=word.confidence,
                    highlighted=self._is_flagged(
                        word.word,
                        result.flagged_words,
                    ),
                )
                for word in result.transcript.words
            ],
        )

        mistakes = []

        for flagged in result.flagged_words:

            llm_match = self._find_llm_mistake(
                flagged.word,
                result.llm_output.mistakes,
            )

            if llm_match is None:
                continue

            mistakes.append(
                Mistake(
                    word=flagged.word,
                    issue_type=llm_match.issue_type,
                    timestamp_seconds=flagged.start,
                    confidence=flagged.confidence,
                    explanation=llm_match.explanation,
                    suggestion=llm_match.suggestion,
                )
            )

        response = AnalysisResult(
            overall_score=result.overall_score,

            score_breakdown=ScoreBreakdown(
                clarity=result.clarity,
                fluency=result.fluency,
                word_accuracy=result.word_accuracy,
            ),

            transcript=transcript,

            duration_seconds=result.transcript.duration_seconds,

            mistakes=mistakes,

            overall_feedback=result.overall_feedback,
        )

        self.log_success("Response Mapping")

        return response

    ####################################################################
    # Helpers
    ####################################################################

    @staticmethod
    def _is_flagged(
        word: str,
        flagged_words,
    ) -> bool:

        return any(
            flagged.word.lower() == word.lower()
            for flagged in flagged_words
        )

    @staticmethod
    def _find_llm_mistake(
        word: str,
        mistakes,
    ):

        for mistake in mistakes:

            if mistake.word.lower() == word.lower():
                return mistake

        return None