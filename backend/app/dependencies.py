"""
Application Dependencies.

Centralized dependency injection for providers,
services and workflows.

"""

from __future__ import annotations

from functools import lru_cache

from app.providers.llm.base import LLMProvider
from app.providers.llm.groq_provider import GroqProvider

from app.providers.speech.base import SpeechProvider
from app.providers.speech.groq_provider import (
    GroqWhisperProvider,
)

from app.services.analysis_service import AnalysisService
from app.services.audio_service import AudioService
from app.services.mapper_service import MapperService
from app.services.scoring_service import ScoringService

from app.workflows.analysis_workflow import (
    AnalysisWorkflow,
)

###############################################################################
# Providers
###############################################################################


@lru_cache
def get_speech_provider() -> SpeechProvider:
    """
    Returns the configured Speech Provider.
    """

    return GroqWhisperProvider()


@lru_cache
def get_llm_provider() -> LLMProvider:
    """
    Returns the configured LLM Provider.
    """

    return GroqProvider()


###############################################################################
# Services
###############################################################################


@lru_cache
def get_audio_service() -> AudioService:
    return AudioService()


@lru_cache
def get_analysis_service() -> AnalysisService:
    return AnalysisService()


@lru_cache
def get_scoring_service() -> ScoringService:
    return ScoringService()


@lru_cache
def get_mapper_service() -> MapperService:
    return MapperService()


###############################################################################
# Workflow
###############################################################################


@lru_cache
def get_analysis_workflow() -> AnalysisWorkflow:
    """
    Builds the application workflow.

    All dependencies are injected here.
    """

    return AnalysisWorkflow(
        audio_service=get_audio_service(),
        speech_provider=get_speech_provider(),
        analysis_service=get_analysis_service(),
        llm_provider=get_llm_provider(),
        scoring_service=get_scoring_service(),
        mapper_service=get_mapper_service(),
    )