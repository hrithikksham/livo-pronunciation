"""
Audio Service.

Responsible for:
- Saving uploaded audio
- Validating uploaded audio
- Normalizing audio
- Building ProcessedAudio
- Cleaning temporary files

Author: Hrithik
"""

from __future__ import annotations

from functools import lru_cache

from fastapi import UploadFile

from app.schemas.common import (
    AudioMetadata,
    ProcessedAudio,
)
from app.services.base import BaseService

from app.utils.audio_utils import (
    get_audio_metadata,
    normalize_audio,
)

from app.utils.file_utils import (
    delete_file,
    save_upload_file,
)

from app.utils.validators import (
    validate_audio_file,
)


class AudioService(BaseService):
    """
    Handles uploaded audio files.
    """

    async def process(
        self,
        upload: UploadFile,
    ) -> ProcessedAudio:
        """
        Complete audio processing pipeline.
        """

        self.log_start("Audio Processing")

        original_path = None
        normalized_path = None

        try:

            ###################################################################
            # Save Upload
            ###################################################################

            original_path = save_upload_file(upload)

            ###################################################################
            # Validate
            ###################################################################

            validation = validate_audio_file(
                original_path,
            )

            ###################################################################
            # Normalize
            ###################################################################

            normalized_path = normalize_audio(
                original_path,
            )

            ###################################################################
            # Metadata
            ###################################################################

            metadata = get_audio_metadata(
                normalized_path,
            )

            processed_audio = ProcessedAudio(
                original_path=original_path,
                normalized_path=normalized_path,
                metadata=AudioMetadata(
                    duration_seconds=metadata[
                        "duration_seconds"
                    ],
                    channels=metadata[
                        "channels"
                    ],
                    frame_rate=metadata[
                        "frame_rate"
                    ],
                    sample_width=metadata[
                        "sample_width"
                    ],
                    frame_width=metadata[
                        "frame_width"
                    ],
                    file_size_mb=validation[
                        "size_mb"
                    ],
                    mime_type=validation[
                        "mime"
                    ],
                    extension=validation[
                        "extension"
                    ],
                ),
            )

            self.log_success(
                "Audio Processing"
            )

            return processed_audio

        except Exception as exc:

            self.cleanup_paths(
                original_path,
                normalized_path,
            )

            self.log_failure(
                "Audio Processing",
                exc,
            )

            raise

    ###########################################################################
    # Cleanup
    ###########################################################################

    def cleanup(
        self,
        audio: ProcessedAudio,
    ) -> None:
        """
        Delete processed audio files.
        """

        self.cleanup_paths(
            audio.original_path,
            audio.normalized_path,
        )

    @staticmethod
    def cleanup_paths(
        original_path,
        normalized_path,
    ) -> None:
        """
        Safely delete temporary files.
        """

        if normalized_path is not None:
            delete_file(normalized_path)

        if original_path is not None:
            delete_file(original_path)


###############################################################################
# Dependency Injection
###############################################################################


@lru_cache
def get_audio_service() -> AudioService:
    return AudioService()