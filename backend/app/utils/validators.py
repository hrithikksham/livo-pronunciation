"""
Audio validation utilities.

Responsible for:
- File extension validation
- File size validation
- Audio duration validation

Author: Hrithik
"""

from __future__ import annotations

from pathlib import Path

from pydub import AudioSegment

from app.constants import (
    SUPPORTED_AUDIO_EXTENSIONS,
)

from app.core.config import settings

from app.core.exceptions import (
    AudioValidationError,
    FileTooLargeError,
    UnsupportedAudioTypeError,
)

from app.utils.file_utils import get_file_size_mb


###############################################################################
# Extension Validation
###############################################################################


def validate_extension(
    file_path: Path,
) -> str:
    """
    Validate file extension.
    """

    extension = file_path.suffix.lower()

    if extension not in SUPPORTED_AUDIO_EXTENSIONS:
        raise UnsupportedAudioTypeError(
            f"Unsupported audio extension: {extension}"
        )

    return extension


###############################################################################
# File Size Validation
###############################################################################


def validate_file_size(
    file_path: Path,
) -> float:
    """
    Validate uploaded file size.

    Returns
    -------
    float
        File size in MB.
    """

    size_mb = get_file_size_mb(file_path)

    if size_mb > settings.MAX_FILE_SIZE_MB:
        raise FileTooLargeError(
            f"Maximum file size is "
            f"{settings.MAX_FILE_SIZE_MB} MB."
        )

    return round(size_mb, 2)


###############################################################################
# Duration Validation
###############################################################################


def validate_duration(
    file_path: Path,
) -> float:
    """
    Validate audio duration.
    """

    try:

        audio = AudioSegment.from_file(
            file_path,
        )

    except Exception as exc:

        raise AudioValidationError(
            "Unable to decode audio file."
        ) from exc

    duration = len(audio) / 1000

    if duration < settings.MIN_DURATION_SECONDS:

        raise AudioValidationError(
            f"Audio must be at least "
            f"{settings.MIN_DURATION_SECONDS} seconds."
        )

    if duration > settings.MAX_DURATION_SECONDS:

        raise AudioValidationError(
            f"Audio must not exceed "
            f"{settings.MAX_DURATION_SECONDS} seconds."
        )

    return duration


###############################################################################
# MIME Guess
###############################################################################


def guess_mime_type(
    extension: str,
) -> str:
    """
    Guess MIME type from extension.

    This avoids requiring python-magic/libmagic.
    """

    mapping = {
        ".wav": "audio/wav",
        ".mp3": "audio/mpeg",
        ".m4a": "audio/mp4",
        ".webm": "audio/webm",
        ".ogg": "audio/ogg",
        ".flac": "audio/flac",
    }

    return mapping.get(
        extension,
        "application/octet-stream",
    )


###############################################################################
# Complete Validation
###############################################################################


def validate_audio_file(
    file_path: Path,
) -> dict:
    """
    Run all validation checks.

    Returns
    -------
    dict
    """

    extension = validate_extension(
        file_path,
    )

    return {
        "mime": guess_mime_type(
            extension,
        ),
        "extension": extension,
        "size_mb": validate_file_size(
            file_path,
        ),
        "duration": validate_duration(
            file_path,
        ),
    }