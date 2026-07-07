"""
Scoring Service.

Responsible for:
- Computing deterministic pronunciation scores
- Applying weighted averages
- Building InternalAnalysisResult

Author: Hrithik
"""

from __future__ import annotations

from app.constants import (
    CLARITY_WEIGHT,
    FLUENCY_WEIGHT,
    WORD_ACCURACY_WEIGHT,
)

from app.schemas.common import (
    AnalysisContext,
    InternalAnalysisResult,
    ProviderUsage,
    STTResult,
)

from app.schemas.llm_output import LLMOutput

from app.services.base import BaseService


class ScoringService(BaseService):
    """
    Computes the final pronunciation score.

    This service never calls an LLM or Speech Provider.
    """

    ###########################################################################
    # Public API
    ###########################################################################

    def calculate(
        self,
        *,
        stt: STTResult,
        context: AnalysisContext,
        llm: LLMOutput,
    ) -> InternalAnalysisResult:
        """
        Compute the final pronunciation result.
        """

        self.log_start("Scoring")

        breakdown = llm.score_breakdown

        overall_score = self._calculate_weighted_score(
            clarity=breakdown.clarity,
            fluency=breakdown.fluency,
            word_accuracy=breakdown.word_accuracy,
        )

        provider = ProviderUsage(
            provider=stt.provider.provider,
            model=stt.provider.model,
            latency_ms=stt.provider.latency_ms,
            tokens=stt.provider.tokens,
        )

        result = InternalAnalysisResult(
            overall_score=overall_score,
            clarity=breakdown.clarity,
            fluency=breakdown.fluency,
            word_accuracy=breakdown.word_accuracy,
            transcript=stt,
            flagged_words=context.flagged_words,
            llm_output=llm,
            overall_feedback=llm.overall_feedback,
            provider_usage=provider,
        )

        self.log_success("Scoring")

        return result

    ###########################################################################
    # Score Calculation
    ###########################################################################

    @staticmethod
    def _calculate_weighted_score(
        *,
        clarity: int,
        fluency: int,
        word_accuracy: int,
    ) -> int:
        """
        Compute weighted pronunciation score.
        """

        score = round(
            (
                clarity * CLARITY_WEIGHT
                + fluency * FLUENCY_WEIGHT
                + word_accuracy * WORD_ACCURACY_WEIGHT
            )
        )

        return max(0, min(100, score))

    ###########################################################################
    # Helpers
    ###########################################################################

    @staticmethod
    def grade(score: int) -> str:
        """
        Convert numeric score into a human-readable grade.
        """

        if score >= 90:
            return "Excellent"

        if score >= 80:
            return "Very Good"

        if score >= 70:
            return "Good"

        if score >= 60:
            return "Fair"

        return "Needs Improvement"

    @staticmethod
    def confidence_level(score: int) -> str:
        """
        Convert score into a proficiency label.
        """

        if score >= 90:
            return "Advanced"

        if score >= 80:
            return "Proficient"

        if score >= 70:
            return "Intermediate"

        if score >= 60:
            return "Basic"

        return "Beginner"

    @staticmethod
    def score_summary(score: int) -> str:
        """
        Short summary used by the UI.
        """

        if score >= 90:
            return "Outstanding pronunciation."

        if score >= 80:
            return "Strong pronunciation with minor improvements."

        if score >= 70:
            return "Good pronunciation with noticeable mistakes."

        if score >= 60:
            return "Average pronunciation. Practice recommended."

        return "Pronunciation needs significant improvement."