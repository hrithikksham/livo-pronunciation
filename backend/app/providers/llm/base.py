"""
LLM Provider Interface.

Defines the contract for every Large Language Model provider.

Author: Hrithik
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.common import AnalysisContext
from app.schemas.llm_output import LLMOutput


class LLMProvider(ABC):
    """
    Base interface for LLM providers.

    Implementations:
        - GroqProvider
        - OpenAIProvider
        - ClaudeProvider
    """

    provider_name: str

    model_name: str

    @abstractmethod
    async def evaluate(
        self,
        context: AnalysisContext,
    ) -> LLMOutput:
        """
        Evaluate pronunciation.

        Args:
            context:
                AnalysisContext produced by
                AnalysisService.

        Returns:
            Validated LLMOutput.
        """

        raise NotImplementedError