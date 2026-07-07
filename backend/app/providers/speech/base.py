"""
Speech Provider Interface.

Defines the contract that every speech-to-text provider
must implement.

Author: Hrithik
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.common import ProcessedAudio, STTResult


class SpeechProvider(ABC):
    """
    Base interface for Speech-to-Text providers.

    Implementations:
        - GroqWhisperProvider
        - OpenAIWhisperProvider
        - DeepgramProvider
        - AzureSpeechProvider
    """

    provider_name: str

    model_name: str

    @abstractmethod
    async def transcribe(
        self,
        audio: ProcessedAudio,
    ) -> STTResult:
        """
        Convert speech into text.

        Args:
            audio:
                Validated and normalized audio.

        Returns:
            STTResult

        Raises:
            STTProviderError
        """

        raise NotImplementedError