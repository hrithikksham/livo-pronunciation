"""
Analysis Workflow.

Coordinates the complete pronunciation analysis pipeline.

Pipeline:

Upload
    ↓
AudioService
    ↓
SpeechProvider
    ↓
AnalysisService
    ↓
LLMProvider
    ↓
ScoringService
    ↓
MapperService
    ↓
AnalysisResponse

Author: Hrithik
"""

from __future__ import annotations

from fastapi import UploadFile

from app.schemas.response import AnalysisResult

from app.providers.speech.base import SpeechProvider
from app.providers.llm.base import LLMProvider

from app.services.audio_service import AudioService
from app.services.analysis_service import AnalysisService
from app.services.scoring_service import ScoringService
from app.services.mapper_service import MapperService

from app.core.logging import get_logger


logger = get_logger(__name__)


class AnalysisWorkflow:
    """
    Orchestrates the pronunciation analysis pipeline.

    Business logic DOES NOT belong here.

    This class only coordinates services.
    """

    def __init__(
        self,
        *,
        audio_service: AudioService,
        speech_provider: SpeechProvider,
        analysis_service: AnalysisService,
        llm_provider: LLMProvider,
        scoring_service: ScoringService,
        mapper_service: MapperService,
    ) -> None:

        self.audio_service = audio_service

        self.speech_provider = speech_provider

        self.analysis_service = analysis_service

        self.llm_provider = llm_provider

        self.scoring_service = scoring_service

        self.mapper_service = mapper_service

    #######################################################################
    # Public API
    #######################################################################

    async def execute(
        self,
        upload: UploadFile,
    ) -> AnalysisResult:
        """
        Execute complete pronunciation analysis.

        Returns
        -------
        AnalysisResult
        """

        logger.info(
            "Starting pronunciation workflow."
        )

        processed_audio = None

        try:

            ###################################################################
            # Audio Processing
            ###################################################################

            processed_audio = await self.audio_service.process(
                upload,
            )

            ###################################################################
            # Speech Recognition
            ###################################################################

            stt_result = await self.speech_provider.transcribe(
                processed_audio,
            )

            ###################################################################
            # Analysis
            ###################################################################

            analysis_context = await self.analysis_service.analyze(
                stt_result,
            )

            ###################################################################
            # LLM Evaluation
            ###################################################################

            llm_result = await self.llm_provider.evaluate(
                analysis_context,
            )

            ###################################################################
            # Score Calculation
            ###################################################################

            internal_result = self.scoring_service.calculate(
                stt=stt_result,
                context=analysis_context,
                llm=llm_result,
            )

            ###################################################################
            # API Mapping
            ###################################################################

            response = self.mapper_service.to_response(
                internal_result,
            )

            logger.info(
                "Workflow completed successfully."
            )

            return response

        finally:

            ###################################################################
            # Cleanup
            ###################################################################

            if processed_audio is not None:

                self.audio_service.cleanup(
                    processed_audio,
                )