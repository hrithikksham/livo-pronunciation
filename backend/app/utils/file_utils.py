
from __future__ import annotations

import os
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from fastapi import UploadFile

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


###########################################################################
# Temporary Directory
###########################################################################


def ensure_temp_directory() -> Path:
    """
    Ensures the configured temporary directory exists.

    Returns:
        Path to the temporary directory.
    """

    temp_dir = Path(settings.TEMP_DIRECTORY)

    temp_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return temp_dir


###########################################################################
# Save UploadFile
###########################################################################


def save_upload_file(
    upload_file: UploadFile,
) -> Path:
    """
    Saves an UploadFile to a temporary location.

    Returns:
        Path to the temporary file.
    """

    temp_dir = ensure_temp_directory()

    suffix = Path(upload_file.filename or "audio.wav").suffix

    with tempfile.NamedTemporaryFile(
        dir=temp_dir,
        delete=False,
        suffix=suffix,
    ) as temp_file:

        shutil.copyfileobj(
            upload_file.file,
            temp_file,
        )

        temp_path = Path(temp_file.name)

    logger.info("Temporary file created: %s", temp_path)

    return temp_path


###########################################################################
# Delete File
###########################################################################


def delete_file(path: Path) -> None:
    """
    Deletes a temporary file.

    Safe to call multiple times.
    """

    try:

        if path.exists():
            path.unlink()

            logger.info(
                "Temporary file deleted: %s",
                path,
            )

    except Exception as exc:
        logger.warning(
            "Failed to delete temporary file: %s (%s)",
            path,
            exc,
        )


###########################################################################
# Temporary File Context Manager
###########################################################################


@contextmanager
def temporary_upload_file(
    upload_file: UploadFile,
) -> Generator[Path, None, None]:
    """
    Context manager that guarantees cleanup.

    Usage:

        with temporary_upload_file(audio) as file_path:
            ...

    """

    temp_path = save_upload_file(upload_file)

    try:
        yield temp_path

    finally:
        delete_file(temp_path)


###########################################################################
# File Size
###########################################################################


def get_file_size_mb(path: Path) -> float:
    """
    Returns file size in MB.
    """

    size_bytes = os.path.getsize(path)

    return size_bytes / (1024 * 1024)