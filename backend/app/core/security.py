"""
Security Dependencies.

Responsible for:
- Upload validation
- Request guards
- Future authentication hooks

Author: Hrithik
"""

from __future__ import annotations

from fastapi import (
    File,
    HTTPException,
    UploadFile,
    status,
)

from app.constants import (
    SUPPORTED_AUDIO_EXTENSIONS,
    SUPPORTED_AUDIO_MIME_TYPES,
)
from app.core.config import settings


###############################################################################
# Upload Validation
###############################################################################


async def validate_audio_upload(
    audio: UploadFile = File(...),
) -> UploadFile:
    """
    Basic request validation.

    Business validation (duration, MIME verification,
    normalization, etc.) happens later in AudioService.
    """

    if audio.filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing filename.",
        )

    extension = "." + audio.filename.split(".")[-1].lower()

    if extension not in SUPPORTED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                f"Unsupported file extension '{extension}'. "
                f"Supported: {', '.join(sorted(SUPPORTED_AUDIO_EXTENSIONS))}"
            ),
        )

    if (
        audio.content_type
        and audio.content_type not in SUPPORTED_AUDIO_MIME_TYPES
    ):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                f"Unsupported MIME type '{audio.content_type}'."
            ),
        )

    return audio


###############################################################################
# Future Authentication Hook
###############################################################################


async def verify_api_key() -> None:
    """
    Reserved for future API-key authentication.

    MVP:
        No authentication required.
    """

    return None


###############################################################################
# Health Dependency
###############################################################################


async def readiness_check() -> None:
    """
    Reserved for future dependency checks.

    Examples:
        - Redis
        - Database
        - Object Storage
        - AI Provider Availability
    """

    return None