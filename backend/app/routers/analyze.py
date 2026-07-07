"""
Analyze Router.

Pronunciation Analysis Endpoint.

Author: Hrithik
"""

from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    status,
)

from app.core.security import validate_audio_upload
from app.dependencies import get_analysis_workflow
from app.schemas.response import AnalysisResult
from app.workflows.analysis_workflow import AnalysisWorkflow

router = APIRouter(
    prefix="/analyze",
    tags=["Pronunciation Analysis"],
)


@router.post(
    "",
    response_model=AnalysisResult,
    status_code=status.HTTP_200_OK,
    summary="Analyze pronunciation",
    description="""
Analyze a spoken English audio recording.

Requirements:
- Supported formats:
  - mp3
  - wav
  - webm
  - ogg
  - m4a
  - flac

- Duration:
  - 35–40 seconds

Returns:
- Overall score
- Transcript
- Mistakes
- Suggestions
- Pronunciation feedback
""",
)
async def analyze_pronunciation(
    audio: UploadFile = Depends(validate_audio_upload),
    workflow: AnalysisWorkflow = Depends(get_analysis_workflow),
) -> AnalysisResult:
    """
    Analyze a pronunciation audio file.
    """

    return await workflow.execute(audio)