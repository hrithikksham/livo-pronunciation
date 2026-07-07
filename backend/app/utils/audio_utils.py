

from __future__ import annotations

import tempfile
from pathlib import Path

from pydub import AudioSegment

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


###########################################################################
# Audio Loading
###########################################################################


def load_audio(file_path: Path) -> AudioSegment:
    """
    Load an audio file.

    Raises:
        CouldntDecodeError
    """

    return AudioSegment.from_file(file_path)


###########################################################################
# Convert to Mono
###########################################################################


def convert_to_mono(audio: AudioSegment) -> AudioSegment:
    """
    Convert audio to mono.
    """

    return audio.set_channels(settings.TARGET_CHANNELS)


###########################################################################
# Normalize Sample Rate
###########################################################################


def normalize_sample_rate(audio: AudioSegment) -> AudioSegment:
    """
    Convert audio to target sample rate.
    """

    return audio.set_frame_rate(settings.TARGET_SAMPLE_RATE)


###########################################################################
# Normalize Volume
###########################################################################


def normalize_volume(audio: AudioSegment) -> AudioSegment:
    """
    Normalize audio loudness.

    Target ≈ -20 dBFS
    """

    target_dbfs = -20.0

    change = target_dbfs - audio.dBFS

    return audio.apply_gain(change)


###########################################################################
# Export WAV
###########################################################################


def export_wav(audio: AudioSegment) -> Path:
    """
    Export normalized audio as WAV.

    Returns:
        Path to temporary WAV file.
    """

    temp = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False,
        dir=settings.TEMP_DIRECTORY,
    )

    output_path = Path(temp.name)

    audio.export(
        output_path,
        format="wav",
    )

    logger.info(
        "Normalized audio exported to %s",
        output_path,
    )

    return output_path


###########################################################################
# Full Normalization Pipeline
###########################################################################


def normalize_audio(file_path: Path) -> Path:
    """
    Complete audio normalization.

    Input:
        Any supported format

    Output:
        WAV
        Mono
        16kHz
        Normalized volume
    """

    logger.info(
        "Normalizing audio: %s",
        file_path,
    )

    audio = load_audio(file_path)

    audio = convert_to_mono(audio)

    audio = normalize_sample_rate(audio)

    audio = normalize_volume(audio)

    return export_wav(audio)


###########################################################################
# Metadata
###########################################################################


def get_audio_metadata(file_path: Path) -> dict:
    """
    Extract metadata from audio.
    """

    audio = load_audio(file_path)

    return {
        "duration_seconds": len(audio) / 1000,
        "channels": audio.channels,
        "frame_rate": audio.frame_rate,
        "sample_width": audio.sample_width,
        "frame_width": audio.frame_width,
    }